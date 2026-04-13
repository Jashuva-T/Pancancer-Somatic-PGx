# Pan-Cancer Somatic Pharmacogenomics Pipeline

This repository contains the analysis pipeline used in the study:

"Pan-Cancer Somatic Pharmacogene Loss-of-Function and Its Impact on Clinically Actionable Drug Metabolism"

## Overview

This pipeline integrates somatic mutation data from TCGA with PharmVar and CPIC pharmacogenomic frameworks to:

- Identify pharmacogene variants (CYP2D6, CYP2C19, DPYD, TPMT)
- Classify loss-of-function (LOF) variants
- Map variants to PharmVar star-alleles
- Quantify tumour-specific disruption frequencies
- Model germline-somatic phenotype override
- Assess clinical actionability using CPIC guidelines

## Data Availability

This repository does NOT host raw genomic datasets.

All data must be obtained directly from official sources:

- TCGA (GDC Data Portal): https://portal.gdc.cancer.gov/
- PharmVar: https://www.pharmvar.org/
- CPIC: https://cpicpgx.org/
- ClinVar: https://www.ncbi.nlm.nih.gov/clinvar/
- gnomAD: https://gnomad.broadinstitute.org/

Users must obtain appropriate authorization where required.

## Workflow

1. Download TCGA MC3 dataset
2. Extract pharmacogene variants
3. Map variants to PharmVar
4. Perform LOF classification
5. Run tumour frequency analysis
6. Execute phenotype override simulation
7. Generate figures

## Reproducibility

- Python 3.11
- R 4.3.1

All scripts are provided for full reproducibility.

## License

MIT Licensey
# Pancancer-Somatic-PGx
Pipeline for pan-cancer analysis of somatic pharmacogene variants (CYP2D6, CYP2C19, DPYD, TPMT), including LOF classification, PharmVar mapping, and phenotype override modelling with CPIC-based clinical actionability.

## Input Format

- TCGA MC3 MAF file (GRCh37)
- Required columns:
  - Hugo_Symbol
  - Variant_Classification
  - HGVSp_Short

## Output Files

| File | Description |
|------|------------|
| pharmacogene_variants.csv | Filtered pharmacogene variants |
| pharmacogene_variants_annotated.csv | Annotated variants |

## Pipeline Overview

TCGA MAF  
↓  
Variant Extraction (Python)  
↓  
Variant Annotation (Python)  
↓  
LOF Classification (Next step)  
↓  
Statistical Analysis (R)  
↓  
Figures  

## Data Versions

- TCGA MC3: v0.2.8
- gnomAD: v4.1
- PharmVar: [add version when used]
- CPIC: [add version when used]

## Example Run

cd scripts  
python3 02_variant_extraction.py  
python3 03_pharmvar_mapping.py  

## Reproducibility Statement

This pipeline reproduces all results presented in the manuscript when executed using the specified data sources and versions.
