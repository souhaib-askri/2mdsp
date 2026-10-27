---
title: "ورشة العمل 3: الوراثة في البرمجة كائنية التوجه وتأمين كلمات المرور في Flask"
subject: "Framework web Python"
type: TP
tags:
  - 2mdsp
  - fwp
  - flask
  - poo
  - inheritance
  - security
  - hashing
  - werkzeug
  - tp
date: 2026-10-23
---

# ورشة العمل 3: الوراثة في البرمجة كائنية التوجه وتأمين كلمات المرور في Flask
## (TP 3 : L'Héritage en POO avec Flask & Hachage Sécurisé des Mots de Passe)
**الأستاذ المسؤول: نبيل الخميري (Nabil KHEMIRI)**  
*المعهد العالي للغات المطبقة والإعلامية بباجة — جامعة جندوبة (ISLAIB / 2MDS)*

---

> [!abstract] أهداف الورشة التطبيقية (Objectifs Pédagogiques)
> تركز هذه الورشة العملية (TP 3) على الانتقال من النمذجة الكائنية البسيطة التي درسناها في [[01_Atelier_1_Installation_Flask_et_Application_Web_POO|ورشة العمل الأولى]] إلى المعمارية المتقدمة عبر تحقيق الأهداف التالية:
> 1. **تطبيق مبدأ الوراثة (Inheritance)**: اشتقاق صنف فرعي `Etudiant` يرث الخصائص الأساسية من الصنف الأب `User` ويعيد استخدام الباني عبر الدالة السحرية `super().__init__()`.
> 2. **تأمين بيانات الاعتماد الحساسة (Cryptographic Security)**: حماية كلمات المرور من التخزين الصريح عبر خوارزميات التجزئة التشفيرية المتقدمة في مكتبة `werkzeug.security` (`generate_password_hash` و `check_password_hash`).
> 3. **التكامل مع فلاسك ومحرك Jinja2**: معالجة طلبات الاستمارة `POST /inscription`، وتجسيد الكائن الفرعي، واستدعاء دوال الوصول الموروثة والمخصصة داخل قوالب HTML.
> 4. **المقارنة المعمارية**: بيان الفارق الجوهري بين التمرير الكائني المنظم وتمرير المتغيرات العشوائية المنفصلة.

---

## 1. مخطط معمارية الوراثة وتدفق الطلبات (SVG Architecture Workflow)

![[assets/flask_poo_inheritance_workflow.svg|850]]

> [!info] التحليل المعماري لتدفق البيانات ومخطط الأصناف (Architecture Breakdown):
> 1. **صنف الأساس الأب (Base Class - `models/user.py`)**:
>    - يمثل المستخدم العام للنظام ويحتوي على الخصائص الخاصة المحمية بالكبسلة: `__nom`, `__prenom`, `__email`, `__age`, بالإضافة إلى `__mot_de_passe`.
>    - يُجري الصنف عملية **تجزئة تشفيرية فورية (Instant Hashing)** لكلمة المرور بمجرد تمريرها للباني عبر الدالة `generate_password_hash(mot_de_passe)`، مما يعني أن كلمة المرور الصريحة لا تستقر إطلاقاً في ذاكرة الكائن.
>    - يوفر التابع `verifier_mot_de_passe()` لمطابقة الرموز بأمان دون كشف التجزئة الأصلية.
> 2. **الصنف الفرعي المشتق (Child Class - `models/etudiant.py`)**:
>    - يرث كافة خصائص وتوابع الصنف الأب: `class Etudiant(User)`.
>    - يستدعي باني الصنف الأب لتفويض تهيئة البيانات العامة: `super().__init__(nom, prenom, email, mot_de_passe, age)`.
>    - يضيف خصائص أكاديمية تخصصية خاصة بالطالب: `__niveau` (المستوى الأكاديمي، مثل "2MDS") و `__specialite` (مثل "علوم البيانات").
> 3. **المتحكم ومسار المعالجة (Flask Controller - `app.py`)**:
>    - يستقبل الطلب `POST` القادم من استمارة التسجيل `inscription.html`.
>    - ينشئ كائناً واحداً موحداً: `etudiant1 = Etudiant(...)`.
>    - يمرر الكائن تحت المتغير `E1` مباشرة إلى القالب `resultat.html`.
> 4. **طبقة العرض والتقديم (Jinja2 Template - `resultat.html`)**:
>    - يستدعي القالب توابع القراءة مباشرة: `{{ E1.get_nom() }}`، والخصائص الموروثة، والمستوى التخصصي `{{ E1.get_niveau() }}`، ويعرض التجزئة الآمنة `{{ E1.get_mot_de_passe() }}` لإثبات حماية سرية المستخدم.

