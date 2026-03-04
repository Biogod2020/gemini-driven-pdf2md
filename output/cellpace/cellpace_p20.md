A critical innovation in TDiF is its handling of time. Sequence diffusion models typically encode temporal structure using sinusoidal embeddings of integer indices, e.g., $x = x + \text{PositionalEmbed}(0, 1, \dots, T - 1)$, implicitly assuming uniformly spaced observations. In developmental biology, sampling is often irregular and the time gaps between stages (for example, between stages with somite counts of 10 and 18) are biologically informative. Thus, in TDiF we replaced these positional embeddings with a continuous biological time embedding that explicitly encodes both position along the developmental axis and the temporal spacing between observations. Specifically, for each developmental state $s_t$, we constructed a two-dimensional temporal feature vector $h_t = [\tau_t, \Delta_t]$ consisting of:

(1) normalized developmental position $\tau_t = \frac{s_t - s_{\min}}{s_{\max} - s_{\min}}$, which maps the developmental stage $s_t$ to the interval $[0, 1]$ using the minimum and maximum stages observed during training and enables the model to generalize to previously unseen stages within or beyond this range, and

(2) elapsed time gap $\Delta_t = s_t - s_{t-1}$, which captures the temporal interval since the previous position in the sequence (with $\Delta_1 = 0$ for the first position).

By providing explicit gap information, CellPace can learn distinct denoising dynamics for short-range transitions (for example, consecutive somite stages with $\Delta = 1$) versus long-range developmental leaps (for example, interpolating across a gap of $\Delta \ge 5$). The gap features are linearly scaled before processing to maintain numerical stability.

To inject this biological context, we used a Transformer backbone equipped with AdaLN (Fig. 1d). Rather than concatenating time features only at the input, the vector $h_t$ is passed through a small multilayer perceptron (MLP) to produce scale and shift parameters $[\text{scale}_t, \text{shift}_t] = \text{MLP}(h_t)$, which modulate activations within every Transformer block:

$$\text{AdaLN}(x_t) = \text{LayerNorm}(x_t) \odot (1 + \text{scale}_t) + \text{shift}_t.$$

The input pipeline concatenates noised latent embeddings $\tilde{z}_t$ with sinusoidal embeddings of the noise levels $k_t$, and the resulting features are processed by the AdaLN-modulated Transformer. We used AdaLN-Zero initialization for the temporal conditioning MLP (final layer initialized to zero), so that blocks behave as standard LayerNorm at the start of training and temporal modulation is introduced gradually.

## Training and Optimization of CellPace

CellPace training follows a two-stage procedure. In Stage 1, we train the VAE (scVI or MultiVI) to maximize the ELBO. In Stage 2, we train the TDiF model on sequences of VAE latent representations. We construct a training dataset by sampling temporal sequences using a geometric strategy that balances local and long-range dependencies. For each sequence, we