**Context-Aware Flow Matching for Trajectory Inference from Spatial Omics Data**

**Weighted 2-Wasserstein.** Implausible velocity fields can steer a cell's transcriptional trajectory in unrealistic directions, potentially leading to entirely different terminal cell types. We thus employ the weighted 2-Wasserstein metric, which ensures the evaluation accounts for both transcriptional similarity and the distributional balance of cell types. We define the *weighted 2-Wasserstein distance* (Weighted $\mathcal{W}_2$) between true and predicted distributions as:

$$\text{Weighted-}\mathcal{W}_2(\mu, \nu) = \sum_{i=1}^{C} \frac{n_i^{\text{true}}}{N} \cdot \mathcal{W}_2 \bigg( \frac{1}{n_i^{\text{true}}} \sum_{j:y_j=i} \delta_{\boldsymbol{x}_j}, \frac{1}{n_i^{\text{pred}}} \sum_{j:\hat{y}_j=i} \delta_{\hat{\boldsymbol{x}}_j} \bigg),$$

where $n_i^{\text{true}}, n_i^{\text{pred}}$ are the number of true and predicted cells of type $i$, and $N$ is the total number of samples. To determine the cell type of generated trajectories, we employ a multi-class classifier $M_\phi$, implemented as an XGBoost model (Chen & Guestrin, 2016) trained for each dataset.

**Energy Distance.** Let $\mu$ and $\nu$ be probability distributions with samples $X = \{\boldsymbol{x}_i\}_{i=1}^m \sim \mu$ and $Y = \{\boldsymbol{y}_j\}_{j=1}^n \sim \nu$. The squared empirical *energy distance* (Energy) is defined as:

$$\text{ED}(\mu, \nu) = \frac{2}{mn} \sum_{i=1}^m \sum_{j=1}^n \|\boldsymbol{x}_i - \boldsymbol{y}_j\| - \frac{1}{m^2} \sum_{i=1}^m \sum_{i'=1}^m \|\boldsymbol{x}_i - \boldsymbol{x}_{i'}\| - \frac{1}{n^2} \sum_{j=1}^n \sum_{j'=1}^n \|\boldsymbol{y}_j - \boldsymbol{y}_{j'}\|,$$

where $\|\cdot\|$ is the Euclidean norm. The distance is non-negative and equals zero if and only if $\mu = \nu$.

**Maximum Mean Discrepancy.** For the same samples, the unbiased empirical estimate of the squared *maximum mean discrepancy* (MMD) with kernel $\kappa$ is defined as:

$$\text{MMD}(\mu, \nu; \kappa) = \frac{1}{m(m-1)} \sum_{i \neq i'} \kappa(\boldsymbol{x}_i, \boldsymbol{x}_{i'}) + \frac{1}{n(n-1)} \sum_{j \neq j'} \kappa(\boldsymbol{y}_j, \boldsymbol{y}_{j'}) - \frac{2}{mn} \sum_{i=1}^m \sum_{j=1}^n \kappa(\boldsymbol{x}_i, \boldsymbol{y}_j).$$

In our evaluations, we use a multi-kernel variant with radial basis function (RBF) kernels $\kappa_\gamma(\boldsymbol{x}, \boldsymbol{y}) = \exp(-\gamma \|\boldsymbol{x} - \boldsymbol{y}\|^2)$, and average over $\gamma \in [2, 1, 0.5, 0.1, 0.01, 0.005]$.

### C. Proofs of Main Theoretical Results

**Proposition C.1.** *Let $C \in \mathbb{R}^{n_0 \times n_1}$ be a cost matrix and $M \in \mathbb{R}^{n_0 \times n_1}$ a prior transition matrix with positive entries. Consider the entropy-regularized OT formulation:*

$$\Pi^* = \text{argmin}_{\Pi \geq 0} \sum_{k,l} \Pi_{kl} C_{kl} + \epsilon \sum_{k,l} \Pi_{kl} (\log(\Pi_{kl}) - 1).$$

*Let $\tilde{\Pi}^*$ be the EOT-coupling where the cost is scaled by a normalization constant $c$ or $\tilde{C}_{ij} = \frac{C_{ij}}{c}$. Let the regularization parameter $\epsilon > 0$ be the same in both cases. Then, for indices $(i, j)$ and $(k, l)$,*

$$\frac{\tilde{\Pi}^*_{ij}}{\tilde{\Pi}^*_{kl}} \leq \gamma \left( \frac{\Pi^*_{ij}}{\Pi^*_{kl}} \right)^{\frac{1}{c}},$$

*where $\gamma$ depends on $\Pi^*_{ij}, c$ and the OT marginal constraints $a, b$.*

*Proof.* For the original optimal transport (OT) formulation, we note:

$$\Pi^*_{ij} = u_i K_{ij} v_j, \quad K_{ij} = e^{-C_{ij}/\epsilon},$$

with the constraints $\Pi^* \mathbf{1} = a$ and $\Pi^{*\top} \mathbf{1} = b$.

Let
$$\Pi^{*1/c}_{ij} = u_i^{1/c} K_{ij}^{1/c} v_j^{1/c},$$

where:
$$\tilde{K}_{ij} = K_{ij}^{1/c} = \exp(-C_{ij}/(c\epsilon))$$