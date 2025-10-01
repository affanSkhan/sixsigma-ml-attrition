## 3. Measure Phase: Data and Baseline Performance

This section establishes the baseline for our process improvement cycle. We performed an Exploratory Data Analysis (EDA) to understand the dataset's characteristics and then evaluated standard machine learning models to quantify initial predictive performance.

### 3.1 Dataset Characteristics

The study utilizes the IBM HR Analytics dataset, which consists of **1470** observations and **35** features. The target variable, `Attrition`, is binary. Our initial analysis confirmed the dataset is imbalanced, with a minority class (employees who left) representing only **16.12%** of the total population.

The EDA revealed no missing values. However, several numeric features exhibit significant skewness and outliers. A correlation analysis also indicated potential multicollinearity between features such as `JobLevel` and `MonthlyIncome`, which will be formally investigated in the Analyze phase.

### 3.2 Baseline Model Performance

To establish a performance baseline, three models were evaluated using a stratified 5-fold cross-validation on the training set: a majority-class Dummy Classifier, a Logistic Regression, and a Decision Tree. The models were applied to the data with minimal preprocessing (median imputation and standard scaling for numeric features; mode imputation and one-hot encoding for categorical features).

The cross-validation results are summarized below, with performance on the hold-out test set used for final comparison.

*(Here, you would embed your table of hold-out metrics or reference the figures `baseline_confusion_matrices.png` and `baseline_roc_curves.png`)*

The Logistic Regression model provided the strongest baseline, achieving an F1-score of **0.51** and a ROC AUC of **0.76** on the hold-out test set. While this performance is significantly better than the dummy classifier, the recall of **0.40** for the positive class is low. This indicates that the baseline model struggles to correctly identify employees who are likely to attrite, capturing only 40% of them.

### 3.3 Identified Issues for Improvement

The Measure phase concludes by identifying the key sources of suboptimal performance that will be addressed in subsequent DMAIC phases:
1.  **Significant Class Imbalance:** The low attrition rate biases the model towards the majority class.
2.  **Low Recall:** The model fails to capture a sufficient number of true positive cases (employees who leave).
3.  **Potential Multicollinearity:** Highly correlated features may destabilize model coefficients.
4.  **Feature Quality:** The presence of skewed distributions and outliers in several numeric features may be negatively impacting performance.