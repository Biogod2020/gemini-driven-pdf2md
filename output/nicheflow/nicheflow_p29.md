The source–target pairs are obtained by computing OT between all microenvironments at time $t$ and $t+1$, yielding a one-to-one coupling used for conditioning and evaluation.

As SPFlow generates individual points and RPCFlow produces randomly sampled, unstructured clouds, these models lack coherent internal structure and are not amenable to structural comparison via GW or FGW. We therefore report these metrics only for models that generate full microenvironments.

The results in Tab. 5 show that NicheFlow, particularly when trained with the GLVFM objective, consistently achieves lower GW and FGW distances compared to baseline models. These findings underscore the structural fidelity of our predictions and further validate the modeling advantages of microenvironment-aware generative training.

**Table 5: Gromov–Wasserstein (GW) and Fused Gromov–Wasserstein (FGW) distances between generated and real microenvironments on mouse embryonic development (MED), axolotl brain development (ABD), and mouse brain aging (MBA). All models are trained with a fixed $\lambda = 0.1$. Results are averaged over five generation runs. Bold indicates the best (lowest) value per column.**

| Model | Objective | GW ($10^2$) MED | FGW MED | GW ($10^2$) ABD | FGW ABD | GW ($10^2$) MBA | FGW MBA |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| NicheFlow | CFM | $0.315 \pm \text{\tiny 0.003}$ | $3.273 \pm \text{\tiny 0.003}$ | $0.783 \pm \text{\tiny 0.002}$ | $3.543 \pm \text{\tiny 0.004}$ | $0.315 \pm \text{\tiny 0.001}$ | $3.531 \pm \text{\tiny 0.000}$ |
| NicheFlow | GVFM | $0.463 \pm \text{\tiny 0.004}$ | $3.167 \pm \text{\tiny 0.007}$ | $0.797 \pm \text{\tiny 0.006}$ | $\mathbf{3.414 \pm \text{\tiny 0.003}}$ | $0.339 \pm \text{\tiny 0.000}$ | $3.387 \pm \text{\tiny 0.000}$ |
| NicheFlow | GLVFM | $\mathbf{0.224 \pm \text{\tiny 0.001}}$ | $\mathbf{3.147 \pm \text{\tiny 0.007}}$ | $\mathbf{0.720 \pm \text{\tiny 0.004}}$ | $3.420 \pm \text{\tiny 0.003}$ | $\mathbf{0.262 \pm \text{\tiny 0.000}}$ | $\mathbf{3.367 \pm \text{\tiny 0.000}}$ |

### D.9 Wasserstein metrics

To complement the local structural assessments with GW and FGW, we additionally include global evaluation metrics that are widely adopted in spatial transcriptomics [48–50]. Specifically, we report the 1-Wasserstein ($\mathcal{W}_1$) and 2-Wasserstein ($\mathcal{W}_2$) distances between predicted and real cell distributions, computed separately over spatial coordinates and gene expression features. These metrics are calculated at the level of individual cell types and averaged across all timepoints and generated samples. This provides a more global perspective on how well the model reconstructs tissue-wide spatial and transcriptional distributions.

**Table 6: Comparison of Wasserstein distances between generated and real tissue structures on the mouse embryonic development (MED) dataset. We compute $\mathcal{W}_1$ and $\mathcal{W}_2$ distances separately for spatial coordinates (Pos.) and gene expression features (Genes), averaged across all generated cell types and timepoints. All models are trained with a fixed value of $\lambda = 0.1$, and results are averaged over five generation runs. Bold indicates the best (lowest) value per column.**

| Model | Obj. | $\mathcal{W}_1$ Pos. | $\mathcal{W}_1$ Genes | $\mathcal{W}_2$ Pos. | $\mathcal{W}_2$ Genes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SPFlow | CFM | $0.634 \pm \text{\tiny 0.004}$ | $6.545 \pm \text{\tiny 0.004}$ | $0.773 \pm \text{\tiny 0.005}$ | $5.585 \pm \text{\tiny 0.005}$ |
| SPFlow | GVFM | $0.612 \pm \text{\tiny 0.005}$ | $6.517 \pm \text{\tiny 0.002}$ | $0.743 \pm \text{\tiny 0.005}$ | $5.609 \pm \text{\tiny 0.113}$ |
| SPFlow | GLVFM | $0.613 \pm \text{\tiny 0.001}$ | $6.457 \pm \text{\tiny 0.003}$ | $0.738 \pm \text{\tiny 0.001}$ | $5.546 \pm \text{\tiny 0.108}$ |
| RPCFlow | CFM | $0.290 \pm \text{\tiny 0.006}$ | $6.303 \pm \text{\tiny 0.004}$ | $0.460 \pm \text{\tiny 0.007}$ | $5.386 \pm \text{\tiny 0.004}$ |
| RPCFlow | GVFM | $0.258 \pm \text{\tiny 0.004}$ | $6.134 \pm \text{\tiny 0.004}$ | $0.398 \pm \text{\tiny 0.006}$ | $5.292 \pm \text{\tiny 0.114}$ |
| RPCFlow | GLVFM | $0.221 \pm \text{\tiny 0.003}$ | $6.087 \pm \text{\tiny 0.002}$ | $0.365 \pm \text{\tiny 0.007}$ | $5.244 \pm \text{\tiny 0.113}$ |
| NicheFlow | CFM | $0.253 \pm \text{\tiny 0.002}$ | $6.177 \pm \text{\tiny 0.001}$ | $0.420 \pm \text{\tiny 0.003}$ | $5.314 \pm \text{\tiny 0.111}$ |
| NicheFlow | GVFM | $0.222 \pm \text{\tiny 0.004}$ | $5.985 \pm \text{\tiny 0.005}$ | $0.352 \pm \text{\tiny 0.006}$ | $5.173 \pm \text{\tiny 0.122}$ |
| NicheFlow | GLVFM | $\mathbf{0.212 \pm \text{\tiny 0.004}}$ | $\mathbf{5.930 \pm \text{\tiny 0.003}}$ | $\mathbf{0.342 \pm \text{\tiny 0.007}}$ | $\mathbf{5.031 \pm \text{\tiny 0.003}}$ |

We evaluate all model variants and training objectives across the three datasets (MED, ABD, MBA) and report the results in Tabs. 6 to 8. NicheFlow with the GLVFM objective consistently achieves the lowest Wasserstein distances across nearly all dimensions in the embryonic development dataset (MED), outperforming both baseline models and alternative objectives.

In the ABD and MBA datasets, which exhibit more gradual spatial evolution or less distinct cell-type boundaries, we observe that RPCFlow sometimes matches or marginally outperforms NicheFlow in isolated metrics. However, as we discussed in Sec. D.7, RPCFlow is not a conditionally consistent model: it does not produce meaningful trajectories given a source microenvironment and lacks

<p align="center">30</p>