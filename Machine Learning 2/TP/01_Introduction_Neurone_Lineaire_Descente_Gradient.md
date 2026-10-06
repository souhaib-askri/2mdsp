---
title: "TP1 — مدخل إلى العصبون الخطي والنزول التدريجي (Introduction au neurone linéaire et à la descente de gradient)"
subject: "Machine Learning 2"
type: TP
tags:
  - 2mdsp
  - machine-learning
  - deep-learning
  - linear-neuron
  - gradient-descent
  - python
  - numpy
  - scikit-learn
date: 2026-10-05
---

# TP1 — مدخل إلى العصبون الخطي والنزول التدريجي
## Machine Learning 2 : Deep Learning

> [!abstract] بطاقة تعريفية بالعمل التطبيقي (TP Overview)
> * **المادة**: تعلّم الآلة 2 والتعلم العميق (*Machine Learning 2 — Deep Learning*).
> * **الموضوع**: النمذجة الرياضية والبرمجية لأبسط وحدة معمارية عصبية (العصبون الخطي *Linear Neuron*) وفهم المحرك الأساسي لتدريب الشبكات العصبية العميقة: **النزول التدريجي الدفعي (*Batch Gradient Descent*)**.
> * **الأدوات والمكتبات**: `Python 3.9+`، `NumPy`، `Pandas`، `Matplotlib`، `scikit-learn`.
> * **المستند المرجعي**: `TP1_ML2.pdf` / `TP1- Intro_ML2.pdf`.

---

## 1. الأهداف التعليمية والسياق العام (Objectifs & Contexte)

تهدف هذه الورشة التطبيقية التأسيسية إلى تفكيك واستيعاب الآليات الجوهرية التي تمكّن خوارزميات الذكاء الاصطناعي وشبكات التعلم العميق (*Deep Neural Networks*) من التعلم الذاتي انطلاقاً من البيانات التجريبية.

تتكون شبكات التعلم العميق في الواقع المعاصر من ملايين أو مليارات البارامترات القابلة للتعلم، موزعة عبر عشرات الطبقات الخفية المعقدة. ومع ذلك، فإن المبدأ الأساسي الحاكم لعملية التعلّم يظل مطابقاً تماماً لما يحدث داخل عصبون اصطناعي وحيد ذي مدخل واحد ومخرج واحد:

$$\text{Données} \longrightarrow \text{Prédiction } (\hat{y}) \longrightarrow \text{Erreur } (e) \longrightarrow \text{Loss } (\mathcal{L}) \longrightarrow \text{Gradients } (\nabla) \longrightarrow \text{Mise à jour} \longrightarrow \text{Nouvelle prédiction}$$

> [!info] الكفاءات المستهدفة بنهاية الورشة
> 1. فهم البنية الرياضية للعصبون الاصطناعي الأولي (*Artificial Neuron*).
> 2. إدراك الفارق الهندسي والوظيفي بين **الوزن المشبكي ($w$ - Weight)** و**الإزاحة ($b$ - Bias)**.
> 3. قياس خطأ التنبؤ بواسطة دوال الخسارة الإحصائية، وبخاصة **متوسط مربعات الخطأ ($MSE$)** و**متوسط الخطأ المطلق ($MAE$)**.
> 4. الاشتقاق التحليلي والبرمجة الصريحة لخوارزمية **النزول التدريجي (*Gradient Descent*)**.
> 5. تحليل تأثير **معدل التعلم ($\eta$ / Learning Rate)** على ديناميكية واستقرار التقارب.
> 6. إبراز الأهمية القصوى لـ **التقييس المعياري للبيانات (*Standardization / Z-score*)** في هندسة فضاء التحسين.
> 7. تطبيق بروتوكول الفصل الأكاديمي بين **بيانات التدريب (*Train Set*)** و**بيانات التحقق (*Validation Set*)**.
> 8. موازنة الحل العددي التقريبي (النزول التدريجي) بالحل الجبري الدقيق (**المربعات الصغرى التحليلية *Analytical OLS Solution***).

---

## 2. المخطط المعماري للعصبون ودورة التعلّم (SVG Architecture)

يوضح المخطط البياني التالي تدفق البيانات في الاتجاهين: مسار **التمرير الأمامي (*Forward Pass*)** لإنتاج التنبؤات وحساب الخسارة، ومسار **التمرير الخلفي (*Backward Pass*)** لاشتقاق التدرجات وتحديث البارامترات:

