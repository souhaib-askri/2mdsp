---
title: "الفصل 3: إدارة الجلسات في فلاسك (Les sessions avec Flask)"
subject: "Framework web Python"
type: Cours
tags:
  - 2mdsp
  - fwp
  - flask
  - sessions
  - cookies
  - flask-session
  - web-security
date: 2026-10-23
---

# الفصل 3: إدارة الجلسات في فلاسك
## (Chapitre 3 : Les sessions avec Flask)
**الأستاذ المسؤول: نبيل الخميري (Nabil KHEMIRI)**  
*المعهد العالي للغات المطبقة والإعلامية بباجة — جامعة جندوبة (ISLAIB / 2MDS)*

---

> [!abstract] ملخص المحاضرة والأهداف البيداغوجية
> يتناول هذا الفصل دراسة معمارية **إدارة الجلسات وحالة المستخدم (Session Management & State Persistence)** في تطبيقات الويب المبنية بإطار العمل **Flask**. ينطلق الدرس من الإشكالية الجوهرية لبروتوكول الويب **HTTP** بصفته بروتوكولاً عديم الحالة (*Stateless Protocol*)، ويستعرض كيفية توظيف **ملفات تعريف الارتباط (Cookies)** وسيطاً للتواصل، ثم يفصل المعمارية المتقدمة لتخزين الجلسات من جانب الخادم (*Server-Side Sessions*) عبر حزمة **Flask-Session** ونظام الملفات (*Filesystem Storage*)، مع استعراض التطبيق البرمجي الكامل وطرق التأمين ضد الاختراق.

---

## 1. مخطط معمارية تدفق الجلسات وتبادل البيانات (SVG Architecture Workflow)

![[assets/flask_session_workflow.svg|850]]

> [!info] التحليل التفصيلي لمسار تبادل الجلسة بين العميل والخادم (End-to-End Architectural Breakdown):
> 1. **العميل والمتصفح (Web Client & Cookie Jar)**:
>    - يرسل العميل طلباً أولياً (طلب تسجيل الدخول `POST /login` حاملاً بيانات الاعتماد مثل الاسم `name`).
>    - يستقبل المتصفح استجابة الخادم متضمنة ترويسة HTTP الخاصة بزرع الكعكة:  
>      `Set-Cookie: session=s:79bc207ee...; HttpOnly; SameSite=Lax`
>    - يُخزن المتصفح هذا الرمز المشفر محلياً في وعاء الكعكات (*Cookie Jar*) دون أن يعلم محتويات الجلسة الفعلية (مثل الصلاحيات، المعرف الداخلي، إلخ)، مما يحمي خصوصية البيانات ويمنع التلاعب بها (*Client Tampering*).
>    - في كل طلب لاحق (مثل `GET /`)، يرفق المتصفح تلقائياً ترويسة `Cookie: session=...` لتعريف هويته للخادم.
> 2. **خادم التطبيق فلاسك (Flask Application Server - `app.py`)**:
>    - يستقبل الطلب ويتحقق من التوقيع الرقمي للكعكة باستخدام المفتاح السري المشفر `SECRET_KEY`.
>    - في مسار الحماية (*Auth Guard*) لصفحة الاستقبال: إذا لم تتضمن الجلسة المفتاح المطلوبة `session.get("name")`، يُعاد توجيه العميل فوراً إلى `/login`.
>    - عند تسجيل الخروج (`GET /logout`)، ينفذ الخادم الدالة `session.clear()` لحذف البيانات وتحرير الموارد.
> 3. **مستودع التخزين على نظام ملفات الخادم (Server-Side Storage - `flask_session/`)**:
>    - بدلاً من تخزين البيانات داخل كعكة العميل (النمط الافتراضي لفلاسك المقيد بـ 4KB)، تقوم إضافة `Flask-Session` بإنشاء ملف مستقل داخل مجلد `flask_session/` يحمل اسماً مشتقاً من معرّف الجلسة (مثل `79bc207ee04a581ab2...`).
>    - تُخزن البيانات داخل هذا الملف بصيغة تسلسلية ثنائية مشفرة (*Serialized Payload*)، مما يضمن أماناً مطلقاً وسرعة قراءة وكتابة فائقة دون إرهاق حزمة شبكة العميل.

---

## 2. الإشكالية المعمارية: بروتوكول HTTP عديم الحالة (Stateless Protocol)

