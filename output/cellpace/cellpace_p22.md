stages), and subsequent steps advance the window by a chosen chunk size using previously generated latents as context.

Inference is accelerated using DDIM sampling; standard DDPM sampling is also supported when the number of sampling steps matches the training schedule. This combination of pyramid scheduling, which allocates denoising effort across timepoints, and DDIM, which accelerates latent updates, enables efficient generation of coherent developmental sequences of latent cell states. Once clean latent representations $z$ are obtained, we decode them to gene expression using the frozen VAE decoder. For multi-omics models trained with MultiVI, we generate the gene-expression modality from the joint latent representation and sample chromatin accessibility separately from its Bernoulli output distribution.

## Datasets and Preprocessing

#### Single-cell RNA-seq datasets:

We obtained developmental single-cell RNA-seq data from the mouse embryo atlas [15], which profiles over 11 million cells across embryonic days E6.5-E13.5. To focus on lineages with fine-grained temporal resolution, we restricted our analysis to cells with somite-level stage annotations, excluding cells labelled “somite_na” (approximately 2 million cells across 32 somite stages), and to protein-coding genes. From this subset, we selected three progenitor cell types for temporal modelling based on two criteria: (1) sufficient temporal coverage, with at least 50 cells per somite stage for most stages to enable stable train-test splits; and (2) representation of diverse developmental contexts and abundance levels. The resulting datasets comprised epithelial cells (n = 54k), retinal progenitor cells (n = 35k) and embryonic blood vessel endothelial progenitor cells (n = 9k).

To assess whether CellPace can preserve biological heterogeneity when modelling multiple interacting lineages simultaneously, we additionally constructed a fourth dataset, “posterior embryo” (n = 121k), comprising five spatially co-located but transcriptionally distinct groups: notochord, ciliated nodal cells, neuromesodermal progenitors (NMPs) and spinal cord progenitors (combined), gut, and mesodermal progenitors (embryonic days E8.0-E10.0), following the filtering criteria in [15].

All datasets underwent standardized preprocessing using Scanpy v1.11 [31]: quality-control filtering (minimum 100 genes per cell and minimum 3 cells per gene), doublet detection using Scrublet [32], normalization to 10,000 counts per cell and $\log_1p$ transformation. Raw count matrices were retained in the AnnData object (layers[“raw_counts”]) and used directly for model training.

<br>

23