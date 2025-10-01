# Appendix: Control Plan & Deployment Considerations

**Project:** Employee Attrition Prediction (DMAIC Framework)  
**Document:** Control plan for monitoring, drift detection, and retraining policy  
**Author:** Data Science Team  
**Date:** 2025-10-01

---

## Purpose

This document defines the operational plan to monitor, detect drift, and maintain the final attrition prediction model in production. It is designed to ensure model performance and fairness remain within acceptable bounds and to provide clear procedures for incident response, retraining, and governance.

---

## 1. Monitoring Strategy — What to monitor & frequency

**Primary monitoring frequency:** daily (near real-time where possible) and weekly aggregated checks.

**Metrics to log and monitor:**
- **Model performance metrics** (per-batch / daily / weekly):
  - F1-score (primary)
  - Recall (sensitivity)
  - Precision
  - ROC-AUC
  - PR-AUC
  - Accuracy (for general tracking)
- **Prediction distribution metrics:**
  - Proportion of positive predictions (p̂)
  - Mean predicted probability (score_avg)
- **Data distribution metrics (per-feature, numeric and categorical):**
  - Feature mean / std / quantiles
  - Category frequency changes
  - Population Stability Index (PSI) per feature (weekly)
  - KL-divergence per feature (weekly)
- **Operational metrics:**
  - Inference latency, error rate, failed requests

**Monitoring granularity & windows:**
- **Real-time / per-request log:** store probability & metadata for each prediction for auditing.
- **Daily batch:** compute daily metrics (F1, recall, precision computed on labeled data if available; otherwise track proxy metrics like fraction_positive).
- **Weekly summary:** PSI, KL, fairness metrics and drift detectors aggregated.

---

## 2. Statistical Process Control (SPC) tools & thresholds

### 2.1 p-chart (proportion chart)
- **Use:** monitor proportion of positive predictions (p̂) or daily accuracy (proportion correct).
- **Control limits (3-sigma):**  
  $$
  \text{UCL} = \bar{p} + 3\sqrt{\frac{\bar{p}(1-\bar{p})}{n}},\quad
  \text{LCL} = \bar{p} - 3\sqrt{\frac{\bar{p}(1-\bar{p})}{n}}
  $$
  where $\bar{p}$ is historical mean proportion and $n$ is sample size per day/batch. Clip LCL at 0.
- **Alert rule:** immediate alert if metric outside UCL/LCL for a single day *or* if metric is outside ±2σ for 3 consecutive days.

### 2.2 EWMA chart (Exponentially Weighted Moving Average)
- **Use:** detect small sustained shifts in proportions or metrics (e.g., daily F1 drift).  
- **EWMA update:** $z_t = \lambda x_t + (1-\lambda) z_{t-1}$, choose $\lambda \in [0.05,0.3]$ (suggest λ=0.2).  
- **Control limits:** compute per standard EWMA formulas (use $\sigma_z = \sqrt{(\lambda/(2-\lambda))(\sigma^2)}$) and set LCL/UCL = $\mu \pm L \sigma_z$, with L typically 3.
- **Alert rule:** alert when EWMA crosses control limits or shows trending drift for 5 consecutive points.

---

## 3. Drift detection methods & thresholds

Use a mix of feature-distribution and label-aware detectors:

### 3.1 Population Stability Index (PSI)
- **Computation:** bin numeric feature into 10 bins (deciles) using training histogram; PSI = sum((actual_pct - expected_pct) * ln(actual_pct/expected_pct)) over bins.
- **Thresholds:**  
  - PSI < 0.1: stable  
  - 0.1 ≤ PSI < 0.2: moderate shift (review)  
  - PSI ≥ 0.2: large shift (action required)
- **Action:** if PSI ≥ 0.1 in > 3 features OR any feature PSI ≥ 0.2 → investigate data pipeline & domain causes.

### 3.2 KL-divergence
- **Use:** alternate measure for categorical distributions.  
- **Rule of thumb:** KL > 0.1 is suspicious; KL > 0.2 is high.

### 3.3 Page-Hinkley (change detection)
- **Use:** detect mean shifts in continuous metrics (e.g., average predicted probability).  
- **Parameters:** delta (small positive threshold), λ (threshold for alarm). Example: delta=0.005, λ=50. Tune on historical data.

### 3.4 ADWIN (Adaptive Windowing) / Online detectors (optional)
- **Use:** streaming drift detection that adapts window size; instant alerts on change.  
- **Tooling:** libraries such as `river` support ADWIN. ADWIN raises immediate drift alarms — treat as high-priority alerts.

---

## 4. Fairness & Performance Parity Checks

**Frequency:** weekly (or monthly for stable environments).

**Checks:**
- Compute recall and precision per protected group (Gender, Age bucket, Department).
- Alert if group-wise recall difference > 10 percentage points or if ratio metrics indicate disparate impact.
- For small groups, apply caution (power) — accumulate data for robust testing.

