# Supplementary Materials

## Six Sigma DMAIC for HR Attrition Prediction

**Paper:** Improving Machine Learning Performance for HR Attrition Prediction with a Six Sigma DMAIC Framework  
**Authors:** Affan Shakir Khan  
**Date:** October 2, 2025  
**Repository:** https://github.com/affanSkhan/sixsigma-ml-attrition

---

## Contents

This supplementary archive contains all artifacts for reproducing the research:

### 1. Raw Data (`data/raw/`)
- `WA_Fn-UseC_-HR-Employee-Attrition.csv` (1,470 employees, 35 features)
- Source: IBM HR Analytics dataset (Kaggle, 2017)
- Citation: See paper references

### 2. Trained Models (`models/`)
- `final_attrition_pipeline.pkl` - Production model (threshold-optimized cost-sensitive LR)
- `baseline_logreg_pipeline.pkl` - Baseline logistic regression
- `baseline_lr_pipeline.joblib` - Baseline (joblib format)
- `exp_smote_rf.joblib` - Experiment E2 (SMOTE+RF, failed)
- `exp_combined_log_smote_rf.joblib` - Experiment E6 (combined, failed)
- `model_metadata.json` - Model provenance and performance

**Usage:**
```python
import joblib
import pandas as pd

# Load production model
model = joblib.load('models/final_attrition_pipeline.pkl')

# Load test data
X_test = pd.read_csv('data/processed/X_test.csv')

# Predict with optimized threshold (0.388)
probas = model.predict_proba(X_test)[:, 1]
predictions = (probas >= 0.388).astype(int)
```

### 3. Result Tables (`tables/`)

All experimental results in CSV format (25 files):

#### Dataset Statistics
- `dataset_summary.csv` - Data quality summary (rows, cols, missing)
- `descriptive_stats_numeric.csv` - Univariate statistics (mean, median, std, min, max)
- `attrition_counts.csv` - Class distribution (237 Yes, 1,233 No)
- `correlation_numeric.csv` - 26×26 correlation matrix

