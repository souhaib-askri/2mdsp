---
title: "الفصل 2: إدارة ومعالجة الاستثناءات في بايثون"
subject: "Framework web Python"
type: Cours
tags:
  - 2mdsp
  - fwp
  - web-framework
  - python
  - exceptions
  - try-except
  - custom-exceptions
date: 2026-10-20
---

# الفصل 2: إدارة ومعالجة الاستثناءات في بايثون
## (La gestion des exceptions en Python)

> [!abstract] ملخص المحاضرة
> يُعنى هذا الفصل بدراسة آليات **إدارة الاستثناءات والأخطاء التشغيلية (Exception Handling)** في لغة بايثون، استناداً إلى المحاضرة المقدمة من الأستاذ **نبيل الخميري (Nabil Khemiri)**. نتناول في هذا الدرس الفارق الجوهري بين الأخطاء اللغوية والاستثناءات البرمجية، ونتعرف على الهيكل الكامل للتحكم `try ... except ... else ... finally`، وكيفية التقاط الاستثناءات المدمجة المحددة، وصولاً إلى بناء واستدعاء **الاستثناءات المخصصة (Custom Exceptions)** عبر الكلمة المفتاحية `raise` لضمان استقرار وتماسك تطبيقات الويب.

---

## 1. الإشكالية البرمجية وأهمية إدارة الاستثناءات في خوادم الويب

في البرمجة التقليدية، عندما يواجه مفسر بايثون تعليمة مستحيلة التنفيذ رياضياً أو منطقياً أثناء وقت التشغيل (Runtime)، يقوم فوراً بـ:
1. إيقاف تنفيذ البرنامج بشكل مفاجئ وفج (Crash).
2. طباعة سجل تتبع تقني طويل (Traceback) في سطر الأوامر.

> [!danger] مخاطر انهيار التطبيق في بيئة الويب
> في خوادم وتطبيقات الويب (مثل خوادم Flask أو Django):
> - انهيار التطبيق يعني حرمان المستخدم من الخدمة وظهور صفحة الخطأ المزعجة **500 Internal Server Error**.
> - طباعة الـ Traceback للمستخدمين الخارجيين يشكل **ثغرة أمنية فادحة (Information Disclosure)** تكشف أسماء الملفات، بنية المجلدات، ومكتبات الخادم للمهاجمين.
> - ترك الاتصالات بقواعد البيانات أو ملفات السيرفر مفتوحة دون إغلاق محكم يسبب تسريب الموارد (Resource Leaks).

لذلك وُجدت آلية **معالجة الاستثناءات** بهدف:
$$\text{الالتقاط (Capter)} \longrightarrow \text{المعالجة (Traiter)} \longrightarrow \text{الإدارة والتعافي (Gérer)}$$

---

## 2. البنية النحوية الشاملة للتحكم في الاستثناءات

تعتمد بايثون على التركيب الرباعي المتكامل:

```python
try:
    # 1. الشيفرة البرمجية الحساسة المعرضة للخطأ (Code protégé)
    ...
except NomException as e:
    # 2. كتلة المعالجة والإنقاذ: تُنفذ حصرياً عند حدوث الخطأ المحدد
    ...
else:
    # 3. كتلة النجاح: تُنفذ حصرياً إذا لم يحدث أي استثناء على الإطلاق
    ...
finally:
    # 4. كتلة التنظيف الإلزامي: تُنفذ دائماً وبشكل مؤكد في كل الأحوال
    ...
```

---

## 3. مخطط مسار تنفيذ معالجة الاستثناءات (SVG Visualization)

![[assets/python_exception_handling_flow.svg|850]]

