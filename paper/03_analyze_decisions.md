# Analyze → Improve Decisions

**Date:** 2025-10-01  
**Dataset:** IBM HR Analytics Employee Attrition  
**Phase:** DMAIC Analyze → Improve Transition  
**Author:** Analysis Team

---

## Executive Summary

This document maps statistical and exploratory findings from the **Analyze phase** to concrete, actionable preprocessing and modeling decisions for the **Improve phase**. All decisions are evidence-based, traceable to quantitative analysis (statistical tests, VIF, feature importance, SHAP, outlier detection), and designed to address root causes of baseline model underperformance (recall = 0.34, F1 = 0.44).

**Key Findings:**
- Class imbalance (16.12% attrition rate)
- Severe multicollinearity (VIF > 10 for JobLevel, MonthlyIncome)
- Significant feature skew and outliers
- 6 potential mislabeled cases requiring review
- Strong associations identified for OverTime, JobRole, TotalWorkingYears

---

## 1. Class Imbalance

### Finding
- **Attrition rate:** 16.12% (237 Yes / 1233 No)
- **Impact:** Baseline models biased toward majority class; low recall (0.34)
- **Source:** `tables/attrition_counts.csv`, baseline metrics

### Decision
**Primary approach:** Apply **SMOTE** (Synthetic Minority Over-sampling Technique) on training data only (never on test/validation).

**Alternatives to compare in Improve phase:**
1. **Class weighting:** Set `class_weight='balanced'` in Logistic Regression, RandomForest, XGBoost
2. **Threshold tuning:** Optimize decision threshold using Youden's J-statistic or cost-sensitive F-beta (beta=2 to favor recall)
3. **Ensemble methods:** Use cost-sensitive learning or focal loss in gradient boosting

**Rationale:**
- SMOTE generates synthetic examples in feature space, increasing minority representation without simple duplication
- Class weighting is model-dependent; SMOTE is preprocessing-agnostic
- Will use stratified cross-validation to ensure balance across all folds

**Implementation notes:**
- Apply SMOTE inside CV loop (never before split) to avoid data leakage
- Evaluate with PR-AUC and F1 at multiple thresholds
- Compare performance with/without SMOTE using same model architecture

---

## 2. Severe Multicollinearity

### Finding
**High VIF features:**
| Feature | VIF | Interpretation |
|---------|-----|----------------|
| JobLevel | 11.21 | Severe collinearity |
| MonthlyIncome | 10.80 | Severe collinearity |
| TotalWorkingYears | 4.77 | Moderate |
| YearsAtCompany | 4.59 | Moderate |

**Source:** `tables/vif_table.csv`

**Context:** JobLevel and MonthlyIncome are highly correlated (senior levels → higher income). TotalWorkingYears correlates with both tenure and age.

### Decision
**Option A (Recommended for linear models):**
- **Drop JobLevel** (redundant predictor; MonthlyIncome captures compensation better)
- Apply **Ridge regularization (L2)** in Logistic Regression (alpha tuning via GridSearch)
- Keep MonthlyIncome with log transformation (see Finding 3)

**Option B (For tree-based models):**
- **Keep both JobLevel and MonthlyIncome** as tree algorithms handle collinearity naturally via splits
- No explicit action needed for RandomForest, XGBoost, LightGBM

**Planned ablation study:**
1. Train with both features
2. Train with only MonthlyIncome
3. Train with JobLevel_MonthlyIncome interaction term
4. Compare validation metrics

**Implementation:**
- Create feature sets: `features_full`, `features_no_joblevel`, `features_ridge`
- Document feature engineering: `JobLevel_Income_Ratio = MonthlyIncome / (JobLevel + 1)` as alternative

---

## 3. Feature Skewness and Transformations

### Finding
**Highly skewed numeric features (from stat tests & descriptive stats):**

