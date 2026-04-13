library(dplyr)
library(readr)

df <- read_csv("../results/pharmacogene_variants_LOF_classified.csv")

cat("Loaded:", nrow(df), "variants\n")

# Only consider HIGH CONFIDENCE LOF
lof_df <- df %>%
  filter(LOF_category == "HIGH_CONFIDENCE_LOF")

# Map gene → phenotype effect
lof_df <- lof_df %>%
  mutate(
    simulated_phenotype = case_when(
      Hugo_Symbol == "CYP2D6" ~ "Poor Metabolizer",
      Hugo_Symbol == "CYP2C19" ~ "Poor Metabolizer",
      Hugo_Symbol == "DPYD" ~ "DPD Deficiency",
      Hugo_Symbol == "TPMT" ~ "Low TPMT Activity",
      TRUE ~ "Unknown"
    ),
    
    clinical_risk = case_when(
      Hugo_Symbol == "DPYD" ~ "Fluoropyrimidine Toxicity",
      Hugo_Symbol == "TPMT" ~ "Thiopurine Toxicity",
      Hugo_Symbol %in% c("CYP2D6", "CYP2C19") ~ "Altered Drug Metabolism",
      TRUE ~ "Unknown"
    )
  )

# Count phenotype shifts per patient
patient_impact <- lof_df %>%
  group_by(Tumor_Sample_Barcode) %>%
  summarise(
    lof_events = n(),
    affected_genes = n_distinct(Hugo_Symbol)
  ) %>%
  arrange(desc(lof_events))

# Save outputs
write_csv(lof_df, "../results/phenotype_simulated_variants.csv")
write_csv(patient_impact, "../results/patient_phenotype_impact.csv")

cat("Simulation complete.\n")
