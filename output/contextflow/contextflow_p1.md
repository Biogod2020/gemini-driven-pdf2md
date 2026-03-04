*Table 1. Comparisons of state-of-the-art spatiotemporal OT and flow matching methods. In particular, ContextFlow excels at efficiently inferring biologically plausible trajectories by incorporating spatial priors into minibatch-OT-based flow-matching frameworks.*

| Method | Generative | Prior Knowledge | Unified Velocity Field | OT Runtime |
| :--- | :---: | :---: | :---: | :---: |
| DeST-OT (Halmos et al., 2025) | ✗ | ✗ | ✗ | $O(N^3)$ |
| TOAST (Ceccarelli et al., 2025) | ✗ | ✗ | ✗ | $O(N^3)$ |
| PASTE (Zeira et al., 2022) | ✗ | ✗ | ✗ | $O(N^3)$ |
| CFM (Lipman et al., 2022) | ✓ | ✗ | ✓ | — |
| MOTFM (Tong et al., 2024) | ✓ | ✗ | ✓ | $O(N^2)$ |
| **ContextFlow (ours)** | ✓ | ✓ | ✓ | $O(N^2)$ |

![Figure 1. ContextFlow integrates local tissue organization and ligand–receptor communications to learn biologically meaningful trajectories from spatial omics data. Prior knowledge acts as a soft filter, discouraging implausible transitions while preserving flexibility in trajectory inference.](assets/fig1.png)

2021; Wei et al., 2022), disease progression (Kukanja et al., 2024), and treatment response (Liu et al., 2024).

Optimal transport (OT) has become a foundational framework for aligning spatially resolved samples and inferring putative developmental or temporal couplings (Zeira et al., 2022; Liu et al., 2023). As a result, state-of-the-art flow matching frameworks such as minibatch-OT flow matching (MOTFM) (Tong et al., 2024) use OT-derived couplings to define conditional paths for training velocity fields, thereby overcoming the lack of generative capabilities in optimal transport. The OT formulation adopted in MOTFM, however, does not account for the contextual richness of spatial transcriptomics and can yield trajectories that are statistically optimal yet biologically implausible (see Figure 4a in Appendix G.1 for an illustration). While recent studies (Halmos et al., 2025; Ceccarelli et al., 2025) have extended OT objectives to spatial transcriptomics, they primarily focus on pairwise alignment of populations across conditions or modalities and do not explicitly incorporate the cell–cell communication patterns that drive cellular state transitions.

To address the above limitations, we introduce a novel flow matching-based framework, *ContextFlow*, that incorporates spatial priors to model temporal tissue dynamics (Figure 1). By encoding local tissue organization and ligand-receptor-derived spatial communication patterns into prior-regularized optimal transport formulations, ContextFlow fully exploits the contextual richness of spatial omics data and embeds both structural and functional aspects of tissue organization into its objective, thereby generating more biologically informed trajectories. Table 1 highlights the key advantages of ContextFlow, compared with the aforementioned existing methods, where detailed discussions on related works are postponed to Appendix A.

In summary, our contributions are as follows:

*   We leverage the structure of local tissue organization and ligand–receptor communication to extract biologically meaningful features from spatial omics data and encode them into an informed transition plausibility matrix to constrain temporal dynamics (Section 3.2).
*   We design two novel integration schemes—cost-based and entropy-based—that incorporate prior knowledge into an OT-coupled flow matching framework, both amenable to efficient Sinkhorn optimization and scalable on modern hardware (Section 3.3).
*   Comprehensive experiments on three regeneration and developmental datasets demonstrate that ContextFlow consistently outperforms baseline flow matching methods under both interpolation and extrapolation settings across multiple evaluation metrics that capture biological plausibility and statistical fidelity (Section 4).

## 2. Preliminaries

### 2.1. Flow Matching Basics

Flow matching (Lipman et al., 2023) is a simulation-free and sample-efficient generative framework for training continuous normalizing flows (Chen et al., 2018). Given a pair of source and target data distributions over $\mathbb{R}^d$ with densities $q_0 = q(\boldsymbol{x}_0)$ and $q_1 = q(\boldsymbol{x}_1)$, the problem task is to learn a time-varying velocity vector field $u_\theta : [0, 1] \times \mathbb{R}^d \rightarrow \mathbb{R}^d$, whose continuous evolution is captured by a function in the form of a neural-net-based model with weights $\theta$, that can transform $q_0$ to $q_1$ through integration via an ordinary differential equation (ODE). To be more specific, *flow matching* (FM) seeks to optimize $\theta$ by minimizing a simple regression loss between $u_\theta$ and a target time-varying velocity vector field $u_t : [0, 1] \times \mathbb{R}^d \rightarrow \mathbb{R}^d$ as follows:

$$\min_\theta \mathbb{E}_{t \sim \mathcal{U}(0,1), \boldsymbol{x} \sim p_t(\boldsymbol{x})} \| u_\theta(t, \boldsymbol{x}) - u_t(\boldsymbol{x}) \|^2. \tag{1}$$