---

## 5. Retraining & Remediation Policy

**Retraining triggers (automated):**
1. **Performance drop:** test-set or production AUC/F1 below lower control limit (3-sigma) for *3 consecutive weeks* → schedule retraining.  
2. **Drift evidence:** PSI > 0.2 for any feature OR PSI > 0.1 for > 3 features → investigate and if confirmed, retrain.  
3. **ADWIN/Page-Hinkley alarm:** immediate investigation; if confirmed drift impacts labels/predictions then retrain.  
4. **Data volume trigger:** once **≥ 500 new labeled events** (preferably ≥ 500 positives) are available → retrain.

**Retraining workflow:**
- Step 1: Triage — Data engineer & Data Scientist check data integrity and feature distributions.  
- Step 2: Root-cause analysis — determine if change is upstream (schema, collection) vs real population shift.  
- Step 3: Temporary mitigation — rollback to previous model version if recent deployment caused degradation.  
- Step 4: Retrain on expanded dataset (include new data), run full evaluation & backtest.  
- Step 5: Validate fairness & calibration.  
- Step 6: Deploy via blue/green or canary rollout; monitor closely.

**Retraining cadence (if no triggers):** quarterly.

---

## 6. Alerting & Incident Response

**Alert severity levels:**
- **Critical:** AUC or F1 drops below emergency threshold or ADWIN alarm + confirmed label drift → immediate on-call paging (1 hour SLA).  
- **High:** PSI ≥ 0.2 or sustained crossing of control limits for 3+ days → investigation within 24 hours.  
- **Medium:** Threshold exceeded for single day (not persistent) → investigate within 3 business days.

**Response playbook:**
1. Acknowledge alert in monitoring system (PagerDuty, Slack).  
2. Owner roles: Model Owner (Data Scientist), Data Owner, MLOps Lead.  
3. Check data freshness, schema, and upstream ETL.  
4. Inspect sample predictions and top features for drift.  
5. If necessary, rollback to previous model and open a post-mortem.

---

## 7. Logging, Storage & Reproducibility

**Logs to store per prediction:** timestamp, feature hash, raw features (or hashed), model probability, assigned label (if later available), model version, batch id. Store in a time-series DB or object store (in compressed parquet) for at least 1 year.

**Metadata & artifacts:**
- Model artifact with version (git commit hash) and DOI if archived (Zenodo).  
- `model_metadata.json` containing training data window, seed, hyperparameters, threshold.  
- Reproducible environment (requirements_freeze.txt / Docker image).

---

## 8. Dashboards & Tooling (recommendations)

**Tools to consider:**
- **Evidently** (Python) — dataset and model monitoring + drift reports.  
- **Prometheus + Grafana** — for continuous metric dashboards and alerts.  
- **MLflow** — experiment tracking & model registry.  
- **River** — streaming drift detectors (ADWIN).  
- **Logging storage:** S3/MinIO + BigQuery/ClickHouse for analytics.

**Suggested dashboards:**  
- Weekly model performance dashboard (F1, Recall, Precision, AUC)  
- PSI/Feature drift heatmap (top 20 features)  
- Fairness panel (group metrics)  
- Model metadata and version timeline

---

## 9. Governance, Roles & Responsibilities

**Model Owner (Data Science):** monitoring thresholds, triage, retraining.  
**Data Owner (Domain/HR):** verify data changes, business context, labeling policy.  
**MLOps Lead:** deployment, rollback, logging, system availability.  
**Compliance Officer:** fairness and privacy reviews quarterly.

---

## 10. Rollback & Safety Plan

If critical performance or fairness alerts require immediate mitigation:
1. **Switch traffic** to previous stable model (blue/green or rollback).  
2. Put a hold on automated retraining until root cause analysis.  
3. Notify stakeholders and schedule a post-mortem.  
4. If the root cause is data collection failure, pause model use for decisioning that affects people.

---

## 11. KPIs for Control Phase Success

- Mean weekly F1 ≥ 0.45 (operational target)  
- Time-to-detect (TTD) for critical drift < 48 hours  
- Time-to-recover (TTR) after critical incident < 72 hours  
- No sustained fairness drift (>10% gap) over a rolling 3-month window

---

## 12. Appendix: Quick-check scripts & simulation (see `notebooks/06_control.ipynb`)

- The accompanying notebook simulates monitoring on historical folds and demonstrates p-chart, EWMA, Page-Hinkley, PSI, KL, and ADWIN examples. Use it to calibrate λ, thresholds, and test alerting logic on historical behavior.

---

## 13. Change Log & Approval

- v1.0 — 2025-10-01 — Initial control plan (approved by Data Science Lead)  
- Approval signatures: Data Scientist, Project Sponsor, IT/MLOps Lead

---
