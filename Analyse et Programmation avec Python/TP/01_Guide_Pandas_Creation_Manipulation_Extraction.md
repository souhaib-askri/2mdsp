---
title: "دليل شامل لمكتبة Pandas: المراحل الثلاث (الإنشاء، التعامل، والاستخراج)"
subject: "Analyse et Programmation avec Python"
type: TP
tags:
  - 2mdsp
  - python
  - pandas
  - data-analysis
  - data-science
  - tp
date: 2026-10-20
---

# الدليل الشامل لمكتبة Pandas: المراحل الثلاث لتحليل البيانات
## (الإنشاء والتكوين • التعامل والتحويل • الاستخراج والتصدير)

> [!abstract] أهداف الكراس والدليل العملي
> يهدف هذا الدليل إلى تمكين طالب ماجستير علوم البيانات من إتقان مكتبة **Pandas** عبر تفكيك دورة معالجة البيانات الجدولية (Tabular Data Processing Cycle) إلى ثلاث مراحل منهجية متكاملة:
> 1. **مرحلة الإنشاء (Creation & Ingestion)**: بناء وتحميل هياكل البيانات (`Series` و `DataFrame`) من الذاكرة ومن مصادر خارجية.
> 2. **مرحلة التعامل والمعالجة (Manipulation & Transformation)**: تنظيف البيانات المفقودة، هندسة الميزات، والعمليات التجميعية والدمج العلائقي.
> 3. **مرحلة الاستخراج والاستعلام (Extraction, Querying & Export)**: التصفية الدقيقة، الاستعلامات الشرطية، واستخراج المؤشرات الإحصائية وتصديرها لبيئات الإنتاج.

---

## 1. المخطط المعماري للمراحل الثلاث (Pandas Architecture Pipeline)

![[assets/pandas_three_stages_workflow.svg|850]]

> [!info] الشرح التفصيلي لمخطط خط الأنابيب (Pipeline Breakdown):
> يوضح المخطط أعلاه المسار الهندسي لتدفق البيانات داخل مكتبة Pandas عبر ثلاث محطات رئيسية:
> 
> 1. **المرحلة الأولى: الإنشاء وتغذية البيانات (Stage 1: Creation & Ingestion)**:
>    - **الهياكل الأساسية (Core Structures)**: تعتمد المكتبة على كائنين رئيسيين هما السلسلة أحادية البعد `pd.Series` والإطار ثنائي الأبعاد `pd.DataFrame`.
>    - **المصادر الداخلية (In-Memory)**: تحويل القواميس (`Dictionaries`)، القوائم المعششة (`JSON-like objects`)، والمصفوفات متعددة الأبعاد (`NumPy ndarrays`) إلى جداول منظمة.
>    - **المصادر الخارجية (I/O File Readers)**: استيراد ملفات `CSV`، `Excel`، و `JSON` مع ضبط الترميز (`UTF-8`) وتحديد أنواع الأعمدة (`dtypes`) وتفسير التواريخ (`parse_dates`).
>
> 2. **المرحلة الثانية: التعامل والتجهيز والتحويل (Stage 2: Manipulation & Processing)**:
>    - **التشخيص وفحص الجودة (Inspection & QA)**: كشف الأبعاد (`shape`)، بنية الذاكرة (`info()`)، وتشخيص القيم المعدومة (`isna().sum()`).
>    - **المعالجة والتعويض (Cleaning & Imputation)**: تطبيق استراتيجيات التعامل مع الفراغات عبر الحذف الذكي (`dropna()`) أو التعويض الإحصائي (`fillna()`) باستخدام المتوسط أو الوسيط.
>    - **هندسة الخصائص والتحويلات (Feature Engineering)**: العمليات الموجهة الفائقة (Vectorized Calculations)، ومعالجة النصوص (`.str`)، وتطبيق الدوال عبر `apply` و `lambda`.
>    - **التجميع والدمج (Aggregation & Merging)**: تطبيق نموذج *Split-Apply-Combine* عبر `groupby()` و `agg()`، وإجراء عمليات الربط والدمج العلائقي (`merge`) بمختلف أنواعه (Inner, Left, Outer).
>
> 3. **المرحلة الثالثة: الاستخراج والاستعلام والتصدير (Stage 3: Extraction & Persistence)**:
>    - **التحديد الدقيق (Subsetting)**: التمييز العملي بين التحديد المعتمد على التسميات والملصقات (`.loc[]`) والتحديد المعتمد على مواقع الفهارس الرقمية (`.iloc[]`).
>    - **الاستعلام الشرطي الديناميكي (Filtering & Querying)**: استخدام الأقنعة البولينية (Boolean Masks) وميثود `.query()` لكتابة شروط تصفية مقروءة ومرنة.
>    - **الجداول التلخيصية (Pivot Tables & Tops)**: استخراج أعلى العناصر (`nlargest`)، وبناء الجداول المحورية لتلخيص الظواهر المعقدة.
>    - **الحفظ والتصدير (Serialization)**: كتابة النتائج وتصديرها بصيغ ملائمة مثل `CSV`، `JSON`، وصيغة الأعمدة عالية الكفاءة `Parquet`.

