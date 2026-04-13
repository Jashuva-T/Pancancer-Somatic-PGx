library(dplyr)
library(readr)

# Load data
df <- read_csv("../results/pharmacogene_variants_LOF_classified.csv")

cat("Total variants:", nrow(df), "\n")

# -----------------------------
# 1. LOF per gene
# -----------------------------
gene_lof <- df %>%
  filter(LOF_category != "NON_LOF") %>%
  group_by(Hugo_Symbol, LOF_category) %>%
  summarise(count = n(), .groups = "drop") %>%
  arrange(desc(count))

write_csv(gene_lof, "../results/gene_LOF_frequency.csv")

# -----------------------------
# 2. Overall LOF distribution
# -----------------------------
lof_summary <- df %>%
  group_by(LOF_category) %>%
  summarise(count = n()) %>%
  mutate(freq = count / sum(count))

write_csv(lof_summary, "../results/LOF_summary.csv")

# -----------------------------
# 3. Per-sample burden
# -----------------------------
sample_lof <- df %>%
  filter(LOF_category != "NON_LOF") %>%
  group_by(Tumor_Sample_Barcode) %>%
  summarise(lof_count = n()) %>%
  arrange(desc(lof_count))

write_csv(sample_lof, "../results/sample_LOF_burden.csv")

cat("Analysis complete.\n")
