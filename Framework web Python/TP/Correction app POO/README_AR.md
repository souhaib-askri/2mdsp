---
title: "دليل تطبيق الويب كائني التوجه (Correction app POO)"
subject: "Framework web Python"
type: TP
tags:
  - 2mdsp
  - fwp
  - flask
  - poo
  - oop
  - jinja2
  - mvc
  - python
date: 2026-10-23
---

# تطبيق الويب فلاسك كائني التوجه (Correction app POO)
## النسخة المعتمدة والمصححة لورشة العمل الأولى (TP 1)

[🇸🇦 النسخة العربية](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/Correction%20app%20POO/README_AR.md) | [🇫🇷 Version Française (README.md)](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/Correction%20app%20POO/README.md)

> [!abstract] بطاقة تعريف المشروع
> - **المقياس الأكاديمي** : أطر عمل الويب بايثون (*Framework Web Python*)
> - **المستوى** : السنة الثانية ماجستير علوم البيانات للمحترفين (2MDSP)
> - **السياق التطبيقي** : العمل التطبيقي الأول (TP 1) — الانتقال من البرمجة الإجرائية إلى البرمجة كائنية التوجه (POO)
> - **الأستاذ المسؤول** : نبيل الخميري (*Nabil KHEMIRI*)

---

## 📌 1. نظرة عامة والهدف المعماري

يمثل مجلد `Correction app POO` **النسخة المرجعية والمصححة** للعمل التطبيقي الأول. يهدف هذا المشروع إلى معالجة أوجه القصور البرمجية في التطبيق الأولي الإجرائي ([`App1`](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/App1))، وإعادة هيكلته بالكامل وفق نمط المعمارية البرمجية ثلاثية الطبقات **نموذج-عرض-متحكم (MVC: Model-View-Controller)** وقواعد **البرمجة كائنية التوجه (Object-Oriented Programming - OOP)**.

