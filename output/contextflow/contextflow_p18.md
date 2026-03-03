**Context-Aware Flow Matching for Trajectory Inference from Spatial Omics Data**

$$\implies \Pi_{kl}^* \to u_k M_{kl} v_l$$
$$\implies \Pi_{\text{CTF-H}}^* \to \text{diag}(\boldsymbol{u}) \cdot \mathbf{M} \cdot \text{diag}(\boldsymbol{v})$$

Such that marginal constraints, $\Pi_{\text{CTF-H}}^* \mathbf{1} = a$ and $\Pi_{\text{CTF-H}}^{* \top} \mathbf{1} = b$ are satisfied. $\square$

### D. Effects of normalization on Prior aware cost matrix

From (Peyré et al., 2019), we know that optimal MOTFM coupling takes the form $\Pi_{\text{EOT}}^* = \text{diag}(u) \cdot K \cdot \text{diag}(v)$, where $K$ is the kernel matrix such that $[K]_{ij} = \exp(\frac{-c_{ij}}{\epsilon})$, with $u, v$ satisfying marginalization constraints $u \odot Kv = a$ and $K^T u \odot v = b$. Sinkhorn updates are given by:

$$u^{l+1} = \frac{a}{Kv^l}; v^{l+1} = \frac{b}{K^T u^{l+1}}.$$

In cases where the OT cost function consists of information from different modalities the distances are usually normalized to have distances of a similar scale. Normalizing the cost results $\tilde{c}_{ij} = \frac{c_{ij}}{c}$ such that the new kernel matrix $[K_{\text{norm}}]_{ij} = \exp(\frac{-c_{ij}}{c_{\text{max}} \epsilon})$ can cause numerical issues if $C_{\text{max}} \gg 1$. The cost normalization should be performed mindfully, when considering different pairwise distances, as in PACM Section 3. Intuitively, scaling the cost has the same effect as that of increasing $\epsilon$, making solutions more diffused.

**Proposition C.1.** *Let $C \in \mathbb{R}^{n_0 \times n_1}$ be a cost matrix and $M \in \mathbb{R}^{n_0 \times n_1}$ a prior transition matrix with positive entries. Consider the entropy-regularized OT formulation:*

$$\Pi^* = \text{argmin}_{\Pi \ge 0} \sum_{k,l} \Pi_{kl} C_{kl} + \epsilon \sum_{k,l} \Pi_{kl} (\log(\Pi_{kl}) - 1).$$

*Let $\tilde{\Pi}^*$ be the EOT-coupling where the cost is scaled by a normalization constant $c$ or $\tilde{C}_{ij} = \frac{C_{ij}}{c}$. Let the regularization parameter $\epsilon > 0$ be the same in both cases. Then, for any indices $(i, j)$ and $(k, l)$ we have*

$$\frac{\tilde{\Pi}_{ij}^*}{\tilde{\Pi}_{kl}^*} \le \gamma \left( \frac{\Pi_{ij}^*}{\Pi_{kl}^*} \right)^{\frac{1}{c}},$$

*where $\gamma$ depends on $\Pi_{ij}^*, c$ and OT marginal constraints $a, b$.*

From Proposition 1, let $\frac{\Pi_{ij}^*}{\Pi_{kl}^*} = m$, such that $m > 1$ ($\Pi_{ij}^* > \Pi_{kl}^*$ or entries are faraway) then, for $c > 1$, we have $\frac{\tilde{\Pi}_{ij}^*}{\tilde{\Pi}_{kl}^*} < m^{\frac{1}{c}} < m$, for $\gamma < 1$, implying that faraway entries are squeezed together. This results in bringing probabilities that are far apart closer to each other or, in essence, in creating more diffused and less sharp couplings.

**Proposition C.2.** *Let $C \in \mathbb{R}^{n_0 \times n_1}$ be a cost matrix and $M \in \mathbb{R}^{n_0 \times n_1}$ a prior transition matrix with positive entries. Consider the entropy-regularized OT formulation:*

$$\Pi^* = \text{argmin}_{\Pi \ge 0} \sum_{k,l} \Pi_{kl} C_{kl} + \epsilon \sum_{k,l} \Pi_{kl} (\log(\Pi_{kl}) - 1)$$

*and $\tilde{\Pi}^*$ be EOT-coupling in the case when cost is scaled by a normalization constant $c$ or $\tilde{C}_{ij} = \frac{C_{ij}}{c}$. Let the regularization parameter $\epsilon > 0$ be the same in both cases. Then we have:*

$$H(\tilde{\Pi}_{ij}) \ge m H(\Pi_{ij}) - s$$

*where $m$ and $s$ are constants, that depend on $\Pi^*$, marginalization constants $a, b$ and normalization constant $c$.*

Corollary C.2 can also be interpreted as supporting the results of Proposition C.1 and our intuition that normalizing has the same effect on the kernel matrix as increasing $\epsilon$, leading to more diffused couplings or couplings with increased entropy.