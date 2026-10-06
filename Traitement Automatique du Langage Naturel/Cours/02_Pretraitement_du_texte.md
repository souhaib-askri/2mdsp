---
title: "المعالجة المسبقة للنصوص (Prétraitement du texte)"
subject: "Traitement Automatique du Langage Naturel"
type: Cours
tags:
  - 2mdsp
  - taln
  - nlp
  - text-preprocessing
  - tokenization
  - stemming
  - lemmatization
date: 2026-10-05
---

# المعالجة المسبقة للنصوص (Text Preprocessing / Prétraitement du texte)

> [!abstract] ملخص الدرس
> المعالجة المسبقة هي **حجر الأساس وأولى مراحل أي نظام معالجة لغات طبيعية**. لا يمكن لخوارزميات التعلم الآلي التعامل مباشرة مع النصوص الخام المليئة بعلامات الترقيم، الرموز، وتصريفات الكلمات. في هذا الدرس، نستعرض خطوة بخطوة كيفية تحويل النص الخام إلى تسلسل من الرموز المعيارية (Tokens) عبر تقنيات **التقطيع (Tokenization)** و**التجذير (Stemming)** و**الرد للأصل المعجمي (Lemmatization)**.

---

## 1. طرح الإشكالية (Présentation du problème)

لنفترض أن لدينا مهمة **تصنيف نصوص (Text Classification)** مثل **تحليل المشاعر (Sentiment Analysis)** لمراجعات الفنادق أو الأفلام:

| النص الخام | الفئة الحقيقية |
| :--- | :---: |
| *"The hotel is really beautiful. Very nice and helpful service at the front desk."* | **إيجابي (Positive)** |
| *"We had problems to get the Wi-Fi working. The pool area was occupied with young party animals. So the area wasn't fun for us."* | **سلبي (Negative)** |

> [!warning] التحدي البرمجي
> كيف يفهم الحاسوب الكلمات المكررة بصيغ مختلفة مثل `is` و `wasn't` و `problems` و `problem`؟
> النصوص مليئة بالزوائد، علامات الترقيم، والأفعال المصرّفة. نحتاج إلى تحويل المستند إلى **تسلسل رموز (Sequence of Tokens)** نقية وذات دلالة.

---

## 2. مستويات تمثيل النص (Représentation du texte)

```
                 مستويات تمثيل النصوص اللغوية
  ┌────────────────────────────────────────────────────────┐
  │ مستوى منخفض (Low-level):                               │
  │ • الحروف والرموز (Caractères)                           │
  ├────────────────────────────────────────────────────────┤
  │ المستوى المعتمد في TALN:                               │
  │ • الكلمات (Mots) ➔ تسلسل من الكلمات المفيدة (Tokens)    │
  ├────────────────────────────────────────────────────────┤
  │ مستوى عالي (High-level):                               │
  │ • الجمل (Phrases)                                      │
  │ • الفقرات (Paragraphes)                                │
  └────────────────────────────────────────────────────────┘
```

> [!note] تعريف الكلمة الصالحة للمعالجة
> **الكلمة (Word)** هي متتالية من الحروف ذات معنى دلالي (`meaningful`).
> في اللغات اللاتينية، تفصل المسافات وعلامات الترقيم بين الكلمات، لكن توجد استثناءات معقدة:
> - **كلمات مركبة بدون مسافات**: مثل الألمانية *"Rechtsschutzversicherungsgesellschaften"* (تعني: شركات التأمين التي تقدم الحماية القانونية).
> - **جمل بدون مسافات**: مثل الهاشتاغات `#Butyoucanstillreaditright`.

---

## 3. خط أنابيب المعالجة المسبقة (SVG Pipeline)

![[assets/preprocessing_pipeline.svg|700]]

> [!info] شرح خطوات مسار المعالجة المسبقة (Pipeline Walkthrough):
> 1. **النص الخام (Raw Text)**: استلام البيانات غير المهيكلة مع الضوضاء والاختصارات مثل `"This is Andrew's text, isn't it?"`.
> 2. **التقطيع (Tokenization)**: تقسيم الجملة إلى وحدات مستقلة (Tokens) مع الحفاظ على المقاطع المنفية وعلامات الترقيم المفيدة.
> 3. **التطبيع (Normalization)**: تقليص التباين اللفظي وإعادة الكلمات إلى جذورها إما عبر التجذير (`Stemming`) أو الرد المعجمي (`Lemmatization`).
> 4. **الرموز الجاهزة (Clean Tokens)**: مصفوفة رموز نقية خالية من الضوضاء جاهزة للترميز المتجهي (Vectorization) والتدريب الإحصائي.

---

## 4. تقنيات التقطيع (Tokenization) بالتفصيل

التقطيع هو عملية تقسيم النص المتصل إلى وحدات لغوية صغرى تسمى **Tokens**.
مكتبة `nltk` توفر عدة أدوات للتقطيع تختلف في كفاءتها ودقتها:

### 1) تقطيع الفراغات (WhitespaceTokenizer)
يفصل النص بناءً على الفراغات (`spaces` و `tabs` و `newlines`) فقط.

```python
import nltk
text = "This is Andrew's text, isn't it?"

tokenizer = nltk.tokenize.WhitespaceTokenizer()
tokens = tokenizer.tokenize(text)
print(tokens)
# الناتج: ['This', 'is', "Andrew's", 'text,', "isn't", 'it?']
```

> [!danger] المشكلة
> تلتصق علامات الترقيم بالكلمات (مثل `'text,'` و `'it?'`). سيعتبر النموذج `'it'` و `'it?'` كلمتين مختلفتين تماماً!

---

### 2) تقطيع الرموز والحروف (WordPunctTokenizer)
يعتمد على التعبيرات النمطية (`RegEx`): يفصل بين الحروف الأبجدية الرقمية والرموز غير الأبجدية.

```python
tokenizer = nltk.tokenize.WordPunctTokenizer()
tokens = tokenizer.tokenize(text)
print(tokens)
# الناتج: ['This', 'is', 'Andrew', "'", 's', 'text', ',', 'isn', "'", 't', 'it', '?']
```

> [!warning] المشكلة
> يفصل النفي اختصاراً بطريقة غير معبرة دلالياً؛ مثل `'isn'` و `'t'` و `'s'`، وهي رموز منفردة لا معنى لها في المعجم.

---

### 3) تقطيع تريبنك المعياري (TreebankWordTokenizer) ⭐
هو المقترح الأفضل والأكثر استخداماً في الأبحاث (وفق معايير Penn Treebank):
- يقسم الاختصارات المنفية بطريقة صحيحة: `isn't` $\rightarrow$ `['is', "n't"]`.
- يفصل علامات الترقيم في نهاية الجملة.
- يعزل الفواصل وعلامات الاقتباس المتبوعة بفراغ.

```python
tokenizer = nltk.tokenize.TreebankWordTokenizer()
tokens = tokenizer.tokenize(text)
print(tokens)
# الناتج: ['This', 'is', 'Andrew', "'s", 'text', ',', 'is', "n't", 'it', '?']
```

---

## 5. توحيد الكلمات: التجذير مقابل الرد للأصل (Stemming vs Lemmatization)

غالبًا ما نرغب في دمج الأشكال الصرفية المتعددة للكلمة الواحدة (مثل `talk` و `talks` و `talking` و `talked`) لتمثيلها برمز موحد:

![[assets/stemming_vs_lemmatization.svg|700]]

> [!tip] شرح الفروق الجوهرية الموضحة في الرسم:
> * **التجذير (Stemming)**: خوارزمية سريعة تقتطع النهايات (مثل `ing`, `ed`, `es`) بحسب قواعد إرشادية جامدة. يعيبها أنها قد تنتج كلمات مشوهة غير صحيحة معجمياً (مثل تحويل `wolves` إلى `wolv`).
> * **الرد للأصل المعجمي (Lemmatization)**: عملية ذكية تعتمد على التحليل الصرفي وقاموس لغوي (مثل WordNet)، وتضمن دائماً إعادة الكلمة إلى أصلها المعجمي الصحيح (مثل إرجاع `feet` إلى المفرد `foot` و `wolves` إلى `wolf`).



### تطبيق عملي للمقارنة في Python:

```python
import nltk
from nltk.tokenize import TreebankWordTokenizer
from nltk.stem import PorterStemmer, WordNetLemmatizer

text = "feet cats wolves talked"
tokens = TreebankWordTokenizer().tokenize(text)

# 1. التجذير (Stemming)
stemmer = PorterStemmer()
stemmed = [stemmer.stem(t) for t in tokens]
print("Stemming:    ", " ".join(stemmed))
# الناتج: 'feet cat wolv talk'  (لاحظ: wolv كلمة غير صحيحة، و feet لم تتغير)

# 2. الرد المعجمي (Lemmatization)
lemmatizer = WordNetLemmatizer()
lemmatized = [lemmatizer.lemmatize(t) for t in tokens]
print("Lemmatization:", " ".join(lemmatized))
# الناتج: 'foot cat wolf talked' (أعاد الجمع المفرد بدقة: foot و wolf)
```

---

## 6. خلاصة الدرس (Synthèse)

1. النص عبارة عن متتالية من الرموز (Tokens).
2. **التقطيع (Tokenization)** عملية استخراج الكلمات المفيدة والتخلص من التشويش.
3. **تطبيع النصوص (Normalization)** يقلل من حجم المعجم (Vocabulary Size) ويمنع تشتت النماذج الإحصائية.
4. يفضل استخدام **`TreebankWordTokenizer`** للتقطيع، واستخدام **`WordNetLemmatizer`** عندما تكون الدقة اللغوية أهم من سرعة المعالجة.

---

> [!tip] التطبيق العملي التالي
> طبق كل هذه الخطوات عملياً على تغريدات تويتر في:
> 👉 **[[01_Atelier_1_Pretraitement_Twitter|الورشة التطبيقية الأولى (Atelier 1 - Twitter Preprocessing)]]**
