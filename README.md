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
│   └── 03_classification_herG.ipynb # Build and evaluate hERG classification models
├── src/
│   ├── preprocessing.py             # SMILES canonicalization
│   ├── features.py                  # RDKit descriptors and Morgan fingerprints
│   └── evaluation.py                # Scaffold utility
├── results/                         # Saved hERG model results and predictions
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
3. `03_classification_herG.ipynb` creates a scaffold-based hERG split, calculates molecular descriptors and Morgan fingerprints, compares Random Forest and SVC models, tunes their hyperparameters, and evaluates the selected model on a held-out test set.

The notebooks save intermediate data and results in `data/processed/` and `data/splits/`. Run earlier notebooks first if those files need to be recreated.

## Modeling workflows and results

### Aqueous solubility regression

The solubility task predicts the continuous `Solubility` value from a molecule's structure.

- The scaffold-based split contains 8,354 training molecules and 1,628 held-out test molecules, with Bemis–Murcko scaffolds kept disjoint.
- The workflow computes 210 RDKit descriptors, removes descriptors with invalid or constant values, and scales features using the training data.
- Random Forest and XGBoost are compared. A five-fold `GroupKFold` search tunes the Random Forest while keeping molecules with the same scaffold together.
- The selected Random Forest uses 100 trees and a maximum depth of 30. Its validation RMSE is 1.107 and its held-out test RMSE is 1.105, compared with 2.360 for a mean-prediction baseline. The much lower training RMSE (0.389) indicates some remaining overfitting.

### hERG classification

The hERG task predicts whether a molecule is a **blocker** (`1`) or **non-blocker** (`0`).

- The cleaned dataset contains 645 molecules and 439 Bemis–Murcko scaffold groups; a scaffold-disjoint split gives 519 training and 126 test molecules.
- Random Forest and SVC classifiers are compared using 210 RDKit descriptors and 2,048-bit Morgan fingerprints (radius 2). Five-fold `StratifiedGroupKFold` cross-validation keeps scaffolds together.
- Average precision is the primary selection metric, with ROC-AUC, F1, precision, recall, and accuracy also reported. The selected model, SVC with RDKit descriptors, achieves 0.924 average precision, 0.882 ROC-AUC, and 0.846 F1 on the held-out test set.
- Test metrics, predictions, and the confusion matrix are saved in `results/` alongside the cross-validation and tuning results.

Both workflows reserve their scaffold-disjoint test sets for final evaluation. The hERG result files are `herg_default_cv_results.csv`, `herg_tuned_cv_results.csv`, `herg_best_params.json`, `herg_test_results.csv`, `herg_test_confusion_matrix.csv`, and `herg_test_predictions.csv`.

## Dependencies

The main libraries are RDKit, pandas, NumPy, scikit-learn, XGBoost, PyTDC, and Jupyter. The complete list is in [`requirements.txt`](requirements.txt).
