Table 2. Interpolation at the middle holdout time point for the Brain Regeneration dataset.

| Sampling | Method | $\lambda$ | $\alpha$ | Weighted $\mathcal{W}_2$ | $\mathcal{W}_2$ | MMD | Energy |
| :--- | :--- | :---: | :---: | :--- | :--- | :--- | :--- |
| Next Step | CFM | -- | -- | $2.618 \pm 0.142$ | $2.579 \pm 0.197$ | $0.043 \pm 0.003$ | $12.505 \pm 1.271$ |
| | MOTFM | -- | -- | $2.567 \pm 0.088$ | $2.476 \pm 0.161$ | $0.040 \pm 0.003$ | $11.269 \pm 1.388$ |
| | CTF-C | 1 | 0.8 | $2.423 \pm 0.164$ | $2.293 \pm 0.103$ | $0.037 \pm 0.001$ | $9.874 \pm 0.659$ |
| | | 0 | 0.2 | $2.396 \pm 0.028$ | $2.100 \pm 0.102$ | $0.033 \pm 0.003$ | $8.577 \pm 0.976$ |
| | | 0.5 | 0.8 | $2.442 \pm 0.173$ | $2.353 \pm 0.241$ | $0.035 \pm 0.004$ | $9.008 \pm 2.094$ |
| | CTF-H | 0 | -- | $2.528 \pm 0.143$ | $2.534 \pm 0.180$ | $0.040 \pm 0.004$ | $11.192 \pm 1.304$ |
| | | 1 | -- | $\mathbf{2.316 \pm 0.141}$ | $\mathbf{1.969 \pm 0.221}$ | $\mathbf{0.030 \pm 0.004}$ | $\mathbf{6.359 \pm 1.336}$ |
| | | 0.5 | -- | $2.519 \pm 0.167$ | $2.412 \pm 0.158$ | $0.039 \pm 0.004$ | $10.304 \pm 1.808$ |
| IVP | CFM | -- | -- | $4.216 \pm 0.463$ | $4.266 \pm 0.308$ | $0.170 \pm 0.029$ | $32.413 \pm 5.122$ |
| | MOTFM | -- | -- | $4.198 \pm 0.319$ | $4.452 \pm 0.243$ | $0.173 \pm 0.017$ | $33.149 \pm 3.321$ |
| | CTF-C | 1 | 0.8 | $3.603 \pm 0.300$ | $3.816 \pm 0.310$ | $0.127 \pm 0.018$ | $24.271 \pm 3.992$ |
| | | 0 | 0.2 | $\mathbf{3.465 \pm 0.232}$ | $\mathbf{3.641 \pm 0.320}$ | $0.119 \pm 0.025$ | $23.055 \pm 5.939$ |
| | | 0.5 | 0.8 | $4.015 \pm 0.351$ | $3.974 \pm 0.442$ | $0.140 \pm 0.038$ | $27.592 \pm 6.669$ |
| | CTF-H | 0 | -- | $3.925 \pm 0.267$ | $4.375 \pm 0.297$ | $0.164 \pm 0.013$ | $32.034 \pm 3.270$ |
| | | 1 | -- | $3.905 \pm 0.395$ | $4.188 \pm 0.685$ | $\mathbf{0.074 \pm 0.014}$ | $\mathbf{1 8.728 \pm 2.689}$ |
| | | 0.5 | -- | $3.917 \pm 0.343$ | $4.159 \pm 0.455$ | $0.147 \pm 0.022$ | $29.613 \pm 4.822$ |

generalization of Equation 3 with respect to conditionals $p_t(x|z)$ and $u_t(x|z)$ defined according to Equation 8.

The pseudocode for the proposed method, named *Conditional Flow Matching with Context-Aware OT Couplings*, is presented in Algorithm 1 in Appendix E.1. We also provide time complexity analysis in Appendix E.2. In particular, to apply the Sinkhorn algorithm to solve our PAER problem in Equation 13, we make use of the following theorem, a generalized result of Peyré et al. (2019).

