import pandas as pd

INPUT_FILE = "../results/pharmacogene_variants_annotated.csv"
OUTPUT_FILE = "../results/pharmacogene_variants_LOF_classified.csv"


def classify_lof(row):
    vc = str(row.get("Variant_Classification", "")).lower()
    impact = str(row.get("IMPACT", "")).upper()

    # -----------------------------
    # Handle missing SIFT / PolyPhen safely
    # -----------------------------
    sift_raw = row.get("SIFT")
    polyphen_raw = row.get("PolyPhen")

    sift = str(sift_raw).lower() if pd.notna(sift_raw) else ""
    polyphen = str(polyphen_raw).lower() if pd.notna(polyphen_raw) else ""

    sift_del = "deleterious" in sift
    poly_dam = ("probably_damaging" in polyphen) or ("possibly_damaging" in polyphen)

    # -----------------------------
    # Tier 1: Definitive LOF (ONLY structural)
    # -----------------------------
    if any(x in vc for x in ["nonsense", "frame_shift", "splice"]):
        return "HIGH_CONFIDENCE_LOF", "structural_variant", "NA"

    # -----------------------------
    # Tier 2: Strong functional prediction
    # (Downgraded to POSSIBLE_LOF — reviewer-safe)
    # -----------------------------
    if sift_del and poly_dam:
        return "POSSIBLE_LOF", "strong_functional_prediction", f"{sift}|{polyphen}"

    # -----------------------------
    # Tier 3: Partial / moderate support
    # -----------------------------
    if (
        ("missense" in vc) and
        (impact in ["MODERATE", "HIGH"]) and
        (sift_del or poly_dam)
    ):
        return "POSSIBLE_LOF", "partial_functional_support", f"{sift}|{polyphen}"

    # conflicting predictions
    if ("missense" in vc) and (sift_del != poly_dam):
        return "POSSIBLE_LOF", "conflicting_predictions", f"{sift}|{polyphen}"

    # -----------------------------
    # Tier 4: Non LOF
    # -----------------------------
    if any(x in vc for x in ["silent", "utr", "intron"]):
        return "NON_LOF", "non_coding_or_silent", "NA"

    return "NON_LOF", "no_evidence", f"{sift}|{polyphen}"


def main():
    print("Loading annotated variants...")
    df = pd.read_csv(INPUT_FILE)

    print(f"Total variants: {len(df)}")

    print("Applying LOF classification...")
    results = df.apply(classify_lof, axis=1)

    df["LOF_category"] = [r[0] for r in results]
    df["LOF_evidence"] = [r[1] for r in results]
    df["functional_support"] = [r[2] for r in results]

    print("Saving results...")
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"LOF classified file saved to: {OUTPUT_FILE}")

    print("\nSummary:")
    print(df["LOF_category"].value_counts())


if __name__ == "__main__":
    main()
