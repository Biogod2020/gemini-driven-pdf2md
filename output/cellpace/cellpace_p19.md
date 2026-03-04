## Methods

### The architecture of CellPace

CellPace is a generative framework designed to model the temporal dynamics of single-cell omics data. First, a VAE is trained to learn low-dimensional latent representations of individual cells, effectively capturing the manifold of cellular identity. Given this pretrained VAE, a Transformer-based diffusion model called TDiF (Temporal Diffusion Forcing) learns the transition probabilities between these latent states over time (Fig. 1a-1d).

#### Latent Representation Learning using VAE:

To avoid the sparsity and high dimensionality of raw count data, we first encode cells into a compressed latent space. For single-modality scRNA-seq datasets, we used scVI [11] to learn latent representations, modeling sparse and over-dispersed gene counts with a Zero-Inflated Negative Binomial (ZINB) likelihood. For paired multiome datasets, we utilized MultiVI [24] to learn a joint latent representation that integrates information from both RNA and chromatin modalities.

#### Temporal Diffusion Forcing (TDiF):

To model cellular transitions within this latent space, we designed an architecture capable of capturing continuous temporal dynamics without the structural limitations of existing generative backbones. Standard U-Nets [27, 28], common in image diffusion, rely on convolutional down sampling and spatial locality—assumptions ill-suited for unordered gene sets. Moreover, their bidirectional processing allows later states to influence the reconstruction of earlier ones during training, violating temporal causality. While recurrent neural networks enforce directionality, they often suffer from vanishing gradients [29] over long developmental trajectories. Similarly, while token-based Transformers [30] capture long-range dependencies, they typically require quantizing continuous molecular profiles into categorical vocabularies, which can obscure the fine-grained metric geometry of the cellular manifold.

To overcome these challenges, we developed Temporal Diffusion Forcing (TDiF), a backbone motivated by the Diffusion Forcing (DiF) [10] framework. Unlike traditional diffusion models that denoise entire sequences at a single noise level, TDiF uses per-position noise levels as a continuous masking signal. This design allows low-noise past frames to act as known context while high-noise future frames serve as uncertain targets within a single forward pass, enabling flexible, causal sequence generation (Fig. 1b-1d). More importantly, its gap-aware temporal encoding enables capturing of continuous temporal dynamics.

#### Gap-Aware Temporal Encoding: