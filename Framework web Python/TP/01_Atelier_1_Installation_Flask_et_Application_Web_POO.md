---
title: "ورشة العمل 1: تثبيت Flask وبناء تطبيق ويب تفاعلي بالبرمجة كائنية التوجه (POO)"
subject: "Framework web Python"
type: TP
tags:
  - 2mdsp
  - fwp
  - flask
  - poo
  - tp
  - jinja2
  - forms
  - web-development
date: 2026-10-20
---

# ورشة العمل 1: تثبيت Flask وبناء تطبيق ويب تفاعلي بالبرمجة كائنية التوجه
## (TP 1 : Installation de Flask & Application Web avec Modèle POO)

> [!abstract] أهداف الورشة التطبيقية
> تهدف هذه الورشة العملية (TP1) في مقياس **أطر عمل الويب بايثون (Framework web Python)** إلى تحقيق الآتي:
> 1. إعداد وتكوين بيئة عمل بايثون المعزولة (**Virtual Environment - `venv`**) وتثبيت إطار العمل المصغر **Flask**.
> 2. بناء أول خادم ويب محلي وتفعيل نمط التنقيح التفاعلي (**Debug Mode**).
> 3. إنشاء تطبيق استمارة تسجيل متكامل: استقبال طلبات العرض **HTTP GET** ومعالجة بيانات الاستمارات عبر **HTTP POST**.
> 4. الربط المنهجي بين مبادئ **البرمجة كائنية التوجه (POO)** من [[01_Rappels_Architectures_Web_et_POO_Python|الفصل الأول]] وإطار Flask، عبر نمذجة كائن المستخدم `User` وتغليف بياناته وتمريره إلى محرك القوالب **Jinja2**.
> 5. دمج آليات **معالجة الاستثناءات (Exception Handling)** من [[02_Gestion_des_Exceptions_en_Python|الفصل الثاني]] للتحقق من صحة المدخلات قبل بناء الكائنات.

---

## 1. مخطط المعمارية ومسار الطلب والاستجابة (SVG Architecture Workflow)

![[assets/flask_poo_request_flow.svg|850]]

> [!info] شرح تدفق البيانات في معمارية التطبيق (End-to-End Workflow Breakdown):
> 1. **العميل (Web Browser)**:
>    - يطلب الصفحة الرئيسية عبر المسار `/` (طريقة `GET`)، فيعرض له المتصفح استمارة التسجيل `inscription.html`.
>    - يقوم المستخدم بتعبئة الحقول (الاسم، اللقب، البريد الإلكتروني، كلمة المرور، وتاريخ الميلاد) ثم يضغط على زر "S'inscrire"، مما يولد طلب **HTTP POST** موجهاً إلى المسار `/inscription`.
> 2. **المتحكم وموجه المسارات (Flask Controller - `app.py`)**:
>    - يستقبل الخادم الطلب ويستخرج المدخلات عبر الكائن القاموسي `request.form`.
>    - بدلاً من التشتت في تمرير كل متغير منفصلاً، يقوم المتحكم ببناء كائن مجسد موحد `user1 = User(...)`.
> 3. **نموذج الأعمال الكائني (OOP Model - `models/user.py`)**:
>    - يطبق الصنف مبدأ **الكبسلة (Encapsulation)** بصرامة؛ حيث تُخزن البيانات في خصائص خاصة تبدأ بشرطتين سفليتين (`__nom`, `__email`, إلخ).
>    - يوفر الصنف دوال وصول وقراءة عمومية (`get_nom()`, `get_email()`, إلخ) لحماية البيانات من التعديل غير المشروع.
> 4. **محرك القوالب (Jinja2 Engine - `resultat.html`)**:
>    - يستلم كائن المستخدم `U1=user1`.
>    - يستدعي المحرك توابع الكائن مباشرة داخل وسوم القالب الديناميكية: `{{ U1.get_nom() }}`.
>    - يُولد ملف HTML متكامل ومُنسق بملف الأنماط `style.css`، وتُعاد الاستجابة برمز الحالة **200 OK**.

---

## 2. دليل الإعداد والتثبيت خطوة بخطوة (Guide d'Installation)

### 2.1 التحقق من بيئة بايثون (Vérification de Python)
في موجه الأوامر (Terminal / CMD / PowerShell):
```bash
python --version
# في حال عدم التعرف على الأمر في ويندوز:
py --version
```
> [!warning] إضافة بايثون إلى متغيرات البيئة (PATH)
> إذا ظهرت الرسالة `python n'est pas reconnu`، يجب إعادة تثبيت بايثون مع التأكد التام من تحديد الخيار **"Add Python to PATH"**.