| Feature | Skewness | Test | p-value | Effect Size | Transformation Needed |
|---------|----------|------|---------|-------------|----------------------|
| MonthlyIncome | High right skew | Mann-Whitney | 2.95e-14 | 0.311 (large) | **log1p** |
| TotalWorkingYears | Moderate skew | Mann-Whitney | 2.40e-14 | 0.312 (large) | **log1p or sqrt** |
| YearsAtCompany | Moderate skew | Mann-Whitney | 2.92e-13 | 0.298 (large) | **log1p** |
| Age | Mild skew | Mann-Whitney | 5.30e-11 | 0.269 (medium) | **StandardScaler only** |

**Source:** `tables/stat_tests_numeric.csv`, descriptive statistics

### Decision
**Transformations to apply:**
1. **MonthlyIncome:** Apply `log1p` transformation → save as `MonthlyIncome_log`
   - Rationale: Reduces right skew, stabilizes variance, improves linear model assumptions
2. **TotalWorkingYears:** Apply `log1p` → save as `TotalWorkingYears_log`
3. **YearsAtCompany:** Apply `log1p` → save as `YearsAtCompany_log`
4. **Age:** Keep raw; apply StandardScaler (already near-normal)

**Verification:**
- Re-run Shapiro-Wilk test after transformation to confirm normality improvement
- Compare model performance with/without transformations
- Document: "Log transformation reduces skewness from X to Y (% improvement)"

**Implementation:**
```python
from sklearn.preprocessing import FunctionTransformer
log_transformer = FunctionTransformer(np.log1p, validate=True)
df['MonthlyIncome_log'] = log_transformer.transform(df[['MonthlyIncome']])
```

---

## 4. Outlier Handling

### Finding
**Features with significant outlier rates (>1% beyond 1.5×IQR):**

| Feature | Outlier % | Count | Action |
|---------|-----------|-------|--------|
| TrainingTimesLastYear | 16.19% | 238 | **Investigate, likely valid** |
| PerformanceRating | 15.37% | 226 | **Valid (rating scale artifact)** |
| MonthlyIncome | 7.76% | 114 | **Winsorize at 99th percentile** |
| YearsSinceLastPromotion | 7.28% | 107 | **Winsorize at 99th percentile** |
| YearsAtCompany | 7.07% | 104 | **Winsorize at 99th percentile** |

**Source:** `tables/outlier_summary.csv`

### Decision
**Feature-specific actions:**

1. **TrainingTimesLastYear & PerformanceRating:** No action (valid extreme values; part of natural distribution)

2. **MonthlyIncome, YearsSinceLastPromotion, YearsAtCompany:**
   - Apply **Winsorization** (cap at 1st and 99th percentiles)
   - Alternative: Use **RobustScaler** instead of StandardScaler for these features
   - Rationale: Extreme values may be influential points; capping preserves ranking without distorting distribution

**Implementation strategy:**
- Compare model performance:
  - No outlier treatment
  - Winsorization
  - RobustScaler
  - Outlier removal (not recommended; reduces sample size)

**Code snippet:**
```python
from scipy.stats.mstats import winsorize
df['MonthlyIncome_winsorized'] = winsorize(df['MonthlyIncome'], limits=[0.01, 0.01])
```

---

## 5. Categorical Feature Encoding

### Finding
**Statistically significant categorical predictors (chi-square tests):**

| Feature | Chi² | p-value | Cramér's V | Effect | Action |
|---------|------|---------|------------|--------|--------|
| OverTime | 87.56 | 8.16e-21 | 0.244 | **Strong** | One-hot (2 levels) |
| JobRole | 86.19 | 2.75e-15 | 0.242 | **Strong** | One-hot (9 levels) |
| MaritalStatus | 46.16 | 9.46e-11 | 0.177 | Moderate | One-hot (3 levels) |
| BusinessTravel | 24.18 | 5.61e-06 | 0.128 | Moderate | One-hot (3 levels) |
| Department | 10.80 | 0.0045 | 0.086 | Small | One-hot (3 levels) |
| EducationField | 16.02 | 0.0068 | 0.104 | Small | One-hot (6 levels) |
| Gender | 1.12 | 0.29 | 0.028 | None | **Consider dropping** |

