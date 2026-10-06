---
title: "ورشة العمل 1 - الجزء 1: المعالجة المسبقة لتغريدات تويتر"
subject: "Traitement Automatique du Langage Naturel"
type: TP
tags:
  - 2mdsp
  - taln
  - nlp
  - tp
  - nltk
  - twitter
  - sentiment-analysis
date: 2026-10-05
---

# ورشة العمل 1 - الجزء 1: المعالجة المسبقة لتغريدات تويتر (NLP Atelier 1)

> [!abstract] أهداف الورشة العملية
> 1. بناء خط أنابيب عملي (Pipeline) لمعالجة بيانات تويتر الخام الموجهة لمهمة **تحليل المشاعر (Sentiment Analysis)**.
> 2. استكشاف واستخدام مجموعة بيانات `twitter_samples` المدمجة في حزمة `NLTK`.
> 3. إجراء تحليل استكشافي للبيانات (EDA) وحساب توازن الفئات ورسمها بيانياً باستخدام `Matplotlib`.
> 4. فحص التغريدات الخام وتحليل مكوناتها الخاصة (الروابط، الهاشتاغات، والرموز التعبيرية Emoticons).

---

## 1. مخطط مراحل ورشة العمل (SVG Workflow)

![[assets/twitter_workflow.svg|700]]

> [!info] شرح مراحل الورشة التطبيقية (Workflow Explanation):
> 1. **تحميل البيانات (Download Corpus)**: جلب عينة التغريدات المجهزة `twitter_samples` عبر مكتبة `nltk`.
> 2. **استخراج النصوص (Extract Strings)**: فصل التغريدات الإيجابية (5000 تغريدة) والسلبية (5000 تغريدة) في مصفوفات نصوص مستقلة.
> 3. **التحليل الاستكشافي والتوزيع (Class Balance)**: التحقق من توازن العينات ورسم النسبة (50% لكل فئة) في مخطط دائري (`Pie Chart`) باستخدام `Matplotlib`.
> 4. **المعاينة البصرية بالألوان (Visual Inspection)**: فحص بنية التغريدات الخام باستخدام ألوان الطرفية لتمييز الروابط (URLs)، الإشارات (`@mentions`)، والرموز التعبيرية تمهيداً لتنظيفها.



---

## 2. الكود البرمجي الكامل للورشة (Implementation)

تم استكمال جميع الفراغات المطلوبة في ورقة عمل الـ TP:

```python
# ==========================================
# 1. استيراد المكتبات الأساسية
# ==========================================
import nltk                                  # مكتبة معالجة اللغات الطبيعية في بايثون
from nltk.corpus import twitter_samples       # مجموعة بيانات التغريدات المجهزة في NLTK
import matplotlib.pyplot as plt              # مكتبة الرسم والتمثيل البياني
import random                                # مكتبة توليد الأرقام العشوائية

# ==========================================
# 2. تنزيل قاعدة بيانات التغريدات
# ==========================================
nltk.download('twitter_samples')

# ==========================================
# 3. تحميل نصوص التغريدات الإيجابية والسلبية
# ==========================================
# استخراج التغريدات كنصوص خام عبر دالة strings()
all_positive_tweets = twitter_samples.strings('positive_tweets.json')
all_negative_tweets = twitter_samples.strings('negative_tweets.json')

# ==========================================
# 4. تقرير إحصائي عن البيانات
# ==========================================
print('Number of positive tweets: ', len(all_positive_tweets))
print('Number of negative tweets: ', len(all_negative_tweets))

print('\nThe type of all_positive_tweets is: ', type(all_positive_tweets))
print('The type of a tweet entry is: ', type(all_positive_tweets[0]))
```

> [!info] المخرجات المتوقعة في Terminal
> ```text
> Number of positive tweets:  5000
> Number of negative tweets:  5000
> 
> The type of all_positive_tweets is:  <class 'list'>
> The type of a tweet entry is:  <class 'str'>
> ```

---

## 3. التمثيل البياني لتوزيع الفئات (Matplotlib Visualization)

لرسم مخطط دائري (Pie Chart) يوضح توازن البيانات وتساوي العينات:

```python
# تحديد حجم الشكل البياني (5x5 بوصة)
fig = plt.figure(figsize=(5, 5))

# عناوين الفئات
labels = 'Positives', 'Negative'

# أحجام الشرائح بناءً على عدد العينات
sizes = [len(all_positive_tweets), len(all_negative_tweets)]

# رسم المخطط الدائري
# autopct='%1.1f%%': لإظهار النسبة المئوية برقم عشري واحد
# startangle=90: لبدء التقسيم بزاوية قائمة
plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)

# جعل نسبة المحاور متساوية لرسم دائرة مثالية
plt.axis('equal')

# إظهار الرسم البياني
plt.title('Twitter Sentiment Dataset Class Distribution')
plt.show()
```

---

## 4. معاينة النصوص الخام بالألوان (Inspecting Raw Tweets)

تتيح أكواد ANSI للألوان في الطرفية طباعة التغريدة الإيجابية باللون **الأخضر** والتغريدة السلبية باللون **الأحمر**:

```python
# طباعة تغريدة إيجابية عشوائية باللون الأخضر (\033[92m)
print('\033[92m' + all_positive_tweets[random.randint(0, 5000)])

# طباعة تغريدة سلبية عشوائية باللون الأحمر (\033[91m)
print('\033[91m' + all_negative_tweets[random.randint(0, 5000)])

# إعادة تعيين اللون الطبيعي للطرفية
print('\033[0m')
```

---

## 5. الملاحظات الجوهرية (Observations) والمرحلة القادمة

> [!important] ما الذي نلاحظه في تغريدات تويتر الخام؟
> عند فحص التغريدات المطبوعة، نجد عناصر خاصة لا توجد في النصوص التقليدية:
> 1. **الروابط الخارجية (URLs)**: مثل `http://t.co/...` (لا تحمل معنى دلالي للمشاعر ويجب حذفها عبر RegEx).
> 2. **الإشارات للمستخدمين (Mentions)**: مثل `@TwitterUser` (تعتبر ضوضاء في التصنيف).
> 3. **علامات الهاشتاغ (Hashtags)**: مثل `#AI` أو `#Awesome` (قد تحتوي على مشاعر، لكن يجب تنظيف رمز `#`).
> 4. **الرموز التعبيرية (Emoticons & Emojis)**: مثل `:)` أو `:-(` (تحمل دلالة مشاعر قوية جداً ويجب التعامل معها بعناية).

---

## 6. الخطوة القادمة (Partie 2 Roadmap)

في الجزء الثاني من الورشة، سيتم تطبيق ما تعلمناه في:
👉 **[[02_Pretraitement_du_texte|درس المعالجة المسبقة للنصوص]]**:
- إزالة الضوضاء والروابط باستخدام تعبيرات `re` النمطية.
- التقطيع باستخدام `TweetTokenizer`.
- حذف الكلمات الشائعة التي لا تضيف معنى (Stopwords).
- تطبيق التجذير (Stemming) على الكلمات.
