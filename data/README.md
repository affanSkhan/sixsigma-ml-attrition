\# Data README





\## Dataset

\- Name: IBM HR Analytics Attrition \& Performance (commonly used public dataset)

\- Source: Download from Kaggle (search "IBM HR Analytics Attrition \& Performance") or obtain from instructor if restricted.

\- Files expected in this repo:

\- `data/raw/WA\_Fn-UseC\_-HR-Employee-Attrition.csv` (original CSV)

\- `data/processed/attrition\_clean.csv` (cleaned dataset used for experiments)





\## Provenance

\- Original dataset is a sample dataset prepared for HR analytics training and widely used in academic demonstrations. Cite the dataset in your paper as: "IBM HR Analytics dataset (Kaggle)" and include the download date.





\## Preprocessing notes

1\. Remove identifier columns (e.g., EmployeeNumber).

2\. Convert categorical variables to appropriate encodings (see `src/preprocess.py`): one-hot for nominal with few categories, target encoding for high-cardinality features if justified.

3\. Handle missing values (impute median for numeric features; mode for categoricals) — document any rows dropped.

4\. Address class imbalance: experiment with class weighting, resampling (SMOTE), or threshold tuning.

5\. Feature scaling: StandardScaler or RobustScaler for numeric features; fit scaler only on training splits to avoid leakage.

6\. Save processed files in `data/processed/` and commit only processed files that are small; avoid committing raw data.





\## Suggested file list

\- data/raw/WA\_Fn-UseC\_-HR-Employee-Attrition.csv

\- data/processed/attrition\_clean.csv

\- data/processed/features\_schema.json # column types and transformations

