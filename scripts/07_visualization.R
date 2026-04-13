library(ggplot2)
library(dplyr)
library(readr)

df <- read_csv("../results/pharmacogene_variants_LOF_classified.csv")
sim <- read_csv("../results/phenotype_simulated_variants.csv")

# Ensure figures folder exists
dir.create("../figures", showWarnings = FALSE)

# -----------------------------
# Figure 1: LOF Category Distribution (context)
# -----------------------------
p1 <- df %>%
  count(LOF_category) %>%
  ggplot(aes(x = LOF_category, y = n)) +
  geom_bar(stat = "identity") +
  labs(title = "Distribution of LOF Categories",
       x = "LOF Category",
       y = "Variant Count") +
  theme_minimal()

ggsave("../figures/Figure1_LOF_Distribution.png", p1, width = 6, height = 4)

# -----------------------------
# Figure 2: Gene-wise HIGH CONFIDENCE LOF
# -----------------------------
p2 <- df %>%
  filter(LOF_category == "HIGH_CONFIDENCE_LOF") %>%
  count(Hugo_Symbol) %>%
  arrange(desc(n)) %>%
  ggplot(aes(x = reorder(Hugo_Symbol, n), y = n)) +
  geom_bar(stat = "identity") +
  coord_flip() +
  labs(title = "Gene-wise Distribution of High-Confidence LOF Variants",
       x = "Gene",
       y = "Number of LOF Variants") +
  theme_minimal()

ggsave("../figures/Figure2_Gene_LOF.png", p2, width = 6, height = 4)

# -----------------------------
# Figure 3: Clinical Impact (STRICT LOF ONLY)
# -----------------------------
p3 <- sim %>%
  count(clinical_risk) %>%
  ggplot(aes(x = clinical_risk, y = n)) +
  geom_bar(stat = "identity") +
  coord_flip() +
  labs(title = "Clinical Risk Associated with Somatic LOF Variants",
       x = "Clinical Outcome",
       y = "Variant Count") +
  theme_minimal()

ggsave("../figures/Figure3_Clinical_Impact.png", p3, width = 6, height = 4)

cat("All manuscript-aligned figures generated.\n")
