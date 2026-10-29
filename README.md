# Real Estate Market Intelligence – Palermo

## Project Overview

This project analyzes residential real estate market data for Palermo using OMI reference quotations.

The goal is to build a reproducible data pipeline that transforms raw real estate data into useful market insights using Python, SQL, SQLite and Power BI.

The analysis covers 49 residential OMI zones and compares property prices, rental values and an indicative rental yield proxy.

## Tech Stack

- Python
- pandas
- SQL
- SQLite
- Power BI
- Git / GitHub

## Key Metrics

The project calculates:

- Average property price per square meter
- Average monthly rent per square meter
- Price range within each OMI zone
- Indicative gross rental yield proxy
- Market comparisons by urban band
- Top zones by price and rental yield

## Data Pipeline

The project follows a simple end-to-end analytics workflow:

1. Raw OMI real estate data is stored in CSV format.
2. Python and pandas are used to clean and validate the dataset.
3. Additional analytical features are calculated, including:
   - Average property price per square meter
   - Price range
   - Indicative rental yield proxy
   - Analysis period
4. The cleaned dataset is loaded into a SQLite database.
5. SQL queries are used to compare market segments and identify top-performing zones.
6. Power BI is used to explore and visualize the processed data.

## Key Insights

The analysis highlights several differences across Palermo's residential market:

- Central zones have the highest average reference price, approximately **€1,540/m²**.
- Semi-central zones show the highest average indicative rental yield proxy, approximately **4.93%**.
- The three zones with the highest yield proxy are all semi-central: **C4, C5 and C3**.
- **B20** is the most expensive zone in the dataset, with an average reference value of approximately **€2,400/m²**.
- High property values do not necessarily correspond to higher rental yields.
- The results suggest a trade-off between property value and potential rental income across different urban areas.

> **Note:** The rental yield metric used in this project is an indicative gross proxy based on OMI reference values. It does not represent actual investment returns and does not include taxes, vacancy, maintenance, transaction costs or other property-related expenses.

## Installation and usage

From a terminal with Python available:

```powershell
git clone https://github.com/joelambga-cpu/real-estate-market-intelligence-palermo.git
cd real-estate-market-intelligence-palermo
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src/cleaning/clean_omi.py
```

On macOS/Linux, replace `.\.venv\Scripts\python.exe` with `.venv/bin/python`.

After cleaning succeeds, run the SQL analysis with your environment's Python:

```powershell
.\.venv\Scripts\python.exe src/analysis/omi_sql.py
```

The SQL script creates `data/database/real_estate.db` and replaces the `omi_quotations` table on each run. Open [RealEstate.pbix](powerbi/RealEstate.pbix) with Power BI Desktop; local data-source paths may need updating before refresh.

## Input and reproducibility limits

The cleaning script uses [palermo_omi_2025S2_49_zone.csv](data/raw/palermo_omi_2025S2_49_zone.csv); the smaller `omi_quotations.csv` is an earlier sample. Price midpoints and annualized rent/price ratios are calculated from the supplied CSV. The script prints quality diagnostics but does not stop on every invalid value. Original source extraction and provenance need fuller documentation; the repository does not automate an OMI download.