> [!info] شرح المخطط التفصيلي (Control Flow Breakdown):
> 1. **كتلة التجربة (TRY Block)**: يبدأ المفسر بتنفيذ الأوامر المحمية سطراً بسطر.
> 2. **نقطة اتخاذ القرار (Exception Raised?)**:
>    - **في حال عدم وقوع أي خطأ (NO - Success)**: يتجاهل المفسر جميع كتل `except`، وينتقل مباشرة إلى كتلة `else` لمعالجة النتائج، ثم يختم حتماً بكتلة `finally`.
>    - **في حال وقوع خطأ (YES - Error)**: يتوقف تنفيذ `try` فوراً عند السطر المتسبب بالخطأ، ويتم البحث عن أول كتلة `except` تطابق نوع الاستثناء أو ترث منه. تُنفذ المعالجة البديلة، ثم ينتقل المفسر مباشرة إلى كتلة `finally`.
> 3. **كتلة التنظيف الإلزامي (FINALLY Block)**: محطة إجبارية تضمن تحرير الموارد وغلق الملفات ومقابس الشبكة (Sockets)، قبل استئناف البرنامج لمساره الطبيعي دون توقف الخادم.

---

## 4. دراسة تفصيلية لأمثلة المحاضرة الرسمية

### 4.1 التقاط خطأ القسمة على الصفر (`ZeroDivisionError`)
عند إدخال المستخدم للرقم $0$ كمقام في عملية قسمة:

```python
try:
    nombre = int(input("Entrez un nombre : "))
    resultat = 10 / nombre
    print(f"Résultat : {resultat}")
except ZeroDivisionError:
    print("Erreur : Impossible de diviser par zéro.")
```

### 4.2 التقاط أخطاء متعددة بالترتيب المتخصص (`Multiple Except Blocks`)
إذا أدخل المستخدم نصاً بدلاً من رقم، ستطلق الدالة `int()` استثناء من نوع `ValueError`:

```python
try:
    nombre = int(input("Entrez un nombre : "))
    resultat = 10 / nombre
    print(f"Résultat : {resultat}")
except ZeroDivisionError:
    print("Erreur : Impossible de diviser par zéro.")
except ValueError:
    print("Erreur : Veuillez entrer un nombre entier valide.")
```

### 4.3 إدارة الملفات، كتلة `else`، والتنظيف عبر `finally`
يوضح المثال التالي القراءة الآمنة من ملف محلي مع ضمان غلقه:

```python
try:
    # محاولة فتح ملف للقراءة
    f = open("C:\\Data\\Ex2.txt", "r", encoding="utf-8")
    contenu = f.read()

except FileNotFoundError as e:
    # التقاط خطأ عدم وجود الملف وفحص كائن الخطأ عبر `as e`
    print("Message d'erreur système :", e)

except PermissionError as e:
    # التقاط خطأ الصلاحيات غير الكافية
    print("Erreur de permission :", e)

except Exception as e:
    # صمام أمان عام لالتقاط أي استثناء غير متوقع
    print("Une erreur inattendue est survenue :", e)

else:
    # تُنفذ فقط إذا تم فتح الملف وقراءته بنجاح تام
    print("Lecture réussie :", contenu)

finally:
    # إغلاق الملف بصورة مؤكدة سواء نجحت القراءة أو حدث خطأ
    if 'f' in locals() and not f.closed:
        f.close()
        print("Fermeture sécurisée du descripteur de fichier.")
```

> [!tip] استخدام مديري السياق (Context Managers - `with`)
> في كود بايثون الحديث، يُفضل غالباً استخدام تعليمة `with open(...) as f:` التي تُغلق الملف تلقائياً حتى عند حدوث استثناء، ومع ذلك تظل بنية `finally` هي المعيار الهندسي لإجراء أي تنظيف مخصص لقواعد البيانات وخدمات الشبكة.

---

## 5. الاستثناءات المخصصة في بايثون (Les Exceptions Personnalisées)

في التطبيقات المتقدمة وأطر عمل الويب، لا تكفي الاستثناءات المدمجة للتعبير عن أخطاء منطق العمل (Business Logic Errors)؛ مثل: *عمر غير منطقي للمستخدم*، أو *رصيد بنكي غير كافٍ*، أو *كلمة مرور ضعيفة*.

