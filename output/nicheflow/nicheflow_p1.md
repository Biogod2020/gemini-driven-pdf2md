Despite these technological advances, modeling trajectories on time-resolved spatial slides is complicated, as no direct correspondence exists between cells across slides due to the destructive nature of acquisition practices. Moreover, current computational methods fall short in modeling the evolution of tissue organization at the level of cellular microenvironments. Most approaches infer trajectories by modeling single-cell dynamics using velocity-based models [17–19] or optimal transport between individual cells [20, 21]. While effective at capturing cell evolution, these cell-centric methods fundamentally miss the coordinated evolution of structured niches within tissues.

This limitation presents a critical research gap that we address with the following question:

*How can we model the spatiotemporal evolution of cellular microenvironments preserving both local neighborhood relationships and cellular state transitions?*

To address this question, we directly model the dynamics of cellular neighborhoods as cohesive units rather than focusing on isolated cell trajectories. This approach aligns naturally with tissue-scale biological processes and enables principled learning of dynamics in structured, high-dimensional, and variably sized spatial domains.

We introduce **Niche Flow Matching (NicheFlow)** (Fig. 1), a generative model for learning spatiotemporal dynamics of cellular niches from time-resolved spatial transcriptomics data. NicheFlow builds on recent advances in Flow Matching (FM) and Optimal Transport (OT) to operate over distributions of microenvironments, which we represent as point clouds. NicheFlow enables accurate modeling of global spatial architecture and local microenvironment composition within evolving tissues.

![Figure 1: Overview of NicheFlow. At time $t_1$, we generate a target microenvironment $\\mathcal{M}^1$ by transforming Gaussian noise $\\mathcal{M}^z$ using a Variational Flow Matching model with a posterior $\\mu_t^\\theta$ conditioned on a source microenvironment $\\mathcal{M}^0$ at $t_0$. Source-target pairs are identified via entropic OT over pooled microenvironment coordinates and gene expression profiles.](assets/fig1.png)

Our contributions include:

*   **A microenvironment-centered trajectory inference paradigm** that shifts from modeling individual cells in time to modeling niches as point clouds, enabling simultaneous prediction of spatial coordinates and gene expression profiles while preserving local tissue context.
*   **A factorized Variational Flow Matching (VFM) approach** with distributional families (Laplace for spatial coordinates, Gaussian for gene expression) that jointly trains on spatial and cell state dynamics using a factorized loss, modeling spatial reconstruction and biological fidelity with tailored distributional assumptions.
*   **A spatially-aware sampling strategy** using OT between niche representations, enabling scalable training on large tissue sections while ensuring comprehensive coverage of heterogeneous regions.

Our approach consistently outperforms baselines in recovering cell-type organization and spatial structure across embryonic, brain development, and ageing datasets. NicheFlow enables principled learning of dynamics in structured, high-dimensional, and variably sized spatial domains, a challenge with parallels in other spatiotemporal modeling domains beyond biology.

## 2 Related Work

NicheFlow is at the interface between generative models and spatiotemporal transcriptomic data.

**FM and single-cell transcriptomics.** We propose a model based on FM, a framework introduced by several seminal works [22–24]. Specifically, we adopt a variational view of the FM objective, following Eijkelboom et al. [25], but extend it to mixed-factorized distributions for point cloud generation. Our method, NicheFlow, combines FM with OT, a pairing that has proven effective in modeling cellular data [26–29]. Unlike these models, however, we focus on point clouds of