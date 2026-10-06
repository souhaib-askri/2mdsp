[English](README.md) | **العربية**

---

# 🎓 2MDSP — Master 2 Data Science & Big Data

مستودع شامل ومساحة عمل أكاديمية متكاملة لبرنامج **ماجستير علوم البيانات (2MDSP)** — المعهد العالي للغات المطبقة والإعلامية بباجة (ISLAI Béja - Institut Supérieur des Langues Appliquées et Informatique de Béja).

يحتوي المستودع على المحاضرات والملخصات التوثيقية، الأعمال التطبيقية (TPs)، التمارين الموجهة (TDs)، والمشاريع، مهيأة بالكامل للتوافق مع **Obsidian** و **Jupyter Notebooks (Jupytext)**.

---

## 📚 المواد الدراسية (Modules & Subjects)

يحتوي البرنامج على 12 مادة دراسية مقسمة وفق الهيكل التالي:

| # | المادة | Subject (Français) | الأقسام المتوفرة |
|---|---|---|---|
| 01 | **المعالجة الآلية للغة الطبيعية** | `Traitement Automatique du Langage Naturel` | `Cours`, `TP` |
| 02 | **بيئات السحابة للبيانات الضخمة** | `Environnement Cloud pour le Big Data` | `Cours`, `TP` |
| 03 | **استراتيجيات المسار المهني** | `Career Strategy Search` | `Cours` |
| 04 | **النماذج اللغوية الكبيرة** | `Large Language Models` | `Cours`, `TD` |
| 05 | **التحليل والبرمجة بلغة بايثون** | `Analyse et Programmation avec Python` | `Cours`, `TP` |
| 06 | **أطر عمل الويب بلغة بايثون** | `Framework web Python` | `Cours`, `TP` |
| 07 | **أطر عمل البيانات الضخمة** | `Frameworks Big Data` | `Cours`, `TP` |
| 08 | **المشروع التجميعي لتعلم الآلة** | `Projet Fédérateur Machine Learning` | `TD`, `TP` |
| 09 | **اللغة الإنجليزية 3** | `Anglais 3` | `Cours` |
| 10 | **تنقيب البيانات الضخمة** | `Fouille de Données Massives` | `Cours`, `TP` |
| 11 | **تعلم الآلة 2** | `Machine Learning 2` | `Cours`, `TP` |
| 12 | **قانون وأخلاقيات المعلوميات** | `Droit et éthique informatique` | `Cours` |

---

## 🗂️ هيكل المجلدات (Repository Tree)

```text
2mdsp/
├── _Inbox/                               # صندوق استلام الملفات الجديدة
│   └── README.md
├── organize.py                           # سكربت الفرز والترتيب الآلي
├── AGENTS.md                             # دليل وقواعد الوكيل الذكي ومعايير التوثيق
├── README.md                             # دليل المستودع الرئيسي (English)
├── README.ar.md                          # دليل المستودع باللغة العربية
│
├── Traitement Automatique du Langage Naturel/
│   ├── Cours/                            # المحاضرات والملخصات النظرية
│   └── TP/                               # الأعمال التطبيقية والبرمجية
│
├── Environnement Cloud pour le Big Data/
│   ├── Cours/
│   └── TP/
│
├── Large Language Models/
│   ├── Cours/
│   └── TD/
│
├── ...                                   # بقية المواد الـ 12 المذكورة أعلاه
```

---

## ⚙️ سير العمل والفرز التلقائي (Automated Workflow)

### 📥 1. إضافة ملفات جديدة عبر `_Inbox`
1. ضع أي ملفات جديدة (PDF, PPTX, IPYNB, ZIP...) داخل المجلد:
   ```text
   _Inbox/
   ```
2. شغّل سكربت التنظيم الذاتي:
   ```bash
   python3 organize.py
   ```
   أو اطلب من الوكيل الذكي (AI Assistant) فرز وترتيب الملفات تلقائياً. يقوم السكربت بتحليل الكلمات المفتاحية واسم الملف، وتحديد المادة والمجلد المناسب (`Cours` / `TP` / `TD`) ونقله دون تصادم في الأسماء.

---

## 📐 معايير التوثيق وتدوين الملاحظات

### 📝 معايير ملخصات الدروس (Obsidian Standard)
- **اللغة**: لغة عربية علمية دقيقة وواضحة، مع تضمين المصطلحات الفرنسية والإنجليزية التقنية.
- **تطبيق Obsidian**:
  - ترويسة **YAML Frontmatter** في بداية كل ملف (الوسوم، التاريخ، المادة، النوع).
  - تنبيهات أوبسيديان التفاعلية (`> [!info]`, `> [!tip]`, `> [!warning]`, `> [!example]`).
  - دعم الصيغ الرياضية عبر $\LaTeX$ (`$...$` و `$$...$$`).
  - ربط المفاهيم والملفات عبر الروابط التفاعلية `[[...]]`.
- **المخططات التوضيحية (SVG Visualizations)**:
  - حفظ الرسوم بملفات منفصلة داخل مجلد فرعي `assets/`.
  - استدعاء الرسم داخل الصفحة بصيغة: `![[assets/diagram_name.svg]]`.
  - خلفية شفافة (`background: transparent`) ونصوص سوداء واضحة (`#000000`).
  - محتوى الرسم باللغة الإنجليزية حصراً، مع شرح تحليلي بالعربية تحته مباشرة.

### 🧪 معايير الأعمال التطبيقية (TPs & Jupytext Standard)
- **اللغة الأكاديمية**: كتابة دفاتر العمل التطبيقي باللغة الفرنسية مع توثيق منهجي لجميع الخلايا البرمجية.
- **التوافق التلقائي مع Jupytext**:
  - تحويل ملف الـ Markdown إلى دفتر Jupyter تفاعلي:
    ```bash
    jupytext --to notebook <path_to_tp>.md
    ```
  - تفعيل المزامنة الثنائية بين `.md` و `.ipynb`:
    ```bash
    jupytext --set-formats ipynb,md <path_to_tp>.ipynb
    ```
- **هيكل الـ Notebook**:
  1. `Objectifs du TP` (أهداف الحصة)
  2. `Installation & Imports` (المكتبات والمتطلبات)
  3. `Data Ingestion & EDA` (تحميل واستكشاف البيانات)
  4. `Implementation` (التنفيذ البرمجي الدقيق)
  5. `Visualizations` (المخططات البيانية التوضيحية)
  6. `Conclusion` (الخلاصة والربط النظري)

---

## 📌 المراجع والتعليمات
للمزيد من التفاصيل حول القواعد المنظمة وسير عمل الوكلاء ومواصفات التوثيق المتبعة في هذا المشروع، راجع ملف:
👉 [`AGENTS.md`](AGENTS.md)
