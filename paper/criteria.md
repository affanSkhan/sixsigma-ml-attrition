# Model Selection Criteria

**Project:** IBM HR Analytics Employee Attrition Prediction  
**Phase:** Control (DMAIC)  
**Date:** October 1, 2025  
**Purpose:** Define objective criteria for final model selection

---

## 1. Primary Metric

### F1-Score (Balanced Precision-Recall)

**Target:** ≥ 0.52 (19% improvement over baseline 0.438)

**Rationale:**
- Attrition prediction is a **class-imbalanced problem** (16.12% positive class)
- **Recall is critical**: Missing attritors costs ~$50k/employee in rehiring & training
- **Precision matters**: False positives waste HR intervention resources
- F1-Score balances both concerns: F1 = 2 × (Precision × Recall) / (Precision + Recall)

**Business Context:**
- High recall (0.50+): Catch 50% of actual attritors → intervention opportunity
- Acceptable precision (0.50+): 50% of flagged employees are true risks → reasonable hit rate

---

## 2. Secondary Criteria

### 2.1 ROC-AUC (Discriminative Ability)

**Target:** ≥ 0.80 (maintain baseline 0.811)

**Rationale:**
- Measures model's ability to rank attritors higher than non-attritors across all thresholds
- Threshold-independent metric → validates model quality before tuning cutoff
- **Business Value:** High AUC (>0.80) means model can be recalibrated for different business scenarios

**Interpretation Scale:**
- 0.90–1.00: Excellent discrimination
- 0.80–0.90: Good discrimination ✅ **Target range**
- 0.70–0.80: Fair discrimination
- 0.60–0.70: Poor discrimination
- 0.50: Random guessing

---

### 2.2 PR-AUC (Precision-Recall Trade-off)

**Target:** ≥ 0.60 (improve from baseline 0.583)

**Rationale:**
- More informative than ROC-AUC for **imbalanced datasets**
- Focuses on positive class performance (attritors)
- **Business Value:** Shows how well model maintains precision as recall increases

**Why PR-AUC Matters for Imbalance:**
- ROC-AUC can be misleadingly high when negatives dominate (83.88% non-attritors)
- PR-AUC penalizes models that achieve recall via excessive false positives

---

### 2.3 Model Stability (Cross-Validation Variance)

**Target:** Standard deviation ≤ 0.10 for F1-Score across 5 folds

**Rationale:**
- Low variance → consistent performance across data splits
- High variance → overfitting or sensitivity to specific samples
- **Business Value:** Stable model = predictable performance in production

**Evaluation Method:**
- 5-fold stratified cross-validation (stratified maintains 16.12% positive rate per fold)
- Report: Mean ± Std for F1, Recall, Precision
- **Acceptance Rule:** If Std(F1) > 0.10, investigate fold-specific failures

**Example:**
- ✅ Good: F1 = 0.52 ± 0.08 (stable)
- ❌ Bad: F1 = 0.55 ± 0.15 (erratic, likely overfit)

---

### 2.4 Interpretability

**Target:** Feature importance explainable to HR stakeholders

**Rationale:**
- **Trust:** HR managers need to understand *why* an employee is flagged
- **Actionability:** Interpretable features → targeted interventions (e.g., "overtime burden")
- **Compliance:** GDPR/EEOC require explainable automated decisions

**Preferred Models (Ranked by Interpretability):**
1. **Logistic Regression** (linear coefficients → direct interpretation)
2. **Decision Trees** (if-then rules)
3. **RandomForest with SHAP** (post-hoc explanations)
4. **XGBoost with SHAP** (complex but explainable via approximations)

**Mandatory Deliverable:**
- Top 10 features by importance with directional effects
- SHAP summary plot for global explanations
- SHAP force plot for 5 sample predictions (individual explanations)

**Business Example:**
- *"Employee X has 80% attrition probability because: OverTime=Yes (+0.25), MonthlyIncome=$2,500 (+0.20), YearsAtCompany=1 (+0.15)"*