### 2.2 إنشاء مجلد المشروع والبيئة الافتراضية (Virtual Environment)
البيئة الافتراضية تعزل مكتبات المشروع وتمنع تضارب الإصدارات مع المشاريع الأخرى:

```bash
# إنشاء مجلد المشروع والدخول إليه
mkdir MonProjetFlask
cd MonProjetFlask

# إنشاء البيئة الافتراضية باسم venv
python -m venv venv

# تفعيل البيئة الافتراضية
# على ويندوز (CMD / PowerShell):
venv\Scripts\activate

# على أنظمة لينكس / ماك:
source venv/bin/activate
```
*عند تفعيل البيئة بنجاح، ستلاحظ ظهور البادئة `(venv)` في بداية سطر الأوامر.*

### 2.3 تثبيت مكتبة Flask والتحقق من الإصدار
```bash
# ترقية أداة التثبيت pip
python -m pip install --upgrade pip

# تثبيت Flask
python -m pip install Flask

# التحقق من نجاح التثبيت وعرض الإصدار
python -m flask --version
```

---

## 3. الهيكلية المعيارية لمشروع Flask الاحترافي

لضمان عمل التطبيق بسلاسة تامة، يجب تنظيم الملفات وفق الهيكل القياسي التالي:

```text
MonProjetFlask/
│
├── app.py                      # المتحكم الرئيسي ومسارات التطبيق (Routing & Controller)
├── models/                     # حزمة نماذج البيانات كائنية التوجه (OOP Models)
│   ├── __init__.py             # تعريف المجلد كحزمة بايثون
│   └── user.py                 # صنف المستخدم User المغلف بالكامل
│
├── templates/                  # قوالب العرض HTML لمحرك Jinja2
│   ├── inscription.html        # واجهة استمارة التسجيل
│   └── resultat.html           # واجهة عرض نتيجة التسجيل
│
├── static/                     # الملفات الثابتة (CSS, JavaScript, صور)
│   └── style.css               # ورقة الأنماط وتنسيق الاستمارة
│
└── venv/                       # مجلد البيئة الافتراضية المعزولة
```

---

## 4. الكود المصدري والشرح البرمجي المعمق

### 4.1 صنف نموذج المستخدم: `models/user.py`
يطبق هذا الصنف مبدأ **الكبسلة التامة (Full Encapsulation)**؛ حيث تكون كافة الخصائص خاصة (`private`)، ولا يمكن الوصول إليها إلا عبر التوابع العامة (Accessors / Mutators):

```python
class User:
    """
    نموذج المستخدم - كائن مغلف يمثل كيان المستخدم في التطبيق
    """
    # الدالة الإنشائية (Constructeur)
    def __init__(self, nom: str, prenom: str, email: str, mot_de_passe: str, date_naissance: str):
        self.__nom = nom
        self.__prenom = prenom
        self.__email = email
        self.__mot_de_passe = mot_de_passe
        self.__date_naissance = date_naissance

    # Accesseurs & Mutateurs (Getters & Setters)
    def get_nom(self) -> str:
        return self.__nom

    def set_nom(self, nom: str):
        self.__nom = nom

    def get_prenom(self) -> str:
        return self.__prenom

    def set_prenom(self, prenom: str):
        self.__prenom = prenom

    def get_email(self) -> str:
        return self.__email

    def set_email(self, email: str):
        self.__email = email

    def get_mot_de_passe(self) -> str:
        return self.__mot_de_passe

    def set_mot_de_passe(self, mot_de_passe: str):
        self.__mot_de_passe = mot_de_passe

    def get_date_naissance(self) -> str:
        return self.__date_naissance

    def set_date_naissance(self, date_naissance: str):
        self.__date_naissance = date_naissance
```

### 4.2 المتحكم الرئيسي: `app.py`
يقوم بتهيئة تطبيق Flask وربط المسارات (Routes) واستدعاء القوالب:

```python
from flask import Flask, render_template, request
from models.user import User

app = Flask(__name__)

# المسار 1: عرض استمارة التسجيل عند زيارة الصفحة الرئيسية
@app.route("/")
def inscription():
    return render_template("inscription.html")

# المسار 2: استقبال ومعالجة البيانات المرسلة عبر POST
@app.route("/inscription", methods=["POST"])
def traiter_inscription():
    # استخراج الحقول من طلب الاستمارة
    nom = request.form.get("nom", "").strip()
    prenom = request.form.get("prenom", "").strip()
    email = request.form.get("email", "").strip()
    mot_de_passe = request.form.get("mot_de_passe", "")
    date_naissance = request.form.get("date_naissance", "")

    # إنشاء كائن المستخدم POO
    user1 = User(nom, prenom, email, mot_de_passe, date_naissance)

    # تمرير الكائن مباشرة إلى محرك القوالب Jinja2
    return render_template("resultat.html", U1=user1)

# تشغيل الخادم في وضع التطوير
if __name__ == "__main__":
    app.run(debug=True)
```

