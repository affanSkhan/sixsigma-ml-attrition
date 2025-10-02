# Quick Start: Compile Manuscript on Overleaf

## ⚡ 5-Minute Setup (No LaTeX Installation Required)

**Goal:** Compile `draft_v1.tex` to `draft_v1.pdf` using Overleaf (free online LaTeX editor)

---

## Step 1: Prepare Files (Local Computer)

### Collect Required Files

You need **3 items** from your repository:

1. **Main manuscript:** `paper/draft_v1.tex`
2. **Bibliography:** `paper/references.bib`
3. **Figures folder:** `figures/` containing these 8 PNG files:
   - `baseline_roc_curves.png`
   - `shap_summary.png`
   - `pareto_issues.png`
   - `threshold_optimization.png`
   - `calibration_curve.png`
   - `shap_final_improved.png`
   - `final_confusion_matrix.png`
   - `final_roc_pr_curves.png`

### Create Upload Package

**Option A: Manual folder (recommended)**
```
overleaf-upload/
├── draft_v1.tex
├── references.bib
└── figures/
    ├── baseline_roc_curves.png
    ├── shap_summary.png
    ├── pareto_issues.png
    ├── threshold_optimization.png
    ├── calibration_curve.png
    ├── shap_final_improved.png
    ├── final_confusion_matrix.png
    └── final_roc_pr_curves.png
```

**Option B: ZIP archive**
```powershell
# PowerShell (from repository root)
cd c:\Users\USER\sixsigma-ml-attrition

# Create temporary folder
New-Item -ItemType Directory -Path overleaf-upload -Force
New-Item -ItemType Directory -Path overleaf-upload\figures -Force

# Copy files
Copy-Item paper\draft_v1.tex overleaf-upload\
Copy-Item paper\references.bib overleaf-upload\
Copy-Item figures\baseline_roc_curves.png overleaf-upload\figures\
Copy-Item figures\shap_summary.png overleaf-upload\figures\
Copy-Item figures\pareto_issues.png overleaf-upload\figures\
Copy-Item figures\threshold_optimization.png overleaf-upload\figures\
Copy-Item figures\calibration_curve.png overleaf-upload\figures\
Copy-Item figures\calibration_curve.png overleaf-upload\figures\
Copy-Item figures\shap_final_improved.png overleaf-upload\figures\
Copy-Item figures\final_confusion_matrix.png overleaf-upload\figures\
Copy-Item figures\final_roc_pr_curves.png overleaf-upload\figures\

# Create ZIP
Compress-Archive -Path overleaf-upload\* -DestinationPath overleaf-manuscript.zip

# Verify
Get-ChildItem overleaf-upload -Recurse
```

---

## Step 2: Create Overleaf Project

### A. Sign Up (Free)
1. Go to https://www.overleaf.com
2. Click **Register** (top right)
3. Sign up with email or Google account
4. Verify email (check inbox)

### B. Create New Project
1. Click **New Project** (green button)
2. Select **Upload Project**
3. Choose:
   - **Option A:** Drag `overleaf-upload` folder
   - **Option B:** Upload `overleaf-manuscript.zip`
4. Wait for upload (5-10 seconds)

**Project created!** You should see file tree on left:
```
draft_v1.tex          ← Main file
references.bib        ← Bibliography
figures/              ← Folder with 8 images
  ├── baseline_roc_curves.png
  ├── shap_summary.png
  ├── ...
```

---

## Step 3: Configure Compiler

### Set Correct Settings
1. Click **Menu** (☰ icon, top left)
2. Under **Settings:**
   - **Compiler:** Select **pdfLaTeX** (NOT XeLaTeX or LuaLaTeX)
   - **TeX Live version:** 2023 or later
   - **Main document:** `draft_v1.tex` (should auto-detect)
   - **Auto compile:** Off (optional, saves credits on free plan)

3. Click outside menu to close

---