---

### 2.5 Fairness (No Bias Across Protected Groups)

**Target:** No statistically significant recall difference across Gender, Age groups

**Rationale:**
- **Legal Compliance:** EEOC prohibits disparate impact in employment decisions
- **Ethical AI:** Model should not systematically fail for demographic subgroups
- **Business Risk:** Biased model → discrimination lawsuits, reputational damage

**Protected Attributes:**
- Gender (Male, Female)
- Age groups (18-30, 31-45, 46-60)
- Department (Sales, R&D, HR) — proxy for role type

**Evaluation Method:**
1. Compute recall separately for each group
2. Statistical test: Proportions z-test for recall parity
3. Acceptance: p-value > 0.05 (no significant difference) OR effect size < 0.10 (small practical difference)

**Example Analysis:**
```
Group        | Recall | Precision | N (Positive) | z-test p-value
-------------|--------|-----------|--------------|----------------
Male         | 0.48   | 0.52      | 29           | 0.67 (n.s.)
Female       | 0.52   | 0.50      | 18           |
```
**Interpretation:** No significant bias (p=0.67 > 0.05)

**Mitigation if Bias Detected:**
- Use `fairlearn` library for fairness constraints
- Re-weight samples by group
- Train separate models per group (last resort)

---

## 3. Tiebreaker Criteria (If Multiple Models Meet Targets)

### 3.1 Simplicity (Occam's Razor)

**Preference Order:**
1. Logistic Regression (fewest parameters)
2. Decision Tree (interpretable rules)
3. Ensemble methods (more complex)

**Rationale:**
- Simpler models → faster inference, easier maintenance, lower production risk
- **Six Sigma Principle:** *"Simplify before you optimize"*

---

### 3.2 Training Time

**Preference:** < 5 minutes on full dataset (N=1470)

**Rationale:**
- Fast training → enables quarterly retraining without infrastructure burden
- **Business Value:** HR can retrain model as workforce composition changes

---

### 3.3 Inference Speed

**Target:** < 1 ms per prediction

**Rationale:**
- Real-time scoring for 1000+ employees during quarterly reviews
- **Business Requirement:** Batch predictions for entire workforce in < 2 seconds

---

## 4. Model Comparison Framework

### Decision Matrix (Example Scoring)

| Model | F1 (Primary) | ROC-AUC | Stability (CV Std) | Interpretability | Fairness | Total Score |
|-------|--------------|---------|---------------------|------------------|----------|-------------|
| LR (class_weight) | 0.52 (5/5) | 0.81 (5/5) | 0.08 (5/5) | High (5/5) | Pass (5/5) | **25/25** ✅ |
| LR (threshold=0.3) | 0.51 (4/5) | 0.81 (5/5) | 0.09 (5/5) | High (5/5) | Pass (5/5) | 24/25 |
| RandomForest | 0.48 (2/5) | 0.79 (4/5) | 0.12 (3/5) | Medium (3/5) | Pass (5/5) | 17/25 ❌ |

**Scoring Rules:**
- F1: 5 if ≥0.52, 4 if 0.50-0.51, 3 if 0.48-0.49, 2 if 0.45-0.47, 1 if <0.45
- ROC-AUC: 5 if ≥0.81, 4 if 0.80-0.80, 3 if 0.75-0.79, 2 if 0.70-0.74, 1 if <0.70
- Stability: 5 if std≤0.10, 3 if 0.10-0.15, 1 if >0.15
- Interpretability: 5=High (LR), 3=Medium (RF), 1=Low (Deep NN)
- Fairness: 5=Pass (p>0.05), 0=Fail (p≤0.05)

**Selection Rule:**
- Choose model with highest total score
- If tied, prefer simpler model (Logistic Regression > Trees > Ensembles)

---

## 5. Robustness Requirements

### 5.1 Bootstrap Confidence Intervals

**Requirement:** 95% CI for F1-Score must exclude random baseline (0.27)