**Source:** `tables/stat_tests_categorical.csv`

### Decision
**Encoding strategy:**
1. **OverTime, MaritalStatus, BusinessTravel, Department:** One-hot encoding (low cardinality, strong/moderate effects)
2. **JobRole:** One-hot encoding (9 categories; manageable dimensionality)
3. **EducationField:** One-hot encoding or group rare categories (if needed)
4. **Gender:** Drop from model (non-significant, p=0.29; also ethical consideration for HR predictions)

**Alternative (for high-cardinality future cases):**
- Target encoding with regularization (leave-one-out encoding)
- Frequency encoding
- CatBoost native categorical handling

**Implementation:**
- Use `OneHotEncoder(handle_unknown='ignore')` to handle unseen categories in test data
- Store encoded feature names for interpretability

---

## 6. Feature Importance and Selection

### Finding
**Top 10 RandomForest feature importances:**

| Rank | Feature | Importance | Interpretation |
|------|---------|------------|----------------|
| 1 | MonthlyIncome | 0.0768 | Compensation strongest predictor |
| 2 | Age | 0.0617 | Demographics important |
| 3 | TotalWorkingYears | 0.0562 | Experience matters |
| 4 | DailyRate | 0.0538 | Pay structure signal |
| 5 | HourlyRate | 0.0457 | Similar to DailyRate |
| 6 | MonthlyRate | 0.0440 | Compensation-related |
| 7 | DistanceFromHome | 0.0420 | Work-life balance proxy |
| 8 | YearsAtCompany | 0.0375 | Tenure effect |
| 9 | YearsWithCurrManager | 0.0358 | Management relationship |
| 10 | NumCompaniesWorked | 0.0346 | Job-hopping indicator |

**Notable categorical:** OverTime_Yes (0.0256), OverTime_No (0.0266)

**Source:** `tables/feature_importances_rf.csv`, `figures/feature_importance_rf.png`

### Decision
**Feature selection strategy:**
1. **Retain all features initially** (no aggressive dropping; let regularization handle weak predictors)
2. **Monitor for redundancy:** DailyRate, HourlyRate, MonthlyRate are all compensation-related; consider PCA or feature bundling if multicollinearity causes issues
3. **SHAP analysis confirms directionality:** Use SHAP waterfall plots for individual predictions in Improve phase

**Future feature engineering:**
- Create interaction: `OverTime × DistanceFromHome` (hypothesis: long commute + overtime → higher attrition)
- Tenure ratio: `YearsAtCompany / Age` (relative career investment)
- Satisfaction composite: Mean of JobSatisfaction, EnvironmentSatisfaction, WorkLifeBalance

**Low-importance candidates for ablation study:**
- PerformanceRating, HourlyRate (if redundant with MonthlyIncome)

---

## 7. SHAP Interpretation

### Finding
**SHAP summary plot insights** (`figures/shap_summary.png`):
- **OverTime (Yes):** Strong positive SHAP values → increases attrition probability
- **MonthlyIncome:** Lower values push predictions toward attrition (inverse relationship)
- **Age:** Younger employees → higher attrition risk
- **TotalWorkingYears:** Similar pattern to Age
- **JobRole, MaritalStatus:** Directional effects visible

**Source:** SHAP TreeExplainer on RandomForest baseline

### Decision
**Use SHAP for:**
1. **Model debugging:** Identify cases where prediction disagrees with intuition
2. **Stakeholder communication:** Explain individual predictions to HR team
3. **Feature validation:** Confirm that model learns sensible patterns (e.g., overtime → attrition makes domain sense)

**Implementation in Improve phase:**
- Generate SHAP force plots for 10 randomly selected test cases
- Create SHAP dependence plots for top 5 features (show interaction effects)
- Use SHAP values as input to meta-model (stacking) if needed

---

## 8. Potential Mislabeled Cases

### Finding
**6 cases flagged** with extreme prediction confidence mismatches:
- Model predicts attrition probability < 0.10 but labeled as "Yes" (or vice versa)
- Indicates possible:
  - Data entry errors
  - Temporal misalignment (e.g., employee left shortly after survey)
  - Model missing contextual information

