# Context-Aware Flow Matching for Trajectory Inference from Spatial Omics Data

Let $\tilde{\Pi}^*$ be the EOT-coupling in the case when cost is scaled by a normalization constant $c$ or $\tilde{C}_{ij} = \frac{C_{ij}}{c}$. Let the regularization parameter $\epsilon > 0$ be the same in both cases. Consider the scaling factors $\alpha, \beta$ such that: $\tilde{u}_i = \alpha_i u_i^{1/c}$, $\tilde{v}_j = \beta_j v_j^{1/c}$ where $u, v$ are the Sinkhorn algorithm converged vectors for the original setting and $\tilde{u}, \tilde{v}$ are for the cost-scaled version. Then, we have

$$\max \{ \|\phi\|_\infty, \|\psi\|_\infty \} \leq \|M^{-1}\|_\infty \cdot \left\| \begin{pmatrix} \Delta_a \\ \Delta_b \end{pmatrix} \right\|_\infty,$$

where $\phi = \log(\alpha)$ and $\psi = \log(\beta)$. We also have that,

$$\max_i |\alpha_i - 1|, \max_i |\beta_i - 1| \leq \|M^{-1}\|_\infty \max(\|\Delta_a\|_\infty, \|\Delta_b\|_\infty),$$

where $M, \Delta_a, \Delta_b$ depend on $\Pi^*$, marginalization constants $a, b$ and normalization constant $c$.

*Proof.* Let $X_{ij} = \Pi_{ij}^{*1/c}$ and $X = \Pi^{*1/c}$. Consider the exponentiated versions of $\alpha$ and $\beta$:

$$\phi = \log(\alpha) \in \mathbb{R}^n, \quad \psi = \log(\beta) \in \mathbb{R}^m.$$

From the marginal constraints, we have:

$$\sum_j X_{ij} e^{\phi_i + \psi_j} = a_i, \quad \sum_i X_{ij} e^{\phi_i + \psi_j} = b_j.$$

Applying a first-order Taylor expansion gives:

$$\sum_j X_{ij}(1 + \phi_i + \psi_j) = a_i \quad \implies \quad \sum_j X_{ij}(\phi_i + \psi_j) = a_i - \sum_j X_{ij},$$
$$\sum_i X_{ij}(1 + \phi_i + \psi_j) = b_j \quad \implies \quad \sum_i X_{ij}(\phi_i + \psi_j) = b_j - \sum_i X_{ij}.$$

Define:

$$\Delta_{a_i} = a_i - \sum_j X_{ij}, \quad \Delta_{b_j} = b_j - \sum_i X_{ij}.$$

Thus, we have:

$$\sum_j X_{ij}(\phi_i + \psi_j) = \Delta a_i, \quad \sum_i X_{ij}(\phi_i + \psi_j) = \Delta b_j.$$

This implies:

$$\phi_i \left( \sum_j X_{ij} \right) + \sum_j X_{ij} \psi_j = \Delta a_i,$$
$$\sum_i X_{ij} \phi_i + \psi_j \left( \sum_i X_{ij} \right) = \Delta b_j.$$

Let:

$$D_r = \text{diag}(X\mathbf{1}) \in \mathbb{R}^{n \times n}, \quad D_c = \text{diag}(X^T\mathbf{1}) \in \mathbb{R}^{m \times m}.$$

Then we can express the system as:

$$\begin{pmatrix} D_r & X \\ X^T & D_c \end{pmatrix} \begin{pmatrix} \phi \\ \psi \end{pmatrix} = \begin{pmatrix} \Delta a \\ \Delta b \end{pmatrix}.$$

Let:

$$M = \begin{pmatrix} D_r & X \\ X^T & D_c \end{pmatrix}.$$