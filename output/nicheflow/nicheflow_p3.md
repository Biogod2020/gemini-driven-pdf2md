### 3.2 Generative OT on incomparable source and target spaces

Klein et al. [29] generalize the OT FM formulation to settings where the source and target distributions are defined on incomparable spaces and propose an approach to generative entropic OT using FM. Given a standard normal noise distribution with samples $z \sim \mathcal{N}(\mathbf{0}, \mathbf{I}_D)$, the authors show that the following sampling procedure:

\begin{equation}
x_0 \sim p_0, \quad x_1 \sim \delta\left(x_1 - \phi_t^\theta(z \mid x_0)\right),
\end{equation}

defines a generative model that implicitly samples from an Entropic OT (EOT) coupling, where $\phi_t^\theta(z \mid x_0)$ is a FM model that maps noise to target samples, conditioned on source points. To achieve this, $\phi_t^\theta$ is trained using source-target pairs $(x_0, x_1)$ drawn from the EOT coupling $\pi_\epsilon^*$, with $\epsilon$ denoting the entropic regularization parameter, which the model aims to approximate.

Crucially, this formulation enables OT between distinct source and target spaces, as $x_0$ does not flow directly into $x_1$, but instead conditions the generation of target samples from noise.

### 3.3 Source-conditioned VFM

Consider the source-conditioned FM formulation in Sec. 3.2. Given a conditioning source $x_0$ and noise-based generation, the marginal field in Eq. (1) can be written as:

\begin{equation}
u_t(x \mid x_0) = \mathbb{E}_{p_t(x_1 \mid x, x_0)} \left[ u_t(x \mid x_1) \right],
\end{equation}

where we drop the conditioning on $x_0$ in the velocity field, as $u_t$ is entirely determined by the target $x_1$ when generating from noise under linear probability paths.

Since $u_t(x \mid x_1)$ is tractable [23], one can recast FM as a variational inference problem, following Eijkelboom et al. [25], by introducing a parameterized approximation $q_t^\theta(x_1 \mid x, x_0)$ to the true posterior $p_t(x_1 \mid x, x_0)$. Integrating the expected velocity in Eq. (5) over $t \in [0, 1]$ enables the generation of target points $x_1$ from noise, conditioned on $x_0$.

During training, the source-conditioned Variational Flow Matching (VFM) loss is:

\begin{equation}
\mathcal{L}_{\text{SC-VFM}}(\theta) = -\mathbb{E}_{t \sim \mathcal{U}[0,1], (x_0, x_1) \sim \pi_\epsilon^*, x \sim p_t(x \mid x_1)} \left[ \log q_t^\theta(x_1 \mid x, x_0) \right],
\end{equation}

where $\pi_\epsilon^*$ is an entropic OT coupling modeling the joint distribution over source and target samples, and $p_t(x \mid x_1)$ interpolates between target samples and noise. In the generation phase, one samples $x_0 \sim p_0$ and noise $z \sim \mathcal{N}(\mathbf{0}, \mathbf{I}_D)$, then simulates the marginal field in Eq. (5) starting from $\phi_0(x) = z$ to generate a target sample $x_1$.

Crucially, under the assumption that $u_t(x \mid x_1)$ is linear in $x_1$, which holds when using straight-line interpolation paths, the marginal field in Eq. (5) only depends on the posterior's first moment on $x_1$:

\begin{equation}
u_t(x \mid x_0) = u_t \left( x \mid \mathbb{E}_{p_t(x_1 \mid x, x_0)} [x_1] \right)
\end{equation}

This implies that the VFM objective reduces to matching the first moment of the approximate posterior $q_t^\theta(x_1 \mid x, x_0)$ to that of the true posterior $p_t(x_1 \mid x, x_0)$. As a result, the approximate posterior can be chosen fully factorized under a *mean field assumption*, since each dimension can be matched independently if the mean of the true posterior is preserved; see Sec. C.2 for more details.

## 4 NicheFlow

We introduce a flow-based generative model to infer the temporal evolution of spatially resolved cellular microenvironments. More specifically, given a spatial microenvironment represented as a point cloud of cell states with their coordinates, NicheFlow predicts the corresponding tissue structure at a later time point. To delineate our approach, we define a list of desiderata.

##### Generative model on structured data.
Similar to prior work [30, 36], we consider a generative model over structured point cloud data representing cellular microenvironments. This approach implicitly accounts for spatial correlations between cells, in contrast to models that study the evolution of spatial trajectories at the single-cell level [20].

##### Sub-regions and variable location.
Crucially, for better memory efficiency, we do not consider an entire spatial slide for trajectory inference, but instead learn the dynamics of variably located

<p align="center">4</p>