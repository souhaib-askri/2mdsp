---
title: "الفصل 1: تذكير بالمفاهيم الأساسية - معماريات الويب والبرمجة كائنية التوجه في بايثون"
subject: "Framework web Python"
type: Cours
tags:
  - 2mdsp
  - fwp
  - web-framework
  - python
  - poo
  - mvc
  - mvt
  - django
  - flask
  - inheritance
  - abstract-classes
  - interfaces
date: 2026-10-27
---

# الفصل 1: تذكير بالمفاهيم الأساسية - معماريات الويب والبرمجة كائنية التوجه في بايثون
## (Rappel sur les notions de base : Architectures Web & POO en Python)
**الأستاذ المسؤول: نبيل الخميري (Nabil KHEMIRI)**  
*المعهد العالي للغات المطبقة والإعلامية بباجة — جامعة جندوبة (ISLAIB / 2MDS)*

> [!abstract] ملخص المحاضرة والأهداف الأكاديمية
> يمثل هذا الفصل المدخل الأساسي والاستراتيجي لمقياس **أطر عمل الويب بايثون (Framework web Python)**. يهدف الدرس إلى ترسيخ الفهم الهندسي الشامل لكيفية بناء تطبيقات الويب المعاصرة؛ بدءاً من التمييز بين المعمارية الفيزيائية والمنطقية، ومقارنة أنماط التصميم الشهيرة (**MVC** و **MVT**)، وفهم طبقات الـ N-Tiers ومنظومات الويب (Full Stack JS/MERN، Java Servlets/Hibernate، و Django/Flask).
> ثم يقدم الدرس شرحاً تطبيقياً مفصلاً وعميقاً لكافة أركان **البرمجة كائنية التوجه (POO)** في لغة بايثون: الأصناف، الكائنات، الوراثة البسيطة والمتعددة وحل معضلة الألماسة (MRO / C3 Linearization)، أساليب الكبسلة المتقدمة (`_` و `__` و `@property`)، تعدد الأشكال وتجاوز الدوال، والأصناف المجردة والواجهات البرمجية عبر مكتبة `abc`.
> يتضمن هذا المستند **ترجمة وشرحاً كاملاً وتفصيلياً لكافة شرائح المحاضرة الـ 139 بكافة أمثلتها البرمجية وملفاتها المصدرية (`Personne`, `Etudiant`, `Enseignant`, `Employe`, `Professeur`, `InterfaceAffichage`, `Vivant`, `Humain`, `Chat`) دون أي تلخيص**.

---

## 1. مدخل إلى أطر العمل (Qu'est-ce qu'un Framework ?) (Slides 2 - 10)

