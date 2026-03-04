The model operates on a source $\mathcal{M}^0$ and noisy $\mathcal{M}^z$ microenvironments with per-cell features $\boldsymbol{x}_i \in \mathbb{R}^D$ and 2D coordinates $\boldsymbol{c}_i \in \mathbb{R}^2$. The architecture consists of the following components:

1.  **Input Embeddings:**
    (a) **Feature Embedding:** A linear transformation is applied to the input features $\boldsymbol{x}_i$ of each cell.
    (b) **Coordinate Embedding:** Spatial coordinates $\boldsymbol{c}_i$ are linearly projected and concatenated to the feature embedding.
    (c) **Time Embedding:** For the noisy microenvironment only, time $t \in [0, 1]$ is encoded using sinusoidal functions $\cos(\omega t)$ and $\sin(\omega t)$, followed by a linear projection and concatenation with the input embedding.
2.  **Transformer Encoder (Source Microenvironment):**
    (a) **Self-Attention:** A stack of transformer encoder blocks with multi-head self-attention processes the embedded source microenvironment.
    (b) **No Time Embedding:** Time information is *not* provided to the encoder, as it encodes the source $\mathcal{M}^0$.
    (c) **Residual Feedforward:** Each block contains a feedforward subnetwork with LeakyReLU activation and a residual connection.
    (d) **Layer Normalization:** Applied after both the attention and feedforward layers.
    (e) **Masking:** Binary masks are used to ignore padding in variable-length microenvironments.
3.  **Transformer Decoder (Noisy Microenvironment):**
    (a) **Time Embedding:** Temporal context is injected into the decoder by embedding the time $t$ and concatenating it to the target point embedding.
    (b) **Cross-Attention:** Decoder layers apply cross-attention between the noisy microenvironment and the encoded source microenvironment.
    (c) **Self-Attention and Feedforward:** Each decoder block includes standard self-attention and residual feedforward layers.
    (d) **Layer Normalization and Masking:** As with the encoder, normalization, and masking are applied throughout.
4.  **Final Output Projection:**
    (a) **Prediction Head:** A linear layer maps the decoder outputs to the desired dimensionality.

This architecture allows for flexible and expressive modeling of temporal dynamics in cellular point clouds. By encoding only the source and decoding the temporally conditioned target, the model supports variational and flow-based training objectives with explicit temporal conditioning.

### F.7 Hyperparameters and Computational Costs

##### Model hyperparameters.
For all experiments, we use the same configuration for the Microenvironment Transformer architecture. The full set of hyperparameters is as follows:

*   **Input feature dimension:** 50 PCA-based gene expression features concatenated with a one-hot encoding of the time-point, resulting in a total dimensionality of $50 + |\mathcal{T}|$, where $|\mathcal{T}|$ is the number of slides (timepoints) in the dataset.
*   **Input coordinate dimension:** 2
*   **Embedding dimension:** 128
*   **MLP hidden dimension:** 256
*   **Number of attention heads:** 4
*   **Number of encoder layers:** 2
*   **Number of decoder layers:** 2
*   **Dropout rate:** 0.1
*   **Output dimension:** 52 (gene expressions features + coordinates)

<center>36</center>