**Method:**
- 1000 bootstrap resamples of test set (with replacement)
- Compute F1 for each resample
- Report: Mean F1 ± CI [lower, upper]

**Acceptance:**
- ✅ CI lower bound > 0.40 → model reliably better than baseline
- ❌ CI lower bound < 0.40 → performance unstable, investigate further

**Example:**
- F1 = 0.52, 95% CI [0.45, 0.59] ✅ **Accepted** (lower bound 0.45 > 0.40)

---

### 5.2 Sensitivity Analysis

**Requirement:** F1-Score variation < 0.05 across preprocessing perturbations

**Tests:**
1. **Threshold Variation:** Test decision thresholds 0.25, 0.30, 0.35 → F1 should vary < 0.05
2. **Imputation Strategy:** Mean vs Median → F1 delta < 0.03
3. **Scaling Method:** StandardScaler vs RobustScaler → F1 delta < 0.02

**Interpretation:**
- Low sensitivity → robust to preprocessing choices
- High sensitivity → model brittle, document exact preprocessing steps

---

### 5.3 Temporal Stability (If Time-Series Component Exists)

**Requirement:** Performance does not degrade on future data

**Method:**
- Split data by EmployeeNumber (proxy for hire date if available)
- Train on earlier 70%, validate on later 30%
- Compare F1 on temporal split vs random split

**Acceptance:**
- F1 delta < 0.05 → no temporal drift
- If F1 delta > 0.05 → recommend quarterly retraining

---

## 6. Documentation Requirements

### 6.1 Model Card (Inspired by Google's Model Cards)

**Required Sections:**
1. **Model Details:** Algorithm, hyperparameters, training date
2. **Intended Use:** Quarterly attrition risk scoring for intervention targeting
3. **Factors:** Protected attributes (Gender, Age), key features (OverTime, Income)
4. **Metrics:** F1=0.52, Recall=0.50, Precision=0.54, ROC-AUC=0.81
5. **Training Data:** N=1176 (80% of 1470), class distribution 16.12%
6. **Evaluation Data:** N=294 (20% hold-out), stratified
7. **Ethical Considerations:** Fairness tested (no gender bias), GDPR-compliant explanations
8. **Caveats & Limitations:** Model trained on 2015 data; retrain if workforce demographics shift

---

### 6.2 Reproducibility Checklist

**Mandatory for Final Model:**
- ✅ Random seed fixed (RANDOM_SEED=42) in all notebooks
- ✅ Environment pinned: `requirements_final.txt` with exact versions
- ✅ Data lineage documented: raw CSV → preprocessing steps → model input
- ✅ Model serialized: `models/final_attrition_pipeline.pkl`
- ✅ SHAP explainer saved: `models/shap_explainer.pkl`
- ✅ Preprocessing fitted on train set only (no leakage)
- ✅ Git commit hash recorded in model metadata

---

## 7. Sign-Off Criteria

### Before Final Model Deployment:

- [ ] **Primary metric met:** F1 ≥ 0.52
- [ ] **Secondary metrics met:** ROC-AUC ≥ 0.80, PR-AUC ≥ 0.60
- [ ] **Stability verified:** CV Std(F1) ≤ 0.10
- [ ] **Bootstrap CI computed:** Lower bound > 0.40
- [ ] **Fairness validated:** No bias across Gender/Age (p > 0.05)
- [ ] **Interpretability delivered:** SHAP summary + top 10 features documented
- [ ] **Sensitivity analysis passed:** F1 variation < 0.05 across preprocessing variants
- [ ] **Model card written:** All 8 sections completed
- [ ] **Reproducibility verified:** Independent team member can retrain from scratch
- [ ] **Stakeholder approval:** HR leadership signs off on intervention strategy

**Final Approval Authority:** Six Sigma Project Lead + HR Director

---

**Document Version:** 1.0  
**Last Updated:** October 1, 2025  
**Status:** ✅ Ready for Final Model Selection (Control Phase)
