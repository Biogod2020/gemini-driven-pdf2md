training stages with held-out somite stages removed) and (iii) augmented (real training stages plus CellPace predictions for the held-out somite stages). We quantified topological similarity using the Ipsen-Mikhailov (IM) distance, a spectral metric that compares eigenvalue distributions of graph Laplacians without requiring explicit node matching (netrd v0.3.0).

### Spatial Mapping and Concordance Analysis

We mapped single-cell transcriptomes from real and CellPace-generated posterior embryos to five coronal tissue sections (E1S1, E2S1-E2S4) from embryonic day 9.5 of the Mouse Organogenesis Spatiotemporal Transcriptomic Atlas (MOSTA [20]) using Tangram [21]. We first harmonized datasets to the intersection of genes shared with the spatial atlas. Tangram was then trained to align single-cell expression profiles with spatial spot expression by minimizing a cosine-similarity loss, yielding per-spot cell-type probability distributions after projecting single-cell annotations onto spatial coordinates. We evaluated mapping quality using per-gene training scores, defined as the cosine similarity between predicted and measured spatial expression. We compared score distributions for real and CellPace-generated mappings using two-sided Kolmogorov-Smirnov tests and stratified genes into four quality tiers (Poor < 0.5; Fair 0.5-0.7; Good 0.7-0.9; Excellent > 0.9) for visualization.

To generate continuous spatial probability maps, we smoothed spot-level probabilities using k-nearest-neighbour averaging with $k = \text{round}(\log_2(N_{\text{spots}})) + 1$, followed by min-max normalization. We quantified spatial concordance between real and CellPace-generated distributions for notochord, neuromesodermal progenitors (NMPs) and spinal cord progenitors, $Tbx6+$ mesodermal progenitors and gut using Pearson and Spearman correlations between probability vectors across all spatial spots.

<br>

29