### ما الذي يميز هذا التطبيق؟
1. **الاستغناء عن المتغيرات المتناثرة** : بدلاً من استقبال مدخلات الاستمارة وتمريرها واحداً تلو الآخر كقيم نصية مستقلة، يتم تجميعها وبناء كائن مجسد موحد يمثل المستخدم من الصنف [`User`](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/Correction%20app%20POO/models/user.py#L2-L51).
2. **تطبيق مبدأ الكبسلة الصارمة (Strict Encapsulation)** : كافة خصائص المستخدم خاصة ومحمية ببادئة شرطتين سفليتين (`__nom`، `__email`، إلخ) لمنع الوصول المباشر والعبث بالبيانات.
3. **التكامل المباشر مع محرك القوالب (Jinja2 Engine)** : تمرير الكائن الكامل `user1` إلى قالب النتيجة [`resultat.html`](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/Correction%20app%20POO/templates/resultat.html)، واستدعاء دوال القراءة والوصول (`get_*()`) ديناميكياً داخل كود HTML.

---

## 🎯 2. الأهداف التعليمية للورشة

- [x] **ربط فلاسك بنماذج الأعمال (Flask & Domain Models)** : بناء تطبيق ويب حقيقي يعتمد على كائنات بايثون المهيكلة.
- [x] **تطبيق مبادئ الكبسلة والتحكم بالوصول** : استخدام دوال الوصول (*Getters*) ودوال التعديل (*Setters*) لإدارة حالة الكائن.
- [x] **بناء حزم بايثون المعيارية (Python Packages)** : تنظيم طبقة النماذج داخل مجلد `models/` مزود بملف `__init__.py`.
- [x] **استدعاء دوال الكائنات داخل Jinja2** : استغلال مرونة محرك القوالب لتشغيل توابع الكائنات تلقائياً أثناء توليد الصفحة.
- [x] **التهيئة لمعالجة الاستثناءات المخصصة** : وضع حجر الأساس لإضافة استثناءات التحقق من صحة البريد والسن قبل إنشاء الكائن.

---

## 📂 3. الهيكلية المعمارية للمشروع

```text
TP/Correction app POO/
├── app.py                      # المتحكم الرئيسي (Flask Controller) ومسارات التوجيه
├── models/                     # حزمة نماذج الأعمال (Business Logic Package)
│   ├── __init__.py             # ملف تعريف الحزمة البرمجية في بايثون
│   └── user.py                 # صنف كائن المستخدم (User Class) بتغليف صارم
├── templates/                  # مجلد واجهات العرض ومحرك القوالب (Jinja2 Views)
│   ├── inscription.html        # استمارة التسجيل (طلب GET /)
│   └── resultat.html           # صفحة عرض النتيجة باستدعاء دوال الكائن (طلب POST /inscription)
├── static/                     # مجلد الأصول الثابتة (Static Assets)
│   └── style.css               # ملف التنسيقات والأنماط البصرية (CSS)
├── user.py                     # نسخة احتياطية من كود الصنف بالجذر
├── inscription.html            # ملف الاستمارة الأصلي
├── resultat.html               # ملف النتيجة الأصلي
├── style.css                   # ملف الأنماط الأصلي
├── README.md                   # التوثيق باللغة الفرنسية
└── README_AR.md                # التوثيق باللغة العربية (هذا الملف)
```

> [!info] ملاحظة معمارية هامة
> - وجود ملف `__init__.py` داخل مجلد `models/` يجعل بايثون يتعامل معه كحزمة رسمية (*Package*)، مما يمكننا من كتابة: `from models.user import User`.
> - يفرض فلاسك اصطلاحاً وضع صفحات HTML داخل مجلد باسم `templates/`، وكافة ملفات التنسيق والصور داخل مجلد `static/`.

---

## 🧩 4. شرح المكونات البرمجية التفصيلية

### أ. نموذج الأعمال الكائني: [`models/user.py`](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/Correction%20app%20POO/models/user.py)

يطبق هذا الملف مبدأ **الكبسلة (Encapsulation)** بحرفية عالية:

```python
class User:
    # 1. دالة البناء والتهيئة (Constructor)
    def __init__(self, nom, prenom, email, mot_de_passe, date_naissance):
        self.__nom = nom                      # خاصية خاصة (Private Attribute)
        self.__prenom = prenom
        self.__email = email
        self.__mot_de_passe = mot_de_passe
        self.__date_naissance = date_naissance

    # 2. دوال القراءة والوصول (Accessors / Getters)
    def get_nom(self):
        return self.__nom

    def get_prenom(self):
        return self.__prenom

    def get_email(self):
        return self.__email

    def get_mot_de_passe(self):
        return self.__mot_de_passe

    def get_date_naissance(self):
        return self.__date_naissance

    # 3. دوال التعديل والتحديث (Mutators / Setters)
    def set_nom(self, nom):
        self.__nom = nom

    def set_prenom(self, prenom):
        self.__prenom = prenom

    def set_email(self, email):
        self.__email = email

    def set_mot_de_passe(self, mot_de_passe):
        self.__mot_de_passe = mot_de_passe

    def set_date_naissance(self, date_naissance):
        self.__date_naissance = date_naissance
```

> [!tip] لماذا نستخدم البادئة `__` في الخصائص؟
> في بايثون، عندما تبدأ الخاصية بشرطتين سفليتين (مثل `__nom`)، يفعل المفسر خاصية **تشويه الأسماء (Name Mangling)**، فيحولها داخلياً إلى `_User__nom`. هذا يمنع أي محاولة خارجية للوصول غير المصرح به مثل `user1.__nom = "Ali"`، ويجبر جميع أجزاء البرنامج على المرور عبر الدوال المعيارية `get_nom()` و `set_nom()`.

---

### ب. المتحكم وموجه المسارات: [`app.py`](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/Correction%20app%20POO/app.py)

يقوم بدور المنسق بين طلبات العميل من المتصفح والنموذج الكائني وقوالب العرض:

```python
from flask import Flask, render_template, request
from models.user import User

app = Flask(__name__)

# 1. مسار عرض الاستمارة (HTTP GET)
@app.route("/")
def inscription():
    return render_template("inscription.html")

# 2. مسار معالجة بيانات الاستمارة (HTTP POST)
@app.route("/inscription", methods=["POST"])
def traiter_inscription():
    # استخراج البيانات من قاموس الطلب
    nom = request.form["nom"]
    prenom = request.form["prenom"]
    email = request.form["email"]
    mot_de_passe = request.form["mot_de_passe"]
    date_naissance = request.form["date_naissance"]

    # تجسيد كائن المستخدم (Object Instantiation)
    user1 = User(nom, prenom, email, mot_de_passe, date_naissance)

    # تمرير الكائن كحزمة موحدة إلى القالب
    return render_template("resultat.html", U1=user1)

# إطلاق السيرفر في وضع التنقيح
if __name__ == "__main__":
    app.run(debug=True)
```

---

### ج. واجهة النتيجة الديناميكية: [`templates/resultat.html`](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/Correction%20app%20POO/templates/resultat.html)

يوضح هذا الملف كيفية استهلاك كائن بايثون داخل محرك قوالب Jinja2:

```html
<div class="container">
    <h2>Informations de l'utilisateur</h2>

    <p>
        <strong>Bonjour :</strong>
        {{ U1.get_nom() }} {{ U1.get_prenom() }}
    </p>

    <p>
        <strong>E-mail :</strong>
        {{ U1.get_email() }}
    </p>

    <p>
        <strong>Mot de passe :</strong>
        {{ U1.get_mot_de_passe() }}
    </p>

    <p>
        <strong>Date de naissance :</strong>
        {{ U1.get_date_naissance() }}
    </p>

    <a href="/">Retour au formulaire</a>
</div>
```

---

## 📊 5. مقارنة معمارية مفصلة: التطبيق الإجرائي مقابل التطبيق الكائني

| وجه المقارنة | التطبيق الإجرائي الأولي ([`App1`](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/App1)) | التطبيق كائني التوجه ([`Correction app POO`](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/Correction%20app%20POO)) |
| :--- | :--- | :--- |
| **النمط البرمجي (Paradigm)** | إجرائي تقليدي (*Procedural*) | موجه نحو الكائنات (*Object-Oriented*) |
| **هيكلية البيانات** | متغيرات منفصلة ومبعثرة | كيان موحد ومتماسك ضمن كائن `User` |
| **مبدأ الكبسلة (Encapsulation)** | منعدم؛ المتغيرات نصوص عادية | مطبق بدقة؛ خصائص خاصة محمية بـ `__` |
| **توقيع دالة الإرجاع** | `render_template(..., nom=nom, prenom=prenom, email=email, ...)` | `render_template("resultat.html", U1=user1)` |
| **الاستدعاء داخل القالب** | وصول مباشر للمتغير: `{{ nom }}` | استدعاء دالة الكائن: `{{ U1.get_nom() }}` |
| **التنظيم الموديولي** | كل المنطق داخل ملف `app.py` واحد | فصل طبقة النماذج في `models/user.py` |
| **القابلية للتوسع والصيانة** | منخفضة؛ إضافة حقل جديد تتطلب تغيير التوقيع والقالب | عالية جداً؛ إضافة خاصية جديدة للصنف تتم دون كسر التوقيع |

---

## 🛠️ 6. دليل التثبيت والتشغيل خطوة بخطوة

### 1. إعداد بيئة العمل الافتراضية (Virtual Environment)
في موجه الأوامر (Terminal):

```bash
# الانتقال إلى مجلد التطبيق
cd "TP/Correction app POO"

# إنشاء البيئة الافتراضية
python3 -m venv venv

# تفعيل البيئة (Linux / macOS)
source venv/bin/activate

# أو في نظام ويندوز (PowerShell)
# .\venv\Scripts\activate
```

### 2. تثبيت الحزم المطلوبة
```bash
pip install Flask
```

### 3. إطلاق الخادم المحلي
```bash
python app.py
```
أو عبر أمر فلاسك الرسمي:
```bash
flask --app app run --debug
```

### 4. معاينة التطبيق
افتح المتصفح وتوجه إلى العنوان المحلي:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## ⚠️ 7. دليل حل المشاكل البرمجية الشائعة (Troubleshooting)

### 1. خطأ عدم العثور على الحزمة: `ModuleNotFoundError: No module named 'models'`
- **السبب** : تشغيل `app.py` من مسار خارجي مختلف أو حذف ملف `models/__init__.py`.
- **الحل** : التأكد من الوجود داخل مجلد `Correction app POO` عند تشغيل الأمر، والتحقق من وجود ملف `__init__.py` فارغ داخل مجلد `models/`.

### 2. خطأ القالب المفقود: `TemplateNotFound: inscription.html`
- **السبب** : وجود ملفات الـ HTML بجانب ملف `app.py` فقط دون وضعها داخل مجلد `templates/`.
- **الحل** : التأكد من نسخ ملفات `inscription.html` و `resultat.html` داخل المجلد الفرعي `templates/`.

### 3. خطأ انشغال المنفذ: `Address already in use (Port 5000)`
- **السبب** : وجود سيرفر آخر قيد التشغيل في الخلفية أو خدمة أخرى تحتجز المنفذ 5000.
- **الحل** : تغيير رقم المنفذ في استدعاء الدالة داخل [`app.py`](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/Correction%20app%20POO/app.py#L29):
  ```python
  app.run(debug=True, port=5001)
  ```
  ثم فتح الرابط `http://127.0.0.1:5001`.

---

## 🔗 8. الروابط التوثيقية ذات الصلة

- [📖 النسخة الفرنسية الكاملة لهذا الدليل (README.md)](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/Correction%20app%20POO/README.md)
- [📝 توثيق ورشة العمل 1 في أوبسيديان](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/01_Atelier_1_Installation_Flask_et_Application_Web_POO.md)
- [📓 دفتر العمل التطبيقي التفاعلي (Jupytext)](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/TP1_Installation_Flask_et_Application_Web_POO.ipynb)
- [📁 النسخة الإجرائية الأولية (App1)](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/App1/README.md)
- [📚 درس تذكير بمعماريات الويب والبرمجة كائنية التوجه](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/Cours/01_Rappels_Architectures_Web_et_POO_Python.md)
- [📚 درس معالجة الاستثناءات في بايثون](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/Cours/02_Gestion_des_Exceptions_en_Python.md)