## Step 4: Compile to PDF

### First Compilation
1. Click **Recompile** button (top bar, looks like play ▶️ icon)
2. Wait 10-30 seconds (first compile takes longer)
3. Check for errors in **Logs and output files** panel (bottom)

**Expected Output:**
```
This is pdfTeX, Version 3.141592653-2.6-1.40.25 (TeX Live 2023)
...
Output written on draft_v1.pdf (12 pages, 1234567 bytes).
Transcript written on draft_v1.log.
```

### If Errors Occur

#### Error 1: "File IEEEtran.cls not found"
**Solution:** Click **Menu → Settings → TeX Live version: 2023** (or later)

#### Error 2: "File not found: figures/baseline_roc_curves.png"
**Solution:** Check file tree. If `figures/` folder is missing:
1. Click **New File** icon (📄+)
2. Click **New Folder**
3. Name it `figures`
4. Upload 8 PNG files into `figures/` folder

#### Error 3: "Undefined control sequence \checkmark"
**Solution:** Add to preamble (after line 11 in draft_v1.tex):
```latex
\usepackage{amssymb}  % For \checkmark symbol
```

---

## Step 5: Verify PDF Quality

### Open PDF Viewer
- PDF preview should show on right side of screen
- If not visible: Click **PDF** tab (top right)

### Quality Checklist
- [ ] **Page count:** ~12 pages
- [ ] **Two-column layout:** Text in 2 columns per page
- [ ] **Figures:** All 8 figures display clearly
  - Figure 1: Baseline ROC curves (3 colored lines)
  - Figure 2: SHAP summary (bee swarm plot)
  - Figure 3: Pareto chart (bars + line)
  - Figure 4: Threshold optimization (precision-recall curve)
  - Figure 5: Calibration curve (diagonal reference line)
  - Figure 6: SHAP final model (bee swarm plot)
  - Figure 7: Confusion matrix (2×2 heatmap)
  - Figure 8: ROC+PR curves (2 subplots)
- [ ] **Tables:** All 10 tables render with horizontal lines (booktabs style)
- [ ] **References:** 15 numbered citations [1]-[15] at end
- [ ] **Hyperlinks:** Clickable (blue underlined text)

### Zoom In/Out
- Use zoom controls (bottom right of PDF viewer)
- Check figure readability at 100% zoom
- Verify table numbers align properly

---

## Step 6: Download Final PDF

### Download
1. Click **Download PDF** button (next to Recompile)
2. Or: Click **Menu → Download → PDF**
3. Save as `draft_v1.pdf` to your computer

**File size:** ~2-3 MB (with embedded figures)

### Verify Download
Open `draft_v1.pdf` in Adobe Reader or browser:
- All pages display
- Figures are crisp (300 DPI)
- Text is searchable (not images of text)

---

## Step 7: Update Author Information

### Edit Lines 19-27
1. In Overleaf, open `draft_v1.tex` (click in file tree)
2. Scroll to lines 19-27 (or press Ctrl+G, type 19)
3. Replace placeholder text:

**Before:**
```latex
\author{
\IEEEauthorblockN{Affan Shakir Khan}
\IEEEauthorblockA{\textit{Department of Data Science} \\
\textit{[Institution Name]}\\
[City, Country] \\
affan.khan@example.com}
}
```

**After (example):**
```latex
\author{
\IEEEauthorblockN{Affan Shakir Khan}
\IEEEauthorblockA{\textit{Department of Computer Science} \\
\textit{University of Example}\\
Karachi, Pakistan \\
affan.khan@university.edu}
}
```

4. Click **Recompile** to regenerate PDF
5. Verify author info appears on page 1

---

## Step 8: Share with Co-Authors (Optional)

### Invite Collaborators
1. Click **Share** button (top right)
2. Enter co-author email addresses
3. Select permissions:
   - **Can edit:** Full editing access
   - **Can view:** Read-only (for reviewers)
