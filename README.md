**English** | [العربية](README.ar.md)

---

# 🎓 2MDSP — Master 2 Data Science & Big Data

A comprehensive workspace and academic knowledge repository for the **Master 2 Data Science & Big Data (2MDSP)** program at the **Higher Institute of Applied Languages and Computer Science of Béja (ISLAI Béja - Institut Supérieur des Langues Appliquées et Informatique de Béja)**.

This repository hosts course summaries and lecture notes, practical lab sessions (`TP`), guided exercises (`TD`), and collaborative projects, fully structured for seamless integration with **Obsidian** and **Jupyter Notebooks (via Jupytext)**.

---

## 📚 Curriculum & Modules

The program comprises 12 academic subjects organized into standard tracks:

| # | Module / Subject | Course Name (French) | Available Tracks |
|---|---|---|---|
| 01 | **Natural Language Processing** | `Traitement Automatique du Langage Naturel` | `Cours`, `TP` |
| 02 | **Cloud Computing for Big Data** | `Environnement Cloud pour le Big Data` | `Cours`, `TP` |
| 03 | **Career Search Strategy** | `Career Strategy Search` | `Cours` |
| 04 | **Large Language Models** | `Large Language Models` | `Cours`, `TD` |
| 05 | **Analysis & Programming with Python** | `Analyse et Programmation avec Python` | `Cours`, `TP` |
| 06 | **Python Web Frameworks** | `Framework web Python` | `Cours`, `TP` |
| 07 | **Big Data Frameworks** | `Frameworks Big Data` | `Cours`, `TP` |
| 08 | **Integrative Machine Learning Project** | `Projet Fédérateur Machine Learning` | `TD`, `TP` |
| 09 | **English 3** | `Anglais 3` | `Cours` |
| 10 | **Massive Data Mining** | `Fouille de Données Massives` | `Cours`, `TP` |
| 11 | **Machine Learning 2** | `Machine Learning 2` | `Cours`, `TP` |
| 12 | **IT Law & Ethics** | `Droit et éthique informatique` | `Cours` |

---

## 🗂️ Directory Tree

```text
2mdsp/
├── _Inbox/                               # Intake directory for incoming raw files
│   └── README.md
├── organize.py                           # Automated keyword-based sorting script
├── AGENTS.md                             # AI Agent instructions & documentation standards
├── README.md                             # Main repository documentation (English)
├── README.ar.md                          # Repository documentation in Arabic
│
├── Traitement Automatique du Langage Naturel/
│   ├── Cours/                            # Theoretical lectures & Obsidian notes
│   └── TP/                               # Practical hands-on notebooks & labs
│
├── Environnement Cloud pour le Big Data/
│   ├── Cours/
│   └── TP/
│
├── Large Language Models/
│   ├── Cours/
│   └── TD/
│
├── ...                                   # Remaining modules listed above
```

---

## ⚙️ Automated Ingestion Workflow

### 📥 1. Staging Files in `_Inbox`
1. Place newly received materials (`.pdf`, `.pptx`, `.ipynb`, `.zip`, etc.) inside:
   ```text
   _Inbox/
   ```
2. Trigger the automated classifier script:
   ```bash
   python3 organize.py
   ```
   *Alternatively, ask your AI assistant to organize newly added files.* The script analyzes the filename and content keywords, detects whether it belongs to a Lecture (`Cours`), Lab (`TP`), or Directed Exercise (`TD`), and moves it into the corresponding module directory without naming collisions.

---

## 📐 Documentation Standards & Conventions

### 📝 Lecture Notes Standard (Obsidian-Optimized)
- **Language**: In-depth scientific Arabic explanations paired alongside technical terminology in French and English.
- **Obsidian Compatibility**:
  - Structured **YAML Frontmatter** at the top of each note (`title`, `subject`, `type`, `tags`, `date`).
  - Interactive **Obsidian Callouts** (`> [!info]`, `> [!tip]`, `> [!warning]`, `> [!example]`).
  - Mathematical formulas formatted with $\LaTeX$ (`$...$` and `$$...$$`).
  - Interconnected note graph using Wikilinks (`[[Note Name]]`).
- **Visual Diagrams (SVG Standard)**:
  - Stored as standalone `.svg` files in an adjacent `assets/` subfolder.
  - Referenced in notes using Obsidian media syntax: `![[assets/diagram_name.svg]]`.
  - Transparent backgrounds (`background: transparent`) with high-contrast `#000000` dark typography.
  - Visual diagrams are labeled in English, accompanied by detailed Arabic explanations directly beneath the embed.

### 🧪 Practical Labs Standard (TPs & Jupytext)
- **Academic Language**: Notebooks are authored in French (standard academic convention) with comprehensive docstrings and cell annotations.
- **Two-Way Synchronization with Jupytext**:
  - Generate an interactive Jupyter notebook from Markdown:
    ```bash
    jupytext --to notebook <path_to_tp>.md
    ```
  - Pair and sync `.md` and `.ipynb` representations:
    ```bash
    jupytext --set-formats ipynb,md <path_to_tp>.ipynb
    ```
- **Standardized Notebook Layout**:
  1. `Objectifs du TP` (Learning goals and objectives)
  2. `Installation & Imports` (Dependencies and package imports)
  3. `Data Ingestion & EDA` (Loading datasets and exploratory data analysis)
  4. `Implementation` (Complete, clean, and commented code implementations)
  5. `Visualizations` (High-quality plots using Matplotlib/Seaborn)
  6. `Conclusion` (Analytical conclusions and theoretical ties)

---

## 📌 Guidelines & References
For full instructions on AI agent rules, note structures, and development guidelines, refer to:
👉 [`AGENTS.md`](AGENTS.md)