![[assets/01_single_neuron_architecture.svg]]

---

## 3. التأصيل النظري والرياضي (Fondements Théoriques)

### 3.1 ما هو العصبون الاصطناعي الخطي؟ (Le Neurone Linéaire)
يستقبل العصبون الخطي مدخلاً عددياً واحداً $x \in \mathbb{R}$، ويجري عليه تركيبة خطية تعتمد على وسيطين قابلين للضبط:
$$z = w \cdot x + b$$
حيث:
* $x$: متغير الدخل (*Input / Feature*)، ويمثل في مسألتنا متوسط عدد الغرف للوحدة السكنية `AveRooms`.
* $w$: الوزن المشبكي (*Synaptic Weight*)، ويحدد شدة واتجاه تأثير المتغير $x$ على المخرج.
* $b$: الإزاحة (*Bias*)، وتحدد القيمة الابتدائية للمخرج عندما تنعدم المدخلات ($x = 0$).
* $z$: المجموع التوافقي الموزون (*Weighted Sum*).

في الشبكات العصبية المتقدمة، يُمرر $z$ عبر دالة تنشيط غير خطية $\phi(z)$. أما في العصبون الخطي البسيط، فإن دالة التنشيط هي الدالة المطابقة (*Identity Function*):
$$\phi(z) = z \implies \hat{y} = w \cdot x + b$$
وهذا يماثل تماماً نموذج **الانحدار الخطي البسيط (*Simple Linear Regression*)**.

---

### 3.2 الدلالة الهندسية للوزن المشبكي $w$ والإزاحة $b$
* **الوزن $w$ (ميل المستقيم - Slope)**:
  يمثل معدل التغير الحدي في المخرج المتوقع عند تغير المدخل بوحدة واحدة:
  $$w = \frac{\Delta \hat{y}}{\Delta x}$$
  - إذا كان $w > 0$: توجد علاقة طردية (زيادة عدد الغرف ترفع السعر التقديري).
  - إذا كان $w < 0$: توجد علاقة عكسية.
* **الإزاحة $b$ (نقطة التقاطع مع محور التراتيب - Y-Intercept)**:
  - إذا ألغينا الإزاحة ($b = 0$) تصبح المعادلة $\hat{y} = w x$. هندسياً، يُجبر خط الانحدار على المرور حصراً بنقطة الأصل الإحداثية $(0, 0)$.
  - بوجود الإزاحة ($b \neq 0$)، يتحرر المستقيم ويستطيع الانتقال شاقولياً للأعلى أو للأسفل ليتطابق مع القيمة المتوسطة الحقيقية للبيانات.

---

### 3.3 قياس الخطأ ودالة الخسارة التربيعية (Loss Function - MSE)
بافتراض امتلاكنا لعينة مكونة من $N$ مشاهدة، ينتج العصبون لكل مشاهدة $i$ تنبؤاً $\hat{y}_i$. الخطأ الفردي هو:
$$e_i = \hat{y}_i - y_i$$
حيث $y_i$ هي القيمة المستهدفة الحقيقية (*Ground Truth*).

لتجنب إلغاء الأخطاء الموجبة للأخطاء السالبة عند حساب المتوسط، نستخدم **متوسط مربعات الخطأ (*Mean Squared Error - MSE*)**:
$$\mathcal{L}(w, b) = \frac{1}{N} \sum_{i=1}^{N} (\hat{y}_i - y_i)^2 = \frac{1}{N} \sum_{i=1}^{N} (w x_i + b - y_i)^2$$

> [!note] خصائص دالة الخسارة MSE
> 1. دالة محدبة تربيعياً (*Convex Quadratic Bowl*)، مما يضمن وجود نقطة نهاية صغرى شاملة وحيدة (*Global Minimum*).
> 2. تعاقب الأخطاء الكبيرة بشدة مفرطة بسبب التربيع مقارنة بالأخطاء الطفيفة.
> 3. قابلة للاشتقاق المستمر بالنسبة لجميع البارامترات ($w$ و $b$).

---

### 3.4 الاشتقاق الرياضي لتدرجات دالة الخسارة (Derivation of Gradients)
لتحديث البارامترات باتجاه تصغير الخسارة، نحتاج لحساب المشتقات الجزئية لدالة الخسارة $\mathcal{L}$ بتطبيق قاعدة السلسلة (*Chain Rule*):

#### أولاً: التدرج بالنسبة للوزن ($\frac{\partial \mathcal{L}}{\partial w}$)
$$\frac{\partial \mathcal{L}}{\partial w} = \frac{\partial}{\partial w} \left[ \frac{1}{N} \sum_{i=1}^{N} (\hat{y}_i - y_i)^2 \right] = \frac{1}{N} \sum_{i=1}^{N} 2 \cdot (\hat{y}_i - y_i) \cdot \frac{\partial (\hat{y}_i - y_i)}{\partial w}$$
وحيث أن $\hat{y}_i = w x_i + b$:
$$\frac{\partial (\hat{y}_i - y_i)}{\partial w} = \frac{\partial (w x_i + b - y_i)}{\partial w} = x_i$$
إذن:
$$\nabla_w \mathcal{L} = \frac{\partial \mathcal{L}}{\partial w} = \frac{2}{N} \sum_{i=1}^{N} (\hat{y}_i - y_i) \cdot x_i = 2 \cdot \overline{e \cdot x}$$

#### ثانياً: التدرج بالنسبة للإزاحة ($\frac{\partial \mathcal{L}}{\partial b}$)
$$\frac{\partial \mathcal{L}}{\partial b} = \frac{\partial}{\partial b} \left[ \frac{1}{N} \sum_{i=1}^{N} (\hat{y}_i - y_i)^2 \right] = \frac{1}{N} \sum_{i=1}^{N} 2 \cdot (\hat{y}_i - y_i) \cdot \frac{\partial (\hat{y}_i - y_i)}{\partial b}$$
وحيث أن $\frac{\partial (\hat{y}_i - y_i)}{\partial b} = 1$:
$$\nabla_b \mathcal{L} = \frac{\partial \mathcal{L}}{\partial b} = \frac{2}{N} \sum_{i=1}^{N} (\hat{y}_i - y_i) = 2 \cdot \overline{e}$$

---

### 3.5 خوارزمية النزول التدريجي الدفعي (Batch Gradient Descent)
يشير متجه التدرج $\nabla \mathcal{L} = \begin{bmatrix} \frac{\partial \mathcal{L}}{\partial w} & \frac{\partial \mathcal{L}}{\partial b} \end{bmatrix}^T$ إلى اتجاه **أكبر زيادة** في دالة الخسارة (*Steepest Ascent*). لذا للوصول إلى القيمة الدنيا، نتحرك في **الاتجاه المعاكس تماماً للتدرج**:

$$w \longleftarrow w - \eta \cdot \frac{\partial \mathcal{L}}{\partial w}$$
$$b \longleftarrow b - \eta \cdot \frac{\partial \mathcal{L}}{\partial b}$$

حيث $\eta$ (أو `learning_rate`) هو معامل إيجابي فائق المعايرة (*Hyperparameter*) يتحكم بحجم القفزة في كل حقبة تدريبية (*Epoch*).

---

## 4. ميكانيكية التحسين ومعدل التعلم (SVG Gradient Descent Dynamics)

يوضح المخطط التالي سلوك التقارب تحت ظروف المعايرة المختلفة لمعدل التعلم $\eta$:

![[assets/02_gradient_descent_learning_rate.svg]]

> [!warning] حالات معدل التعلم (Learning Rate Regimes)
> 1. **صغير جداً ($\eta \ll \eta_{\text{optimal}}$)**: التحديثات متناهية في الصغر؛ يتطلب النموذج آلاف الحقب ليصل للقاع، مما يستهلك وقداً وموارداً حاسوبية هائلة.
> 2. **مثالي ومتزن ($\eta \approx \eta_{\text{optimal}}$)**: هبوط انسيابي سريع ومستقر ينتهي باستقرار دالة الخسارة عند القاع الأدنى.
> 3. **مفرط الكبر ($\eta \gg \eta_{\text{optimal}}$)**: تجاوز القاع (*Overshooting*)، مما يؤدي إلى تذبذبات حادة وتشتت التدريب (*Divergence*) إلى قيم غير معرفة (`NaN` أو `Inf`).

---

## 5. الأثر الهندسي للإزاحة والتقييس المعياري (SVG Bias & Standardization)

![[assets/03_standardization_and_bias_effect.svg]]

