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
date: 2026-10-20
---

# الفصل 1: تذكير بالمفاهيم الأساسية - معماريات الويب والبرمجة كائنية التوجه في بايثون
## (Rappel sur les notions de base : Architectures Web & POO en Python)

> [!abstract] ملخص المحاضرة
> يُشكل هذا الفصل المدخل الأساسي والاستراتيجي لمقياس **أطر عمل الويب بايثون (Framework web Python)** تحت إشراف الأستاذ **نبيل الخميري (Nabil Khemiri)**. يهدف الدرس إلى ترسيخ المفاهيم الهندسية التأسيسية التي تُبنى عليها تطبيقات الويب المعاصرة؛ بدءاً من التمييز بين المعمارية الفيزيائية والمنطقية، وفحص أنماط التصميم الشهيرة مثل **MVC** و **MVT**، وصولاً إلى تعميق شامل وعملي لمبادئ **البرمجة كائنية التوجه (POO)** في بايثون (الأصناف، الكائنات، الوراثة البسيطة والمتعددة، الكبسلة، تعدد الأشكال، الأصناف المجردة، والواجهات).

---

## 1. مدخل إلى أطر العمل (Qu'est-ce qu'un Framework ?)

### 1.1 التعريف الهندسي
**إطار العمل (Framework / « Cadre de travail »)** هو بنية برمجية متكاملة توفر للمطورين هيكلاً معيارياً جاهزاً لتطوير التطبيقات البرمجية بكفاءة وموثوقية، ويتكون جوهرياً من ثلاثة عناصر أساسية:
1. **مجموعة من الأدوات (Outils)**: مولدات الأكواد الآلية (Code Generators)، أدوات التنقيح وتتبع الأخطاء (Debugging Tools)، ومحركات إدارة قواعد البيانات والترحيل (Migrations).
2. **قواعد وتنسيقات موحدة (Règles & Conventions)**: تنظيم قياسي للمجلدات والملفات، معايير لكتابة الشفرات البرمجية، وتطبيق لمبدأ *الاتفاقية تفوق التكوين (Convention over Configuration)*.
3. **مكونات برمجية جاهزة (Composants Logiciels Prêts à l'emploi)**: وحدات المصادقة وإدارة الجلسات (Authentication / Sessions)، أمن التطبيقات (الحماية من هجمات CSRF، XSS، و SQL Injection)، ومحركات التوجيه (Routing).

> [!quote] الغاية المحورية لأطر العمل
> توفير الوقت والجهد عبر تجنب "إعادة اختراع العجلة" (Don't Repeat Yourself - DRY)، وضمان قابلية صيانة التطبيق (Maintainability)، وقابلية التوسع (Scalability) ضمن معايير أمنية صارمة.

---

## 2. المعمارية الفيزيائية مقابل المعمارية المنطقية (Architecture Physique vs Logique)

في هندسة البرمجيات وتطبيقات الويب، يجب الفصل بوضوح بين الكيان المادي الذي يستضيف التطبيق والكيان المنطقي الذي ينظم مسار البيانات والتعليمات البرمجية:

### 2.1 المعمارية الفيزيائية (Architecture Physique / Technique)
تصف المكونات المادية والعتادية (Hardware Infrastructure) والشبكات التي يُنشر عليها النظام البرمجي. من أبرز نماذجها:
* **المعمارية متعددة الطبقات (Architecture N-Tiers)**:
  - **طبقة العميل (Client Tier / Presentation Hardware)**: الحواسيب والهواتف الذكية ومتصفحات الويب التي تتصل بالخوادم.
  - **طبقة خادم التطبيقات (Application / Logic Tier)**: خوادم المعالجة المركزية (مثل خوادم Nginx, Gunicorn, Apache) التي تشغل بيئة بايثون وتنفذ المنطق البرمجي.
  - **طبقة خادم البيانات (Database Tier)**: خوادم قواعد البيانات المخصصة (مثل PostgreSQL, MySQL, MongoDB).

### 2.2 المعمارية المنطقية (Architecture Logique / Conceptuelle)
تحدد كيفية تنظيم الوحدات البرمجية وتوزيع المسؤوليات داخل الكود المصدر (Design Patterns)، بغض النظر عن عدد الخوادم الفيزيائية التي سيعمل عليها الكود. الهدف منها هو تحقيق **فصل الاهتمامات (Separation of Concerns - SoC)**.

---

## 3. مقارنة معماريات تطبيقات الويب: نمط MVC مقابل نمط MVT

تعتمد معظم أطر عمل الويب على توزيع المهام وفق نماذج تصميم محددة:

| وجه المقارنة | نمط MVC (Model - View - Controller) | نمط MVT (Model - View - Template) |
| :--- | :--- | :--- |
| **البيئة الشائعة** | Spring MVC (Java), Ruby on Rails, Express (Node.js) | Django (بايثون)، ومحركات Flask الموجهة بالقوالب |
| **المسؤول عن استلام الطلب** | **المتحكم (Controller)**: يستقبل طلبات HTTP مباشرة | **موجه الروابط (URL Router)**: يوجه الطلب للـ View المناسبة |
| **معالجة منطق الأعمال (Business Logic)** | يتولى المتحكم التنسيق مع النموذج (Model) وتحديد المخرجات | تتولاه **العرض (View)**؛ حيث تستدعي النماذج وتمرر السياق |
| **العرض والواجهة (UI Rendering)** | تتولاه **العرض (View)** لتوليد واجهة المستخدم | يتولاه **القالب (Template)** عبر محركات مثل Jinja2 أو DTL |
| **إدارة البيانات (Data Layer)** | **النموذج (Model)**: كائنات الأعمال والاتصال بقواعد البيانات | **النموذج (Model)**: تعريف الجداول عبر الـ ORM والاتصال بقواعد البيانات |

---

## 4. مخطط مقارنة معماريات MVC و MVT (SVG Visualization)

![[assets/mvc_vs_mvt_architecture.svg|850]]

> [!info] شرح المخطط التفصيلي (Architecture Breakdown):
> 1. **الجانب الأيسر (MVC Architecture)**:
>    - يرسل العميل (المتصفح) طلب HTTP Request إلى **المتحكم (Controller)**.
>    - يُعد المتحكم هو "دماغ" المنظومة، حيث يستدعي **النموذج (Model)** لجلب البيانات أو تحديث حالة قاعدة البيانات.
>    - يقوم النموذج بإرجاع البيانات المعالجة إلى المتحكم، الذي يختار بدوره **العرض (View)** المناسبة، لتقوم العرض بإنشاء صفحة الـ HTML وإعادتها للعميل.
> 2. **الجانب الأيمن (MVT Architecture في Django وبايثون)**:
>    - يستقبل إطار العمل الطلب، ويحدد مسار التوجيه (URL Routing) الدالّة المسؤولة التي تمثل **العرض (View)**.
>    - تقوم الـ View في بايثون بدور المتحكم؛ فهي تتواصل مع **النموذج (Model / ORM)** لإجراء العمليات الحسابية والاستعلامية.
>    - تقوم الـ View بتجهيز كائن السياق (Context Dictionary) وتمريره إلى **القالب (Template)**.
>    - يقوم القالب (ملف HTML مدمج مع وسوم Jinja2/DTL) بتصيير البيانات في صيغة HTML نهائية وإرجاعها للمتصفح.

---

## 5. نظرة عامة على تطور أطر الويب ومحركات العرض

استعرض الفصل تطور منظومات البرمجة عبر مختلف الأنظمة:
1. **منظومة جافا المتقدمة (Java Enterprise Stack)**:
   - **الخادم الصغير (Servlet)**: فئة جافا تعمل في جانب الخادم (Server-side) لمعالجة طلبات HTTP بشكل منخفض المستوى.
   - **صفحات جافا (JSP - JavaServer Pages)**: خلط كود جافا داخل وسوم HTML للعرض الديناميكي.
   - **أطر الربط العلائقي للكائنات (Hibernate ORM)** وكائنات الوصول للبيانات (**DAO - Data Access Objects**).
2. **منظومة جافاسكربت الشاملة (Full Stack JS / MERN)**:
   - واجهة أمامية ديناميكية عبر React/Vue، وخلفية عبر Node.js/Express، وقاعدة بيانات مستندية غير علائقية NoSQL (مثل **MongoDB** التي تعتمد صيغة BSON/JSON).
3. **منظومة بايثون للويب (Python Web Stack)**:
   - **Django**: إطار عمل متكامل وشامل (Batteries-Included) يعتمد نمط MVT ونظام ORM صارم ولوحة تحكم تلقائية (Admin Panel).
   - **Flask**: إطار عمل مصغر فائق المرونة (Microframework) يعتمد مواصفات WSGI، محرك القوالب Jinja2، ومكتبة Werkzeug للتوجيه.

---

## 6. البرمجة كائنية التوجه في بايثون (POO en Python)

تُعد لغة بايثون لغة كائنية التوجه بالكامل؛ ففي بايثون **كل شيء هو كائن (Everything is an object)**.

### 6.1 المفاهيم الجوهرية: الصنف والكائن (Classe & Objet)
* **الصنف (Classe)**: قالب أو مخطط عام (Blueprint) يجمع الخصائص (Attributs) والسلوكيات أو الوظائف (Méthodes) في كيان برمجي موحد.
* **الكائن أو النسخة (Objet / Instance)**: تجسيد حي للصنف في الذاكرة. الصنف الواحد يمكن أن يشتق منه عدد غير محدود من الكائنات المستقلة.

```python
# تعريف صنف يمثل مستخدماً
class Personne:
    # دالة البناء (Constructeur)
    def __init__(self, nom: str, prenom: str, age: int):
        self.nom = nom        # خاصية نسخة (Instance Attribute)
        self.prenom = prenom
        self.age = age

    # دالة صلبة للكائن (Instance Method)
    def se_presenter(self) -> str:
        return f"Bonjour, je m'appelle {self.prenom} {self.nom} et j'ai {self.age} ans."

# إنشاء نسخ (Instanciation)
p1 = Personne("ABIDI", "Rania", 21)
p2 = Personne("KHEMIRI", "Nabil", 40)
print(p1.se_presenter())
```

### 6.2 دورة حياة الكائن والكلمة المفتاحية `self`
تمر دورة حياة الكائن بثلاث مراحل متتالية:
1. **الإنشاء والتهيئة (Instanciation & Initialisation)**:
   - تبدأ باستدعاء ميثود الحجز المدمجة `__new__()`، يليها فوراً استدعاء **الدالة الإنشائية (Constructeur)** `__init__(self, ...)`.
   - **الكلمة `self`**: هي مؤشر صريح يشير إلى النسخة الحالية قيد المعالجة في الذاكرة (Current Instance Reference). عند استدعاء `p1.se_presenter()`، يقوم بايثون تلقائياً بتمرير `p1` كوسيط أول للميثود: `Personne.se_presenter(p1)`.
2. **الاستخدام (Utilisation)**: استدعاء التوابع وقراءة وتعديل الخصائص.
3. **التدمير وتحرير الذاكرة (Destruction & Garbage Collection)**:
   - يتم تدمير الكائن تلقائياً عندما ينعدم عدد المؤشرات المرجعية المشيرة إليه (Reference Count = 0).
   - توفر بايثون التابع `__del__(self)` لتنفيذ مهام ختامية (مثل إغلاق الاتصالات بالملفات أو الشبكة) قبل الحذف النهائي من الذاكرة.

### 6.3 متغيرات ودوال الأصناف (Variables et Méthodes de Classe)
* **متغير الصنف (Class Variable)**: متغير يُعرّف خارج الدوال داخل الصنف ويكون مشتركاً بين جميع الكائنات المشتقة (يُخزن في مساحة اسم الصنف نفسه).
* **دوال الصنف والمجاميع الثابتة**:
  - `@classmethod`: تأخذ الوسيط الأول `cls` المشير إلى الصنف ككل، وتُستخدم كدوال بناء بديلة (Factory Methods).
  - `@staticmethod`: دالة مستقلة لا ترتبط لا بـ `self` ولا بـ `cls`، وتوضع داخل الصنف لغرض تنظيمي منطقي.

```python
class Compteur:
    nb_instances = 0  # متغير صنف مشترك

    def __init__(self):
        Compteur.nb_instances += 1

    @classmethod
    def total_crees(cls):
        return f"Nombre total d'objets créés : {cls.nb_instances}"

    @staticmethod
    def valider_valeur(val: int) -> bool:
        return val >= 0
```

---

## 7. أركان البرمجة كائنية التوجه الأربعة في بايثون

![[assets/python_poo_pillars.svg|850]]

> [!info] شرح أركان البرمجة الكائنية الأربعة (POO Pillars Explained):
> 1. **الكبسلة (Encapsulation)**: عزل البيانات الداخلية للكائن ومنع التعديل العشوائي عليها، واستخدام الاتفاقيات (`_` و `__`) وآليات الوصول المنضبطة.
> 2. **الوراثة (Inheritance)**: إعادة استخدام الشيفرات عبر علاقة الصنف الأب (Classe Mère) والصنف الابن (Classe Fille) مع دعم الوراثة المتعددة.
> 3. **تعدد الأشكال (Polymorphism)**: القدرة على التعامل مع كائنات مختلفة من خلال واجهة موحدة، عبر إعادة تعريف الدوال (Method Overriding) وخاصية الكتابة البطيّة (Duck Typing).
> 4. **التجريد (Abstraction)**: إخفاء التفاصيل التنفيذية المعقدة وإلزام الأصناف الفرعية بتطبيق عقود وواجهات وظيفية محددة باستخدام وحدة `abc`.

---

### 7.1 الركن الأول: الكبسلة في بايثون (Encapsulation)

في لغات مثل C++ أو Java، تُفرض الكبسلة عبر الكلمات المفتاحية (`public`, `protected`, `private`). أما في بايثون، فالفلسفة مبنية على مقولة غيدو فان روسوم: *"نحن جميعاً بالغون وواعون هنا (We are all consenting adults here)"*. ومع ذلك، تطبق بايثون نظاماً دقيقاً:

1. **الخصائص العامة (Attributs Publics)**: متاحة للقراءة والكتابة من أي مكان (`self.nom`).
2. **الخصائص المحمية (Attributs Protégés - Convention `_`)**: تبدأ بشرطة سفلية واحدة (`self._solde`). هي مجرد اتفاقية تحذيرية تعني "هذا العنصر داخلي، لا تعدله مباشرة من خارج الصنف".
3. **الخصائص الخاصة وتشويه الأسماء (Attributs Privés & Name Mangling - `__`)**:
   - عند بدء اسم الخاصية بشرطتين سفليتين (مثل `self.__mot_de_passe`)، تقوم بايثون بتغيير اسمها داخلياً في جدول الرموز ليصبح:
     $$\text{\_NomDeClasse\_\_attribut}$$
   - هذا التشويه يمنع الوصول العرضي المباشر ويحمي الخاصية من التضارب عند الوراثة.

#### استخدام ممتلكات بايثون (Les Propriétés - `@property`)
تتيح بايثون المزخرف `@property` للجمع بين أمان الكبسلة وسلاسة القراءة:

```python
class CompteBancaire:
    def __init__(self, titulaire: str, solde_initial: float):
        self.titulaire = titulaire
        self.__solde = solde_initial  # خاصية خاصة جداً

    # Getter الكلاسيكي
    def get_solde(self) -> float:
        return self.__solde

    # Setter الكلاسيكي مع التحقق
    def set_solde(self, nouveau_solde: float):
        if nouveau_solde >= 0:
            self.__solde = nouveau_solde
        else:
            raise ValueError("Le solde ne peut pas être négatif !")

    # الأسلوب المعاصر والاحترافي في بايثون (Pythonic Property)
    @property
    def solde(self) -> float:
        """Accesseur moderne"""
        return self.__solde

    @solde.setter
    def solde(self, montant: float):
        """Mutateur moderne avec contrôle strict"""
        if montant < 0:
            raise ValueError("Montant invalide !")
        self.__solde = montant
```

---

### 7.2 الركن الثاني: الوراثة والوراثة المتعددة (Héritage & Héritage Multiple)

#### الوراثة البسيطة واستدعاء الدالة `super()`
ترث الفئة الفرعية جميع خصائص وتوابع الفئة الأم المتاحة، وتستخدم الدالة `super()` لتمرير التعليمات الإنشائية للأب:

```python
class Personne:
    def __init__(self, nom: str, prenom: str):
        self.nom = nom
        self.prenom = prenom

    def afficher(self):
        print(f"Nom : {self.nom}, Prénom : {self.prenom}")

class Etudiant(Personne):
    def __init__(self, nom: str, prenom: str, filiere: str):
        super().__init__(nom, prenom)  # استدعاء دالة بناء الفئة الأم
        self.filiere = filiere

    def afficher(self):
        super().afficher()  # إعادة استخدام عرض الأب
        print(f"Filière : {self.filiere}")
```

#### الوراثة المتعددة وترتيب استدعاء الميثود (MRO - Method Resolution Order)
تدعم بايثون وراثة الصنف لعدة فئات آباء في آن واحد:
$$\text{class Professeur(Personne, Employe):}$$
لتفادي معضلة الألماسة (Diamond Problem)، تستخدم بايثون خوارزمية **C3 Linearization** لتحديد أولويات البحث في شجرة الوراثة، ويمكن فحصها عبر:
```python
print(Professeur.__mro__)
```

---

### 7.3 الركن الثالث: تعدد الأشكال (Polymorphisme)

تعدد الأشكال هو قدرة كائنات تنتمي لأصناف مختلفة على الاستجابة لنفس استدعاء التابع بطرق مخصصة:
1. **إعادة تعريف التوابع (Method Overriding)**: تعيد الفئة الفرعية كتابة محتوى تابع موروث من الفئة الأم.
2. **الكتابة البطيّة (Duck Typing)**:
   > "إذا كان يمشي كالبطة، ويصدر صوتاً كالبطة، فهو بطة."
   في بايثون، لا يشترط أن تنتمي الكائنات لنفس شجرة الوراثة؛ يكفي أن تحتوي على الميثود المطلوبة ليتم استدعاؤها بأمان.

---

### 7.4 الركن الرابع: الأصناف المجردة والواجهات (Classes Abstraites & Interfaces)

تُستخدم الأصناف المجردة لفرض بنية موحدة ومنع إنشاء نسخ ناقصة مباشرة. يتم تحقيق ذلك بالاعتماد على وحدة `abc` (Abstract Base Classes):

```python
from abc import ABC, abstractmethod

# صنف مجرد يعمل كواجهة (Interface)
class InterfaceServiceWeb(ABC):

    @abstractmethod
    def authentifier(self, token: str) -> bool:
        """Méthode abstraite obligatoire"""
        pass

    @abstractmethod
    def traiter_requete(self, data: dict) -> dict:
        """Doit impérativement être implémentée par les classes filles"""
        pass

class ServiceClient(InterfaceServiceWeb):
    def authentifier(self, token: str) -> bool:
        return token == "SECRET_TOKEN_2MDSP"

    def traiter_requete(self, data: dict) -> dict:
        return {"status": "success", "result": f"Traitement de {data}"}
```

> [!danger] محاولة استنساخ صنف مجرد
> إذا حاولت استدعاء `s = InterfaceServiceWeb()` مباشرة، سيقوم مفسر بايثون بإطلاق الخطأ التالي:
> `TypeError: Can't instantiate abstract class InterfaceServiceWeb without an implementation for abstract methods...`

---

## 8. ملخص ومكتسبات الفصل (Conclusion & Transition)

* توفر أطر عمل بايثون (Frameworks Web) مثل **Django** و **Flask** طبقة حماية وتنظيم هندسي متقدم عبر تطبيق أنماط معمارية مفصولة المسؤوليات (**MVT / MVC**).
* يشكل التمكن الصارم من آليات بايثون كائنية التوجه (POO)؛ لاسيما **الكبسلة مع الدوال الخاصة `__`**، و**الوراثة مع `super()`**، و**تعدد الأشكال**، الحجر الأساس لبناء نماذج البيانات (Models) والخدمات الخلفية.
* يمهد هذا الإتقان للانتقال المباشر إلى [[02_Gestion_des_Exceptions_en_Python|الفصل الثاني: إدارة ومعالجة الاستثناءات في بايثون (La gestion des exceptions)]] لضمان متانة الكود وموثوقيته.
