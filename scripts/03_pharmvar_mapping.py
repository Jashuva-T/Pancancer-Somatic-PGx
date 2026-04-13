"""
Script: 03_pharmvar_mapping.py

Purpose:
Annotate pharmacogene variants and classify variant types

Input:
- results/pharmacogene_variants.csv

Output:
- results/pharmacogene_variants_annotated.csv
"""
#!/usr/bin/env python3

import pandas as pd
import os

# ==============================
# CONFIGURATION
# ==============================

INPUT_FILE = "../results/pharmacogene_variants.csv"
OUTPUT_FILE = "../results/pharmacogene_variants_annotated.csv"

# ==============================
# FUNCTION: CLEAN HGVSp
# ==============================

def clean_protein_change(hgvsp):
    if pd.isna(hgvsp):
        return None

    # Remove encoding artifacts
    hgvsp = str(hgvsp).replace("%3D", "=")

    # Keep only standard protein notation
    if hgvsp.startswith("p."):
        return hgvsp
    else:
        return None

# ==============================
# FUNCTION: CLASSIFY VARIANT TYPE
# ==============================

def classify_variant(row):
    vc = row.get("Variant_Classification", "")

    if vc in ["Nonsense_Mutation"]:
        return "LOF"

    elif vc in ["Frame_Shift_Del", "Frame_Shift_Ins"]:
        return "LOF"

    elif vc in ["Splice_Site"]:
        return "LOF"

    elif vc in ["Missense_Mutation"]:
        return "MISSENSE"

    elif vc in ["Silent"]:
        return "SILENT"

    else:
        return "OTHER"

# ==============================
# MAIN PIPELINE
# ==============================

def annotate_variants():
    print("Loading extracted variants...")

    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE)

    print(f"Total variants loaded: {len(df)}")

    # Clean protein change column
    df["Protein_Change"] = df["HGVSp_Short"].apply(clean_protein_change)

    # Classify variant types
    df["Variant_Category"] = df.apply(classify_variant, axis=1)

    # Flag high-impact variants
    df["High_Impact"] = df["Variant_Category"].apply(
        lambda x: "YES" if x == "LOF" else "NO"
    )

    # Remove rows without protein info (optional but cleaner)
    df_clean = df[df["Protein_Change"].notna()].copy()

    print(f"Variants with protein annotation: {len(df_clean)}")

    # Save output
    os.makedirs("../results", exist_ok=True)
    df_clean.to_csv(OUTPUT_FILE, index=False)

    print(f"Annotated variants saved to: {OUTPUT_FILE}")


# ==============================
# RUN
# ==============================

if __name__ == "__main__":
    annotate_variants()
