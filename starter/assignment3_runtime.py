"""Pinned Assignment 3 inference protocol shared by local and Gradescope runs."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import time
import urllib.error
import urllib.request

CONTEXT_TOKENS = 4096
MAX_OUTPUT_TOKENS = 512
RESERVE_TOKENS = 64
MAX_PROMPT_TOKENS = 1500
PROFILE = "assignment3-qwen35-cpu-v1"


class ProtocolError(Exception):
    """Base class for a controlled, student-readable protocol failure."""


class InputError(ProtocolError):
    """The submitted input is invalid."""


class InfrastructureError(ProtocolError):
    """The fixed runtime or official batch failed."""


class OutputError(ProtocolError):
    """The model response did not satisfy the required output contract."""

    def __init__(self, message, request=None, response=None):
        super().__init__(message)
        self.request = request
        self.response = response


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    except UnicodeDecodeError as exc:
        raise InputError(f"{path.name} is not valid UTF-8") from exc
    except (OSError, ValueError) as exc:
        raise InputError(f"Cannot read {path.name} as strict JSON: {exc}") from exc


def load_questions(path: Path):
    questions = load_json(path)
    if type(questions) is not list or len(questions) != 10:
        raise InfrastructureError(f"{path.name} must contain exactly ten questions")
    ids = []
    for number, question in enumerate(questions, 1):
        if type(question) is not dict or set(question) != {"id", "question", "options"}:
            raise InfrastructureError(f"Question {number} must contain only id, question, and options")
        if type(question["id"]) is not str or type(question["question"]) is not str:
            raise InfrastructureError(f"Question {number} has a non-string ID or stem")
        options = question["options"]
        if type(options) is not dict or set(options) != {"1", "2", "3", "4"}:
            raise InfrastructureError(f"Question {number} must have options 1 through 4")
        if not all(type(value) is str for value in options.values()):
            raise InfrastructureError(f"Question {number} has non-string option text")
        ids.append(question["id"])
    if len(set(ids)) != 10:
        raise InfrastructureError("Question IDs must be unique")
    return questions, ids


def load_key(path: Path, ids):
    key = load_json(path)
    if type(key) is not dict or set(key) != set(ids):
        raise InfrastructureError(f"{path.name} does not match the question IDs")
    if not all(type(value) is int and 1 <= value <= 4 for value in key.values()):
        raise InfrastructureError(f"{path.name} contains an invalid answer")
    return key


def read_prompt(path: Path):
    try:
        return path.read_bytes().decode("utf-8")
    except FileNotFoundError as exc:
        raise InputError(f"Missing required file: {path.name}") from exc
    except UnicodeDecodeError as exc:
        raise InputError(f"{path.name} is not valid UTF-8") from exc
    except OSError as exc:
        raise InputError(f"Could not read {path.name}: {exc}") from exc


class LlamaClient:
    def __init__(self, port=8947, timeout=1200):
        self.base_url = f"http://127.0.0.1:{port}"
        self.timeout = timeout

    def post(self, path, body):
        request = urllib.request.Request(
            self.base_url + path,
            json.dumps(body, ensure_ascii=False).encode("utf-8"),
            {"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return json.load(response, object_pairs_hook=unique_object)
        except (OSError, ValueError, urllib.error.HTTPError) as exc:
            raise InfrastructureError(f"Pinned inference server request {path} failed: {exc}") from exc

    def ready(self):
        try:
            with urllib.request.urlopen(self.base_url + "/health", timeout=2) as response:
                return response.status == 200
        except OSError:
            return False

    def wait_until_ready(self, seconds=180):
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            if self.ready():
                return
            time.sleep(0.25)
        raise InfrastructureError(f"Pinned inference server was not ready after {seconds} seconds")


def request_body(prompt, questions, ids):
    return {
        "model": "local",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(questions, ensure_ascii=False)},
        ],
        "temperature": 0,
        "seed": 314159,
        "max_tokens": MAX_OUTPUT_TOKENS,
        "cache_prompt": False,
        "chat_template_kwargs": {"enable_thinking": False},
        "reasoning_budget_tokens": 0,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "answers",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        key: {"type": "integer", "enum": [1, 2, 3, 4]} for key in ids
                    },
                    "required": ids,
                    "additionalProperties": False,
                },
            },
        },
    }


def run_batch(client, prompt, questions, ids):
    prompt_tokens = len(client.post("/tokenize", {"content": prompt, "add_special": False})["tokens"])
    if prompt_tokens > MAX_PROMPT_TOKENS:
        raise InputError(
            f"Prompt is {prompt_tokens} Qwen tokens; the limit is {MAX_PROMPT_TOKENS}. "
            "Nothing was generated or truncated."
        )
    body = request_body(prompt, questions, ids)
    rendered = client.post(
        "/apply-template",
        {"messages": body["messages"], "chat_template_kwargs": body["chat_template_kwargs"]},
    )
    input_tokens = len(
        client.post(
            "/tokenize",
            {"content": rendered["prompt"], "add_special": False, "parse_special": True},
        )["tokens"]
    )
    if input_tokens + MAX_OUTPUT_TOKENS + RESERVE_TOKENS > CONTEXT_TOKENS:
        raise InfrastructureError(
            "Official question-batch/context configuration error: a compliant prompt and batch do not fit. "
            "The prompt was not truncated and this is not a student violation."
        )
    started = time.monotonic()
    response = client.post("/v1/chat/completions", body)
    elapsed = time.monotonic() - started
    try:
        choice = response["choices"][0]
        raw = choice["message"]["content"]
        answers = json.loads(raw, object_pairs_hook=unique_object)
        if choice.get("finish_reason") != "stop":
            raise OutputError(f"Generation ended with finish_reason={choice.get('finish_reason')!r}")
        if choice["message"].get("reasoning_content"):
            raise OutputError("The model returned reasoning content even though thinking is disabled")
        if type(answers) is not dict or set(answers) != set(ids):
            raise OutputError("Model JSON does not contain exactly the ten required question IDs")
        if not all(type(value) is int and 1 <= value <= 4 for value in answers.values()):
            raise OutputError("Every model answer must be an integer from 1 through 4")
    except OutputError as exc:
        exc.request = body
        exc.response = response
        raise
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise OutputError(f"Malformed or truncated model response: {exc}", body, response) from exc
    return {
        "profile": PROFILE,
        "prompt_tokens": prompt_tokens,
        "input_tokens": input_tokens,
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "seconds": elapsed,
        "request": body,
        "response": response,
        "answers": answers,
    }


def compare(answers, key, ids):
    rows = [
        {"id": key_id, "expected": key[key_id], "predicted": answers[key_id], "match": key[key_id] == answers[key_id]}
        for key_id in ids
    ]
    return rows, sum(row["match"] for row in rows)
