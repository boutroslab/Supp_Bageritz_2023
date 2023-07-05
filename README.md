# Bageritz et al., G3 (Bethesda) 2023

Supplemental code for the publication "Glyoxal as alternative fixative for single cell RNA sequencing"

We provide the code for normalizing single-cell RNA sequencing data to account for differences in sequencing depth, ensuring that each sample has the same average number of reads per cell (see Supplementary Figure 2).

## Abstract

Single cell RNA sequencing has become an important method to identify cell types, delineate the trajectories of cell differentiation in whole organisms and understand the heterogeneity in cellular responses. Nevertheless, sample collection and processing remain a severe bottleneck for single cell RNA sequencing experiments. Cell isolation protocols often lead to significant changes in the transcriptomes of cells, requiring novel methods to preserve cell states. Here, we developed and benchmarked protocols using glyoxal as a fixative for single cell RNA sequencing application. Using Drop-seq methodology, we detected high numbers of transcripts and genes from glyoxal-fixed Drosophila cells after scRNA-seq. The effective glyoxal fixation of transcriptomes in Drosophila and human cells was further supported by a high correlation of gene expression data between glyoxal-fixed and unfixed samples. Accordingly, we also found highly expressed genes overlapping to a large extent between experimental conditions. These results indicated that our fixation protocol did not induce considerable changes in gene expression and conserved the transcriptome for subsequent single cell isolation procedures. In conclusion, we present glyoxal as a suitable fixative for Drosophila cells and potentially cells of other species that allows high-quality scRNA-seq applications.

## Content

The python script automatic_samtools_pysam.py needs to be run from a directory that contains:
 1. the metadata_file in tsv format (metadata.tsv)
 2. the cell_barcode_directory with the list of valid cell barcodes per sample
 3. the bam_files_directory containing the bam files to subsample.
It requires python3 and the packages pandas and pysam.

In order to run it please type: __python3 automatic_samtools_pysam.py__ in the right directory.

It first extracts the cell_barcodes in the cell barcode list from the bam files, then subsamples them to the value listed in the metadata_file and then further subsamples it to 75%, 50% and 25% of that value.

If you have any question please contact Erica Valentini e.valentini@dkfz.de