#### Statistical Tests
- `stat_tests_numeric.csv` - t-tests/Mann-Whitney for 26 features (p-values, effect sizes)
- `stat_tests_categorical.csv` - Chi-square tests for 9 features (Cramér's V)
- `vif_table.csv` - Multicollinearity assessment (JobLevel VIF=11.21)

#### Data Quality
- `outlier_summary.csv` - Outlier frequencies by IQR method
- `potential_mislabeled.csv` - 6 high-confidence mispredictions for review

#### Model Performance
- `baseline_metrics_cv.csv` - 5-fold CV results for 3 baseline models
- `baseline_holdout_metrics.csv` - Hold-out test results (N=294)
- `experiment_results.csv` - 6 controlled experiments with p-values, effect sizes
- `final_test_metrics.csv` - Final model with bootstrap 95% CIs
- `final_model_comparison_cv.csv` - 3 candidate models comparison

#### Robustness Analysis
- `threshold_sensitivity.csv` - Performance across 6 thresholds (0.30-0.50)
- `sensitivity_analysis.csv` - Preprocessing variation impact
- `fairness_gender.csv` - Bias analysis (baseline)
- `final_fairness_gender.csv` - Bias analysis (final model)

#### Control Phase
- `control_batch_metrics.csv` - Simulated monitoring (10 batches)
- `psi_by_batch.csv` - Population Stability Index by feature
- `kl_by_batch.csv` - KL-divergence by feature

#### Feature Importance
- `feature_importances_rf.csv` - Random Forest Gini importance (all features)

### 4. Figures (`figures/`)

126 publication-quality plots (300 DPI, PNG format):

#### Baseline & EDA (17 main figures)
- `baseline_confusion_matrices.png` - 3 baseline models
- `baseline_roc_curves.png` - ROC comparison (AUC values)
- `eda_corr_heatmap.png` - Correlation heatmap (26 features)
- `feature_importance_rf.png` - Top 20 features (RF)
- `pareto_issues.png` - Data quality issues ranked

#### Final Model Performance (6 figures)
- `final_confusion_matrix.png` - Test set (TN=245, FP=2, FN=26, TP=21)
- `final_roc_pr_curves.png` - ROC (AUC=0.811) + PR (AUC=0.583)
- `threshold_optimization.png` - Precision-Recall tradeoff
- `threshold_sensitivity_analysis.png` - Metrics across 6 thresholds
- `calibration_curve.png` - Predicted vs observed frequencies (Brier=0.124)
- `bootstrap_distributions.png` - 1,000 bootstrap resamples (95% CIs)

#### Interpretability (2 figures)
- `shap_summary.png` - SHAP for baseline RF
- `shap_final_improved.png` - SHAP for final model (OverTime, Income, Age)

#### Control Phase Monitoring (5 figures)
- `pchart_pos_rate.png` - p-chart with control limits
- `ewma_f1.png` - Exponentially Weighted Moving Average
- `page_hinkley.png` - Online change detection
- `psi_heatmap.png` - PSI by feature and batch
- `kl_divergence.png` - KL-divergence heatmap

#### EDA Subdirectories (96 plots)
- `eda_distributions/` - Histograms for 26 numeric features
- `bivariate_plots/` - Bar/box plots by attrition status

### 5. Analysis Notebooks (`notebooks/`)

Six Jupyter notebooks implementing DMAIC phases:

1. **01_EDA.ipynb** (Measure Phase - EDA)
   - Dataset profiling, missing values, distributions
   - Correlation analysis, bivariate plots
   - Outputs: 109 figures, 3 tables

2. **02_baseline_models.ipynb** (Measure Phase - Baseline)
   - 3 baseline models (Dummy, LR, DT)
   - 5-fold CV + hold-out test
   - Outputs: Confusion matrices, ROC curves, 2 tables

3. **03_analyze.ipynb** (Analyze Phase)
   - Statistical tests (t-test, chi-square, Mann-Whitney)
   - VIF multicollinearity analysis
   - SHAP feature importance
   - Outlier detection, mislabeling
   - Outputs: 6 tables, 2 figures

4. **04_improve_experiments.ipynb** (Improve Phase)
   - 6 controlled experiments (E1-E6)
   - Statistical validation (McNemar, FDR correction)
   - Negative results documentation
   - Outputs: experiment_results.csv

5. **05_final_model.ipynb** (Control Phase - Model Selection)
   - Threshold optimization (0.388)
   - Bootstrap CIs (1,000 resamples)
   - Robustness validation (5 checks)
   - Fairness analysis (gender bias)
   - Outputs: 6 figures, 5 tables

6. **06_control.ipynb** (Control Phase - Monitoring)
   - SPC tools (p-chart, EWMA)
   - Drift detection (PSI, KL, Page-Hinkley)
   - Simulated monitoring (10 batches)
   - Outputs: 5 figures, 3 tables

**Running Notebooks:**
```bash
# Create environment
conda env create -f environment.yml
conda activate sixsigma-ml-attrition

# Or use pip
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Launch Jupyter
jupyter lab

# Open notebooks/01_EDA.ipynb and run cells sequentially
```

### 6. Environment Specifications

#### `environment.yml` (Conda)
```yaml
name: sixsigma-ml-attrition
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.12
  - pandas=2.2
  - numpy=1.26
  - scikit-learn=1.5
  - matplotlib=3.8
  - seaborn=0.13
  - jupyter=1.0
  - shap=0.44
  # ... (see file for complete list)
```

#### `requirements.txt` (pip)
```
pandas==2.2.0
numpy==1.26.3
scikit-learn==1.5.0
matplotlib==3.8.2
seaborn==0.13.1
jupyter==1.0.0
shap==0.44.0
scipy==1.12.0
statsmodels==0.14.1
imbalanced-learn==0.12.0
# ... (see file for complete list)
```

**Python Version:** 3.12  
**Seed:** 42 (all experiments)

### 7. Documentation (`paper/`)

#### Research Paper Documents (7 markdown files)
- `01_introduction.md` - Motivation, RQ, hypotheses, contributions
- `02_measure_phase.md` - Dataset characteristics, baseline performance
- `03_analyze_decisions.md` - 14 evidence-based preprocessing decisions
- `04_improve_results.md` - 6 experiments with statistical validation
- `05_final_results.md` - Final model performance, robustness, model card
- `06_control_phase_summary.md` - Production deployment, SPC monitoring
- `appendix_control_plan.md` - Detailed control plan (SPC, drift detection)

#### Quality Assurance
- `VERIFICATION_REPORT.md` - Cross-reference verification (100% accuracy)
- `CORRECTION_SUMMARY.md` - Verification corrections applied
- `PUBLICATION_CHECKLIST.md` - Pre-submission checklist

#### LaTeX Manuscript
- `draft_v1.tex` - IEEE conference paper (12 pages)
- `references.bib` - BibTeX bibliography (15 citations)
- `COMPILATION_GUIDE.md` - LaTeX compilation instructions

### 8. Control Plan (`paper/appendix_control_plan.md`)

Production deployment guide:

#### Monitoring Strategy
- **Metrics:** F1, Recall, Precision, Positive prediction rate
- **Frequency:** Batch monitoring (every 30 predictions) + monthly review

#### SPC Tools
- **p-Chart:** Positive prediction rate (UCL=0.265, LCL=0.135)
- **EWMA:** F1-score trend (λ=0.2, ±3σ control limits)

#### Drift Detection
- **PSI:** <0.1 stable, 0.1-0.2 moderate, >0.2 severe shift
- **KL-Divergence:** Threshold=0.5 per feature
- **Page-Hinkley:** δ=0.005, λ=50
- **ADWIN:** Adaptive sliding window (online)

#### Retraining Triggers
- **Performance:** F1 < 0.40 for 2 consecutive weeks
- **Drift:** Any PSI>0.2 or KL>0.5
- **Fairness:** Gender bias >0.10
- **Scheduled:** Monthly retraining on 6-month rolling window

#### Alerting
- **Critical:** Immediate Slack/email + incident ticket
- **Warning:** Dashboard flag + weekly review
- **Info:** Log to monitoring database

### 9. Reproducibility Instructions

#### Full Reproduction (All Notebooks)
```bash
# 1. Clone repository
git clone https://github.com/affanSkhan/sixsigma-ml-attrition.git
cd sixsigma-ml-attrition

# 2. Create environment
conda env create -f environment.yml
conda activate sixsigma-ml-attrition

# 3. Run all notebooks (sequential)
jupyter nbconvert --execute --to notebook \
  --inplace notebooks/01_EDA.ipynb

jupyter nbconvert --execute --to notebook \
  --inplace notebooks/02_baseline_models.ipynb

jupyter nbconvert --execute --to notebook \
  --inplace notebooks/03_analyze.ipynb

jupyter nbconvert --execute --to notebook \
  --inplace notebooks/04_improve_experiments.ipynb

jupyter nbconvert --execute --to notebook \
  --inplace notebooks/05_final_model.ipynb

jupyter nbconvert --execute --to notebook \
  --inplace notebooks/06_control.ipynb

# 4. Verify outputs
ls figures/*.png  # Should show 126 figures
ls tables/*.csv   # Should show 25 tables
ls models/*.pkl   # Should show 6 models
```

**Expected Runtime:** ~45 minutes on standard laptop (Intel i7, 16GB RAM)

#### Quick Validation (Final Model Only)
```python
import joblib
import pandas as pd
from sklearn.metrics import classification_report

# Load model and test data
model = joblib.load('models/final_attrition_pipeline.pkl')
X_test = pd.read_csv('tables/X_test.csv')  # If saved
y_test = pd.read_csv('tables/y_test.csv')

# Predict with threshold=0.388
probas = model.predict_proba(X_test)[:, 1]
y_pred = (probas >= 0.388).astype(int)

# Verify metrics
print(classification_report(y_test, y_pred))
# Expected: F1=0.506, Recall=0.447, Precision=0.583
```

---

## File Manifest

```
supplementary/
├── data/
│   └── raw/
│       └── WA_Fn-UseC_-HR-Employee-Attrition.csv  (1,470 rows, 220 KB)
├── models/
│   ├── final_attrition_pipeline.pkl               (78 KB)
│   ├── baseline_logreg_pipeline.pkl               (52 KB)
│   ├── baseline_lr_pipeline.joblib                (51 KB)
│   ├── exp_smote_rf.joblib                        (1.2 MB)
│   ├── exp_combined_log_smote_rf.joblib           (1.1 MB)
│   └── model_metadata.json                        (3 KB)
├── tables/                                         (25 CSV files, 512 KB)
├── figures/                                        (126 PNG files, 15 MB)
├── notebooks/                                      (6 ipynb files, 2.1 MB)
├── environment.yml                                 (2 KB)
├── requirements.txt                                (1 KB)
├── paper/
│   ├── appendix_control_plan.md                   (11 KB)
│   ├── 03_analyze_decisions.md                    (28 KB)
│   └── draft_v1.tex                               (45 KB)
├── README.md                                       (This file)
└── LICENSE                                         (MIT License)

Total Size: ~20 MB (compressed ZIP: ~8 MB)
```

---

## Citation

If you use this code or data in your research, please cite:

```bibtex
@article{khan2025sixsigma,
  title={Improving Machine Learning Performance for HR Attrition Prediction 
         with a Six Sigma DMAIC Framework},
  author={Khan, Affan Shakir},
  journal={IEEE Conference Proceedings},
  year={2025},
  note={Code and data: https://github.com/affanSkhan/sixsigma-ml-attrition}
}
```

---

## License

**Code:** MIT License (see repository LICENSE file)  
**Dataset:** IBM HR Analytics dataset (Kaggle, public domain)  
**Paper:** © 2025 Authors. All rights reserved.

---

## Contact

**Repository:** https://github.com/affanSkhan/sixsigma-ml-attrition  
**Issues:** https://github.com/affanSkhan/sixsigma-ml-attrition/issues  
**Email:** affan.khan@example.com

---

## Acknowledgments

- IBM for providing the HR Analytics dataset
- Kaggle community for dataset curation
- scikit-learn, SHAP, pandas developers for open-source tools
- IEEE for publication template

---

**Version:** 1.0  
**Last Updated:** October 2, 2025  
**DOI:** [To be assigned upon Zenodo deposit]
