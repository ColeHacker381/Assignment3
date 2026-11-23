# Course material review through November 11

The [course page](https://www.davidinouye.com/course/ece57000-fall-2026/) describes its dynamic materials as revised, chronological course notes. This inventory uses those notes for topic coverage and the [November 11 frozen slides](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/frozen/2026-11-11/generating-images-by-diffusion.pdf) to identify the date boundary. The dynamic diffusion deck continues beyond that boundary. Through November 11, the frozen slides reach the continuous noising SDE and its Gaussian marginal. Later reverse SDE, probability-flow ODE and solver details should be checked against the dated slides before inclusion.

## Concepts to consider for prompt development

- **Working with AI** covers effective delegation, verification, and dividing work into components with observable checks. Course launch and stakeholder discovery provide context for AI-assisted work.
- **Linear algebra and PCA** cover linear transformations, projections, orthonormal bases, singular value decomposition, reconstruction error, variance retained, and numerical implementation with NumPy. For orthonormal columns of W, squared reconstruction error is ||X||²_F − ||XW||²_F.
- **Prediction and evaluation** cover binary outcomes, conditional probabilities, nearest neighbors, generalization, data splits, and evaluating the full model-selection pipeline. KNN relies on nearby inputs having similar conditional outcome probabilities.
- **Linear models and optimization** cover least squares, logistic scores and probabilities, log loss, convexity, gradients, numerical optimization, and regularization. Convexity bounds the objective at a convex combination by the corresponding weighted average of objective values.
- **Neural networks and vision** cover nonlinear representations, chain rule and backpropagation, PyTorch training, convolutions and receptive fields, architectural assumptions, residual connections, and U-Net segmentation.
- **Sequences and transformers** cover autoregressive prediction, recurrent models, attention, position, transformer components, causal masking, decoding, and inference and training systems. For a query at position i, causal attention masks keys at positions j > i. Top-k sampling renormalizes over the retained tokens.
- **Generative models** cover autoencoders, denoising, probabilistic latent variables, variational autoencoders and diffusion. For additive Gaussian corruption x̃ = x + σϵ, predicting noise and predicting the clean input are equivalent parameterizations at fixed σ. A network trained across noise levels supports a progression from broad coverage to finer detail.

These notes are a starting inventory. The example batch contains ten questions and cannot establish hidden-set accuracy or identify which facts are most valuable under the 1,500-token prompt limit.

## Dynamic course sources

- [Artificial Intelligence in the Age of AI](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/01-course-redesign-and-syllabus)
- [Scale Your Intelligence](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/02-working-effectively-with-ai)
- [Dimensionality Reduction: Motivation and Problem Setup](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/02-01-linear-algebra-introduction)
- [Linear Transformations: What Do They Do?](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/02-02-linear-transformations)
- [Reconstruction and Principal Component Analysis](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/02-03-dimension-projection-pca)
- [NumPy and Numerical Computation for PCA](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/02-04-numpy-numerical-pca)
- [Binary Prediction: Generalization, Evaluation, and the Limits of Locality](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/03-01-binary-prediction)
- [Learning and Interpreting Linear Regression](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/04-01-linear-predictive-scores)
- [Logistic Classification: Scores, Probabilities, and Log Loss](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/04-02-logistic-classification)
- [Why the Shape of the Objective Matters](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/04-03-convexity)
- [Fitting Models with Local Information](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/04-04-numerical-optimization)
- [Controlling Model Complexity for Generalization](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/04-05-regularization-and-generalization)
- [Learning Nonlinear Representations](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/05-01-nonlinear-representations)
- [Training Neural Networks](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/05-02-training-neural-networks)
- [Implementing Neural Network Training in PyTorch](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/05-03-pytorch-implementation)
- [Convolutions and Image Structure](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/05-04-convolutional-networks)
- [Testing Architectural Assumptions](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/05-05-architecture-evaluation)
- [Image Classification with ResNet](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/05-06-resnet-image-classification)
- [Image Segmentation with U-Net](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/05-07-unet-image-segmentation)
- [Sequence Prediction and Representation](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/06-01-sequence-prediction)
- [Recurrent Sequence Models](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/06-02-recurrent-sequence-models)
- [Attention and Position](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/06-03-attention-and-position)
- [Building a Transformer](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/06-04-transformer-assembly)
- [From Prediction to Generation](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/06-05-autoregressive-generation)
- [Serving and Training a Transformer](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/06-06-transformer-systems)
- [Email Completion: RNN and Transformer Evidence](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/06-07-sequence-empirical-comparison)
- [Learning to Reconstruct and Restore Images](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/07-01-autoencoders)
- [From Probabilistic Autoencoders to VAEs](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/07-02-variational-autoencoders)
- [Generating Images by Diffusion](https://www.davidinouye.com/course/ece57000-fall-2026/lectures/07-03-diffusion-models)
