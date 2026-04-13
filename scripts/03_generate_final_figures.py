import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# Load data
lof_summary = pd.read_csv("../results/LOF_summary.csv")
gene_lof = pd.read_csv("../results/gene_LOF_frequency.csv")
patient_lof = pd.read_csv("../results/patient_phenotype_impact.csv")

# Figure 1
plt.figure()
sns.barplot(data=lof_summary, x="LOF_category", y="freq")
plt.title("Distribution of LOF Variants")
plt.tight_layout()
plt.savefig("../figures/Figure1_final.png")
plt.close()

# Figure 2
plt.figure()
sns.barplot(data=gene_lof, x="Hugo_Symbol", y="count", hue="LOF_category")
plt.title("Gene-wise LOF Burden")
plt.tight_layout()
plt.savefig("../figures/Figure2_final.png")
plt.close()

# Figure 3
plt.figure()
sns.histplot(patient_lof["lof_events"], bins=10, kde=True)
plt.title("LOF Events per Patient")
plt.tight_layout()
plt.savefig("../figures/Figure3_final.png")
plt.close()

# Figure 4
plt.figure()
sns.countplot(x="affected_genes", data=patient_lof)
plt.title("Genes Affected per Patient")
plt.tight_layout()
plt.savefig("../figures/Figure4_final.png")
plt.close()

print("All final figures generated.")
