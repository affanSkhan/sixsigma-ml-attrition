\# Reproducibility quick guide





1\. Create environment (conda recommended):

conda env create -f environment.yml

conda activate sixsigma-ml-attrition





2\. Download dataset (see data/README.md for instructions). Place raw CSV in `data/raw/`.





3\. Run EDA: Open `notebooks/01\_EDA.ipynb` and run all cells.





4\. Execute experiments: `notebooks/02\_baseline\_models.ipynb` and `notebooks/04\_improve\_experiments.ipynb`.





5\. Generate figures: run `notebooks/06\_generate\_figures.ipynb` which saves high-res PNGs to `figures/`.





6\. Save environment packages: `pip freeze > requirements\_freeze.txt`





7\. To reproduce final results exactly: ensure you use `requirements\_freeze.txt` and the same random seed as specified in `src/config.py`.

