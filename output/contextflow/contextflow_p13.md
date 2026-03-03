**Context-Aware Flow Matching for Trajectory Inference from Spatial Omics Data**

is the kernel for the scaled/normalized OT formulation. Let $\tilde{\Pi}_{ij}^*$ be the coupling for the scaled version, then:

$$\tilde{\Pi}_{ij}^* = \tilde{u}_i \tilde{K}_{ij} \tilde{v}_j.$$

Thus, there exist scaling factors $\alpha_i, \beta_j \in \mathbb{R}$ such that:

$$\tilde{u}_i = \alpha_i u_i^{\frac{1}{c}},$$
$$\tilde{v}_j = \beta_j v_j^{\frac{1}{c}}.$$

This implies:

$$\tilde{\Pi}_{ij}^* = (\alpha_i u_i^{1/c}) \tilde{K}_{ij} (\beta_j v_j^{1/c}),$$
$$\implies \tilde{\Pi}^* = \text{diag}(\alpha u^{1/c}) \tilde{K} \text{diag}(\beta v^{1/c}), \tag{g1}$$
$$\implies \tilde{\Pi}^* = \text{diag}(\alpha) \Pi^{1/c} \text{diag}(\beta).$$

Subject to the constraints:

$$\sum_j \alpha_i \beta_j \Pi_{ij}^{*1/c} = a_i, \quad \sum_i \alpha_i \beta_j \Pi_{ij}^{*1/c} = b_j.$$

For any pair $(i, j) \& (k, l)$, we can express:

$$\frac{\tilde{\Pi}_{ij}^*}{\tilde{\Pi}_{kl}^*} = \frac{\alpha_i}{\alpha_k} \frac{\beta_j}{\beta_l} \left( \frac{\Pi_{ij}^*}{\Pi_{kl}^*} \right)^{1/c}.$$

Taking logarithms on both sides, we have:

$$\log \left( \frac{\tilde{\Pi}_{ij}^*}{\tilde{\Pi}_{kl}^*} \right) = \log(\alpha_i) - \log(\alpha_k) + \log(\beta_j) - \log(\beta_l) + \frac{1}{c} \log \left( \frac{\Pi_{ij}^*}{\Pi_{kl}^*} \right).$$

Let $\log(\alpha) = \phi$ and $\log(\beta) = \psi$, then:

$$\log \left( \frac{\tilde{\Pi}_{ij}^*}{\tilde{\Pi}_{kl}^*} \right) = (\phi_i - \phi_k) + (\psi_j - \psi_l) + \frac{1}{c} \log \left( \frac{\Pi_{ij}^*}{\Pi_{kl}^*} \right).$$

This implies:

$$\left| \log \left( \frac{\tilde{\Pi}_{ij}^*}{\tilde{\Pi}_{kl}^*} \right) - \frac{1}{c} \log \left( \frac{\Pi_{ij}^*}{\Pi_{kl}^*} \right) \right| \leq |\phi_i| + |\phi_k| + |\psi_j| + |\psi_l|.$$

From Proposition 3 C.3, we have:

$$\max_i \phi_i \leq E, \quad \max_i \psi_i \leq E.$$

Thus:

$$\left| \log \left( \frac{\tilde{\Pi}_{ij}^*}{\tilde{\Pi}_{kl}^*} \right) - \frac{1}{c} \log \left( \frac{\Pi_{ij}^*}{\Pi_{kl}^*} \right) \right| \leq 4E.$$

Therefore:

$$-4E + \frac{1}{c} \log \left( \frac{\Pi_{ij}^*}{\Pi_{kl}^*} \right) \leq \log \left( \frac{\tilde{\Pi}_{ij}^*}{\tilde{\Pi}_{kl}^*} \right) \leq 4E + \frac{1}{c} \log \left( \frac{\Pi_{ij}^*}{\Pi_{kl}^*} \right).$$

14