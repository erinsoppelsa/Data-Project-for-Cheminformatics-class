# Cheminformatics Project

This project explores molecular data and uses machine learning to study two properties:

- **Aqueous solubility** as a regression task.
- **hERG channel blocking** as a binary classification task.

The analysis uses molecular structures in SMILES format, RDKit features, and scaffold-based data splits. Scaffold splits help keep molecules with similar core structures together when separating training and test data.

## Project structure

```text
.
├── data/
│   ├── solubility_aqsoldb.tab       # Raw AqSolDB solubility data
│   ├── herg.tab                     # Raw hERG data
│   ├── processed/                   # Cleaned data and saved model inputs/results
│   └── splits/                      # Saved scaffold split data
├── notebooks/
│   ├── 01_data_exploration.ipynb    # Load, inspect, and clean both datasets
│   ├── 02_regression_solubility.ipynb # Build and evaluate solubility models
│   └── 03_classification_herG.ipynb # Split hERG data and create molecular features
├── src/
│   ├── preprocessing.py             # SMILES canonicalization
│   ├── features.py                  # RDKit descriptors and Morgan fingerprints
│   └── evaluation.py                # Scaffold utility
├── results/                         # Space for final figures and tables
└── requirements.txt
```

## Setup

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Run the notebooks

Start Jupyter from the project directory:

```bash
jupyter lab
```

Run the notebooks in order:

1. `01_data_exploration.ipynb` loads the AqSolDB and hERG datasets from the Therapeutics Data Commons (TDC), checks the data, and saves cleaned CSV files under `data/processed/`.
2. `02_regression_solubility.ipynb` creates a scaffold-based split, builds molecular features, and compares regression models, including Random Forest and XGBoost.
3. `03_classification_herG.ipynb` creates a scaffold-based hERG split and calculates molecular descriptors and Morgan fingerprints.

The notebooks save intermediate data and results in `data/processed/` and `data/splits/`. Run earlier notebooks first if those files need to be recreated.

## Dependencies

The main libraries are RDKit, pandas, NumPy, scikit-learn, XGBoost, PyTDC, and Jupyter. The complete list is in [`requirements.txt`](requirements.txt).