### 4.3 قالب الاستمارة: `templates/inscription.html`
يحتوي على نموذج HTML يرسل البيانات عبر طريقة `POST` مع ربط ملف التنسيق عبر دالة `url_for`:

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inscription</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <h1>Formulaire d'inscription</h1>
        <form action="/inscription" method="POST">
            <div class="form-group">
                <label for="nom">Nom :</label>
                <input type="text" id="nom" name="nom" required>
            </div>
            <div class="form-group">
                <label for="prenom">Prénom :</label>
                <input type="text" id="prenom" name="prenom" required>
            </div>
            <div class="form-group">
                <label for="email">Adresse e-mail :</label>
                <input type="email" id="email" name="email" required>
            </div>
            <div class="form-group">
                <label for="mot_de_passe">Mot de passe :</label>
                <input type="password" id="mot_de_passe" name="mot_de_passe" required>
            </div>
            <div class="form-group">
                <label for="date_naissance">Date de naissance :</label>
                <input type="date" id="date_naissance" name="date_naissance" required>
            </div>
            <button type="submit">S'inscrire</button>
        </form>
    </div>
</body>
</html>
```

### 4.4 قالب عرض النتيجة: `templates/resultat.html`
يوظف تعبيرات **Jinja2** لاستدعاء دوال الكائن `U1`:

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Résultat de l'inscription</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <h2>Informations de l'utilisateur</h2>
        <p><strong>Bonjour :</strong> {{ U1.get_nom() }} {{ U1.get_prenom() }}</p>
        <p><strong>E-mail :</strong> {{ U1.get_email() }}</p>
        <p><strong>Mot de passe :</strong> {{ U1.get_mot_de_passe() }}</p>
        <p><strong>Date de naissance :</strong> {{ U1.get_date_naissance() }}</p>
        <a href="/">Retour au formulaire</a>
    </div>
</body>
</html>
```

---

## 5. مقارنة معمارية: التطبيق الإجرائي (`App1`) مقابل التطبيق الكائني (`App POO`)

| وجه المقارنة | التطبيق الإجرائي (App1) | التطبيق كائن التوجه (App POO) |
| :--- | :--- | :--- |
| **هيكلية البيانات** | متغيرات متناثرة مبعثرة (`nom`, `prenom`, `email`) | كيان مدمج ومتماسك داخل كائن `User` واحد |
| **تمرير البيانات للقالب** | `render_template(..., nom=nom, prenom=prenom, email=email, ...)` | `render_template(..., U1=user1)` |
| **الكبسلة والحماية** | منعدمة؛ يمكن التلاعب بالقيم في أي مرحلة | تامة؛ الخصائص خاصة ومحمية بدوال الفحص |
| **القابلية للتوسع** | إضافة حقل جديد تتطلب تعديل التوقيع والمتغيرات في كل مكان | تعديل بسيط في الصنف ينعكس تلقائياً على كل الكود |

---

## 6. دليل حل المشاكل الشائعة (Dépannage & Troubleshooting)

1. **انشغال المنفذ 5000 (`Address already in use / Port 5000`)**:
   - يحدث عندما يكون هناك سيرفر قيد التشغيل في الخلفية أو خدمة أخرى تشغل المنفذ (مثل AirPlay على Mac أو خدمة نظام).
   - **الحل**: تغيير رقم المنفذ في الاستدعاء:
     ```python
     app.run(debug=True, port=5001)
     ```
     ثم فتح الرابط `http://127.0.0.1:5001` في المتصفح.

2. **خطأ `TemplateNotFound: inscription.html`**:
   - يحدث إذا تم وضع ملفات الـ HTML بجانب `app.py` دون وضعها داخل مجلد باسم `templates`.
   - **الحل**: التأكد من وضع كافة ملفات الـ HTML داخل مجلد `templates/`.

3. **خطأ `No module named 'models'`**:
   - يحدث عندما يتم استيراد `from models.user import User` دون وجود مجلد `models/` يحتوي على ملف `__init__.py`.
   - **الحل**: إنشاء مجلد `models` ووضع الملفات فيه بصورة مطابقة للمعيار.