4. Click **Share project**

### Track Changes
- Click **Review** tab (top bar)
- Enable **Track changes** mode
- All edits will be highlighted for review

---

## ✅ Success Criteria

**You're done when:**
- ✅ PDF compiles without errors (0 errors in log)
- ✅ All 8 figures display in PDF
- ✅ All 10 tables render correctly
- ✅ References [1]-[15] appear at end
- ✅ Author information updated
- ✅ PDF downloaded to local computer

**Result:** `draft_v1.pdf` ready for submission! 🎉

---

## 🆘 Troubleshooting

### Problem: "Exceeded compile timeout"
**Cause:** Large figures or slow server  
**Solution:**
1. Click **Menu → Settings → Compiler: pdfLaTeX**
2. Reduce figure sizes (open figures in Paint, resize to 1200px width, save as PNG)
3. Try compiling during off-peak hours (not 9am-5pm GMT)

### Problem: Bibliography not showing
**Cause:** BibTeX not run  
**Solution:**
1. Click **Logs and output files** (bottom panel)
2. Click **Other logs & files** dropdown
3. Verify `draft_v1.bbl` exists
4. If missing: Menu → Settings → Clear cached files → Recompile

### Problem: Figures appear tiny or huge
**Cause:** `\includegraphics` width setting  
**Solution:** Edit line 17 of draft_v1.tex:
```latex
% Change from:
\includegraphics[width=\linewidth]{figure.png}

% To (for smaller figures):
\includegraphics[width=0.8\linewidth]{figure.png}
```

### Problem: "Package hyperref Warning: Token not allowed"
**Ignore:** This warning is cosmetic, PDF still generates correctly

---

## 📊 Expected Compilation Output

### Terminal Log (Success)
```
This is pdfTeX, Version 3.141592653-2.6-1.40.25 (TeX Live 2023)
restricted \write18 enabled.
entering extended mode
...
[Loading MPS to PDF converter (version 2006.09.02).]
) (/usr/local/texlive/2023/texmf-dist/tex/latex/hyperref/puenc.def)
[1{/usr/local/texlive/2023/texmf-var/fonts/map/pdftex/updmap/pdftex.map}]
[2] [3] [4] [5] [6] [7] [8] [9] [10] [11] [12]
(./draft_v1.bbl) [13] (./draft_v1.aux) )
(see the transcript file for additional information){/usr/local/texlive/2023/texmf-dist/fonts/enc/dvips/base/8r.enc}</usr/local/texlive/2023/texmf-dist/fonts/type1/public/amsfonts/cm/cmr10.pfb>
Output written on draft_v1.pdf (12 pages, 2345678 bytes).
Transcript written on draft_v1.log.
```

**Key Indicators:**
- ✅ `Output written on draft_v1.pdf (12 pages, ...)`
- ✅ No "Error:" lines
- ⚠️ Warnings are OK (as long as PDF generates)

---

## 🎓 Next Steps After PDF Generation

1. **Read through PDF** - Check for typos, formatting issues
2. **Run plagiarism check** - Turnitin or iThenticate (<15% similarity)
3. **Grammar check** - Grammarly Premium (fix critical errors)
4. **Circulate for review** - Send to co-authors/advisor
5. **Create supplementary ZIP** - Package code, data, models
6. **Submit to IEEE venue** - Upload PDF + supplementary materials

See [`paper/SUBMISSION_CHECKLIST.md`](paper/SUBMISSION_CHECKLIST.md) for detailed pre-submission steps.

---

## 📧 Support

**Overleaf Documentation:** https://www.overleaf.com/learn  
**IEEE Author Resources:** https://www.ieee.org/publications/authors  
**Repository Issues:** https://github.com/affanSkhan/sixsigma-ml-attrition/issues

---

**Quick Start Version:** 1.0  
**Last Updated:** October 2, 2025  
**Estimated Time:** 15-20 minutes (first-time users)