### 2.1 طبيعة بروتوكول HTTP
صُمم بروتوكول نقل النص الفائق (HTTP) معمارياً وفق مبدأ **انعدام الحالة (Stateless)**:
$$\forall \text{ Request } R_i, \quad \mathcal{P}(R_i \mid R_1, R_2, \dots, R_{i-1}) = \mathcal{P}(R_i)$$
أي أن الخادم يتعامل مع كل طلب $R_i$ ككيان مستقل ومعزول تماماً، دون امتلاك أي ذاكرة تدرك أن الطلب الحالي صادر من نفس المستخدم الذي أرسل الطلب السابق قبل ثانية واحدة.

### 2.2 مفهوم الجلسة (Session Definition)
> [!info] تعريف الجلسة الأكاديمي
> **الجلسة (Session)** هي فترة تفاعل نشطة ومستمرة بين مستخدم (أو تطبيق عميل) ونظام الخادم عبر الزمن. تهدف الجلسة إلى الحفاظ على سياق وبيانات المستخدم عبر عدة طلبات متتالية، مثل:
> - حالة تسجيل الدخول والتوثيق (*Authentication State*).
> - محتويات سلة التسوق (*Shopping Cart*).
> - بيانات الهوية المرجعية (*User ID, Name, Email, Permissions*).

رياضياً، تمثل الجلسة دالة إسناد مستمرة:
$$\mathcal{S}: \text{Session\_ID} \times \text{Key} \longrightarrow \text{Value}$$

---

## 3. ملفات تعريف الارتباط (Cookies): الوسيط المادي للجلسات

### 3.1 ما هو الكعكة (Cookie)؟
ملف تعريف الارتباط (*Cookie*) هو كتلة نصية صغيرة يرسلها خادم الويب ويخزنها متصفح المستخدم على جهاز العميل بصيغة أزواج (مفتاح / قيمة):
$$\text{Cookie} = \langle \text{Name}, \text{Value}, \text{Domain}, \text{Path}, \text{Expires}, \text{Secure}, \text{HttpOnly}, \text{SameSite} \rangle$$

### 3.2 بروتوكول التبادل عبر ترويسات HTTP
1. **أمر الإنشاء من الخادم**:
   ```http
   HTTP/1.1 200 OK
   Content-Type: text/html
   Set-Cookie: session=eyJhbGciOi...; Path=/; HttpOnly; SameSite=Lax
   ```
2. **إرسال الكعكة التلقائي من المتصفح في الطلبات اللاحقة**:
   ```http
   GET /dashboard HTTP/1.1
   Host: localhost:5000
   Cookie: session=eyJhbGciOi...
   ```

> [!tip] أعلام الأمان الحيوية للكعكات (Security Flags)
> - **`HttpOnly`**: يمنع كود JavaScript من قراءة الكعكة (`document.cookie`)، مما يحمي الجلسة من هجمات حقن الشيفرات الخبيثة (**XSS - Cross-Site Scripting**).
> - **`Secure`**: يفرض إرسال الكعكة حصرياً عبر اتصالات **HTTPS** المشفرة لمنع التنصت على الشبكة (**Man-in-the-Middle**).
> - **`SameSite=Lax / Strict`**: يقيد إرسال الكعكة عند التوجيه من مواقع خارجية، مما يُبطل هجمات تزوير الطلبات عبر المواقع (**CSRF - Cross-Site Request Forgery**).

---

## 4. مقارنة معمارية: جلسات Flask الافتراضية مقابل Flask-Session

| وجه المقارنة | جلسات فلاسك الافتراضية (Client-Side Cookies) | جلسات خادم Flask-Session (Server-Side Filesystem) |
| :--- | :--- | :--- |
| **موضع تخزين البيانات** | على متصفح العميل داخل الكعكة المشفرة. | على خادم الويب (داخل مجلد `flask_session/`). |
| **محتوى كعكة المتصفح** | كامل بيانات الجلسة (موقعة رقمياً عبر itsdangerous). | معرّف الجلسة العشوائي فقط (*Session Token ID*). |
| **سعة التخزين القصوى** | محدودة جداً بـ **4 كيلوبايت (4 KB)** وفق معيار المتصفحات. | غير محدودة تقريباً (مرتبطة بسعة القرص الصلب أو خادم Redis). |
| **مستوى الأمان والسرية** | البيانات مقروءة للعميل (Base64) رغم تعذر التعديل. | سرية تامة؛ العميل لا يرى إطلاقاً ما بداخل الجلسة. |
| **حزم البيانات والشبكة** | ثقيلة؛ كل طلب HTTP ينقل كافة بيانات الجلسة ذهاباً وإياباً. | خفيفة جداً؛ ينتقل فقط معرّف الجلسة القصير في الترويسة. |
| **حذف الجلسة وإبطالها** | صعب الإبطال الفوري قبل انتهاء الصلاحية (*No Invalidation*). | فوري بمجرد حذف الملف المقابل من الخادم عبر `session.clear()`. |

