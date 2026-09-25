from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "omi_quotations_clean.csv"
)

DB_FILE = (
    BASE_DIR
    / "data"
    / "database"
    / "real_estate.db"
)

# 1. Leggiamo il dataset pulito
df = pd.read_csv(PROCESSED_FILE)

# 2. Connessione SQLite
conn = sqlite3.connect(DB_FILE)

# 3. Carichiamo il DataFrame nel database
df.to_sql(
    "omi_quotations",
    conn,
    if_exists="replace",
    index=False
)

print("Database creato:")
print(DB_FILE)

print("\nRighe caricate:")
print(len(df))

##Query zone più costose
query = """
SELECT
    codice_zona,
    fascia,
    zona_omi,
    prezzo_medio_mq
FROM omi_quotations
ORDER BY prezzo_medio_mq DESC;
"""

result = pd.read_sql_query(query, conn)

print("\nZone ordinate per prezzo medio:")
print(result)

##Query yield proxy più elevato
query = """
SELECT
    codice_zona,
    fascia,
    zona_omi,
    prezzo_medio_mq,
    affitto_medio_mq_mese,
    rental_yield_proxy_pct
FROM omi_quotations
ORDER BY rental_yield_proxy_pct DESC;
"""

result = pd.read_sql_query(query, conn)

print("\nZone ordinate per rental yield proxy:")
print(result)

##Query analisi per fascia urbana

result = pd.read_sql_query(query, conn)

query_fascia = """
SELECT
    fascia,
    COUNT(*) AS numero_zone,
    ROUND(AVG(prezzo_medio_mq), 2) AS prezzo_medio_mq,
    ROUND(AVG(affitto_medio_mq_mese), 2) AS affitto_medio_mq_mese,
    ROUND(AVG(rental_yield_proxy_pct), 2) AS yield_proxy_medio
FROM omi_quotations
GROUP BY fascia
ORDER BY prezzo_medio_mq DESC;
"""

result_fascia = pd.read_sql_query(query_fascia, conn)

print("\nAnalisi per fascia:")
print(result_fascia)

query_top_prezzi = """
SELECT
    codice_zona,
    fascia,
    zona_omi,
    ROUND(prezzo_medio_mq, 2) AS prezzo_medio_mq
FROM omi_quotations
ORDER BY prezzo_medio_mq DESC
LIMIT 5;
"""

top_prezzi = pd.read_sql_query(
    query_top_prezzi,
    conn
)

print("\nTop 5 zone per prezzo medio €/m²:")
print(top_prezzi)

query_top_yield = """
SELECT
    codice_zona,
    fascia,
    zona_omi,
    ROUND(prezzo_medio_mq, 2) AS prezzo_medio_mq,
    ROUND(affitto_medio_mq_mese, 2) AS affitto_medio_mq_mese,
    ROUND(rental_yield_proxy_pct, 2) AS rental_yield_proxy_pct
FROM omi_quotations
ORDER BY rental_yield_proxy_pct DESC
LIMIT 5;
"""

top_yield = pd.read_sql_query(
    query_top_yield,
    conn
)

print("\nTop 5 zone per rental yield proxy:")
print(top_yield)

conn.close()