**Source:** `tables/potential_mislabeled.csv`

### Decision
**Manual review required (not automated):**
1. Share flagged cases with HR domain experts for validation
2. If confirmed as errors → correct labels in cleaned dataset
3. If uncertain → mark as "high noise" but retain in training (use label smoothing or robust loss functions)
4. **Do NOT auto-flip labels** based on model predictions (risk of confirmation bias)

**Alternative if review impossible:**
- Use **confident learning** (cleanlab library) to assign sample weights
- Train with **focal loss** or **noise-robust cross-entropy**
- Exclude from test set; keep in training with reduced weight

**Documentation:**
- Record review outcomes: "X/6 corrected, Y/6 confirmed noisy, Z/6 ambiguous"

---

## 9. Pareto Analysis and Prioritization

### Finding
**Pareto chart of flagged issues** (`figures/pareto_issues.png`):

Cumulative impact of top issues accounts for 80% of quality problems (approximate Pareto principle).

**Issue ranking (by frequency):**
1. **Significant associations:** 29 features (numeric + categorical combined with p < 0.05)
2. **High skew:** ~10 features with skewness > 1
3. **High VIF:** 2 features (JobLevel, MonthlyIncome)
4. **Many outliers:** 5 features with >1% outlier rate
5. **Class imbalance:** 1 dataset-level issue

**Source:** Analysis aggregation across all tables

### Decision
**Prioritization for Improve phase (80/20 rule):**

**Tier 1 (must address):**
- Class imbalance (SMOTE + threshold tuning)
- Multicollinearity (drop JobLevel or regularize)
- MonthlyIncome skew (log transform)

**Tier 2 (significant impact):**
- Outlier winsorization (3 key features)
- OverTime encoding (strongest categorical predictor)

**Tier 3 (nice to have):**
- Feature engineering (interactions, ratios)
- Advanced ensemble methods (stacking, blending)

**Rationale:** Focus on root causes (imbalance, collinearity) before adding complexity.

---

## 10. Statistical Reporting Standards

### Conventions Used
All reported statistics follow APA-style guidelines:
- **Test selection:** Shapiro-Wilk for normality; Mann-Whitney U or Welch's t-test based on normality; chi-square for categorical associations
- **Effect sizes:** Cohen's d (t-tests), rank-biserial correlation (Mann-Whitney), Cramér's V (chi-square)
- **Multiple testing correction:** Benjamini-Hochberg FDR (False Discovery Rate) at α = 0.05
- **Significance threshold:** p < 0.05 after FDR correction

### Example Interpretation
**TotalWorkingYears vs. Attrition:**
> "TotalWorkingYears significantly differs between attritors and non-attritors (Mann–Whitney U = 100567, p < 0.001, rank-biserial r = 0.312, large effect). Employees who leave have fewer years of total work experience (median difference ≈ 5 years)."

### Tables Produced
- `tables/stat_tests_numeric.csv` — all numeric feature tests with effect sizes
- `tables/stat_tests_categorical.csv` — all categorical feature tests with Cramér's V
- `tables/vif_table.csv` — multicollinearity diagnostics
- `tables/feature_importances_rf.csv` — RandomForest Gini importances
- `tables/outlier_summary.csv` — IQR-based outlier rates per feature

---

## 11. Implementation Roadmap for Improve Phase

### Preprocessing Pipeline (Ordered Steps)

**Step 1: Data Cleaning**
```python
# Drop Gender (non-significant)
# Handle mislabeled cases (manual review outcomes)
```

**Step 2: Feature Engineering**
```python
# Log transformations
df['MonthlyIncome_log'] = np.log1p(df['MonthlyIncome'])
df['TotalWorkingYears_log'] = np.log1p(df['TotalWorkingYears'])
df['YearsAtCompany_log'] = np.log1p(df['YearsAtCompany'])

# Winsorization
from scipy.stats.mstats import winsorize
df['MonthlyIncome'] = winsorize(df['MonthlyIncome'], limits=[0.01, 0.01])
df['YearsSinceLastPromotion'] = winsorize(df['YearsSinceLastPromotion'], limits=[0.01, 0.01])
```