---

## 5. دليل التثبيت والتكوين البرمجي (Configuration & Setup)

### 5.1 تثبيت الحزم المطلوبة
في بيئة بايثون الافتراضية المعزولة:
```bash
pip install flask flask-session
# أو عبر مشغل بايثون المباشر:
py -m pip install flask flask-session
```

### 5.2 إعداد التطبيق في كود بايثون (`app.py`)
```python
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
import uuid
import secrets

app = Flask(__name__)

# 1. المفتاح السري لتوقيع الكعكات ومنع التزوير
# secrets.token_hex() يولد قيمة عشوائية تشفيرية عالية الإنتروبيا
app.config["SECRET_KEY"] = secrets.token_hex()

# 2. تحديد مدة بقاء الجلسة: غير دائمة (تنتهي بإغلاق المتصفح)
app.config["SESSION_PERMANENT"] = False

# 3. نمط التخزين من جانب الخادم: ملفات على نظام التشغيل
app.config["SESSION_TYPE"] = "filesystem"

# 4. تفعيل وربط إضافة Flask-Session بالتطبيق
Session(app)
```

> [!warning] المفتاح السري وعمليات إعادة التشغيل (Secret Key Caveat)
> استخدام `secrets.token_hex()` أثناء تشغيل التطبيق في كل مرة يُنشئ مفتاحاً جديداً، مما يؤدي إلى إبطال جلسات المستخدمين الحالية عند إعادة تشغيل الخادم. في بيئات الإنتاج الفعلية (*Production*)، يُحفظ المفتاح السري الثابت داخل متغيرات البيئة:
> ```python
> import os
> app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "fallback-static-key-for-dev")
> ```

---

## 6. التحليل البرمجي المعمق للشيفرة المصدرية (Code Walkthrough)

### 6.1 المتحكم وموجه المسارات (`app.py`)

#### أ. مسار العرض والتحقق من التوثيق (`/`)
```python
@app.route("/")
def index():
    # التحقق من تسجيل الدخول (Authentication Guard)
    if not session.get("name"):
        return redirect("/login")

    # في حال كان المستخدم موثقاً، يتم تمرير المتغيرات لقالب العرض
    return render_template(
        "index.html",
        name=session["name"],
        session_id=session["session_id"]
    )
```

#### ب. مسار تسجيل الدخول المزدوج (`/login`)
يدعم المسار طريقتي `GET` لعرض الاستمارة و `POST` لمعالجة البيانات:
```python
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # استخراج الاسم من حقول الاستمارة وحفظه في الجلسة
        session["name"] = request.form.get("name")

        # إنشاء معرف فريد للجلسة باستخدام خوارزمية UUID v4 لمرة واحدة فقط
        if "session_id" not in session:
            session["session_id"] = str(uuid.uuid4())
        
        # إعادة التوجيه إلى المسار الرئيسي
        return redirect("/")
        
    # إذا كانت طريقة الطلب GET، يتم عرض واجهة التسجيل
    return render_template("login.html")
```

#### ج. مسار إنهاء الجلسة وتسجيل الخروج (`/logout`)
```python
@app.route("/logout")
def logout():
    # تدمير كافة محتويات الجلسة وحذف ملف التخزين المرتبط من الخادم
    session.clear()
    
    # إعادة التوجيه إلى صفحة تسجيل الدخول
    return redirect("/login")
```

---

### 6.2 هيكل القوالب الديناميكية وميراث Jinja2

يعتمد المشروع على مبدأ **وراثة القوالب (Template Inheritance)** لتوحيد تصميم صفحات الموقع:

#### 1. القالب الأساسي (`Templates/layout.html`)
```html
<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta name="viewport" content="initial-scale=1, width=device-width">
        <title>Les sessions avec Flask</title>
    </head>
    <body>
        <!-- كتلة المحتوى الديناميكي التي يتم تعبئتها بواسطة الصفحات الفرعية -->
        {% block content %}
        {% endblock %}
    </body>
</html>
```

#### 2. صفحة تسجيل الدخول (`Templates/login.html`)
```html
{% extends "layout.html" %}

{% block content %}
   <h1>Inscription</h1>
   <form action="/login" method="POST">
      <label><b>Nom : </b></label>
      <input placeholder="Votre nom" type="text" name="name" autofocus required>
      <input type="submit" value="Envoyer">
   </form>
{% endblock %}
```

#### 3. صفحة الاستقبال الرئيسية (`Templates/index.html`)
```html
{% extends "layout.html" %}

{% block content %}
   {% if session.name %}
      <strong>Vous êtes enregistré(e) en tant que : </strong> {{ session.name }}. <br>
      <strong>Votre ID de session est : </strong> {{ session_id }}. <br><br>
      
      <form action="/logout" method="GET">
          <button type="submit">Se déconnecter</button>
      </form>
   {% else %}
      <strong>Vous n'êtes pas enregistré(e). </strong><a href="/login">Login</a>.
   {% endif %}
{% endblock %}
```

---

## 7. آلية تخزين ملفات الجلسة على الخادم (Filesystem Deep-Dive)

عند تشغيل الخادم وتفاعل المستخدم عبر تسجيل الدخول، يُنشئ Flask مجلداً تلقائياً باسم `flask_session/`:

```text
Session/
├── app.py
├── flask_session/
│   └── 79bc207ee04a581ab2348ca1f3494e64cd0ec36128735b8c6bc85ddd8fe1938c
└── Templates/
    ├── index.html
    ├── layout.html
    └── login.html
```

> [!example] فحص ملف الجلسة السيرفري
> - **اسم الملف**: تجزئة تشفيرية بطول 64 خانة ست عشرية (*SHA-256 Hash*) مستمدة من قيمة الـ Session Token.
> - **محتوى الملف**: يحتوي على البيانات المسلسلة لقاموس الجلسة عبر خوارزمية `pickle`:
>   ```python
>   # تمثيل بياني لما يتم تخزينه داخلياً:
>   {
>       'name': 'Souhaib',
>       'session_id': '4f3a9e21-d1c8-472e-9d22-7cb625f38a19'
>   }
>   ```
> - عند استدعاء `session.clear()`، يُحذف الملف المادي مباشرة من القرص الصلب، مما يضمن استحالة إعادة استخدام معرف الجلسة القديم.

---

## 8. تدابير الحماية الأمنية المتقدمة للجلسات (Web Security Best Practices)

1. **تثبيت الجلسات (Session Fixation Defense)**:  
   يجب إعادة توليد معرف الجلسة فور ترقية صلاحيات المستخدم أو نجاح تسجيل الدخول لمنع المهاجم من فرض معرف جلسة مسبق الصنع.
2. **سرقة الجلسات (Session Hijacking Mitigation)**:  
   - تفعيل `SESSION_COOKIE_HTTPONLY = True`.
   - تفعيل `SESSION_COOKIE_SECURE = True` في بيئات الإنتاج.
   - ربط الجلسة بعنوان IP أو بصمة المتصفح (*User-Agent Fingerprinting*).
3. **حماية ملفات الجلسة من التخريب (Storage Permissions)**:  
   يجب ضبط صلاحيات مجلد `flask_session/` على الخادم لتكون مقصورة على مستخدم الخادم فقط (`chmod 700 flask_session`) لمنع قراءتها من مستخدمين محليين آخرين.

---

## 9. روابط ومراجع أكاديمية (Wikilinks)
- المبادئ السابقة: [[01_Rappels_Architectures_Web_et_POO_Python]]
- التعامل مع الأخطاء والاستثناءات: [[02_Gestion_des_Exceptions_en_Python]]
- التطبيق العملي السابق: [[01_Atelier_1_Installation_Flask_et_Application_Web_POO]]
- الورشة التطبيقية للجلسات: [[03_Atelier_Gestion_des_Sessions_Flask]]
- ورشة الوراثة والتأمين: [[02_Atelier_3_Heritage_POO_et_Securite_Flask]]