---

## 2. تفكيك المرحلة الأولى: الإنشاء والتكوين (Data Creation)

### أ. الهياكل البيانية: السلسلة (Series) مقابل الإطار (DataFrame)
- **`pd.Series`**: مصفوفة متجانسة أحادية البعد تحمل فهرساً ملصقاً (Labeled Index).
- **`pd.DataFrame`**: جدول بيانات ثنائي الأبعاد يتكون من أعمدة من نوع `Series` تشترك في نفس الفهرس.

```python
import pandas as pd
import numpy as np

# 1. إنشاء Series بفهرس مخصص
notes = pd.Series([15.5, 18.0, 12.0], index=["Amine", "Sarah", "Youssef"], name="Score_Python")

# 2. إنشاء DataFrame من قاموس بيانات
data = {
    "etudiant_id": [101, 102, 103],
    "nom": ["Amine", "Sarah", "Youssef"],
    "score": [15.5, 18.0, 12.0],
    "specialite": ["Data Science", "Machine Learning", "Data Engineering"]
}
df = pd.DataFrame(data)
```

### ب. قراءة واستيراد البيانات الخارجية (External I/O Ingestion)

> [!tip] نصيحة احترافية عند استيراد البيانات
> عند استخدام `pd.read_csv()`، يُفضل دائماً تحديد الأعمدة الزمنية عبر المعامل `parse_dates=['date_col']` لتجنب معالجتها كسلاسل نصية (`object`)، مما يوفر استهلاك الذاكرة ويسرع العمليات اللاحقة.

```python
# استيراد متقدم مع تحديد الأعمدة وتنسيق التواريخ
df_clients = pd.read_csv(
    "clients.csv",
    sep=",",
    encoding="utf-8",
    parse_dates=["date_inscription"],
    dtype={"code_postal": str, "statut": "category"}
)
```

---

## 3. تفكيك المرحلة الثانية: التعامل والتحويل (Data Manipulation)

### أ. تشخيص جودة البيانات ومعالجة القيم المفقودة (Handling Missing Data)
تظهر القيم المفقودة في Pandas بالرمز `np.nan` (Not a Number). يتم التعامل معها عبر استراتيجيتين أساسيتين:
1. **الحذف (Dropping)**: عبر `dropna()` في حال كانت نسبة الفقد ضئيلة أو السجل غير صالح بالكامل.
2. **التعويض (Imputation)**: عبر `fillna()` بالاعتماد على مقاييس النزعة المركزية:
   $$\text{Median} = \tilde{x}, \quad \text{Mean} = \bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i$$

```python
# تشخيص نسبة القيم المفقودة
taux_nan = df.isna().mean() * 100

# تعويض الراتب بالقيمة الوسيطة لتفادي تأثير القيم الشاذة (Outliers)
mediane_salaire = df["salaire"].median()
df["salaire"] = df["salaire"].fillna(mediane_salaire)
```

### ب. العمليات الموجهة وهندسة الخصائص (Vectorized Operations)
تعتمد Pandas داخلياً على لغة C عبر مصفوفات NumPy، مما يجعل العمليات الموجهة (Vectorized) أسرع بمئات المرات من حلقات `for` التقليدية في بايثون.

