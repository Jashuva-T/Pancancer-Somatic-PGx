#!/usr/bin/env python3

import pandas as pd
import gzip
import os

# ==============================
# CONFIGURATION
# ==============================

INPUT_FILE = "../data/mc3.v0.2.8.PUBLIC.maf.gz"
OUTPUT_FILE = "../results/pharmacogene_variants.csv"

PHARMACOGENES = ["CYP2D6", "CYP2C19", "DPYD", "TPMT"]

CHUNK_SIZE = 500000  # adjust based on RAM


# ==============================
# FUNCTION: FILTER MAF
# ==============================

def extract_pharmacogene_variants():
    print("Starting variant extraction...")

    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"MAF file not found: {INPUT_FILE}")

    filtered_chunks = []

    chunk_iter = pd.read_csv(
        INPUT_FILE,
        sep="\t",
        comment="#",
        chunksize=CHUNK_SIZE,
        low_memory=False
    )

    total_rows = 0
    kept_rows = 0

    for i, chunk in enumerate(chunk_iter):
        print(f"Processing chunk {i+1}...")

        total_rows += len(chunk)

        # Ensure correct column exists
        if "Hugo_Symbol" not in chunk.columns:
            raise ValueError("Column 'Hugo_Symbol' not found in MAF file.")

        filtered = chunk[chunk["Hugo_Symbol"].isin(PHARMACOGENES)]

        kept_rows += len(filtered)

        filtered_chunks.append(filtered)

    print(f"\nTotal rows processed: {total_rows}")
    print(f"Pharmacogene rows retained: {kept_rows}")

    final_df = pd.concat(filtered_chunks, ignore_index=True)

    os.makedirs("../results", exist_ok=True)
    final_df.to_csv(OUTPUT_FILE, index=False)

    print(f"\nSaved filtered variants to: {OUTPUT_FILE}")


# ==============================
# RUN
# ==============================

if __name__ == "__main__":
    extract_pharmacogene_variants()