---

## 2. النمذجة الكائنية المتقدمة: الوراثة والكبسلة (OOP Inheritance & Encapsulation)

### 2.1 الصنف الأب `User` وحماية كلمة المرور (`models/user.py`)
```python
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, nom, prenom, email, mot_de_passe, age):
        # تغليف الخصائص بحماية خاصة (Private Attributes)
        self.__nom = nom
        self.__prenom = prenom
        self.__email = email
        # التشفير التلقائي لكلمة المرور باستخدام خوارزمية تجزئة قوية
        self.__mot_de_passe = generate_password_hash(mot_de_passe)
        self.__age = age

    # توابع الوصول والقراءة (Getters)
    def get_nom(self):
        return self.__nom

    def get_prenom(self):
        return self.__prenom

    def get_email(self):
        return self.__email

    def get_age(self):
        return self.__age

    def get_mot_de_passe(self):
        return self.__mot_de_passe

    # توابع التعديل (Setters)
    def set_nom(self, nom):
        self.__nom = nom

    def set_prenom(self, prenom):
        self.__prenom = prenom

    def set_email(self, email):
        self.__email = email

    def set_age(self, age):
        self.__age = age

    # دالة التحقق الآمن من كلمة المرور
    def verifier_mot_de_passe(self, mot_de_passe):
        return check_password_hash(self.__mot_de_passe, mot_de_passe)
```

### 2.2 الصنف الابن `Etudiant` واستدعاء `super()` (`models/etudiant.py`)
```python
from models.user import User

class Etudiant(User):
    def __init__(self, nom, prenom, email, mot_de_passe, age, niveau, specialite):
        # استدعاء باني الفئة الأم User لتفويض تهيئة الخصائص الأساسية
        super().__init__(nom, prenom, email, mot_de_passe, age)

        # سمات إضافية خاصة بالطالب
        self.__niveau = niveau
        self.__specialite = specialite

    def get_niveau(self):
        return self.__niveau

    def set_niveau(self, niveau):
        self.__niveau = niveau

    def get_specialite(self):
        return self.__specialite

    def set_specialite(self, specialite):
        self.__specialite = specialite
```