```python
# حساب عمود جديد بعملية موجهة مباشرة (Vectorized)
df["anciennete_annees"] = (pd.to_datetime("today") - df["date_embauche"]).dt.days / 365.25

# معالجة النصوص بكفاءة
df["nom_majuscule"] = df["nom"].str.strip().str.upper()
```

### ج. نموذج التقسيم والتطبيق والتجميع (Split-Apply-Combine)
تُعد دالة `groupby()` المحرك الأساسي للتحليل التلخيصي للبيانات.

```python
# حساب مؤشرات متعددة لكل قسم وظيفي
synthese = df.groupby("departement").agg(
    salaire_moyen=("salaire", "mean"),
    score_max=("performance_score", "max"),
    effectif=("etudiant_id", "count")
)
```

### د. الدمج والربط العلائقي (Merging & Joining)
تماماً كاستعلامات `SQL JOIN`، تتيح Pandas دمج الجداول بالاعتماد على مفتاح أساسي مشترك (`Key`).

```python
# دمج جدول الموظفين مع جدول الميزانيات (Left Join)
df_complet = pd.merge(df_employes, df_budgets, on="departement", how="left")
```

---

## 4. تفكيك المرحلة الثالثة: الاستخراج والاستعلام (Data Extraction)

### أ. التحديد المرجعي: المقارنة الجوهرية بين `loc` و `iloc`

| المعيار | `df.loc[]` | `df.iloc[]` |
| :--- | :--- | :--- |
| **أساس التحديد** | بالاعتماد على **تسميات وعناوين** الفهرس والأعمدة (Label-based) | بالاعتماد على **المواقع الرقمية الصحيحة** من 0 إلى n-1 (Integer index) |
| **شمل النهاية في التقطيع (Slicing)** | يشمل العنصر الأخير (`'A':'C'` يتضمن C) | لا يشمل العنصر الأخير (`0:3` يشمل 0, 1, 2 فقط) |
| **دعم الشروط البولينية** | يدعم مباشرة الأقنعة الشرطية `df.loc[df['age'] > 20, :]` | يتطلب مصفوفات إحداثيات رقمية |

```python
# استخراج باستخدام loc (شرط + أسماء الأعمدة)
resultat_loc = df.loc[df["salaire"] > 4000, ["nom", "departement", "salaire"]]

# استخراج باستخدام iloc (أول 5 صفوف وأول 3 أعمدة)
resultat_iloc = df.iloc[0:5, 0:3]
```

### ب. الاستعلامات التعبيرية المتقدمة عبر `.query()`
تسمح دالة `.query()` بصياغة شروط استعلام معقدة باستخدام صيغة نصية واضحة ومقروءة تشبه استعلامات SQL:

```python
seuil = 4500
dept_cibles = ["Data Science", "Machine Learning"]

# استخراج عبر query مع الإشارة لمتغيرات بايثون باستخدام علامة @
df_elite = df.query("salaire >= @seuil and departement in @dept_cibles")
```

### ج. استخراج القمم والجداول المحورية (Top N & Pivot Tables)
```python
# استخراج أعلى 3 رواتب
top_salaires = df.nlargest(3, "salaire")

# جدول محوري للمتوسطات حسب القسم وفئة الأقدمية
pivot = df.pivot_table(
    index="departement",
    columns="seniorite",
    values="salaire",
    aggfunc="mean",
    fill_value=0
)
```

### د. التصدير والحفظ لبيئة الإنتاج (Exportation & Serialization)
```python
# تصدير إلى CSV دون الفهرس التلقائي
df_elite.to_csv("salaires_hauts.csv", index=False, encoding="utf-8")

# تصدير إلى صيغة Parquet المضغوطة وعالية الأداء
df_elite.to_parquet("salaires_hauts.parquet", index=False)
```

---

## 5. مرجع الملفات والروابط التفاعلية

- **ملف الكراس التفاعلي (Jupyter Notebook)**: `[[TP_Pandas_Creation_Manipulation_Extraction.ipynb]]`
- **ملف الكراس بصيغة Jupytext Markdown**: `[[TP_Pandas_Creation_Manipulation_Extraction.md]]`
- **المخطط التوضيحي للهندسة المعمارية**: `![[assets/pandas_three_stages_workflow.svg]]`