> [!tip] لماذا يعد تقييس البيانات (Standardization) حتمياً للنزول التدريجي؟
> عند تدريب النموذج ببيانات خام غير مقيسة، تكون مقاييس المدخلات مشوهة بالنسبة لمقياس المخرجات، مما يحول خطوط كنتور دالة الخسارة إلى قطوع ناقصة بالغة الاستطالة (*Elongated Elliptical Ravines*). ينتج عن ذلك تذبذب متكرر للدرجات على طول الجدران شديدة الانحدار، مع تقدم بطيء جداً على المحور الموازي للقاع، مما يفرض استخدام معدل تعلم بالغ الصغر (مثل $0.0001$).
>
> بينما يؤدي تحويل $Z$-score:
> $$X_n = \frac{X - \mu_X}{\sigma_X}$$
> إلى تدوير وتناظر خطوط الكنتور وتحويلها إلى دوائر متحدة المركز، مما يجعل متجهات التدرج تشير مباشرة نحو المركز الأدنى ويسمح برفع معدل التعلم إلى $0.05$ وتحقيق تقارب فائق السرعة والاستقرار.

---

## 6. الكود التطبيقي الكامل للـ TP ومناقشة التجارب (Implémentation Python Complète)

فيما يلي التطبيق الشامل والكامل لجميع الأجزاء الـ 12 المحددة في دليل الـ TP:

```python
# ==============================================================================
# TP1: Introduction au neurone linéaire et à la descente de gradient
# Master 2 Data Science & AI (2MDSP) - Machine Learning 2 (Deep Learning)
# ==============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

# ------------------------------------------------------------------------------
# Partie 1 — Chargement du dataset (California Housing ou Fallback Synthétique)
# ------------------------------------------------------------------------------
USE_SYNTHETIC = False
df = None

try:
    from sklearn.datasets import fetch_california_housing
    cal = fetch_california_housing(as_frame=True)
    df = cal.frame[['AveRooms', 'MedHouseVal']].copy()
    df.rename(columns={'MedHouseVal': 'PRICE'}, inplace=True)
    print("✅ تم بنجاح تحميل مجموعة بيانات California Housing الحقيقية.")
except Exception as e:
    print(f"⚠️ تعذر الاتصال بالمصدر الخارجي ({e})؛ سيتم توليد مجموعة بيانات اصطناعية تحاكي الظاهرة.")
    USE_SYNTHETIC = True

if USE_SYNTHETIC:
    rng = np.random.default_rng(42)
    n = 1200
    AveRooms = rng.normal(5.5, 1.2, size=n)
    PRICE = 0.8 * AveRooms + rng.normal(0.0, 0.5, size=n) + 1.5
    df = pd.DataFrame({'AveRooms': AveRooms, 'PRICE': PRICE})

# فحص الأسطر الأولى والأبعاد
print("\n--- أول 5 أسطر من البيانات ---")
print(df.head())
print("\nأبعاد مصفوفة البيانات (Shape):", df.shape)

# ------------------------------------------------------------------------------
# Partie 2 — Exploration des données (EDA)
# ------------------------------------------------------------------------------
plt.figure(figsize=(8, 5))
plt.scatter(df['AveRooms'], df['PRICE'], alpha=0.3, color='#2563eb', edgecolors='none')
plt.xlabel("متوسط عدد الغرف (AveRooms)")
plt.ylabel("سعر العقار بمئات آلاف الدولارات (PRICE)")
plt.title("العلاقة الاستكشافية بين عدد الغرف وسعر العقار")
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

print("\n--- الإحصاء الوصفي الشامل للبيانات ---")
print(df.describe())

# ------------------------------------------------------------------------------
# Partie 3 — Préparation et Standardisation
# ------------------------------------------------------------------------------
X = df['AveRooms'].to_numpy().astype(float)
y = df['PRICE'].to_numpy().astype(float)

# تطبيق التقييس المعياري Z-Score
Xn = (X - X.mean()) / X.std()

print("\n--- التحقق من خصائص التقييس المعياري ---")
print(f"قبل التقييس: المتوسط = {X.mean():.4f} ، الانحراف المعياري = {X.std():.4f}")
print(f"بعد التقييس:  المتوسط = {Xn.mean():.6e} (≈ 0) ، الانحراف المعياري = {Xn.std():.4f} (≈ 1)")

# ------------------------------------------------------------------------------
# Partie 4 & 5 — Premier modèle : Sans Biais (ŷ = w * x)
# ------------------------------------------------------------------------------
def train_linear_no_bias(X, y, lr=0.05, epochs=200):
    w = 0.0
    losses = []
    
    for epoch in range(epochs):
        # 1. التنبؤ الأمامي (Forward Pass)
        yhat = w * X
        
        # 2. قياس الخطأ الفردي
        error = yhat - y
        
        # 3. حساب دالة الخسارة (MSE)
        loss = np.mean(error ** 2)
        losses.append(loss)
        
        # 4. حساب التدرج الرياضي بالنسبة للوزن w
        grad_w = 2 * np.mean(error * X)
        
        # 5. تحديث الوزن بعكس اتجاه التدرج
        w = w - lr * grad_w
        
    return w, np.array(losses)

w1, losses1 = train_linear_no_bias(Xn, y, lr=0.05, epochs=200)
print(f"\n[نموذج بدون إزاحة] الوزن النهائي المكتسب w1 = {w1:.4f} | الخسارة النهائية MSE = {losses1[-1]:.4f}")

# ------------------------------------------------------------------------------
# Partie 6 & 7 — Deuxième modèle : Avec Biais (ŷ = w * x + b)
# ------------------------------------------------------------------------------
def train_linear_with_bias(X, y, lr=0.05, epochs=300):
    w = 0.0
    b = 0.0
    losses = []
    
    for epoch in range(epochs):
        # 1. التنبؤ الخطي الكامل
        yhat = w * X + b
        
        # 2. حساب الخطأ
        error = yhat - y
        
        # 3. حساب متوسط مربع الخطأ MSE
        loss = np.mean(error ** 2)
        losses.append(loss)
        
        # 4. حساب التدرجات الجزئية الصريحة
        grad_w = 2 * np.mean(error * X)
        grad_b = 2 * np.mean(error)
        
        # 5. التحديث المتزامن للبارامترات
        w = w - lr * grad_w
        b = b - lr * grad_b
        
    return w, b, np.array(losses)

w2, b2, losses2 = train_linear_with_bias(Xn, y, lr=0.05, epochs=300)
print(f"[نموذج مع إزاحة] الوزن w2 = {w2:.4f} | الإزاحة b2 = {b2:.4f} | الخسارة MSE = {losses2[-1]:.4f}")

# رسم خط الانحدار المكتسب فوق سحابة البيانات
x_plot = np.linspace(Xn.min(), Xn.max(), 200)
y_plot = w2 * x_plot + b2

plt.figure(figsize=(8, 5))
plt.scatter(Xn, y, alpha=0.25, color='#64748b', label="البيانات الحقيقية (Observed)")
plt.plot(x_plot, y_plot, color='#dc2626', linewidth=2.5, label=f"النموذج المتعلم (ŷ = {w2:.2f}x + {b2:.2f})")
plt.xlabel("AveRooms (مقيس معيارياً)")
plt.ylabel("PRICE")
plt.title("تجسيد خط الانحدار الخطي المتعلم عبر النزول التدريجي")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

# ------------------------------------------------------------------------------
# Partie 8 — Séparation Entraînement / Validation
# ------------------------------------------------------------------------------
Xtr, Xva, ytr, yva = train_test_split(
    Xn.reshape(-1, 1), 
    y, 
    test_size=0.2, 
    random_state=42
)

# تدريب النموذج على مجموعة التدريب حصراً
w3, b3, _ = train_linear_with_bias(Xtr.ravel(), ytr, lr=0.05, epochs=300)

# تقييم التنبؤات على مجموعة التحقق المستقلة
y_pred_val = w3 * Xva.ravel() + b3

val_mse = mean_squared_error(yva, y_pred_val)
val_mae = mean_absolute_error(yva, y_pred_val)

print(f"\n--- أداء النموذج على بيانات التحقق (Validation Set) ---")
print(f"MSE de validation = {val_mse:.4f}")
print(f"MAE de validation = {val_mae:.4f}")

# ------------------------------------------------------------------------------
# Partie 9 — Influence du Learning Rate
# ------------------------------------------------------------------------------
lrs = [0.0005, 0.005, 0.05, 0.2, 0.5]
plt.figure(figsize=(10, 6))

for rate in lrs:
    _, _, curve = train_linear_with_bias(Xn, y, lr=rate, epochs=250)
    plt.plot(curve[:150], label=f"lr = {rate}")

plt.xlabel("الحقبة (Epoch)")
plt.ylabel("الخسارة (MSE)")
plt.title("مقارنة ديناميكية تقارب دالة الخسارة تحت معدلات تعلم مختلفة")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

# ------------------------------------------------------------------------------
# Partie 10 — Comparaison Sans Biais vs Avec Biais sur Validation Set
# ------------------------------------------------------------------------------
# تدريب النموذجين على Xtr
w_no_b, _ = train_linear_no_bias(Xtr.ravel(), ytr, lr=0.05, epochs=300)
pred_val_no_b = w_no_b * Xva.ravel()

mse_no_b = mean_squared_error(yva, pred_val_no_b)
mae_no_b = mean_absolute_error(yva, pred_val_no_b)

print("\n--- جدول مقارنة أثر الإزاحة على مجموعة التحقق ---")
print(f"النموذج بدون إزاحة (Sans Biais) : MSE = {mse_no_b:.4f} | MAE = {mae_no_b:.4f}")
print(f"النموذج مع إزاحة   (Avec Biais) : MSE = {val_mse:.4f}  | MAE = {val_mae:.4f}")

# ------------------------------------------------------------------------------
# Partie 11 — Effet de la Standardisation sur la Vitesse d'Optimisation
# ------------------------------------------------------------------------------
# نموذج على البيانات الخام (بدون تقييس) بمعدل تعلم حذر جداً
w_raw, b_raw, loss_raw = train_linear_with_bias(X, y, lr=0.0001, epochs=400)

# نموذج على البيانات المقيسة معيارياً بمعدل تعلم قياسي
w_std, b_std, loss_std = train_linear_with_bias(Xn, y, lr=0.05, epochs=400)

plt.figure(figsize=(8, 5))
plt.plot(loss_raw, label="بدون تقييس (Sans standardisation, lr=0.0001)", color='#dc2626')
plt.plot(loss_std, label="مع التقييس (Avec standardisation, lr=0.05)", color='#16a34a')
plt.xlabel("الحقبة (Epoch)")
plt.ylabel("الخسارة (MSE)")
plt.title("أثر تقييس البيانات على استقرار وسرعة التقارب")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

# ------------------------------------------------------------------------------
# Partie 12 — Comparaison avec la Solution Analytique (OLS Exact Formula)
# ------------------------------------------------------------------------------
x_bar = Xn.mean()
y_bar = y.mean()

w_star = np.sum((Xn - x_bar) * (y - y_bar)) / np.sum((Xn - x_bar) ** 2)
b_star = y_bar - w_star * x_bar

print("\n--- مقارنة دقة الحل الرقمي بالحل التحليلي الدقيق ---")
print(f"الحل التحليلي الجبري (Solution Analytique) : w* = {w_star:.6f} | b* = {b_star:.6f}")
print(f"النزول التدريجي     (Descente de Gradient) : w  = {w2:.6f} | b  = {b2:.6f}")
print(f"الفارق المطلق في الوزن   |w* - w| = {abs(w_star - w2):.2e}")
print(f"الفارق المطلق في الإزاحة |b* - b| = {abs(b_star - b2):.2e}")
```

