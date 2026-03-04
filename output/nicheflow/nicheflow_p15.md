straight paths [23], the marginal generative field becomes:
\begin{equation}
\begin{aligned}
u_t(\boldsymbol{x}) & = \mathbb{E}_{q_t^\theta(\boldsymbol{x}_1 \mid \boldsymbol{x})} \left[ u_t(\boldsymbol{x} \mid \boldsymbol{x}_1) \right] \\
& = u_t \left( \boldsymbol{x} \mid \mathbb{E}_{q_t^\theta(\boldsymbol{x}_1 \mid \boldsymbol{x})} [\boldsymbol{x}_1] \right) \\
& = \frac{\mu_t^\theta(\boldsymbol{x}) - \boldsymbol{x}}{1 - t} .
\end{aligned}
\end{equation}
which can be easily simulated in the range $t \in [0, 1]$.

### 3.2 Factorized posterior

Similar to Eijkelboom et al. [25], in our work, we use a fully factorized posterior, where individual dimensions can follow different families of distributions with finite moments (see Sec. 4.3). Notably, a factorized approximate posterior over $\boldsymbol{x}_1$ is allowed as a choice for $q_t^\theta$, since the only requirement to simulate $u_t(\boldsymbol{x})$ is for $q_t^\theta(\boldsymbol{x}_1 \mid \boldsymbol{x})$ to match the expectation of $p_t(\boldsymbol{x}_1 \mid \boldsymbol{x})$ over $\boldsymbol{x}_1$, irrespectively of higher moments or correlations between factors.

In this regard, it is useful to consider the following proposition.

**Proposition 1.** *Let $\boldsymbol{x}_1 \in \mathbb{R}^D$ be a D-dimensional target data point, $p_t(\boldsymbol{x}_1 \mid \boldsymbol{x})$ the posterior probability path conditioned on a noisy point $\boldsymbol{x} \sim p_t(\boldsymbol{x})$, and $u_t(\boldsymbol{x} \mid \boldsymbol{x}_1)$ the conditional velocity field. Assume that $u_t(\boldsymbol{x} \mid \boldsymbol{x}_1)$ is linear in $\boldsymbol{x}_1$. Then, for any dimension $d \in \{1, \dots, D\}$, the following holds:*
\begin{equation}
\mathbb{E}_{p_t(\boldsymbol{x}_1 \mid \boldsymbol{x})} [x_1^d] = \mathbb{E}_{p_t(x_1^d \mid \boldsymbol{x})} [x_1^d]
\end{equation}
\begin{equation}
u_t(x^d) = u_t \left( x^d \mid \mathbb{E}_{p_t(x_1^d \mid \boldsymbol{x})} [x_1^d] \right) ,
\end{equation}
*where $x^d$ refers to the $d^{\text{th}}$ scalar dimension of the vector $\boldsymbol{x}$.*

*Proof.* We begin by proving Eq. (19) using marginalization:
\begin{equation}
\begin{aligned}
\mathbb{E}_{p_t(\boldsymbol{x}_1 \mid \boldsymbol{x})} [x_1^d] & = \int x_1^d p_t(\boldsymbol{x}_1 \mid \boldsymbol{x}) \mathrm{d}\boldsymbol{x}_1 \\
& = \int x_1^d \left( \int p_t(\boldsymbol{x}_1 \mid \boldsymbol{x}) \mathrm{d}\boldsymbol{x}_1^{\setminus d} \right) \mathrm{d}x_1^d \\
& = \int x_1^d p_t(x_1^d \mid \boldsymbol{x}) \mathrm{d}x_1^d .
\end{aligned}
\end{equation}
Next, we prove Eq. (20). Under the assumption that the conditional velocity field $u_t(\boldsymbol{x} \mid \boldsymbol{x}_1)$ is linear in $\boldsymbol{x}_1$, we have:
\begin{equation}
\begin{aligned}
u_t(x^d) & = \mathbb{E}_{p_t(\boldsymbol{x}_1 \mid \boldsymbol{x})} \left[ u_t(x^d \mid \boldsymbol{x}_1) \right] \\
& \stackrel{(1)}{=} \mathbb{E}_{p_t(\boldsymbol{x}_1 \mid \boldsymbol{x})} \left[ u_t(x^d \mid x_1^d) \right] \\
& = \mathbb{E}_{p_t(\boldsymbol{x}_1 \mid \boldsymbol{x})} \left[ \frac{x_1^d - x^d}{1 - t} \right] \\
& = \frac{\mathbb{E}_{p_t(\boldsymbol{x}_1 \mid \boldsymbol{x})} [x_1^d] - x^d}{1 - t} \\
& \stackrel{Eq. (21)}{=} \frac{\mathbb{E}_{p_t(x_1^d \mid \boldsymbol{x})} [x_1^d] - x^d}{1 - t} \\
& = u_t \left( x^d \mid \mathbb{E}_{p_t(x_1^d \mid \boldsymbol{x})} [x_1^d] \right) .
\end{aligned}
\end{equation}
Here, step (1) follows from the linearity assumption, which ensures that the conditional velocity at $x^d$ depends only on $x_1^d$.

In other words, the expected value under the posterior at an individual feature $d$ does not depend on the other features and has an influence only on the $d$-th dimension of the conditional vector field. This flexibility allows each dimension's approximate posterior to be chosen from a potentially different distributional family, as long as the first moment exists and is correctly parameterized.

<center>16</center>