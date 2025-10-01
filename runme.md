# Reproducibility Quick Guide

Follow these steps to recreate the environment, data processing, experiments, and figures.

## 1. Create environment (conda recommended)

```powershell
conda env create -f environment.yml
conda activate sixsigma-ml-attrition
```

If `environment.yml` is empty or unavailable, use:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Download dataset

See `data/README.md` for instructions. Place the raw CSV in:

```
data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv
```

## 3. Run exploratory data analysis

Open and run all cells in:

```
notebooks/01_EDA.ipynb
```

## 4. Run baseline and improvement experiments

Execute (in order if possible):

```
notebooks/02_baseline_models.ipynb
notebooks/04_improve_experiments.ipynb
```

## 5. Generate publication figures

Run:

```
notebooks/06_generate_figures.ipynb
```

This will save high-resolution PNGs into `figures/`.

## 6. Freeze exact environment (optional but recommended)

```powershell
pip freeze > requirements_freeze.txt
```

Commit the freeze file only for archival or publication tagging.

## 7. Exact reproducibility checklist

- Use `requirements_freeze.txt` to recreate the environment
- Confirm seed in `src/config.py` (SEED=42)
- Ensure same preprocessing steps (see `data/README.md`)
- Avoid modifying notebooks mid-run; restart kernel and run all

## 8. (Optional) Validate metrics

Add assertions / metric logging in future scripts (not yet included). If present, re-run with:

```powershell
python scripts/validate_final_model.py
```

(Script not yet implemented.)

## 9. Troubleshooting

| Issue                                      | Fix                                                                                     |
|--------------------------------------------|----------------------------------------------------------------------------------------|
| ImportError                                 | Verify environment active: `conda activate sixsigma-ml-attrition`                     |
| FileNotFoundError for raw CSV              | Check path: `data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv`                        |
| Different metrics than reported             | Confirm seed & library versions; regenerate processed data                            |

## 10. Suggested future automation

- Add a Makefile or `invoke` tasks
- Add a single `reproduce_all.sh` / `.ps1` script
- Persist Optuna study to an RDB backend for tuning continuity

---

If you need an automated script version of these steps, open an issue.