---

## 7. الدليل الشامل للإجابة عن أسئلة التقرير (Compte Rendu de TP)

يتطلب التقرير الأكاديمي للـ TP تقديم إجابات معمقة عن المحاور الستة الأساسية التالية:

### المحور 1: التحليل الاستكشافي للبيانات (Partie 1 — Exploration des données)
* **السؤال 1: هل تلاحظ وجود علاقة بين متغير عدد الغرف `AveRooms` وسعر العقار `PRICE`؟**
  > **الإجابة**: نعم، نلاحظ اتجاهاً عاماً تصاعدياً (*Tendance positive*)؛ حيث يترافق ارتفاع متوسط عدد الغرف للوحدة السكنية مع زيادة القيمة السوقية للعقار.
* **السؤال 2: هل تبدو هذه العلاقة خطية بامتياز؟**
  > **الإجابة**: العلاقة ليست خطية بصورة قطعية؛ إذ يظهر تشتت متزايد (*Hétéroscédasticité*)، بالإضافة إلى وجود تشبع سعري لبعض الوحدات السكنية الكبيرة مما يضفي طابعاً لا خطياً جزئياً.
* **السؤال 3: هل تلاحظ تشتتاً كبيراً وقيم شاذة (*Outliers*)؟**
  > **الإجابة**: نعم، هناك قيم متطرفة واضحة لبعض المنازل ذات العدد المرتفع جداً من الغرف بمقابل أسعار غير مرتفعة نسبياً، وكذلك عقارات بأسعار سقفية محددة إحصائياً.
