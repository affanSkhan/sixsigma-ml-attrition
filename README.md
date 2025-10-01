# Employee Attrition Prediction with Six Sigma DMAIC

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.7-orange)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **DMAIC-driven machine learning for HR attrition prediction with production-ready monitoring**

---

## 🎯 Key Results

| Metric | Baseline | Final Model | Improvement |
|--------|----------|-------------|-------------|
| **F1-Score** | 0.438 | 0.506 | +15.5% |
| **Recall** | 0.340 | 0.447 | **+31.3%** |
| **Precision** | 0.630 | 0.583 | -7.5% |
| **ROC-AUC** | 0.812 | 0.811 | -0.1% |

✅ **+31% recall improvement** = ~5 additional at-risk employees identified per cycle  
✅ **Threshold optimization** from 0.50 → 0.388 for balanced F1  
✅ **Production monitoring** with SPC charts, PSI, and drift detection

---

## 📊 Project Overview

**Problem:** IBM HR Analytics dataset (1,470 employees, 16.1% attrition)  
**Goal:** Predict employee attrition to enable proactive retention  
**Method:** Six Sigma DMAIC methodology applied to ML lifecycle  
**Result:** Cost-sensitive logistic regression with 7 robustness checks

---

## 🔬 DMAIC Phases

### 1️⃣ **Define**
- Business problem: $50K replacement cost per employee
- Success criteria: F1 ≥ 0.52, Recall ≥ 0.40, ROC-AUC ≥ 0.80

### 2️⃣ **Measure**
- Baseline: Logistic Regression (F1=0.438, ROC-AUC=0.812)
- Data quality checks, EDA, correlation analysis

### 3️⃣ **Analyze**
- Statistical tests (t-test, chi-square, Mann-Whitney)
- SHAP feature importance analysis
- 14 preprocessing decisions documented

### 4️⃣ **Improve**
- 6 experiments tested: SMOTE, Random Forest, Transformations, RobustScaler
- **Result:** All failed to beat baseline (negative results documented)
- **Winner:** Simple threshold optimization on baseline model

### 5️⃣ **Control**
- Final model: Cost-Sensitive LR + Threshold=0.388
- 7 robustness checks: Bootstrap CIs, preprocessing sensitivity, threshold sensitivity, calibration, fairness, hold-out test
- Production monitoring: p-chart, EWMA, Page-Hinkley, PSI, KL-divergence

---

## 📁 Repository Structure

```
├── data/                    # Raw dataset (IBM HR Analytics)
├── notebooks/              # 6 Jupyter notebooks (EDA → Control)
│   ├── 01_EDA.ipynb
│   ├── 02_baseline_models.ipynb
│   ├── 03_analyze.ipynb
│   ├── 04_improve_experiments.ipynb
│   ├── 05_final_model.ipynb
│   └── 06_control.ipynb    # Monitoring simulation
├── models/                 # Trained pipelines + metadata
├── figures/                # 17 publication-quality figures (300 DPI)
├── tables/                 # 17 CSV result tables
├── paper/                  # DMAIC documentation + appendices
│   ├── 05_final_results.md           # Full model card
│   ├── 06_control_phase_summary.md   # Paper Section 5
│   └── appendix_control_plan.md      # Deployment guide
└── src/                    # Configuration
```

---

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Clone repository
git clone https://github.com/affanSkhan/sixsigma-ml-attrition.git
cd sixsigma-ml-attrition

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Notebooks
```bash
# Run notebooks in order (1-6)
jupyter notebook notebooks/
```

### 3. View Results
- **Model performance:** `tables/final_test_metrics.csv`
- **Feature importance:** `figures/shap_final_improved.png`
- **Monitoring:** `reports/control_report.json`

---

## 📈 Monitoring Features

Production-ready monitoring with:
- **p-chart:** Positive prediction rate (3σ limits)
- **EWMA:** F1-score trend detection (λ=0.2)
- **Page-Hinkley:** Mean shift detection
- **PSI:** Feature drift (34 features tracked)
- **KL-divergence:** Categorical distribution monitoring

**Retraining triggers:**
- PSI ≥ 0.2 on any feature
- F1 below control limits for 3+ weeks
- ≥500 new labeled observations

---

## 📚 Key Findings

1. **Simple > Complex:** Threshold-tuned logistic regression beat all complex methods (SMOTE, RF, transformations)
2. **Threshold matters:** Moving from 0.50 → 0.388 improved F1 by 15.5%
3. **Cost-sensitive learning:** `class_weight='balanced'` crucial for imbalanced data
4. **Negative results:** 6/6 experiments failed - transparently documented
5. **Robustness checks:** 7 validations ensure production stability

---

## 🛠️ Tech Stack

- **Python 3.8+** | **scikit-learn 1.7** | **pandas** | **numpy**
- **SHAP** for interpretability | **matplotlib/seaborn** for viz
- **Statistical tests:** scipy | **Monitoring:** Custom SPC implementation

---

## 📄 Documentation

- **Full model card:** [`paper/05_final_results.md`](paper/05_final_results.md) (565 lines)
- **Control plan:** [`paper/appendix_control_plan.md`](paper/appendix_control_plan.md)
- **Paper Section 5:** [`paper/06_control_phase_summary.md`](paper/06_control_phase_summary.md)
- **Publication checklist:** [`paper/PUBLICATION_CHECKLIST.md`](paper/PUBLICATION_CHECKLIST.md)

---

## 🎓 Citation

If you use this work, please cite:
```bibtex
@misc{khan2025sixsigma,
  author = {Khan, Affan},
  title = {Employee Attrition Prediction with Six Sigma DMAIC},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/affanSkhan/sixsigma-ml-attrition}
}
```

---

## 📧 Contact

**Affan Khan**  
GitHub: [@affanSkhan](https://github.com/affanSkhan)

---

## 📜 License

[MIT License](LICENSE) - Free to use for research and education

