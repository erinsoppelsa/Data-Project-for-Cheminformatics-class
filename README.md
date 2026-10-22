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

## hERG classification workflow

The hERG task predicts whether a molecule is a **blocker** (`1`) or **non-blocker** (`0`).

- The cleaned dataset contains 645 molecules and 439 Bemis–Murcko scaffold groups.
- A scaffold-disjoint split produces 519 training molecules and 126 held-out test molecules.
- The training set is evaluated with five-fold `StratifiedGroupKFold` cross-validation, keeping molecules with the same scaffold in the same fold.
- Two molecular representations are compared:
  - 210 RDKit numerical descriptors.
  - 2,048-bit Morgan fingerprints with radius 2.
- Two classifiers are evaluated with each representation:
  - Random Forest.
  - Support Vector Classifier (SVC).
- Average precision is used as the primary model-selection metric because it evaluates blocker ranking across thresholds and is appropriate when class proportions are unequal. Precision, recall, F1, and ROC-AUC are also reported.
- Missing descriptor values are imputed inside the model pipeline, using parameters learned from the training data only.

The selected final model is **SVC with RDKit descriptors**. On the held-out test set, it achieves:

| Metric | Score |
| --- | ---: |
| ROC-AUC | 0.882 |
| Average precision | 0.924 |
| F1 | 0.846 |
| Precision | 0.825 |
| Recall | 0.868 |
| Accuracy | 0.810 |

The corresponding test confusion matrix contains 36 true negatives, 14 false positives, 10 false negatives, and 66 true positives. The precision–recall curve is included to show the trade-off between detecting more blockers and reducing false blocker predictions. The test set is kept untouched until model selection and final evaluation.

The hERG outputs saved in `results/` are:

- `herg_default_cv_results.csv`: cross-validation results before tuning.
- `herg_tuned_cv_results.csv`: tuned cross-validation comparison.
- `herg_best_params.json`: best hyperparameters for each model and representation.
- `herg_test_results.csv`: final held-out test metrics.
- `herg_test_confusion_matrix.csv`: final held-out test confusion matrix.
- `herg_test_predictions.csv`: held-out test predictions and model scores.

## Dependencies

The main libraries are RDKit, pandas, NumPy, scikit-learn, XGBoost, PyTDC, and Jupyter. The complete list is in [`requirements.txt`](requirements.txt).
