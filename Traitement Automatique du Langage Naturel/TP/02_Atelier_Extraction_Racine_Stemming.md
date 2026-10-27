---
title: "ورشة العمل 2: استخراج جذور الكلمات (Stemming / Extraction de la racine)"
subject: "Traitement Automatique du Langage Naturel"
type: TP
tags:
  - 2mdsp
  - taln
  - nlp
  - stemming
  - porter-stemmer
  - snowball-stemmer
  - normalization
date: 2026-10-12
---

# ورشة العمل 2: استخراج جذور الكلمات (Stemming / Extraction de la racine)

> [!abstract] أهداف الورشة العملية
> 1. فهم وتطبيق آليات **التجذير واستخراج الجذور (Stemming / Racinisation)** كخطوة أساسية في خط أنابيب المعالجة المسبقة للنصوص.
> 2. المقارنة العملية بين خوارزميتي التجذير الشهيرتين: **PorterStemmer** (النسخة القياسية لعام 1980) و **SnowballStemmer** (المعروفة بـ Porter2 لعام 2001).
> 3. تطبيق التجذير على قائمة كلمات تشتمل على مشتقات متعددة (`exemple_mots`).
> 4. تطبيق تقطيع الجمل وتجذير الكلمات على جملة كاملة (`exemple`)، ودراسة سلوك الخوارزميتين في توحيد الكلمات المشتقة من أصل واحد مثل (*consider*).

---

## 1. مقارنة خوارزميات التجذير (SVG Visualization)

![[assets/stemming_algorithms_comparison.svg]]

> [!info] شرح المقارنة بين PorterStemmer و SnowballStemmer (Algorithmic Comparison):
> يوضح الرسم البياني أعلاه الفروق الجوهرية بين الخوارزميتين:
> - **خوارزمية بورتر (PorterStemmer - 1980)**: خوارزمية استدلالية (Heuristic) تعتمد على 5 مراحل متتالية من قواعد حذف اللواحق والزوائد الإنجليزية (Suffix Stripping). تتميز بالسرعة ولكنها قد تعطي أحياناً جذوراً غير دقيقة؛ فمثلاً حوّلت الكلمة `pythonly` إلى `pythonli` باستبدال حرف `y` بـ `i`.
> - **خوارزمية سنوبول (SnowballStemmer - 2001)**: نسخة محسنة ومطورة من قِبل مارتن بورتر نفسه (Martin Porter). تتميز بدعم متعدد اللغات (الإنجليزية، الفرنسية، الإسبانية، العربية، إلخ)، وامتلاكها لقواعد أكثر دقة تتفادى التجذير الخاطئ، حيث نجحت في إرجاع `pythonly` مباشرة إلى الجذر الصحيح `python`.

---

## 2. المسائل والتطبيقات العملية في الورشة

### المسألة الأولى: استخراج الجذور من قائمة كلمات (`exemple_mots`)
المعطيات:
```python
exemple_mots = ["python", "pythoner", "pythoning", "pythoned", "pythonly"]
```

النتائج المقارنة:
| الكلمة الأصلية | نتيجة PorterStemmer | نتيجة SnowballStemmer | الملاحظة والتحليل |
| :--- | :---: | :---: | :--- |
| `python` | `python` | `python` | تطابق تام |
| `pythoner` | `python` | `python` | تم حذف لاحقة الفاعل `-er` بنجاح |
| `pythoning` | `python` | `python` | تم حذف لاحقة الاستمرار `-ing` بنجاح |
| `pythoned` | `python` | `python` | تم حذف لاحقة الماضي `-ed` بنجاح |
| `pythonly` | `pythonli` | `python` | **اختلاف**: عالج Snowball حرف `ly` بدقة أكبر وأعاد الجذر النظيف |

---

### المسألة الثانية: تقطيع وتجذير جملة كاملة (`exemple`)
المعطيات:
```python
exemple = "You are not considering the considerable performance considerably. Its consequences will not be considered."
```

خطوات الحل:
1. تقطيع النص إلى وحدات لغوية عبر `word_tokenize(exemple)` من مكتبة `nltk`.
2. تصفية علامات الترقيم والأقواس.
3. استخراج الجذور عبر الخوارزميتين وملاحظة عائلة الكلمة `consider`:
   - `considering` $\rightarrow$ `consid`
   - `considerable` $\rightarrow$ `consid`
   - `considerably` $\rightarrow$ `consid`
   - `considered` $\rightarrow$ `consid`

> [!tip] النتيجة التحليلية
> على الرغم من أن الجذر الناتج `consid` ليس كلمة معجمية إنجليزية صحيحة (وهذا هو الفرق الجوهري بين التجذير Stemming والرد المعجمي Lemmatization)، إلا أن الخوارزمية نجحت في تقليص أبعاد المفردات (Dimensionality Reduction) عبر توحيد 4 كلمات مختلفة في رمز موحد يمثل المعنى الدلالي المشترك.

---

## 3. الدفتر التفاعلي وملفات الورشة

- تم إعداد وتوليد كراس العمل التفاعلي بالكامل وفق معيار Jupytext:
  - ملف الماركداون: `[[NLP_Atelier_Extraction_Racine_Stemming.md]]`
  - كراس العمل التفاعلي: `[[NLP_Atelier_Extraction_Racine_Stemming.ipynb]]`
- ملف نص المسألة الأصلي: `[[Extraction de la racine du mot.pdf]]`
- الدرس النظري المرتبط: `[[02_Pretraitement_du_texte.md]]`
