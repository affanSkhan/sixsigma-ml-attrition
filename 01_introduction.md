\# 1. Introduction



\## Title (working)

Improving Machine Learning Performance for HR Attrition Prediction with a Six Sigma DMAIC Framework



\## Background and Motivation

Employee attrition imposes substantial, often hidden, costs on organizations, with replacement expenses estimated to be 1.5 to 2 times an employee's annual salary. Beyond direct financial impact, high turnover degrades institutional knowledge, disrupts team cohesion, and ultimately hinders strategic growth. While machine learning (ML) models are widely adopted to predict and mitigate attrition, their performance is often inconsistent, limited by underlying data issues like class imbalance, feature noise, and suboptimal preprocessing.



The Six Sigma DMAIC (Define–Measure–Analyze–Improve–Control) cycle is a proven, data-driven methodology for systematically improving processes by identifying and eliminating sources of error and variation. By conceptualizing the end-to-end ML pipeline—from data ingestion to model validation—as a process, we can apply the DMAIC framework to enhance its accuracy, stability, and reproducibility in a structured and measurable way.



---



\## Research Question

Can a Six Sigma DMAIC framework, when systematically applied to the machine learning workflow, produce a statistically significant improvement in predictive performance for employee attrition compared to a standard baseline approach?



---



\## Hypotheses



\### Primary Hypotheses

\* \*\*H0 (Null):\*\* The application of a DMAIC-guided improvement cycle does not produce a statistically significant improvement in the primary classification metric (e.g., F1-score) compared to the baseline model.

\* \*\*H1 (Alternative):\*\* The application of a DMAIC-guided improvement cycle produces a statistically significant improvement in the primary classification metric compared to the baseline model.



\### Secondary Hypotheses

\* \*\*H2:\*\* DMAIC-driven interventions reduce the performance variance (i.e., increase stability) of the model across cross-validation folds.

\* \*\*H3:\*\* The improved model demonstrates better calibration and a more favorable balance between Type I and Type II errors, which is critical for HR decision support.



---



\## Research Objectives

This study aims to:

1\.  \*\*Operationalize\*\* the DMAIC framework within a typical ML workflow for attrition prediction, defining clear tasks and statistical tools for each phase.

2\.  \*\*Establish\*\* a quantitative baseline of model performance using standard algorithms and evaluation protocols.

3\.  \*\*Identify\*\* the root causes of suboptimal model performance through rigorous statistical analysis and feature diagnostics.

4\.  \*\*Implement and statistically validate\*\* a series of targeted improvements to the preprocessing and modeling pipeline.

5\.  \*\*Propose\*\* a practical control plan for monitoring the improved model's performance and detecting data drift over time.



---



\## Contribution Statement

This research makes the following contributions:



\* \*\*A Novel Methodological Framework\*\* that formally integrates the Six Sigma DMAIC cycle into the ML development lifecycle for an HR use case.

\* \*\*Rigorous Empirical Evidence\*\* from a statistically validated comparison between baseline and DMAIC-improved pipelines, reporting both statistical significance and effect sizes.

\* \*\*Practitioner-Oriented Artifacts\*\*, including a reproducible codebase, a model monitoring control plan, and a transparent preprocessing workflow.



---



\## Novelty and Research Gap

A review of literature from 2020-2025 reveals a gap: while ML for attrition and Six Sigma for process improvement are mature fields, no empirical study explicitly integrates the DMAIC framework to structure and validate the ML modeling process itself. Current research typically treats model improvement as an ad-hoc, algorithm-centric task rather than a systematic process. This paper fills that gap by demonstrating and quantifying the value of applying a structured process improvement methodology to a complex data science workflow.



---



\## Scope and Limitations

\* \*\*Scope:\*\* This study utilizes the publicly available IBM HR Analytics dataset and focuses on common classification algorithms (e.g., logistic regression, gradient boosting). The interventions are centered on data preprocessing, feature engineering, and controlled model tuning.

\* \*\*Limitations:\*\* The findings are based on a single dataset, and further research is required to validate the framework's generalizability. This study prioritizes methodological rigor and reproducibility over creating a production-ready enterprise system.

