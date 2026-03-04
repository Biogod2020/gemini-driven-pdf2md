This implies:
$$\frac{\tilde{\Pi}_{ij}^*}{\tilde{\Pi}_{kl}^*} \leq \exp(4E) \left( \frac{\Pi_{ij}^*}{\Pi_{kl}^*} \right)^{1/c}.$$

Let $\gamma = \exp(4E)$, then:
$$\frac{\tilde{\Pi}_{ij}^*}{\tilde{\Pi}_{kl}^*} \leq \gamma \left( \frac{\Pi_{ij}^*}{\Pi_{kl}^*} \right)^{1/c}.$$
<p align="right">$\square$</p>

**Corollary C.2.** *Let $\mathbf{C} \in \mathbb{R}^{n_0 \times n_1}$ be a cost matrix and $\mathbf{M} \in \mathbb{R}^{n_0 \times n_1}$ a prior transition matrix with positive entries. Consider the entropy-regularized OT formulation:*
$$\Pi^* = \text{argmin}_{\Pi \geq 0} \sum_{k,l} \Pi_{kl} C_{kl} + \epsilon \sum_{k,l} \Pi_{kl} (\log(\Pi_{kl}) - 1).$$

*Let $\tilde{\Pi}^*$ be the EOT-coupling in the case when cost is scaled by a normalization constant $c$ or $\tilde{C}_{ij} = \frac{C_{ij}}{c}$. Let the regularization parameter $\epsilon > 0$ be the same in both cases. Then:*
$$H(\tilde{\Pi}_{ij}) \geq m H(\Pi_{ij}) - s,$$
*where $m$ and $s$ are constants that depend on $\Pi^*$, the marginalization constants $a, b$ and the normalization constant $c$.*

*Proof.* From equation (g1) in Proposition 1 above, we know that:
$$\tilde{\Pi}_{ij}^* = (\Pi_{ij}^*)^{1/c} \cdot \exp(\phi_i, \psi_j)$$
and from Proposition 2, we have that,
$$\tilde{\Pi}_{ij}^* \leq (\Pi_{ij}^*)^{1/c} \cdot e^{2E}$$
$$\Rightarrow \log(\tilde{\Pi}_{ij}^*) \leq \frac{1}{c} \log(\Pi_{ij}^*) + 2E$$
$$\Rightarrow -\tilde{\Pi}_{ij}^* \log(\tilde{\Pi}_{ij}^*) \geq -\frac{1}{c} (\Pi_{ij}^*)^{1/c-1} \cdot \Pi_{ij}^* \log(\Pi_{ij}^*) \cdot e^{2E} - 2E \cdot e^{2E} \cdot (\Pi_{ij}^*)^{1/c}$$

For $c \gg 1, \frac{1}{c} \to 0$:
$$\Rightarrow -\tilde{\Pi}_{ij}^* \log(\tilde{\Pi}_{ij}^*) \geq -\frac{1}{c \Pi_{ij}^*} \cdot \Pi_{ij}^* \log(\Pi_{ij}^*) \cdot e^{2E} - 2E \cdot e^{2E} \cdot (\Pi_{ij}^*)^{1/c}$$
$$\Rightarrow -\tilde{\Pi}_{ij}^* \log(\tilde{\Pi}_{ij}^*) \geq -\frac{1}{c \Pi_{\min}^*} \cdot \Pi_{ij}^* \log(\Pi_{ij}^*) \cdot e^{2E} - 2E \cdot e^{2E} \cdot (\Pi_{ij}^*)^{1/c}$$

Summing for all $(i, j)$ we get,
$$H(\tilde{\Pi}^*) \geq m H(\Pi^*) - s,$$
where $m = \frac{e^{2E}}{c \Pi_{\min}^*}$ and $s = 2E \cdot e^{2E}$.
<p align="right">$\square$</p>

**Proposition C.3.** *Let $\mathbf{C} \in \mathbb{R}^{n_0 \times n_1}$ be a cost matrix and $\mathbf{M} \in \mathbb{R}^{n_0 \times n_1}$ a prior transition matrix with positive entries. Consider the entropy-regularized OT formulation:*
$$\Pi^* = \text{argmin}_{\Pi \geq 0} \sum_{k,l} \Pi_{kl} C_{kl} + \epsilon \sum_{k,l} \Pi_{kl} (\log(\Pi_{kl}) - 1).$$

<p align="center">15</p>