**Theorem 3.1.** *Let $\mathbf{C} \in \mathbb{R}^{n_0 \times n_1}$ be a cost matrix and $\mathbf{M} \in \mathbb{R}^{n_0 \times n_1}$ be a prior transition probability matrix. Suppose $\Pi_{\text{CTF-H}}^*$ is the solution to the following prior-aware optimal transport problem:*

$$ \min_{\Pi \in \mathbb{R}^{n_0 \times n_1}} \sum_{k,l} \Pi_{kl} C_{kl} - \epsilon \sum_{k,l} \Pi_{kl} (\log(\Pi_{kl}/M_{kl}) - 1), $$

*where $\epsilon > 0$ is the regularization parameter. Then, we can show that $\Pi_{\text{CTF-H}}^*$ can be computed by Sinkhorn and takes the form $\text{diag}(\mathbf{u}) \cdot \mathbf{M} \odot \exp(-\mathbf{C}/\epsilon) \cdot \text{diag}(\mathbf{v})$, where $\odot$ denotes element-wise multiplication, and $\mathbf{u} \in \mathbb{R}^{n_0}, \mathbf{v} \in \mathbb{R}^{n_1}$ are vectors satisfying the marginalization constraints.*

Theorem 3.1, proven in Appendix C, suggests a new Gibbs kernel $\mathbf{K} = \mathbf{M} \odot \exp(-\mathbf{C}/\epsilon)$, which combines both the transport cost and the prior joint probability matrices. When $\epsilon \to 0, \Pi_{\text{CTF-H}}^* \to \Pi_{\text{ot}}^*$, thereby recovering the standard OT couplings in Equation 14. When $\epsilon \to \infty$, the optimal coupling $\Pi_{\text{CTF-H}}^* \to \text{diag}(\mathbf{u}) \cdot \mathbf{M} \cdot \text{diag}(\mathbf{v})$, which corresponds to a plan that aligns with the prior defined by $\mathbf{M}$ rather than the independent couplings obtained with EOT defined by Equation 7. This has the same effect as constraining our transport plan through the proposed prior and, by extension, the flow. By varying the parameter $\epsilon$, we can thus efficiently optimize for a desirable coupling via the Sinkhorn algorithm.

## 4. Experiments

**Datasets.** We evaluate ContextFlow on three longitudinal spatial transcriptomics datasets: Axolotl Brain Regeneration (Wei et al., 2022), Mouse Embryo Organogenesis (Chen et al., 2022), and Liver Regeneration (Ben-Moshe et al., 2021). For all the evaluated datasets, the gene expression values are log-normalized, and we extract the top 50 principal components (PCs) as feature vectors. The strength of ligand–receptor interactions in the microenvironment was inferred using spatially informed bivariate statistics implemented in LIANA+ (Dimitrov et al., 2024), where we applied the cosine similarity metric to gene expression profiles. Interaction evidence was aggregated using the consensus of multiple curated ligand–receptor resources, ensuring robustness of the inferred signals.

**Baselines & Metrics.** We benchmark ContextFlow using its two prior integration strategies—cost-regularized (CTF-C) and entropy-regularized (CTF-H)—against several existing flow matching baselines. As a non-spatial baseline, we include conditional flow matching (CFM), which uses only transcriptomic data with random couplings. We further compare against minibatch-OT flow matching (MOTFM), which leverages OT-derived couplings but does not incorporate spatial priors. For evaluation, we employed the 2-Wasserstein distance ($\mathcal{W}_2$), a commonly used OT-based metric, as well as MMD and Energy Distance for statistical fidelity. Furthermore, to assess the biological plausibility of our predicted dynamics, we evaluate them using a cell-type-weighted Wasserstein distance (Weighted $\mathcal{W}_2$), where the weights correspond to the relative frequency of each cell type in the dataset. Exact metric definitions are present in Appendix B.2. To account for randomness, all reported metrics are averaged across 10 runs.