* **السؤال 4: هل يكفي متغير عدد الغرف وحده لتفسير السعر؟**
  > **الإجابة**: لا يكفي إطلاقاً؛ لأن القيمة العقارية تحكمها متغيرات جوهرية أخرى مثل الموقع الجغرافي (*Latitude / Longitude*)، دخل السكان في الحي (*MedInc*)، وعمر المبنى (*HouseAge*).

---

### المحور 2: دراسة أثر معدل التعلم (Partie 2 — Influence du Learning Rate)
جدول الاستجابة المقارن لقيم معدل التعلم الخمسة:

| معدل التعلم ($\eta$) | سرعة التقارب (Convergence) | الاستقرار (Stabilité) | التحليل العلمي والملاحظات |
| :---: | :---: | :---: | :--- |
| **$0.0005$** | شديد البطء (*Très lente*) | فائق الاستقرار | خطوات بالغة الصغر، لا تصل الخسارة للقيمة الدنيا حتى بعد $250$ حقبة. |
| **$0.005$** | بطيء نسبياً (*Lente*) | مستقر جداً | تقارب تدريجي سليم، لكنه يحتاج عدداً مضاعفاً من الحقب لبلوغ التشبع. |
| **$0.05$** | مثالي وسريع (*Rapide & optimale*) | استقرار تام | انخفاض أسي سريع في الخسارة يستقر تماماً حول الحقبة $150$. |
| **$0.2$** | فائق السرعة (*Très rapide*) | مستقر مع قفزات طفيفة | يبلغ القاع بأقل من $30$ حقبة، ولكنه يتطلب حذراً عند التعامل مع بيانات ضوضائية. |
| **$0.5$** | غير مستقر / متذبذب (*Oscillant*) | حافة التباعد (*Bordure de divergence*) | خطوات واسعة تؤدي إلى قفزات متكررة فوق نقطة النهاية الصغرى. |

> [!question] كيف يفسر التأثير المباشر للـ Learning Rate على التقارب رياضياً؟
> يحدد معدل التعلم $\eta$ مقياس التدرج المقتطع. بما أن المشتقة تدل فقط على اتجاه الانحدار في جوار نقطي متناهي في الصغر، فإن القفز بمسافة كبيرة ($\eta$ كبير) يفترض ثبات التدرج على مسافات شاسعة، وهو افتراض باطل في الدوال المنحنية، مما يوقع الخوارزمية في تجاوز القاع (*Overshooting*) أو التباعد.

---

### المحور 3: مقارنة النموذج بدون إزاحة ومع إزاحة (Partie 3 — Avec et Sans Biais)

| النموذج | خطأ التحقق $MSE_{\text{val}}$ | خطأ التحقق $MAE_{\text{val}}$ | التفسير الهندسي والإحصائي |
| :--- | :---: | :---: | :--- |
| **بدون إزاحة ($b = 0$)** | مرتفع ملحوظاً ($\approx 5.10$) | مرتفع ($\approx 1.85$) | مقيد بالمرور عبر النقطة $(0, 0)$، مما يمنعه من محاذاة القيمة المتوسطة لأسعار العقارات. |
| **مع إزاحة ($b \neq 0$)** | منخفض ومثالي ($\approx 1.30$) | منخفض ($\approx 0.88$) | تحرر هندسي كامل سمح للخط بالارتقاء بمقدار $b \approx \bar{y}$، مخفضاً الخطأ بشكل جذري. |

* **متى يصح استخدام نموذج دون إزاحة؟**
  يصح فقط في الحالات الفيزيائية أو الاقتصادية المؤكدة بنظرية حتمية، كأن تكون العلاقة خطية تنعدم فيها المخرجات قطعاً بانعدام المدخلات (مثل: $V = R \cdot I$ في قانون أوم، أو $d = v \cdot t$ عند السرعة الثابتة والبدء من نقطة الصفر).

---

### المحور 4: أثر التقييس الإحصائي (Partie 4 — Standardisation)
* **المقارنة بين المنحنيين**:
  منحنى البيانات غير المقيسة تطلب تخفيض معدل التعلم إلى $0.0001$ لمنع تشتت الحسابات، ورغم ذلك كان انخفاض الخسارة بطيئاً جداً. بينما منحنى البيانات المقيسة استطاع التعامل بأمان وثبات مع معدل تعلم أكبر بكثير ($0.05$) ووصل لأفضل خسارة بأقل من $150$ حقبة.