**Step 3: Feature Selection**
```python
# Drop JobLevel (if VIF ablation confirms redundancy)
# Drop Gender
features_to_drop = ['Gender', 'JobLevel']  # conditional
```

**Step 4: Encoding**
```python
# One-hot encode categoricals
cat_features = ['OverTime', 'JobRole', 'MaritalStatus', 'BusinessTravel', 'Department', 'EducationField']
encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
```

**Step 5: Scaling**
```python
# StandardScaler for most; RobustScaler for outlier-prone features
from sklearn.preprocessing import StandardScaler, RobustScaler
scaler_robust = RobustScaler()
scaler_standard = StandardScaler()
```

**Step 6: Resampling**
```python
# SMOTE inside CV loop
from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state=42, k_neighbors=5)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
```

**Step 7: Model Training**
- Logistic Regression with Ridge (alpha tuning)
- RandomForest with class weights
- XGBoost with scale_pos_weight
- LightGBM with is_unbalance=True

**Step 8: Threshold Optimization**
```python
from sklearn.metrics import precision_recall_curve
precision, recall, thresholds = precision_recall_curve(y_val, y_proba)
# Select threshold maximizing F1 or F2 (recall-weighted)
```

---

## 12. Success Metrics for Improve Phase

**Baseline Performance (Hold-out Test Set):**
- Accuracy: 0.8605
- Precision: 0.6154
- Recall: 0.3404 ⚠️ **(Primary improvement target)**
- F1-Score: 0.4384
- ROC-AUC: 0.8115
- PR-AUC: 0.5836

**Target Improvements:**
- **Recall:** ≥ 0.55 (+61% relative improvement)
- **F1-Score:** ≥ 0.60 (+37% relative)
- **PR-AUC:** ≥ 0.70 (+20% relative)
- Maintain Precision ≥ 0.50 (acceptable false positive rate)

**Evaluation Strategy:**
- 5-fold stratified cross-validation with 3 repeats (15 total folds)
- Final evaluation on untouched holdout test set
- Report mean ± std across folds
- Conduct statistical significance tests (paired t-test) between baseline and improved models

---

## 13. Control Phase Preparation

**Artifacts to Preserve:**
- Finalized preprocessing pipeline (scikit-learn Pipeline object)
- Best hyperparameters (Optuna study or GridSearchCV results)
- Feature names and transformations log
- SHAP explainer for production model
- Model performance benchmarks (confusion matrices, PR curves, ROC curves)

**Reproducibility Checklist:**
- All preprocessing decisions documented in this file
- Random seed fixed (SEED = 42) across all experiments
- Environment pinned: `pip freeze > requirements_freeze.txt`
- Git commit all notebooks, tables, figures, and decision docs

---

## 14. Conclusion

This document provides a comprehensive, evidence-based action plan derived from rigorous statistical analysis in the DMAIC Analyze phase. Each decision is:
- **Traceable:** Linked to specific tables, figures, or test results
- **Justified:** Grounded in statistical significance, effect sizes, or domain knowledge
- **Actionable:** Includes concrete implementation steps (code snippets, parameter choices)
- **Measurable:** Tied to quantitative success criteria for the Improve phase

**Next Steps:**
1. Implement preprocessing pipeline as outlined in Section 11
2. Train improved models with SMOTE, regularization, and optimized thresholds
3. Validate improvements using cross-validation and holdout test
4. Document results in `paper/03_improve_phase.md`
5. Commit all changes:
   ```bash
   git add paper/analyze_decisions.md tables/*.csv figures/*.png
   git commit -m "Add comprehensive analyze decisions with statistical justification"
   git push
   ```

---

**Document Version:** 1.0  
**Last Updated:** 2025-10-01  
**Review Status:** Ready for Improve Phase Implementation
