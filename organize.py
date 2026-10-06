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
        "keywords": ["taln", "nlp", "langage naturel", "abdelkhalek", "zawali", "natural language", "tokenization", "stemming", "lemmatiz", "prétraitement du texte", "pretraitement du texte", "prétraitement", "pretraitement", "analyse syntaxique", "corpus"]
    },
    {
        "subject": "Environnement Cloud pour le Big Data",
        "keywords": ["cloud", "aws", "azure", "gcp", "docker", "kubernetes", "openstack"]
    },
    {
        "subject": "Career Strategy Search",
        "keywords": ["career", "strategy", "cv", "yaakoubi", "soft skills"]
    },
    {
        "subject": "Large Language Models",
        "keywords": ["llm", "large language", "transformer", "bert", "gpt", "rag", "huggingface", "prompt"]
    },
    {
        "subject": "Analyse et Programmation avec Python",
        "keywords": ["analyse et programmation", "mzoughi", "numpy", "pandas", "matplotlib", "seaborn"]
    },
    {
        "subject": "Framework web Python",
        "keywords": ["django", "flask", "fastapi", "framework web", "manel"]
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

def detect_subfolder(filename: str, available_subfolders: list) -> str:
    name_lower = filename.lower()
    if any(k in name_lower for k in ["tp", "lab", "pratique", "atelier"]):
        if "TP" in available_subfolders:
            return "TP"
    if any(k in name_lower for k in ["td", "exercice", "serie", "travaux dirig"]):
        if "TD" in available_subfolders:
            return "TD"
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

        for rule in RULES:
            for kw in rule["keywords"]:
                if re.search(r'\b' + re.escape(kw) + r'\b', name_lower) or kw in name_lower:
                    matched_subject = rule["subject"]
                    break
            if matched_subject:
                break

        if matched_subject:
            target_sub = BASE_DIR / matched_subject
            available_subs = [d.name for d in target_sub.iterdir() if d.is_dir()]
            subfolder = detect_subfolder(file_path.name, available_subs)
            
            dest_dir = target_sub / subfolder if subfolder else target_sub
            dest_file = dest_dir / file_path.name

            # Avoid collision
            counter = 1
            while dest_file.exists():
                dest_file = dest_dir / f"{file_path.stem}_{counter}{file_path.suffix}"
                counter += 1

            shutil.move(str(file_path), str(dest_file))
            print(f"Moved: {file_path.name} -> {matched_subject}/{subfolder}")
        else:
            print(f"Unmatched: {file_path.name} (left in _Inbox for review)")

if __name__ == "__main__":
    organize()