### 1.1 التعريف الهندسي لإطار العمل (Framework)
**إطار العمل (Framework / « Cadre de travail »)** هو بنية برمجية متكاملة توفر للمطورين هيكلاً معيارياً جاهزاً لتطوير التطبيقات البرمجية بكفاءة وموثوقية، ويتكون جوهرياً من ثلاثة عناصر أساسية:
1. **مجموعة من الأدوات (Outils)**: مولدات الأكواد الآلية (Code Generators)، أدوات التنقيح وتتبع الأخطاء (Debugging Tools)، ومحركات إدارة قواعد البيانات والترحيل (Migrations).
2. **قواعد وتنسيقات موحدة (Règles & Conventions)**: تنظيم قياسي للمجلدات والملفات، معايير لكتابة الشفرات البرمجية، وتطبيق لمبدأ *الاتفاقية تفوق التكوين (Convention over Configuration)*.
3. **مكونات برمجية جاهزة (Composants Logiciels Prêts à l'emploi)**: وحدات المصادقة وإدارة الجلسات (Authentication / Sessions)، أمن التطبيقات (الحماية من هجمات CSRF، XSS، و SQL Injection)، ومحركات التوجيه (Routing).

> [!quote] الغاية المحورية لأطر العمل
> توفير الوقت والجهد عبر تجنب "إعادة اختراع العجلة" (**Don't Repeat Yourself - DRY**)، وضمان قابلية صيانة التطبيق (**Maintainability**)، وقابلية التوسع (**Scalability**) ضمن معايير أمنية صارمة.

---

## 2. المعمارية الفيزيائية مقابل المعمارية المنطقية (Slides 11 - 21)

في هندسة البرمجيات وتطبيقات الويب، يجب الفصل بوضوح بين الكيان المادي الذي يستضيف التطبيق والكيان المنطقي الذي ينظم مسار البيانات والتعليمات البرمجية:

### 2.1 المعمارية الفيزيائية (Architecture Physique / N-Tiers)
تصف المكونات المادية والعتادية (Hardware Infrastructure) والشبكات التي يُنشر عليها النظام البرمجي:
* **طبقة العميل (Client Tier)**: الحواسيب والهواتف الذكية ومتصفحات الويب التي تتصل بالخوادم عبر HTTP.
* **طبقة خادم التطبيقات (Application / Logic Tier)**: خوادم المعالجة المركزية (مثل Nginx, Gunicorn, Apache) التي تشغل بيئة بايثون وتنفذ المنطق البرمجي.
* **طبقة خادم البيانات (Database Tier)**: خوادم قواعد البيانات المخصصة (مثل PostgreSQL, MySQL, MongoDB).

### 2.2 المعمارية المنطقية (Architecture Logique / MVC vs MVT)
تحدد كيفية تنظيم الوحدات البرمجية وتوزيع المسؤوليات داخل الكود المصدري لتحقيق مبدأ **فصل الاهتمامات (Separation of Concerns - SoC)**.

#### مقارنة معمارية: نمط MVC مقابل نمط MVT
| وجه المقارنة | نمط MVC (Model - View - Controller) | نمط MVT (Model - View - Template) |
| :--- | :--- | :--- |
| **البيئة الشائعة** | Spring MVC (Java), Express (Node.js) | **Django** (بايثون)، ومحركات Flask الموجهة بالقوالب |
| **المسؤول عن استلام الطلب** | **المتحكم (Controller)** | **موجه الروابط (URL Router)** |
| **معالجة منطق الأعمال** | المتحكم بالتنسيق مع النموذج (Model) | **العرض (View)** في بايثون |
| **العرض والواجهة** | **العرض (View)** | **القالب (Template)** عبر محركات مثل Jinja2 |
| **إدارة البيانات** | **النموذج (Model)** | **النموذج (Model / ORM)** |

---

### 2.3 مقارنة أطر وتكنولوجيات الويب المعاصرة (Slides 11 - 21)
1. **منظومة جافا المتقدمة (Java Enterprise Stack) (Slides 15 - 17)**:
   * **Servlet**: صنف جافا يعمل في جانب الخادم لمعالجة طلبات HTTP بشكل منخفض المستوى.
   * **Hibernate ORM**: إطار عمل يدير استمرارية البيانات ونقل كائنات جافا إلى جداول علائقية عبر طبقة DAO (Data Access Object).
2. **منظومة جافاسكربت الشاملة (Full Stack JS / MERN) (Slides 12 - 14)**:
   * واجهة أمامية ديناميكية عبر React/Angular، وخلفية عبر Node.js/Express، وقاعدة بيانات مستندية NoSQL (**MongoDB**) تعتمد صيغ BSON/JSON المستندية المرنة.
3. **منظومة بايثون للويب (Django & Flask)**:
   * **Django (Slides 18 - 21)**: معمارية MVT متكاملة توفر أدوات ORM جاهزة، نظام توجيه URLs متقدم، وإدارة قوالب صارمة.
   * **Flask**: إطار عمل مصغر عالي المرونة يعتمد مواصفات WSGI ومحرك قوالب Jinja2.

---

## 3. المخطط التوضيحي لمقارنة معماريات الويب MVC و MVT (SVG Diagram)

![[assets/mvc_vs_mvt_architecture.svg]]

> [!info] شرح المخطط التفصيلي (Architecture Breakdown):
> 1. **الجانب الأيسر (MVC)**: يرسل المتصفح الطلب إلى المتحكم (Controller)، الذي يستدعي النموذج (Model) لجلب البيانات، ثم يمرر النتيجة إلى العرض (View) لتوليد الواجهة.
> 2. **الجانب الأيمن (MVT في Django)**: يستقبل موجه الروابط الطلب، ويوجهه إلى دالة الـ View التي تنفذ منطق الأعمال وتتخاطب مع الـ ORM (Model)، ثم تمرر قاموس السياق إلى القالب (Template) لتصيير الـ HTML النهائي وإعادته للمتصفح.

---

## 4. المفاهيم التأسيسية للبرمجة كائنية التوجه في بايثون (Slides 22 - 60)

### 4.1 الصنف والكائن (Classe & Objet) (Slides 26 - 35)
* **الصنف (Classe)**: قالب أو مخطط عام (Blueprint) يجمع الخصائص (Attributs) والسلوكيات أو الوظائف (Méthodes) في كيان برمجي موحد.
* **الكائن (Objet / Instance)**: تجسيد حي للصنف في الذاكرة. الصنف الواحد يمكن أن يشتق منه عدد غير محدود من الكائنات المستقلة.

```python
class Personne:
    # دالة البناء (Constructeur)
    def __init__(self, nom: str, prenom: str, age: int):
        self.nom = nom        # خاصية نسخة (Instance Attribute)
        self.prenom = prenom
        self.age = age

    # دالة صلبة للكائن (Instance Method)
    def se_presenter(self) -> str:
        return f"Bonjour, je m'appelle {self.prenom} {self.nom} et j'ai {self.age} ans."

p1 = Personne("SALHI", "Farah", 22)
print(p1.se_presenter())
```

---

### 4.2 دورة حياة الكائن والكلمة المفتاحية `self` (Slides 36 - 51)
* **`self`**: مؤشر صريح يشير إلى النسخة الحالية قيد المعالجة في الذاكرة. عند استدعاء `p1.se_presenter()`، يقوم بايثون تلقائياً بتمرير `p1` كوسيط أول للميثود: `Personne.se_presenter(p1)`.
* **دورة حياة الكائن**:
  1. الحجز المبدئي عبر `__new__()`.
  2. التهيئة عبر المشيد `__init__()`.
  3. الاستخدام واستدعاء التوابع.
  4. التدمير وتحرير الذاكرة عبر جامع القمامة وميثود `__del__()` عند وصول عداد المراجع إلى الصفر.

---

## 5. الركن الأول: الكبسلة (Encapsulation) وتطبيقاتها الكاملة (Slides 61 - 69)

### أ. المفهوم النظري (Slides 61 - 63)
* **الكبسلة**: تجميع البيانات والوظائف داخل كبسولة موحدة وحماية الحالة الداخلية من الوصول العشوائي المباشر من الخارج.
* بايثون لا تحتوي على كلمات مفتاحية صلبة مثل `private` في Java، لكنها تتبنى اتفاقيات صارمة:
  * **العام (Public)**: متاح مباشرة (`self.nom`).
  * **المحمي (Protected `_`)**: اتفاقية تفاهم تعني أن الخاصية داخلية (`self._age`).
  * **الخاص وتشويه الأسماء (Private & Name Mangling `__`)**: عند وضع شرطتين سفليتين (`self.__salaire`)، يقوم المترجم بتعديل اسم المتغير داخلياً إلى `_NomClasse__attribut`.

---

### ب. أمثلة الكبسلة الثلاثة من المحاضرة الرسمية (Slides 64 - 69)

#### المثال 1 (`Exemple_v1` - حماية الخاصية والوصول عبر Getters/Setters) (Slides 64 - 65):
```python
# personne.py
class Personne:
    def __init__(self, nom, prenom, age):
        self.nom = nom
        self.prenom = prenom
        self.__age = age  # خاصية خاصة جداً (Private)

    # محدد القراءة (Getter)
    def get_age(self):
        return self.__age

    # محدد التعديل (Setter) مع التحقق من صحة البيانات
    def set_age(self, age):
        if age > 0:
            self.__age = age
        else:
            print("Erreur : L'âge doit être positif !")

# تجربة الكود:
p = Personne("KHEMIRI", "Amira", 29)
print(p.get_age())       # يعرض: 29
p.set_age(30)
print(p.get_age())       # يعرض: 30
# print(p.__age)         # يولد خطأ AttributeError: 'Personne' object has no attribute '__age'
```

#### المثال 2 و 3 (`Exemple_v2` و `Exemple_v3` مع المزخرف `@property`) (Slides 66 - 69):
الأسلوب البايثوني المعاصر الذي يتيح التعامل مع الدوال كخصائص طبيعية:
```python
class Personne:
    def __init__(self, nom, prenom, age):
        self.nom = nom
        self.prenom = prenom
        self.__age = age

    @property
    def age(self):
        """Getter حديث"""
        return self.__age

    @age.setter
    def age(self, nouvelle_valeur):
        """Setter حديث مع فحص منطقي"""
        if nouvelle_valeur > 0:
            self.__age = nouvelle_valeur
        else:
            raise ValueError("L'âge ne peut pas être négatif !")

# main.py (Slide 68 - 69):
p = Personne("ALOUI", "Kais", 30)
print(p.age)      # استدعاء دالة age عبر صيغة الخاصية -> 30
p.age = 31        # استدعاء دالة setter بسلاسة
print(p.age)      # -> 31
```

---

## 6. الركن الثاني: الوراثة والوراثة المتعددة (Inheritance) (Slides 70 - 109)

### أ. الوراثة البسيطة واستدعاء المشيد `super()` (Slides 70 - 93)
* ترث الفئة الفرعية (Classe Fille) كافة خصائص وتوابع الفئة الأم (Classe Mère) باستثناء الخصائص الخاصة (`__`).
* ميثود `super().__init__(...)` تسمح باستدعاء مشيد الصنف الأب دون تكرار كود التهيئة.

#### المثال الشامل 1 (`Exemple_v1` - الأصناف `Personne`, `Etudiant`, `Enseignant`, `main.py`) (Slides 79 - 85):
```python
# personne.py (Slide 80 - 81)
class Personne:
    def __init__(self, nom, prenom, age):
        self.nom = nom
        self.prenom = prenom
        self.age = age

    def affiche(self):
        print(f"Nom : {self.nom} , Prenom : {self.prenom} , age : {self.age}")

# etudiant.py (Slide 82)
from personne import Personne

class Etudiant(Personne):
    def __init__(self, nom, prenom, age, numEtd):
        super().__init__(nom, prenom, age)
        self.numEtd = numEtd

    def affiche(self):
        super().affiche()
        print(f", NumEtd : {self.numEtd}")

# enseignant.py (Slide 83 - 84)
from personne import Personne

class Enseignant(Personne):
    def __init__(self, nom, prenom, age, specialite, grade, salaire):
        super().__init__(nom, prenom, age)
        self.specialite = specialite
        self.grade = grade
        self.salaire = salaire

    def affiche(self):
        super().affiche()
        print(f", specialité : {self.specialite} , grade : {self.grade} , salaire : {self.salaire}")

# main.py (Slide 85)
from etudiant import Etudiant
from enseignant import Enseignant

et1 = Etudiant("ALOUI", "kais", 30, 587)
en1 = Enseignant("KHEMIRI", "Amira", 29, "Informatique", "MA", 2500)

et1.affiche()
# Nom : ALOUI , Prenom : kais , age : 30
# , NumEtd : 587

en1.affiche()
# Nom : KHEMIRI , Prenom : Amira , age : 29
# , specialité : Informatique , grade : MA , salaire : 2500
```

---

### ب. تسلسل البحث عن الدوال ومثال الصنف `Vehicule` و `Voiture` (Slides 92 - 93)
```python
class Vehicule:
    def demarrer(self):
        print("Démarrage du véhicule...")

class Voiture(Vehicule):
    pass

v = Voiture()
v.demarrer()
```
> [!info] قاعدة تسلسل استدعاء الميثود:
> عند استدعاء `v.demarrer()`:
> 1. يبحث بايثون أولاً داخل الصنف المباشر للكائن (`Voiture`).
> 2. إذا لم يجد الدالة فيه، ينتقل بالبحث تلقائياً إلى الصنف الأب (`Vehicule`).

---

### ج. مخطط الأصناف والوراثة البسيطة والمتعددة (Slides 76 - 109)

![[assets/poo_uml_class_hierarchy.svg]]

> [!info] الشرح التفصيلي لمخطط أصناف UML للوراثة البسيطة والمتعددة
> يوضح المخطط الهيكلي بالأعلى نمطي الوراثة المطبقين في المحاضرة:
> 1. **الوراثة الأحادية والتخصيص (Pattern A: Single Inheritance & Specialization)**:
>    - يمثل صنف **`Personne`** الصنف الأب الأساسي (Superclass) الذي يجمع الخصائص العامة المشتركة بين جميع الأفراد (`nom`, `prenom`, `age`) والدالة `affiche()`.
>    - يرث منه صنف **`Etudiant`** ويضيف خاصيته المميزة (`numEtudiant`) مع دالة طباعة مخصصة.
>    - يرث منه صنف **`Enseignant`** ويضيف تفاصيل الرتبة والراتب والتخصص (`specialite`, `grade`, `salaire`).
> 2. **الوراثة المتعددة (Pattern B: Multiple Inheritance)**:
>    - تتيح لغة بايثون للصنف المشتق أن يرث من أكثر من صنف أب في آن واحد.
>    - يرث الصنف المشتق **`Professeur`** من الصنفين الأبوين معاً: **`Personne`** (البيانات الشخصية) و **`Employe`** (البيانات المهنية والمالية: `codeEmp`, `salaire`, `anneeRec`).
>    - يستدعي مشيّد الصنف الابن مشيّدي الفئتين الأبوين معاً لتهيئة كافة الحقول الموروثة بالكامل (`Personne.__init__` و `Employe.__init__`).

#### التطبيق العملي الكامل للوراثة المتعددة (`Héritage multiple_v1` & `v2`):
```python
# meres.py (Slides 96 - 99, 104 - 106)
class Personne:
    def __init__(self, nom, prenom, dateN):
        self.nom = nom
        self.prenom = prenom
        self.dateN = dateN

    def afficherInfos(self):
        print(f"Nom : {self.nom} , Prenom : {self.prenom} , Date naissance : {self.dateN}")

class Employe:
    def __init__(self, codeEmp, salaire, anneeRec):
        self.codeEmp = codeEmp
        self.salaire = salaire
        self.anneeRec = anneeRec

    def afficherInfos(self):
        print(f"Code employé : {self.codeEmp} , Salaire : {self.salaire} , anneeRec : {self.anneeRec}")

# fille.py (Slides 100 - 101, 107 - 108)
class Professeur(Personne, Employe):
    def __init__(self, nom, prenom, dateN, codeEmp, salaire, anneeRec, specialite):
        # استدعاء مشيدي الفئتين الأم صراحة لتفادي الغموض
        Personne.__init__(self, nom, prenom, dateN)
        Employe.__init__(self, codeEmp, salaire, anneeRec)
        self.specialite = specialite

    def afficherInfos(self):
        Personne.afficherInfos(self)
        Employe.afficherInfos(self)
        print(f", Specialite : {self.specialite}")

# main.py (Slide 102, 109)
p1 = Professeur("SOULI", "Slim", "09/10/1985", 123, 1600, 2020, "informatique")
p1.afficherInfos()
# المخرجات:
# Nom : SOULI , Prenom : Slim , Date naissance : 09/10/1985
# Code employé : 123 , Salaire : 1600 , anneeRec : 2020
# , Specialite : informatique
```

---

## 7. الركن الثالث: الأصناف المجردة (Classes Abstraites) (Slides 110 - 119)

### أ. المفهوم النظري (Slides 111 - 112)
* **الصنف المجرد (Classe Abstraite)**: صنف يحتوي على الأقل على دالة مجردة واحدة (**Méthode Abstraite**)؛ وهي دالة يُعلن عن توقيعها واسمها فقط دون كتابة كود تنفيذي لها (`pass`).
* **القاعدة الصارمة**: **الصنف المجرد غير قابل للإنشاء المباشر (Non Instanciable)**! لا يمكن إنشاء كائن منه في الذاكرة عبر `p = Personne(...)`، بل يُستخدم كعقد وقالب للأصناف المشتقة.

---

### ب. التطبيق العملي الكامل وفحص رسالة الخطأ (Slides 114 - 119)
```python
# personne.py (Slide 114)
from abc import ABC, abstractmethod

class Personne(ABC): # الوراثة من ABC تجعل الصنف مجرداً
    def __init__(self, nom, prenom, age):
        self.nom = nom
        self.prenom = prenom
        self.age = age

    @abstractmethod
    def affiche(self):
        """دالة مجردة تفرض على الأبناء تنفيذها"""
        pass

# etudiant.py (Slide 115)
from personne import Personne

class Etudiant(Personne):
    def __init__(self, nom, prenom, age, numEtd):
        super().__init__(nom, prenom, age)
        self.numEtd = numEtd

    def affiche(self):
        print(f"Nom : {self.nom} , Prenom : {self.prenom} , age : {self.age} , NumEtd : {self.numEtd}")

# enseignant.py (Slide 116 - 117)
from personne import Personne

class Enseignant(Personne):
    def __init__(self, nom, prenom, age, specialite, grade, salaire):
        super().__init__(nom, prenom, age)
        self.specialite = specialite
        self.grade = grade
        self.salaire = salaire

    def affiche(self):
        print(f"Nom : {self.nom} , Prenom : {self.prenom} , age : {self.age}")
        print(f", specialité : {self.specialite} , grade : {self.grade} , salaire : {self.salaire}")
```

#### ماذا يحدث عند محاولة إنشاء نسخة من `Personne`؟ (Slide 118):
```python
# main.py
p1 = Personne("SALHI", "Farah", 22)
```
> [!danger] الخطأ التشغيلي من المحاضرة:
> ينهار البرنامج فوراً بالرسالة الموضحة بالشريحة 118:
> `TypeError: Can't instantiate abstract class Personne with abstract method affiche`
> لأن بايثون تمنع منعاً باتاً إنشاء كائنات من الفئات المجردة التي تمتلك ميثود مجردة لم تُنفذ.
> بينما إنشاء كائنات من `Etudiant` و `Enseignant` يعمل بنجاح تام لأنها نفذت الدالة `affiche()`.

---

## 8. الركن الرابع: الواجهات البرمجية (Interfaces) (Slides 120 - 137)

### أ. المفهوم النظري (Slides 121 - 122)
* **الواجهة (Interface)**: هي حالة خاصة ونقية من الأصناف المجردة؛ حيث **لا تحتوي على أي خاصية (Attribut)** و **لا تحتوي على أي دالة منفذة (Pas de méthode concrète)**؛ فجميع دوالها مجردة بنسبة 100%.
* أي صنف يطبق واجهة برمجية يُلزم بتوفير كود تنفيذي لكافة دوال الواجهة دون استثناء.

---

### ب. المثال العملي 1: واجهة العرض (`InterfaceAffichage`) (Slides 123 - 130)
```python
# affichage.py (Slide 125)
from abc import ABC, abstractmethod

class InterfaceAffichage(ABC):
    @abstractmethod
    def affiche(self):
        pass

# personne.py (Slide 126)
class Personne:
    def __init__(self, nom, prenom, age):
        self.nom = nom
        self.prenom = prenom
        self.age = age

# etudiant.py (Slide 127) - وراثة من Personne وتطبيق InterfaceAffichage
from personne import Personne
from affichage import InterfaceAffichage

class Etudiant(Personne, InterfaceAffichage):
    def __init__(self, nom, prenom, age, numEtd):
        super().__init__(nom, prenom, age)
        self.numEtd = numEtd

    def affiche(self):
        print(f"Nom : {self.nom} , Prenom : {self.prenom} , age : {self.age} , NumEtd : {self.numEtd}")

# enseignant.py (Slide 128 - 129)
from personne import Personne
from affichage import InterfaceAffichage

class Enseignant(Personne, InterfaceAffichage):
    def __init__(self, nom, prenom, age, specialite, grade, salaire):
        super().__init__(nom, prenom, age)
        self.specialite = specialite
        self.grade = grade
        self.salaire = salaire

    def affiche(self):
        print(f"Nom : {self.nom} , Prenom : {self.prenom} , age : {self.age} , specialité : {self.specialite} , grade : {self.grade} , salaire : {self.salaire}")

# main.py (Slide 130)
et1 = Etudiant("ALOUI", "kais", 30, 587)
en1 = Enseignant("KHEMIRI", "Amira", 29, "Informatique", "MA", 2500)
et1.affiche()
en1.affiche()
```

---

### ج. المثال العملي 2 الشامل: نمذجة الحياة والموت (`Vivant`, `Humain`, `Chat`) (Slides 131 - 137)
تستعرض الشرائح من 131 إلى 137 تصميماً كاملاً لمحاكاة الكائنات الحية والفرق السلوكي بين الإنسان والقط عبر تعدد الأشكال والواجهات:

1. **الواجهة المجردة `Vivant`**:
   * تُعرف سلوكيات الكائن الحي: `vivre()`, `mourir()`, `est_vivant()`.
2. **الصنف `Humain`**:
   * يمتلك حياة واحدة فقط. عند استدعاء `mourir()` يموت نهائياً، وتفشل أي محاولة لاحقة لإنعاشه (*"L'être humain est mort ! Impossible de réanimer cet Humain il est déjà mort !"*).
3. **الصنف `Chat` (القط ذو السبعة أرواح)**:
   * يمتلك القط مخزوناً من 7 أو 9 أرواح. عند استدعاء `mourir()` ينقص عداد أرواحه بمقدار 1 مع إشعار: (*"Le chat est en train de mourir ! Ce chat est toujours en vie"*). ولا يموت القط فعلياً إلا بعد نفاد كافة أرواحه!

```python
# التنفيذ التفاعلي كما ظهر في مخرجات الشريحة 137:
# Est-il vivant? : True
# L'être humain est mort!
# Impossible de réanimer cet Humain il est déjà mort!
# ------------------------------
# Est-il vivant? : True
# Le chat est en train de mourir!
# Ce chat est toujours en vie.
```

---

## 9. المخطط التوضيحي لأركان البرمجة الكائنية الأربعة (SVG Diagram)

![[assets/python_poo_pillars.svg]]

> [!info] شرح مخطط أركان البرمجة كائنية التوجه:
> يوضح المخطط الهيكلية التكاملية بين الركائز الأربع:
> 1. **الكبسلة**: حماية المتغيرات بـ `__` وتأمينها بالمزخرف `@property`.
> 2. **الوراثة**: إعادة استخدام الكود ودعم الوراثة المتعددة المنضبطة عبر `super()`.
> 3. **تعدد الأشكال**: التعامل مع فئات مختلفة (`Etudiant`, `Enseignant`, `Humain`, `Chat`) عبر واجهة استدعاء موحدة.
> 4. **التجريد والواجهات**: إلزام الهياكل بعقود صارمة باستخدام مكتبة `abc` ومنع إنشاء كائنات ناقصة التنفيذ.
