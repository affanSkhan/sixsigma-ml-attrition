# Reproducibility Guide

Complete instructions to reproduce all analyses, experiments, and results.

---

## Prerequisites

- **Python:** 3.8 or higher
- **OS:** Windows (PowerShell) / Linux / macOS
- **RAM:** 4GB minimum
- **Storage:** 500MB for data + outputs

---

## Quick Start (5 minutes)

### 1. Clone Repository
```bash
git clone https://github.com/affanSkhan/sixsigma-ml-attrition.git
cd sixsigma-ml-attrition
```

### 2. Create Environment
**Option A: Virtual Environment (Recommended)**
```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac
pip install -r requirements.txt
```

**Option B: Conda**
```bash
conda env create -f environment.yml
conda activate sixsigma-attrition
```

### 3. Verify Dataset
Ensure raw data is in place:
```
data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv
```
(Dataset: IBM HR Analytics Employee Attrition - [Kaggle link](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset))

---

## Complete Reproduction (1-2 hours)

Run notebooks **in order** (restart kernel before each):

### Phase 1: Measure
```bash
jupyter notebook notebooks/01_EDA.ipynb              # 10 min - Exploratory analysis
jupyter notebook notebooks/02_baseline_models.ipynb  # 15 min - Baseline models
```

**Outputs:** `figures/eda_*.png`, `tables/baseline_*.csv`

### Phase 2: Analyze
```bash
jupyter notebook notebooks/03_analyze.ipynb          # 20 min - Statistical tests + SHAP
```

**Outputs:** `figures/shap_*.png`, `tables/stat_tests_*.csv`, `paper/03_analyze_decisions.md`

### Phase 3: Improve
```bash
jupyter notebook notebooks/04_improve_experiments.ipynb  # 30 min - 6 experiments
```

**Outputs:** `tables/experiment_results.csv`, `models/exp_*.joblib`

### Phase 4: Control (Final Model)
```bash
jupyter notebook notebooks/05_final_model.ipynb      # 25 min - Model selection + validation
```

**Outputs:** 
- `models/final_attrition_pipeline.pkl`
- `models/model_metadata.json`
- `figures/final_*.png`
- `tables/final_test_metrics.csv`

### Phase 5: Control (Monitoring)
```bash
jupyter notebook notebooks/06_control.ipynb          # 15 min - SPC monitoring simulation
```

**Outputs:** 
- `figures/pchart_pos_rate.png`, `ewma_f1.png`, `psi_heatmap.png`
- `tables/control_batch_metrics.csv`, `psi_by_batch.csv`
- `reports/control_report.json`

---

## Expected Results

### Key Metrics (Test Set)
| Metric | Value | 95% CI |
|--------|-------|--------|
| F1-Score | 0.506 | [0.366, 0.630] |
| Recall | 0.447 | [0.308, 0.587] |
| Precision | 0.583 | [0.417, 0.743] |
| ROC-AUC | 0.811 | [0.739, 0.882] |

### Outputs Generated
- **Figures:** 17 PNG files (300 DPI) in `figures/`
- **Tables:** 17 CSV files in `tables/`
- **Models:** 3 serialized pipelines in `models/`
- **Reports:** JSON alert summary in `reports/`

---

## Reproducibility Notes

### Random Seed
All notebooks use `RANDOM_SEED = 42` for consistency:
- Train/test splits
- Cross-validation folds
- Bootstrap resampling
- Data shuffling

### Dependencies
Exact versions used:
```
scikit-learn==1.7.2
pandas==2.2.2
numpy==1.26.4
matplotlib==3.8.4
seaborn==0.13.2
shap==0.45.0
```

### Known Variations
Minor differences (< 0.01) may occur due to:
- NumPy/scikit-learn version differences
- OS-specific floating point precision
- Parallel processing randomness

---

## Troubleshooting

### Issue: ModuleNotFoundError
**Fix:** Activate environment first
```bash
venv\Scripts\activate  # Windows
pip list  # Verify packages installed
```

### Issue: FileNotFoundError for dataset
**Fix:** Download from Kaggle and place in `data/raw/`
```bash
# Verify file exists
ls data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv
```

### Issue: Kernel dies during notebook execution
**Fix:** Increase memory or reduce batch size
```python
# In notebook, reduce n_batches:
n_batches = 15  # Instead of 30
```

### Issue: ValueError - columns are missing
**Fix:** Restart kernel and run all cells from top
```
Kernel → Restart → Run All
```

### Issue: Different metrics than reported
**Fix:** 
1. Check scikit-learn version: `pip show scikit-learn`
2. Verify random seed: `RANDOM_SEED = 42` in all notebooks
3. Re-run from scratch with fresh environment

---

## Validation Checklist

Before submitting/publishing, verify:

- [ ] All 6 notebooks run without errors
- [ ] 17 figures generated in `figures/`
- [ ] 17 tables saved in `tables/`
- [ ] Final model saved: `models/final_attrition_pipeline.pkl`
- [ ] Metrics match reported values (± 0.01 tolerance)
- [ ] Git commit hash matches paper/documentation
- [ ] Environment frozen: `pip freeze > requirements_freeze.txt`

---

## Docker (Optional)

For complete reproducibility across systems:

```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root"]
```

```bash
docker build -t sixsigma-ml-attrition .
docker run -p 8888:8888 -v $(pwd):/app sixsigma-ml-attrition
```

---

## Citation

If you reproduce this work:

```bibtex
@misc{khan2025sixsigma,
  author = {Khan, Affan},
  title = {Employee Attrition Prediction with Six Sigma DMAIC},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/affanSkhan/sixsigma-ml-attrition},
  note = {Commit: [insert-git-hash]}
}
```

---

## Support

- **Issues:** [GitHub Issues](https://github.com/affanSkhan/sixsigma-ml-attrition/issues)
- **Questions:** Open a discussion on GitHub
- **Bug reports:** Include OS, Python version, and error traceback

