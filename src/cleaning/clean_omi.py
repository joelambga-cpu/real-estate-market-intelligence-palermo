from pathlib import Path
import csv
import pandas as pd

# Visualizzazione più leggibile nel terminale
pd.set_option("display.max_colwidth", None)
pd.set_option("display.width", 200)

# -----------------------------------
# Percorsi progetto
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

# Vecchio dataset MVP
# RAW_FILE = (
#     BASE_DIR
#     / "data"
#     / "raw"
#     / "omi_quotations.csv"
# )

# Dataset completo Palermo 2025 S2
RAW_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "palermo_omi_2025S2_49_zone.csv"
)

PROCESSED_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "omi_quotations_clean.csv"
)

print("File letto:")
print(RAW_FILE)

# -----------------------------------
# 1. Controllo struttura CSV
# -----------------------------------

with open(RAW_FILE, encoding="utf-8-sig") as file:
    reader = csv.reader(file)

    for numero_riga, row in enumerate(reader, start=1):
        print(
            f"Riga {numero_riga}: "
            f"{len(row)} colonne"
        )

# -----------------------------------
# 2. Caricamento dataset
# -----------------------------------

df = pd.read_csv(
    RAW_FILE,
    encoding="utf-8-sig"
)

print("\nPrime righe:")
print(df.head())

print("\nDimensioni dataset:")
print(df.shape)

print("\nTipi di dato:")
print(df.dtypes)

print("\nValori mancanti:")
print(df.isna().sum())

# -----------------------------------
# 3. Conversione colonne numeriche
# -----------------------------------

numeric_cols = [
    "anno",
    "semestre",
    "prezzo_min_mq",
    "prezzo_max_mq",
    "affitto_medio_mq_mese",
]

for col in numeric_cols:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

# -----------------------------------
# 4. KPI immobiliari
# -----------------------------------

df["prezzo_medio_mq"] = (
    df["prezzo_min_mq"]
    + df["prezzo_max_mq"]
) / 2

df["range_prezzo_mq"] = (
    df["prezzo_max_mq"]
    - df["prezzo_min_mq"]
)

df["rental_yield_proxy_pct"] = (
    (
        df["affitto_medio_mq_mese"]
        * 12
    )
    / df["prezzo_medio_mq"]
    * 100
)

# -----------------------------------
# 5. Periodo analitico
# -----------------------------------

df["periodo"] = (
    df["anno"].astype(str)
    + "-S"
    + df["semestre"].astype(str)
)

# -----------------------------------
# 6. Prime metriche
# -----------------------------------

print("\nPrime metriche immobiliari:")

print(
    df[
        [
            "comune",
            "codice_zona",
            "fascia",
            "zona_omi",
            "prezzo_medio_mq",
            "affitto_medio_mq_mese",
            "range_prezzo_mq",
            "rental_yield_proxy_pct",
        ]
    ].head()
)

# -----------------------------------
# 7. Quality checks
# -----------------------------------

print("\nControlli qualità:")

print(
    "Prezzi vendita non validi:",
    (
        df["prezzo_min_mq"]
        > df["prezzo_max_mq"]
    ).sum()
)

print(
    "Affitti medi nulli o negativi:",
    (
        df["affitto_medio_mq_mese"]
        <= 0
    ).sum()
)

duplicate_cols = [
    "anno",
    "semestre",
    "comune",
    "codice_zona",
    "destinazione",
    "tipologia",
    "stato_conservativo",
]

print(
    "Righe duplicate:",
    df.duplicated(
        subset=duplicate_cols
    ).sum()
)

# -----------------------------------
# 8. Salvataggio dataset pulito
# -----------------------------------

df.to_csv(
    PROCESSED_FILE,
    index=False
)

print("\nDataset pulito salvato in:")
print(PROCESSED_FILE)