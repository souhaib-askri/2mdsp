#!/usr/bin/env python3
import os
import shutil
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INBOX_DIR = BASE_DIR / "_Inbox"

RULES = [
    {
        "subject": "Traitement Automatique du Langage Naturel",
        "keywords": ["taln", "nlp", "langage naturel", "abdelkhalek", "zawali", "natural language", "tokenization", "stemming", "lemmatiz", "prétraitement du texte", "pretraitement du texte", "prétraitement", "pretraitement", "analyse syntaxique", "corpus", "racine", "racinisation", "stemmer"]
    },
    {
        "subject": "Environnement Cloud pour le Big Data",
        "keywords": ["cloud", "aws", "azure", "gcp", "docker", "kubernetes", "openstack", "traitement de données big data", "données big data avec pyspark", "donnees big data avec pyspark", "big data avec pyspark"]
    },
    {
        "subject": "Career Strategy Search",
        "keywords": ["career", "strategy", "cv", "yaakoubi", "soft skills"]
    },
    {
        "subject": "Large Language Models",
        "keywords": ["llm", "large language", "transformer", "bert", "gpt", "rag", "huggingface", "prompt", "ezzameli", "kaouther"]
    },
    {
        "subject": "Analyse et Programmation avec Python",
        "keywords": ["analyse et programmation", "mzoughi", "numpy", "pandas", "panda", "matplotlib", "seaborn", "programmation python", "programmation avec python"]
    },
    {
        "subject": "Framework web Python",
        "keywords": ["django", "flask", "fastapi", "framework web", "manel", "fwp", "khemiri", "app1", "correction app", "user.py", "session", "héritage", "heritage", "monprojetflask", "etudiant"]
    },
    {
        "subject": "Frameworks Big Data",
        "keywords": ["spark", "hadoop", "hdfs", "mapreduce", "pyspark", "dakhli"]
    },
    {
        "subject": "Projet Fédérateur Machine Learning",
        "keywords": ["projet federateur", "federateur", "pfml"]
    },
    {
        "subject": "Anglais 3",
        "keywords": ["anglais", "english", "maddouri", "toeic", "ielts"]
    },
    {
        "subject": "Fouille de Données Massives",
        "keywords": ["fouille", "data mining", "mhamdi", "donnees massives", "association rules", "clustering"]
    },
    {
        "subject": "Machine Learning 2",
        "keywords": ["machine learning 2", "ml2", "jerbi", "svm", "random forest", "deep learning", "gradient boosting"]
    },
    {
        "subject": "Droit et éthique informatique",
        "keywords": ["droit", "ethique", "deontologie", "rgpd", "zbouna", "propriete intellectuelle", "cybersecurite"]
    },
]

def extract_pdf_preview(pdf_path: Path, max_pages: int = 3) -> str:
    try:
        import pypdf
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        for i in range(min(max_pages, len(reader.pages))):
            extracted = reader.pages[i].extract_text()
            if extracted:
                text += extracted + " "
        return text.lower()
    except Exception:
        return ""

def extract_zip_preview(zip_path: Path) -> str:
    try:
        import zipfile
        with zipfile.ZipFile(zip_path, 'r') as z:
            return " ".join(z.namelist()).lower()
    except Exception:
        return ""

def detect_subfolder(filename: str, available_subfolders: list) -> str:
    name_lower = filename.lower()
    if any(k in name_lower for k in ["tp", "lab", "pratique", "atelier", "racine", "extraction", "stemm", "app1", "correction app", "user.py", "session", "héritage", "heritage"]):
        if "TP" in available_subfolders:
            return "TP"
    if any(k in name_lower for k in ["td", "exercice", "serie", "travaux dirig"]):
        if "TD" in available_subfolders:
            return "TD"
    if any(k in name_lower for k in ["devoir", "projet", "recherche", "assignment", "activite", "activité", "تكليف", "تكليفات"]):
        if "Assignments" in available_subfolders:
            return "Assignments"
        if "تكليفات" in available_subfolders:
            return "تكليفات"
    if any(k in name_lower for k in ["cours", "chapitre", "ch", "cm", "lecture", "slide", "presentation"]):
        if "Cours" in available_subfolders:
            return "Cours"
    
    # Defaults
    if "Cours" in available_subfolders:
        return "Cours"
    elif "TP" in available_subfolders:
        return "TP"
    elif "TD" in available_subfolders:
        return "TD"
    return ""

def organize():
    if not INBOX_DIR.exists():
        print(f"Directory {INBOX_DIR} does not exist.")
        return

    files = [f for f in INBOX_DIR.iterdir() if f.is_file() and f.name != "README.md"]
    if not files:
        print("Inbox is empty. No files to organize.")
        return

    for file_path in files:
        name_lower = file_path.name.lower()
        matched_subject = None

        # 1. Match by filename
        for rule in RULES:
            for kw in rule["keywords"]:
                if re.search(r'\b' + re.escape(kw) + r'\b', name_lower) or kw in name_lower:
                    matched_subject = rule["subject"]
                    break
            if matched_subject:
                break

        # 2. Match by content if PDF
        if not matched_subject and file_path.suffix.lower() == ".pdf":
            preview_text = extract_pdf_preview(file_path)
            if preview_text:
                for rule in RULES:
                    for kw in rule["keywords"]:
                        if re.search(r'\b' + re.escape(kw) + r'\b', preview_text) or kw in preview_text:
                            matched_subject = rule["subject"]
                            break
                    if matched_subject:
                        break

        # 3. Match by content if ZIP
        if not matched_subject and file_path.suffix.lower() == ".zip":
            preview_text = extract_zip_preview(file_path)
            if preview_text:
                for rule in RULES:
                    for kw in rule["keywords"]:
                        if re.search(r'\b' + re.escape(kw) + r'\b', preview_text) or kw in preview_text:
                            matched_subject = rule["subject"]
                            break
                    if matched_subject:
                        break

        if matched_subject:
            target_sub = BASE_DIR / matched_subject
            available_subs = [d.name for d in target_sub.iterdir() if d.is_dir()]
            subfolder = detect_subfolder(file_path.name, available_subs)
            
            dest_dir = target_sub / subfolder if subfolder else target_sub
            clean_stem = re.sub(r'\s*\(\d+\)$', '', file_path.stem).strip()
            clean_name = f"{clean_stem}{file_path.suffix}"
            dest_file = dest_dir / clean_name

            # Avoid collision
            counter = 1
            while dest_file.exists():
                dest_file = dest_dir / f"{clean_stem}_{counter}{file_path.suffix}"
                counter += 1

            shutil.move(str(file_path), str(dest_file))
            print(f"Moved: {file_path.name} -> {matched_subject}/{subfolder}/{dest_file.name}")
        else:
            print(f"Unmatched: {file_path.name} (left in _Inbox for review)")

if __name__ == "__main__":
    organize()

