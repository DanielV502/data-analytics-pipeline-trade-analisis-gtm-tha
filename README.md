# LAB 01 — Data Analytics Pipeline

Data Analytics pipeline analyzing bilateral trade between Guatemala and Thailand (GRULAC to APAC) from 2017 to 2024, using UN Comtrade / ITC Trade Map data at HS2 and HS6 product code levels.

## Project Overview

This project explores Guatemala's trade position within the GRULAC (Latin America & Caribbean) region, focusing on exports to APAC (Asia-Pacific) markets with Thailand as the primary partner. The analysis covers:

- **HS2 Macro Analysis** — Guatemala's trade funnel from world exports down to specific partners
- **HS6 Micro Analysis** — Product-level competition among GRULAC reporters
- **Pre/Post Pandemic Analysis** — Impact and recovery trends (2017–2024)

## Project Structure

```
lab-01-data-analytics-pipeline/
├── data/
│   ├── external/               # Third-party or reference datasets
│   ├── interim/                # Intermediate transformed data
│   ├── output/                 # Final output files
│   ├── processed/              # Cleaned and processed datasets (.parquet)
│   └── raw/                    # Original source data files
├── notebooks/
│   ├── 01_exploration.ipynb    # Main exploration and analysis notebook
│   ├── 02_cleaning.ipynb       # Data cleaning notebook
│   └── 03_insights.ipynb       # Insights and summary notebook
├── reports/
│   └── figures/                # Generated charts and visualizations
├── src/
│   ├── config.py               # Paths and shared business constants
│   ├── dataset.py              # Raw CSV loading and concatenation
│   ├── features.py             # Feature engineering and transformations
│   ├── validation.py           # Schema, type, value, and business rule checks
│   ├── services/
│   │   └── io.py               # Processed dataset persistence (parquet + csv)
│   └── pipelines/
│       └── run_pipeline.py     # Pipeline entry point
├── pyproject.toml              # Project metadata and dependencies
└── LICENSE                     # MIT License
```

## Getting Started

### Prerequisites

- Python >= 3.12
- conda (recommended) or pip

### Installation

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/lab-01-data-analytics-pipeline.git
cd lab-01-data-analytics-pipeline
```

2. Create and activate a conda environment:

```bash
conda create -p .conda python=3.12 -y
conda activate ./.conda
```

3. Install dependencies:

```bash
pip install -e .
```

### Running the Pipeline

The data pipeline loads raw trade data, applies transformations and validations, and saves the processed dataset under `data/processed/` (both `.parquet` and `.csv` by default). Run from the project root with the env active:

```bash
python -m pipelines.run_pipeline
```

### Running the Notebooks

Open Jupyter and run the notebooks in order:

1. `01_exploration.ipynb` — Main analysis (requires processed data from the pipeline)
2. `02_cleaning.ipynb` — Data cleaning steps
3. `03_insights.ipynb` — Summary insights

## Data Sources

- [World Integrated Trade Solutions (WITS)](https://wits.worldbank.org/) — Bilateral trade data exports (UN Comtrade / ITC Trade Map)

## Tech Stack

- **Python 3.12** — pandas, matplotlib, seaborn, numpy, pyarrow
- **Data formats** — CSV (raw, from WITS exports), Parquet + CSV (processed)
- **Pipeline** — Custom Python modules under `src/`

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
