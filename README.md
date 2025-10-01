# Improving ML Model Accuracy using Six Sigma DMAIC: A Case Study on HR Attrition

**Short description:** This repository contains code, notebooks, and documentation for a DMAIC-driven approach to improve machine learning model performance on an employee attrition dataset.

## Structure
- `data/` — datasets (download instructions in `data/README.md`)
- `notebooks/` — EDA and experiments
- `src/` — reusable scripts for preprocessing, modeling, metrics
- `paper/` — manuscript drafts and outline
- `figures/` — plots and figures for the paper

## Quick start
1. Create a conda environment:
   ```powershell
   conda env create -f environment.yml
   conda activate sixsigma-ml-attrition
   ```
   Or create a virtual environment with pip:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
2. Populate `data/raw/` with the dataset or run `data/download_data.sh` (if provided).
3. Open `notebooks/01_EDA.ipynb` to reproduce EDA results.

## Reproducibility
See `runme.md` for full reproduction steps. For publication, this project will include a DOI via Zenodo.

## License
[MIT License](LICENSE)

## Contact
Affan — your-email@example.com

