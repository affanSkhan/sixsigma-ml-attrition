# Manuscript Compilation Guide

## IEEE Conference Paper: draft_v1.tex

**Status:** ✅ LaTeX source complete  
**Date:** October 2, 2025  
**Pages:** ~12 pages (estimated in IEEE two-column format)  
**Figures:** 8 referenced  
**Tables:** 10 referenced  
**References:** 15 citations

---

## Prerequisites

### Required Software

1. **LaTeX Distribution:**
   - **Windows:** MiKTeX (https://miktex.org/download) or TeX Live
   - **Mac:** MacTeX (https://www.tug.org/mactex/)
   - **Linux:** `sudo apt-get install texlive-full` (Ubuntu/Debian)

2. **LaTeX Packages Required:**
   - IEEEtran (document class)
   - cite, amsmath, amssymb, amsfonts
   - algorithmic, graphicx, textcomp, xcolor
   - booktabs, hyperref, url, multirow

3. **Alternative: Overleaf (Online, No Installation):**
   - Upload `draft_v1.tex` + `references.bib` + `figures/` folder to Overleaf
   - Select "Compiler: pdfLaTeX"
   - Click "Recompile"

---

## Compilation Instructions

### Method 1: Command Line (Recommended)

```bash
# Navigate to paper directory
cd c:\Users\USER\sixsigma-ml-attrition\paper

# First pass (resolve references)
pdflatex draft_v1.tex

# Process bibliography
bibtex draft_v1

# Second pass (resolve citations)
pdflatex draft_v1.tex

# Third pass (resolve cross-references)
pdflatex draft_v1.tex
```

**Output:** `draft_v1.pdf` (publication-ready IEEE conference paper)

### Method 2: LaTeX Editor (TeXstudio, TeXworks, etc.)

1. Open `draft_v1.tex` in your LaTeX editor
2. Set compiler to **pdfLaTeX**
3. Set bibliography tool to **BibTeX**
4. Click **Build & View** (or press F5/F6)
5. Editor will automatically run the 3-pass compilation

### Method 3: Overleaf (No Installation)

1. Go to https://www.overleaf.com (free account)
2. Create **New Project → Upload Project**
3. Upload as ZIP:
   - `draft_v1.tex`
   - `references.bib`
   - `figures/` folder (all PNG files)
4. Set **Compiler: pdfLaTeX** (Menu → Settings)
5. Click **Recompile**
6. Download `draft_v1.pdf`

---

## Troubleshooting

### Issue 1: "File IEEEtran.cls not found"

**Solution:** Install IEEEtran package
```bash
# MiKTeX (Windows)
mpm --install=ieeetran

# TeX Live (Mac/Linux)
tlmgr install ieeetran
```

Or copy `IEEEtran.cls` from https://www.ctan.org/pkg/ieeetran into the `paper/` folder.

### Issue 2: "Figures not found"

**Solution:** Ensure figures are in correct path. Current setup looks for:
- `../figures/` (relative to `paper/` directory)
- `figures/` (if compiling from root)

If figures are missing, adjust `\graphicspath` in line 17 of `draft_v1.tex`:
```latex
\graphicspath{{../figures/}{./figures/}}
```

### Issue 3: Missing packages

**Solution:** Install all packages:
```bash
# MiKTeX (auto-installs on first run)
pdflatex draft_v1.tex  # Accept prompts to install

# TeX Live
tlmgr install cite booktabs hyperref
```

### Issue 4: Bibliography not showing

**Solution:** Ensure 3-pass compilation:
```bash
pdflatex draft_v1.tex   # Pass 1
bibtex draft_v1         # Process references
pdflatex draft_v1.tex   # Pass 2
pdflatex draft_v1.tex   # Pass 3 (final)
```

---

## File Structure

```
paper/
├── draft_v1.tex           # Main manuscript (LaTeX source)
├── references.bib         # BibTeX bibliography
├── draft_v1.pdf           # Compiled PDF (output)
├── COMPILATION_GUIDE.md   # This file
├── figures/               # Required figures (ensure these exist)
│   ├── baseline_roc_curves.png
│   ├── shap_summary.png
│   ├── pareto_issues.png
│   ├── threshold_optimization.png
│   ├── calibration_curve.png
│   ├── shap_final_improved.png
│   ├── final_confusion_matrix.png
│   └── final_roc_pr_curves.png
└── [auxiliary files]
    ├── draft_v1.aux       # Cross-references
    ├── draft_v1.bbl       # Formatted bibliography
    ├── draft_v1.blg       # BibTeX log
    ├── draft_v1.log       # Compilation log
    └── draft_v1.out       # Hyperref data
```

---

## Verification Checklist

Before submission, verify:

- [ ] **PDF compiles without errors**
  ```bash
  pdflatex draft_v1.tex  # Check terminal for "0 errors"
  ```

- [ ] **All figures display correctly**
  - Open PDF, check Figures 1-8 render at proper resolution
  - Captions match figure content

- [ ] **All tables display correctly**
  - Tables 1-10 formatted with booktabs style
  - Numbers match source CSV files in `tables/`

- [ ] **Bibliography complete**
  - All 15 citations appear in References section
  - No `[?]` placeholders in text

- [ ] **Page count acceptable**
  - IEEE conference: typically 4-6 pages
  - Current manuscript: ~12 pages (may need compression)

- [ ] **Formatting correct**
  - Two-column IEEE layout
  - 10pt font, single spacing
  - Figures/tables placed appropriately

---

## Compression Tips (If Over Page Limit)

If manuscript exceeds 6 pages for conference submission:

### 1. Reduce Figure Sizes
```latex
% Change from \linewidth to 0.8\linewidth
\includegraphics[width=0.8\linewidth]{figure.png}
```

### 2. Consolidate Tables
- Merge Tables 3 and 4 (experiment results)
- Move detailed tables to supplementary materials

### 3. Tighten Text
- Remove redundant sentences in Discussion
- Shorten Related Work section (keep only most relevant studies)
- Move detailed preprocessing log to appendix

### 4. Use Compact List Formatting
```latex
\usepackage{enumitem}
\setlist{noitemsep, topsep=0pt, parsep=0pt, partopsep=0pt}
```

### 5. Adjust Spacing
```latex
% Add after \begin{document}
\setlength{\textfloatsep}{10pt plus 1pt minus 2pt}
\setlength{\intextsep}{10pt plus 1pt minus 2pt}
```

---

## Submission Preparation

### Step 1: Generate Camera-Ready PDF
```bash
pdflatex draft_v1.tex
bibtex draft_v1
pdflatex draft_v1.tex
pdflatex draft_v1.tex
```

### Step 2: Verify PDF Properties
- Open in Adobe Reader
- Check **File → Properties**:
  - Page size: Letter (8.5" × 11")
  - Fonts: All embedded
  - PDF version: 1.4 or higher

### Step 3: Prepare Supplementary ZIP
```bash
# From repository root
zip -r supplementary.zip \
  data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv \
  models/final_attrition_pipeline.pkl \
  models/model_metadata.json \
  tables/*.csv \
  figures/*.png \
  notebooks/*.ipynb \
  environment.yml \
  requirements.txt \
  paper/appendix_control_plan.md \
  README.md
```

### Step 4: Copyright Form
- Complete IEEE copyright transfer form (provided by conference)
- Sign electronically via IEEE eXpress portal

### Step 5: Submit via Conference Portal
- Upload `draft_v1.pdf`
- Upload `supplementary.zip`
- Enter metadata (title, authors, keywords, abstract)

---

## Contact for Issues

**Repository:** https://github.com/affanSkhan/sixsigma-ml-attrition  
**Issues:** https://github.com/affanSkhan/sixsigma-ml-attrition/issues

For LaTeX compilation errors, include:
1. `draft_v1.log` file
2. LaTeX distribution and version (`pdflatex --version`)
3. Operating system

---

## License

Manuscript: © 2025 Authors. All rights reserved.  
Code/Data: MIT License (see repository LICENSE file)

---

**Last Updated:** October 2, 2025  
**Manuscript Version:** v1.0