> [!tip] فائدة استخدام `super()`
> تضمن الدالة `super()` عدم تكرار كود الباني التابع للفئة الأم (*DRY - Don't Repeat Yourself*)، كما تدعم معمارية الوراثة المتعددة (*MRO - Method Resolution Order*) في بايثون بكفاءة وتلقائية.

---

## 3. التشفير والتجزئة الأمنية لكلمات المرور (Cryptographic Hashing with Werkzeug)

### 3.1 مخاطر التخزين النصي الصريح (Plaintext Storage Dangers)
> [!danger] فخاخ أمنية فادحة
> - تخزين كلمات المرور كنص صريح (*Plaintext*) في قواعد البيانات أو ملفات السيرفر يُعد جريمة أمنية تقنية؛ ففي حال تسريب قاعدة البيانات أو اختراق جزئي، تنكشف حسابات جميع المستخدمين فوراً.
> - استخدام دوال التجزئة السريعة والقديمة (مثل **MD5** أو **SHA-1**) لم يعد آمناً بسبب سهولة كسرها عبر جداول قوس قزح (*Rainbow Tables*) وحواسيب الهجوم المتوازية (GPUs).

### 3.2 معيار Werkzeug الحديث: `scrypt` و `PBKDF2`
تعتمد مكتبة `Werkzeug` تلقائياً على خوارزمية `scrypt` المقاومة للهجمات المادية والمعتمدة على الذاكرة والوقت:
$$\text{Hash} = \text{scrypt}(\text{Password}, \text{Salt}, N=32768, r=8, p=1)$$

مبنى السلسلة الناتجة:
```text
scrypt:32768:8:1$SaltString$DerivedKeyHash
```
- **الملح العشوائي (Salt)**: يُولد عشوائياً لكل كلمة مرور لمنع هجمات الجداول المسبقة (*Rainbow Tables*).
- **معاملات الصعوبة ($N, r, p$)**: ترفع التكلفة الحسابية وزمن المعالجة على المهاجمين، مما يجعل محاولات التخمين بالقوة الغاشمة (*Brute Force*) شبه مستحيلة عملياً.
- **التحقق الآمن (`check_password_hash`)**: ينفذ مقارنة ذات وقت ثابت (*Constant-Time Comparison*) لمنع هجمات تحليل التوقيت الزمني (*Timing Attacks*).

---

## 4. مسارات خادم فلاسك (`app.py`) وقوالب العرض

### 4.1 شيفرة المتحكم (`app.py`)
```python
from flask import Flask, render_template, request
from models.etudiant import Etudiant

app = Flask(__name__)

@app.route("/")
def inscription():
    # عرض صفحة الاستمارة
    return render_template("inscription.html")

@app.route("/inscription", methods=["POST"])
def traiter_inscription():
    # 1. استخراج المدخلات من الطلب
    nom = request.form["nom"]
    prenom = request.form["prenom"]
    email = request.form["email"]
    mot_de_passe = request.form["mot_de_passe"]
    age = request.form["age"]
    niveau = request.form["niveau"]
    specialite = request.form["specialite"]

    # 2. إنشاء كائن الطالب بتطبيق الوراثة والكبسلة والتشفير
    etudiant1 = Etudiant(nom, prenom, email, mot_de_passe, age, niveau, specialite)

    # 3. تمرير الكائن كحزمة موحدة إلى القالب
    return render_template("resultat.html", E1=etudiant1)

if __name__ == "__main__":
    app.run(debug=True)
```

---

### 4.2 مقارنة تصميم قوالب Jinja2: الكائني مقابل المنفصل

#### القالب الكائني المنظم (`templates/resultat.html`)
```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Données de l'étudiant</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="card">
        <h2>Données de l'étudiant (Modèle POO)</h2>
        <!-- استدعاء دوال الكائن الموروثة والخاصة -->
        <p><strong>Nom :</strong> {{ E1.get_nom() }}</p>
        <p><strong>Prénom :</strong> {{ E1.get_prenom() }}</p>
        <p><strong>Email :</strong> {{ E1.get_email() }}</p>
        <p><strong>Âge :</strong> {{ E1.get_age() }}</p>
        <p><strong>Niveau :</strong> {{ E1.get_niveau() }}</p>
        <p><strong>Spécialité :</strong> {{ E1.get_specialite() }}</p>
        <p><strong>Mot de passe (Haché) :</strong> <br><code>{{ E1.get_mot_de_passe() }}</code></p>
        <br>
        <a href="/">Retour au formulaire</a>
    </div>
</body>
</html>
```

#### القالب التقليدي غير الكائني (`templates/resultat_sans POO.html`)
في النمط غير الكائني، يتشتت المتحكم في استخراج وتمرير متغيرات منفردة:
```python
# كود ضعيف التصميم:
return render_template("resultat_sans POO.html",
                       nom=nom, prenom=prenom, email=email,
                       mdp=mot_de_passe, age=age,
                       niveau=niveau, spec=specialite)
```
> [!warning] عيوب التصميم غير الكائني:
> 1. غياب الكبسلة وحماية الخصائص.
> 2. تضخم معاملات دوال التوجيه (*Long Parameter Lists*).
> 3. صعوبة التوسع عند إضافة خصائص جديدة للمستخدم أو الطالب.
> 4. مرور كلمة المرور كنص صريح غير مشفر إلى واجهة العرض.

---

## 5. تعليمات التشغيل والاختبار العملي

### 5.1 هيكل المجلدات المعتمد
```text
TP3 Héritage/
└── MonProjetFlask/
    ├── app.py
    ├── models/
    │   ├── __init__.py
    │   ├── user.py
    │   └── etudiant.py
    ├── static/
    │   └── style.css
    └── templates/
        ├── inscription.html
        ├── resultat.html
        └── resultat_sans POO.html
```

### 5.2 تشغيل التطبيق
```bash
cd "TP3 Héritage/MonProjetFlask"
python app.py
```
افتح المتصفح على العنوان `http://127.0.0.1:5000/`، وقم بتعبئة بيانات استمارة الطالب والتأكد من ظهور النتيجة مشفرة ومنسقة.

---

## 6. مراجع وروابط المنهج (Wikilinks)
- الدرس التأسيسي الأول: [[01_Rappels_Architectures_Web_et_POO_Python]]
- ورشة التثبيت السابقة: [[01_Atelier_1_Installation_Flask_et_Application_Web_POO]]
- درس إدارة الاستثناءات: [[02_Gestion_des_Exceptions_en_Python]]
- درس الجلسات وإدارة الحالة: [[03_Les_Sessions_avec_Flask]]
- كراس العمل التفاعلي المصاحب: [[TP3_Heritage_POO_et_Securite_Flask]]
