---
title: "TD 1: البيرسبترون البسيط وتصنيف أرقام MNIST (Perceptron Simple)"
subject: "Large Language Models"
type: TD
tags:
  - 2mdsp
  - llm
  - deep-learning
  - perceptron
  - mnist
  - tensorflow
  - keras
date: 2026-10-13
---

# الأعمال الموجهة 1: البيرسبترون البسيط وتصنيف أرقام MNIST (TD 1 - Perceptron Simple)

> [!abstract] بطاقة العمل الموجه (TD Overview)
> * **المادة الدراسية**: نماذج اللغة الكبيرة (Large Language Models - LLM).
> * **الأستاذ المشرف**: د. قيس الزمالي (**Dr. K. EZZAMELI**).
> * **الموضوع**: الجزء الأول: بناء وتدريب بيرسبترون بسيط (Partie 1: Perceptron simple) للتعرف على الأرقام المكتوبة بخط اليد باستخدام إطار العمل **TensorFlow / Keras**.
> * **الهدف البيداغوجي**: فهم اللبنة الأساسية للشبكات العصبية الاصطناعية (Artificial Neural Networks)، والتحويل الخطي واللاخطي، قبل الانتقال إلى البنى المتقدمة مثل الشبكات متعددة الطبقات (MLP) والترانسفورمرز (Transformers) التي تشكل أساس نماذج اللغة الكبيرة (LLMs).

> [!example] الشريحة الأصلية للدرس (Original Slide Capture)
> ![[assets/slide_perceptron_simple.png|500]]

---

## 1. نص المطلوب كاملاً (Énoncé de l'Exercice)

تتضمن الشريحة الدراسية 6 خطوات منهجية لإعداد ومعالجة البيانات وبناء النموذج العصبي:

| الرقم | المطلوب بالفرنسية (Texte Original) | الترجمة الدقيقة والمفهوم البرمجي |
| :---: | :--- | :--- |
| **1** | **Charger le jeu de données mnist à partir de keras.datasets de la bibliothèque tensorflow en utilisant load_data(). Sauvegarder les données chargées dans (x_train, y_train) et (x_test, y_test).** | **تحميل قاعدة بيانات MNIST**: استيراد مجموعة البيانات من وحدة `keras.datasets` باستخدام الدالة `load_data()` وحفظها في أربعة متغيرات تمثل حزمتي التدريب والاختبار. |
| **2** | **Choisir une image, l'afficher en utilisant matshow de matplotlib.pyplot et afficher ses dimensions.** | **معاينة بصرية للصورة**: اختيار عينة من الصور، واستعراضها بصرياً عبر دالة `matshow()` من مكتبة `matplotlib.pyplot`، وطباعة أبعادها المصفوفية (`shape`). |
| **3** | **Normaliser la base de donnée en divisant x_train et x_test sur 255 pour obtenir dans chaque image des valeurs entre 0 et 1.** | **تطبيع البيانات (Normalization)**: قسمة مصفوفات بكسلات التدريب والاختبار على $255$ لحصر قيم الإضاءة داخل المجال $[0.0, 1.0]$. |
| **4** | **Modifier les dimensions de x_train et x_test pour les adapter au modèle en utilisant la fonction reshape. Selon la taille des images :**<br>`x_train_flatten = x_train.reshape(len(x_train), 28*28)`<br>`x_test_flatten = x_test.reshape(len(x_test), 28*28)` | **تسطيح المصفوفات (Flattening / Reshape)**: تحويل كل صورة من مصفوفة ثنائية الأبعاد ($28 \times 28$) إلى متجه أحادي البعد بطول $784$ ليتوافق مع دخل طبقة البيرسبترون المتصلة كلياً. |
| **5** | **Construire un réseau de neurone avec un perceptron simple en utilisant sequential de keras et les paramètres suivants :**<br>• Le nombre de classes dans la base est 10 (de 0 à 9).<br>• La taille d'une image entrée est égale à 28*28.<br>• La fonction d'activation est sigmoid.<br>`model = keras.Sequential([keras.layers.Dense(10, input_shape=(784,), activation='sigmoid')])` | **بناء نموذج البيرسبترون البسيط**: إنشاء شبكة عصبية بطبقة واحدة كثيفة (`Dense`) باستخدام النموذج التتابعي `Sequential`، بحيث تستقبل $784$ مدخلاً وتنتج $10$ مخرجات (تمثل الأرقام من 0 إلى 9) بدالة تنشيط سيجمويد (`sigmoid`). |
| **6** | **Compiler le modèle en utilisant model.compile avec les paramètres suivants :**<br>*(مُحسِّن Adam، ودالة الخسارة Sparse Categorical Crossentropy، ومقياس الدقة Accuracy).* | **تجميع وتدريب النموذج (Compilation & Training)**: ضبط دالة الخسارة وخوارزمية تحسين الانحدار التدريجي ومؤشرات الأداء تمهيداً لبدء عملية التعلم وتقييم الدقة على بيانات الاختبار. |