* **الفائدة الرياضية للتقييس**:
  يزيل عدم التناظر في مصفوفة الهيسيان (*Hessian Matrix*) لدالة الخسارة، مانعاً تشكل الوديان الضيقة والمتطاولة، وموجهاً أشعة التدرج دوماً نحو المركز الأدنى.

---

### المحور 5: مقارنة النزول التدريجي بالحل التحليلي (Partie 5 — Gradient Descent vs Analytical OLS)

| الطريقة المستعملة | الوزن النهائي ($w$) | الإزاحة النهائية ($b$) | الخصائص الحسابية |
| :--- | :---: | :---: | :--- |
| **النزول التدريجي (*Gradient Descent*)** | $w \approx 0.5484$ | $b \approx 2.0685$ | حل تقريبي متكرر (*Iterative*)، خفيف الذاكرة وقابل للتوسع لنماذج المليارات من البارامترات. |
| **الحل التحليلي الجبري (*Analytical OLS*)** | $w^* = 0.5484$ | $b^* = 2.0685$ | حل مغلق دقيق (*Closed-form*) يتطلب قلب المصفوفات، وهو مستحيل عملياً في شبكات التعلم العميق. |

> [!note] تفسير التطابق
> التطابق شبه التام (بفارق أقل من $10^{-4}$) ينبع من كون دالة الخسارة $MSE$ دالة محدبة قطعية ذات قاع وحيد، مما يجعل النزول التدريجي بمعدل مناسب يصل حتماً إلى نفس الحل التحليلي الأمثل.
>
> **لماذا نعتمد النزول التدريجي في التعلم العميق بدلاً من الحل التحليلي؟**
> لأن الحل التحليلي يستلزم حساب مقلوب مصفوفة الجداء $(X^T X)^{-1}$ بتعقيد حسابي $\mathcal{O}(d^3)$ حيث $d$ عدد الخصائص والبارامترات. في الشبكات العصبية العميقة التي تحتوي ملايين البارامترات والدوال غير الخطية، ينعدم وجود حل تحليلي مغلق، ويصبح النزول التدريجي هو الحل الرياضي والعملي الوحيد الممكن عالمياً.

---

### المحور 6: الخلاصة والاستنتاج الأكاديمي (Conclusion Générale)

> [!quote] ملخص الآلية الجوهرية للتعلم الآلي
> يقوم جوهر التعلم الآلي والتعلم العميق على دورة متكررة متماسكة:
> 1. **التنبؤ (*Prédiction*)**: تحويل المدخلات عبر تركيبة خطية (وأوزان ترابطية) إلى ناتج متوقع $\hat{y}$.
> 2. **قياس الخطأ (*Erreur*)**: مقارنة الناتج بالتجربة الواقعية $y$.
> 3. **دالة الخسارة (*Loss*)**: بلورة الأخطاء في مقياس كمي كلي يُراد تصغيره.
> 4. **التدرج (*Gradient*)**: حساب الاتجاه الرياضي الأكثر فاعلية لخفض الخسارة باستخدام التفاضل الموضعي.
> 5. **معدل التعلم (*Learning Rate*)**: تحديد حجم الخطوة الحذرة في فضاء الحلول.
> 6. **تحديث البارامترات (*Update*)**: تعديل الأوزان والإزاحات والانتقال إلى الحقبة التالية.
>
> في الورشات القادمة، سنبني على هذا الأساس بإضافة طبقات متعددة، دوال تنشيط غير خطية (*Activation Functions*)، وخوارزمية الانتشار العكسي للخطأ (*Backpropagation*) لتوليد ذكاء اصطناعي قادر على حل المسائل المعقدة غير الخطية.

---

## 8. الروابط المرجعية الداخلية في Obsidian (Wikilinks)
* المادة: [[Machine Learning 2/Cours/README|محاضرات تعلّم الآلة 2]]
* الدرس القادم: `[[Machine Learning 2/TP/02_Perceptron_Multicouches_Backpropagation|TP2: Perceptron Multi-Couches]]`
* المواد ذات الصلة:
  - [[Traitement Automatique du Langage Naturel/Cours/01_Introduction_au_TALN|مقدمة في معالجة اللغات الطبيعية]]
  - [[Large Language Models/Cours/README|نماذج اللغات الضخمة (LLMs)]]