### 5.1 كيفية إنشاء استثناء مخصص
لإنشاء استثناء جديد، نقوم بإنشاء صنف جديد يرث من الصنف الأساسي `Exception`، ثم نطلق الكائن عند تحقق شرط الخطأ باستخدام الكلمة المفتاحية `raise`.

### 5.2 التطبيق العملي الرسمي: التحقق من صحة العمر في صنف `Personne`

#### النموذج الأول: استثناء مخصص برسالة افتراضية
```python
# تعريف الاستثناء المخصص
class AgeInvalideException(Exception):
    def __init__(self):
        super().__init__("Erreur : l'âge est invalide (ne peut pas être négatif).")

class Personne:
    def __init__(self, nom: str, prenom: str, age: int):
        # التحقق من القيود المنطقية
        if age < 0:
            raise AgeInvalideException()

        self.nom = nom
        self.prenom = prenom
        self.age = age

# تجربة الاستدعاء والالتقاط
try:
    p1 = Personne(nom="Khemiri", prenom="Nabil", age=-10)
    print(p1.nom, p1.prenom, p1.age)
except AgeInvalideException as e:
    print(e)  # يطبع: Erreur : l'âge est invalide (ne peut pas être négatif).
```

#### النموذج الثاني: استثناء مخصص ديناميكي يستقبل معطيات الخطأ
في هذا النموذج، نمرر القيمة غير الصحيحة إلى باني الاستثناء لطباعة رسالة تشخيصية دقيقة:

```python
class AgeInvalideException(Exception):
    def __init__(self, age: int):
        self.age = age
        # تمرير رسالة مخصصة تتضمن القيمة المدخلة
        super().__init__(f"Erreur : l'âge '{age}' est invalide (l'âge doit être compris entre 0 et 120).")

class Personne:
    def __init__(self, nom: str, prenom: str, age: int):
        if age < 0 or age > 120:
            raise AgeInvalideException(age)

        self.nom = nom
        self.prenom = prenom
        self.age = age

# اختبار إنشاء كائن بقيمة غير مسموحة
try:
    p2 = Personne(nom="Khemiri", prenom="Nabil", age=150)
    print(p2.nom, p2.prenom, p2.age)
except AgeInvalideException as e:
    print(e)  # يطبع: Erreur : l'âge '150' est invalide (l'âge doit être compris entre 0 et 120).
```

---

## 6. الربط مع بيئة تطوير تطبيقات الويب (Flask Web Integration)

في أطر الويب مثل **Flask**، تُترجم معالجة الاستثناءات إلى ردود استجابة مهيكلة (HTTP Error Responses):

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

# معالج مخصص لأخطاء التحقق
@app.errorhandler(AgeInvalideException)
def handle_invalid_age(error):
    response = jsonify({
        "status": "error",
        "error_type": "AgeValidationFailed",
        "message": str(error)
    })
    response.status_code = 400  # Bad Request
    return response
```

---

## 7. خلاصة القواعد الذهبية للتعامل مع الاستثناءات

1. **كن محدداً في الاستثناءات**: تجنب تماماً استخدام `except:` الفارغة أو التقاط `Exception` العامة في البداية؛ بل التقط دائماً النوع الدقيق للخطأ (`ValueError`, `FileNotFoundError`).
2. **استخدم `as e` للتشخيص**: احتفظ بكائن الخطأ لتوثيقه في سجلات الخادم (Logging).
3. **لا تكتم الأخطاء بصمت**: تجنب كتابة `except: pass`؛ لأنها تخفي الأخطاء وتجعل تتبع الأعطال شبه مستحيل.
4. **فصل منطق النجاح عن التنظيف**: استخدم `else` لما يجب أن يعمل بعد النجاح فقط، واستخدم `finally` لما يجب أن يعمل دائماً.
5. **اربط الاستثناءات بالتحقق من المدخلات**: في تطبيقات الويب، استخدم الاستثناءات المخصصة لحماية سلامة الكائنات ونماذج البيانات قبل حفظها.