---

## 2. المخطط المعماري للنموذج (Architectural Diagram)

![[assets/perceptron_simple_mnist.svg|850]]

> [!info] شرح تدفق البيانات في البيرسبترون البسيط (Architecture Walkthrough):
> يوضح الرسم البياني أعلاه دورة حياة العينة منذ دخولها كصورة وحتى تصنيفها النهائي:
> 1. **الصورة الأصلية (Input Image)**: مصفوفة ثنائية الأبعاد بدقة $28 \times 28$ بكسل بقيم تتراوح بين $0$ (خلفية سوداء) و $255$ (كتابة بيضاء)، وتتحول بعد التطبيع إلى مجال $[0.0, 1.0]$.
> 2. **التسطيح (Flattening via `reshape`)**: يتم فك تشابك أسطر الصورة لتتحول إلى شعاع أحادي البعد يتكون من $784$ قيمة ($x_0, x_1, \dots, x_{783}$).
> 3. **طبقة الأوزان والانحياز (Dense Weights & Biases)**: يرتبط كل مدخل بجميع الخلايا العصبية العشر، مما ينتج مصفوفة أوزان بحجم $784 \times 10 = 7840$ وزناً، بالإضافة إلى $10$ معاملات انحياز (Biases)، بإجمالي **7,850 معاملاً قابلاً للتعلم**.
> 4. **دالة التنشيط السيجمويدية (Sigmoid Activation)**: تطبق كل خلية عصبية المعادلة:
>    $$\hat{y}_j = \sigma(z_j) = \frac{1}{1 + e^{-z_j}} \quad \text{حيث} \quad z_j = \sum_{i=0}^{783} W_{ij} x_i + b_j$$
> 5. **التنبؤ النهائي (Class Prediction)**: يمثل الفئة الأعلى احتمالاً (Argmax) الرقم المتوقع من $0$ إلى $9$.

---

## 3. الشرح النظري والتطبيقي المفصل للخطوات (Detailed Breakdown)

### الخطوة 1: استيراد بيانات MNIST وتقسيمها
* **ماهية قاعدة بيانات MNIST**: تُعد "أبجدية التعلم العميق"، وتتكون من 70,000 صورة رقمية لأرقام كُتبت يدوياً بواسطة موظفي التعداد السكاني وطلاب المدارس الثانوية في الولايات المتحدة.
* **التقسيم المعياري**:
  - `(x_train, y_train)`: يحتوي على **60,000 صورة** وتسمياتها لتدريب أوزان النموذج.
  - `(x_test, y_test)`: يحتوي على **10,000 صورة** مستقلة لم يتم عرضها على النموذج لقياس قدرته على التعميم (Generalization) والتأكد من عدم حدوث حفظ أعمى (Overfitting).

```python
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np

# 1) تحميل البيانات
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
print(f"أبعاد التدريب: x_train: {x_train.shape}, y_train: {y_train.shape}")
print(f"أبعاد الاختبار: x_test: {x_test.shape}, y_test: {y_test.shape}")
```

---

### الخطوة 2: المعاينة البصرية عبر `matshow`
* دالة `matshow()` من مكتبة Matplotlib مصممة خصيصاً لعرض المصفوفات الرياضية كصور رسومية ذات تدرج لوني.
* أبعاد الصورة الفردية هي `(28, 28)`.

```python
# 2) اختيار صورة (مثلاً الصورة الأولى رقم فهرسها 0)
image_index = 0
plt.matshow(x_train[image_index], cmap='gray')
plt.title(f"Label: {y_train[image_index]}")
plt.show()

print(f"أبعاد الصورة المختارة: {x_train[image_index].shape}")
```

---

### الخطوة 3: تطبيع البيانات (Data Normalization)

> [!tip] لماذا نقسم قيم البكسلات على 255؟
> 1. **تسريع التقارب (Faster Convergence)**: خوارزميات الانحدار التدريجي (Gradient Descent) تعمل بكفاءة رياضية أعلى عندما تكون المدخلات في مجال عددي صغير وموحد $[0, 1]$.
> 2. **تفادي تلاشي التدرج (Vanishing Gradient)**: دالة التنشيط السيجمويدية تتشبع عند القيم الكبيرة جداً وتصبح مشتقتها قريبة من الصفر؛ وبالتالي حصر القيم بين 0 و 1 يحافظ على استقرار التحديثات التدريجية للأوزان.

