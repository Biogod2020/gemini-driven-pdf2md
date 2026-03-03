![Figure 15: Comparison between NicheFlow and RPCFlow in a fixed-source microenvironment setting. Each row shows input (source), ground truth target, model prediction, and KDE-estimated likelihood. While NicheFlow (top) produces well-localized samples consistent with the input, RPCFlow (bottom) generates less structured and spatially inaccurate predictions.](assets/fig15.png)

compute both metrics over collections of microenvironments tiled across the tissue, providing an indirect assessment of global morphological accuracy.

To directly assess the preservation of internal structure within generated microenvironments, we additionally evaluate Gromov-Wasserstein (GW) and Fused Gromov-Wasserstein (FGW) distances [47, 40]. These metrics compare the intra-point pairwise distances in predicted and ground truth point clouds, capturing latent structural relationships. FGW further incorporates transcriptomic similarity, offering a holistic measure of structural and feature-based alignment.

Given the computational cost of GW and FGW, we restrict their evaluation to microenvironment-level generations. For each source niche, we sample predictions from the trained model and compute GW/FGW against the corresponding real microenvironment, averaging results across multiple runs.

29