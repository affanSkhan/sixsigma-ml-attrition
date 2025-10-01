# Data README

## Dataset
- **Name:** IBM HR Analytics Attrition & Performance (commonly used public dataset)  
- **Source:** Download from Kaggle (search "IBM HR Analytics Attrition & Performance") or obtain from instructor if restricted.  
- **Files expected in this repo:**  
  - `data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv` (original CSV)  
  - `data/processed/attrition_clean.csv` (cleaned dataset used for experiments)  

## Provenance
- Original dataset is a sample dataset prepared for HR analytics training and widely used in academic demonstrations.  
- Cite the dataset in your paper as: *"IBM HR Analytics dataset (Kaggle)"* and include the download date.  

## Preprocessing Notes
1. Remove identifier columns (e.g., `EmployeeNumber`).  
2. Convert categorical variables to appropriate encodings (see `src/preprocess.py`): one-hot for nominal features with few categories, target encoding for high-cardinality features if justified.  
3. Handle missing values: impute median for numeric features; mode for categorical features — document any rows dropped.  
4. Address class imbalance: experiment with class weighting, resampling (SMOTE), or threshold tuning.  
5. Feature scaling: use `StandardScaler` or `RobustScaler` for numeric features; fit scaler only on training splits to avoid data leakage.  
6. Save processed files in `data/processed/` and commit only processed files that are small; avoid committing raw data.  

## Suggested File List
- `data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv`  
- `data/processed/attrition_clean.csv`  
- `data/processed/features_schema.json` (column types and transformations)  