```python
# 3) التطبيع
x_train = x_train / 255.0
x_test = x_test / 255.0
```

---

### الخطوة 4: تسطيح المدخلات (Reshaping / Flattening)
* الشبكات العصبية الكثيفة التقليدية (Dense Layers) لا تقبل مدخلات ثنائية الأبعاد (مصفوفات $28 \times 28$)، بل تتطلب متجهاً خطياً أحادي البعد.
* يتم الحساب: $28 \times 28 = 784$ عنصراً لكل عينة.
* ينتج عن ذلك مصفوفة تدريب جديدة بأبعاد `(60000, 784)`.

```python
# 4) إعادة التشكيل (Flattening)
x_train_flatten = x_train.reshape(len(x_train), 28 * 28)
x_test_flatten = x_test.reshape(len(x_test), 28 * 28)

print(f"الأبعاد بعد التسطيح: {x_train_flatten.shape}")
```

---

### الخطوة 5: بناء هيكل البيرسبترون البسيط (Perceptron Simple)
* **المفهوم**: النموذج يتكون من طبقة إدخال تحتوي على 784 عصبوناً متصلة مباشرة بطبقة إخراج تحتوي على 10 عصبونات دون أي طبقات خفية (No Hidden Layers).
* **دالة التنشيط (Sigmoid)**:
  $$\sigma(z) = \frac{1}{1 + e^{-z}}$$
  تنتج قيماً تنحصر بين 0 و 1 تمثل درجة تنشيط كل فئة من الفئات العشر.
* **حساب المعاملات (Parameters Count)**:
  $$\text{Parameters} = (784 \times 10) + 10 = 7,840 + 10 = 7,850$$

```python
# 5) بناء النموذج باستخدام Keras Sequential
model = keras.Sequential([
    keras.layers.Dense(10, input_shape=(784,), activation='sigmoid')
])

model.summary()
```

---

### الخطوة 6: تجميع وتدريب وتقييم النموذج (Compile & Fit)

> [!important] معلمات التجميع (Compilation Hyperparameters)
> - **المُحسِّن (Optimizer)**: `'adam'` - خوارزمية تكيفية تجمع بين مميزات RMSprop و Momentum لتعديل معدل التعلم تلقائياً.
> - **دالة الخسارة (Loss Function)**: `'sparse_categorical_crossentropy'` - تُستخدم لأن مصفوفة التسميات (`y_train`) تحتوي على أرقام صحيحة من 0 إلى 9 (وليس تشفيراً أحادياً One-Hot).
> - **المقياس (Metrics)**: `['accuracy']` - نسبة التنبؤات الصحيحة على إجمالي العينات.

```python
# 6) تجميع النموذج
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# تدريب النموذج (Training)
history = model.fit(x_train_flatten, y_train, epochs=5, batch_size=32)

# تقييم الأداء على بيانات الاختبار (Evaluation)
test_loss, test_acc = model.evaluate(x_test_flatten, y_test)
print(f"دقة النموذج على مجموعة الاختبار: {test_acc * 100:.2f}%")
```

---

## 4. مقارنة وتوصيات أكاديمية (Discussion & Next Steps)

> [!warning] قيود البيرسبترون البسيط والانتقال إلى MLP و CNN و LLMs
> - **الحد الخطي (Linear Decision Boundary)**: على الرغم من استخدام دالة السيجمويد غير الخطية، فإن غياب الطبقات الخفية (Hidden Layers) يجعل البيرسبترون قادراً فقط على الفصل الخطي بين الأنماط المعقدة، محققاً دقة تقارب **92%** فقط على MNIST.
> - **فقدان العلاقات المكانية (Spatial Loss)**: تسطيح الصورة من $28 \times 28$ إلى $784$ يُفقد النموذج إدراك الجوار المكاني للبكسلات المتلاصقة (وهو ما تعالجه لاحقاً الشبكات الالتفافية **CNN**).
> - **الارتباط بنماذج اللغة الكبيرة (LLMs)**: تمثل كل خلية في طبقات الـ Feed-Forward Network داخل كتلة الترانسفورمر (Transformer Block) توسعاً لهذه العمليات الرياضية الدقيقة ($W \cdot x + b$)، حيث تشكل هذه الحسابات الأساس المتين لفهم انحدار التدرج، والدوال التنشيطية، ومعمارية أطر الحساب مثل Keras و PyTorch.
