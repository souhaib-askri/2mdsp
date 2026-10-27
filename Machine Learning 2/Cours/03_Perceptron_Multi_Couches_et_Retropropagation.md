---
title: "المحاضرة 3: البيرسبترون متعدد الطبقات وخوارزمية الانتشار العكسي للخطأ (Le Perceptron Multi-Couches (MLP) et la Rétropropagation du Gradient)"
subject: "Machine Learning 2"
type: Cours
tags:
  - 2mdsp
  - machine-learning
  - deep-learning
  - mlp
  - neural-networks
  - forward-propagation
  - backpropagation
  - chain-rule
  - weight-initialization
  - mnist
date: 2026-10-12
---

# المحاضرة 3: البيرسبترون متعدد الطبقات وخوارزمية الانتشار العكسي للخطأ
## Machine Learning 2 : Deep Learning

> [!abstract] الأطروحة التأسيسية للمحاضرة
> بعد أن أثبتنا في [[02_Classification_Logistique_et_Fonctions_Activation|المحاضرة السابقة]] عجز النماذج الخطية المنفردة عن فصل الفضاءات غير الخطية (مسألة XOR)، ننتقل في هذه المحاضرة إلى القلب النابض للتعلم العميق: **البيرسبترون متعدد الطبقات (Multi-Layer Perceptron - MLP)**. نستعرض البناء المعماري المتجهي للشبكات الأمامية، ونناقش **نظرية التقريب الشامل (Universal Approximation Theorem)**، ثم نُفصّل البرهان الرياضي والاشتقاق التحليلي الكامل لخوارزمية **الانتشار العكسي للخطأ (Backpropagation)** عبر قاعدة السلسلة التفاضلية، وصولاً إلى استراتيجيات تهيئة الأوزان (**He & Xavier Initialization**) لتفادي مأزق تلاشي وانفجار التدرجات.

---

## 1. المعمارية العامة للبيرسبترون متعدد الطبقات (Architecture du MLP)

يتكون البيرسبترون متعدد الطبقات من تراكب طبقات متتالية من العصبونات الصناعية المترابطة بالكامل (**Fully Connected / Dense Layers**)، حيث يُوجّه تدفق المعلومات حصراً من المدخلات نحو المخرجات (**Feedforward**):

![[assets/06_mlp_feedforward_architecture.svg]]

> [!info] شرح معمارية MLP لمهمة تصنيف أرقام MNIST (MLP Architecture Walkthrough):
> يوضح المخطط الهيكلي أعلاه مسار معالجة صورة من قاعدة بيانات [[Projet Fédérateur Machine Learning/TP/01_TP1_Projet_Federateur_Exploration_MNIST|MNIST]]:
> 1. **طبقة المدخلات (Input Layer - $a^{[0]}$)**: يتم تسطيح الصورة ($28 \times 28$ بكسل) في متجه أحادي الأبعاد $\mathbf{x} \in \mathbb{R}^{784}$.
> 2. **الطبقة الخفية الأولى (Hidden Layer 1 - $a^{[1]}$)**: تتكون من 128 عصبوناً بدالة تنشيط ReLU، وتتطلب مصفوفة أوزان $\mathbf{W}^{[1]} \in \mathbb{R}^{128 \times 784}$ ومتجه إزاحة $\mathbf{b}^{[1]} \in \mathbb{R}^{128}$.
> 3. **الطبقة الخفية الثانية (Hidden Layer 2 - $a^{[2]}$)**: تتكون من 64 عصبوناً بدالة تنشيط ReLU، بأوزان $\mathbf{W}^{[2]} \in \mathbb{R}^{64 \times 128}$ وإزاحة $\mathbf{b}^{[2]} \in \mathbb{R}^{64}$.
> 4. **طبقة المخرجات (Output Layer - $a^{[3]}$)**: تتكون من 10 عصبونات تطبق دالة **Softmax** لإنتاج الاحتمالات الفئوية للأرقام من $0$ إلى $9$.

---

## 2. خوارزمية الانتشار الأمامي (Propagation Avant / Forward Pass)

لأي طبقة عامة $l \in \{1, 2, \dots, L\}$، حيث يرمز $L$ للطبقة النهائية:
- نرمز لعدد عصبونات الطبقة بالرمز $n^{[l]}$، مع اعتبار $n^{[0]} = d$ (أبعاد المدخلات).
- مصفوفة الأوزان: $\mathbf{W}^{[l]} \in \mathbb{R}^{n^{[l]} \times n^{[l-1]}}$.
- متجه الإزاحة: $\mathbf{b}^{[l]} \in \mathbb{R}^{n^{[l]}}$.
- دالة التنشيط: $\phi^{[l]}(\cdot)$.

### الصياغة المتجهة للانتشار الأمامي:
لكل طبقة $l = 1, 2, \dots, L$:
$$\mathbf{z}^{[l]} = \mathbf{W}^{[l]} \mathbf{a}^{[l-1]} + \mathbf{b}^{[l]}$$
$$\mathbf{a}^{[l]} = \phi^{[l]}(\mathbf{z}^{[l]})$$
حيث $\mathbf{a}^{[0]} = \mathbf{x}$ هي المدخلات الخام، و $\hat{\mathbf{y}} = \mathbf{a}^{[L]}$ هي تنبؤات النموذج النهائية.

---

## 3. نظرية التقريب الشامل (Théorème d'Approximation Universelle)

> [!quote] مبرهنة سيبينكو وهورنيك (Cybenko 1989 / Hornik 1991)
> *"شبكة عصبية أمامية التغذية تحتوي على **طبقة خفية وحيدة** ذات عدد كافٍ من العصبونات، ومزودة بدالة تنشيط غير خطية مستمرة (مثل Sigmoid أو ReLU)، قادرة على تقريب أي دالة رياضية مستمرة $f: \mathbb{R}^d \to \mathbb{R}^m$ على مجموعة مدمجة (Compact Set) بدقة كيفية $\epsilon > 0$."*

### السؤال المحوري: إذا كانت طبقة واحدة كافية، فلماذا نلجأ إلى الشبكات العميقة (Deep Networks)؟
1. **الكفاءة البارامترية الأسية (Efficiency)**: تقريب بعض الدوال المعقدة بطبقة وحيدة يتطلب عدداً فلكياً (أسياً) من العصبونات، بينما تستطيع الشبكات متعددة الطبقات تمثيل نفس الدالة بعدد أقل بكثير من المعاملات.
2. **التمثيل الهرمي للميزات (Hierarchical Features)**: في معالجة الصور، تتعلم الطبقات الأولى كشف الحواف والخطوط، والطبقات الوسطى تكشف الأشكال الهندسية والزوايا، والطبقات العميقة تجمعها لتشكيل الأرقام والوجوه والأجسام.

---

## 4. الاشتقاق الرياضي الكامل للانتشار العكسي للخطأ (Rétropropagation du Gradient)

هدف خوارزمية الانتشار العكسي (**Backpropagation**) هو حساب المشتقات الجزئية لدالة الخسارة الإجمالية $\mathcal{L}$ بالنسبة لكل معامل قابل للتدريب في الشبكة:
$$\frac{\partial \mathcal{L}}{\partial \mathbf{W}^{[l]}} \quad \text{و} \quad \frac{\partial \mathcal{L}}{\partial \mathbf{b}^{[l]}} \qquad \forall l \in \{1, \dots, L\}$$

![[assets/07_backpropagation_computational_graph.svg]]

> [!info] شرح مخطط الرسم الحسابي وتدفق الأخطاء (Backpropagation Dynamics Walkthrough):
> يوضح المخطط دورة التعلم المغلقة:
> 1. **المسار الأمامي (الأزرق)**: انتقال الإشارات من $\mathbf{a}^{[l-1]}$ إلى التركيبة التآلفية $\mathbf{z}^{[l]}$، ثم دالة التنشيط لإنتاج $\mathbf{a}^{[l]}$، وصولاً إلى دالة الخسارة $\mathcal{L}$.
> 2. **المسار العكسي (الأحمر)**: انتشار متجهات الخطأ التراجعي $\boldsymbol{\delta}^{[l]}$ من الطبقة الأخيرة نحو الطبقات الأولى عبر قاعدة السلسلة ومصفوفة الأوزان المنقولة $(\mathbf{W}^{[l+1]})^T$.
> 3. **تحديث المعاملات**: حساب التدرج اللحظي وتحديث الأوزان بمعدل التعلم $\eta$.

---

### 4.1 تعريف متجه خطأ الطبقة ($\boldsymbol{\delta}^{[l]}$)
نُعرّف الخطأ الداخلي للطبقة $l$ بأنه المشتق الجزئي للخسارة بالنسبة لمدخل التنشيط الخطي $\mathbf{z}^{[l]}$:
$$\boldsymbol{\delta}^{[l]} \triangleq \frac{\partial \mathcal{L}}{\partial \mathbf{z}^{[l]}} \in \mathbb{R}^{n^{[l]}}$$

### 4.2 خطوة الأساس: حساب خطأ الطبقة الأخيرة ($\boldsymbol{\delta}^{[L]}$)
بتطبيق قاعدة السلسلة:
$$\delta_i^{[L]} = \frac{\partial \mathcal{L}}{\partial z_i^{[L]}} = \sum_k \frac{\partial \mathcal{L}}{\partial a_k^{[L]}} \frac{\partial a_k^{[L]}}{\partial z_i^{[L]}}$$

* **في حالة دالة Softmax مع الإنتروبيا المتقاطعة (Categorical Cross-Entropy)** كما في تصنيف MNIST:
  $$\boldsymbol{\delta}^{[L]} = \mathbf{a}^{[L]} - \mathbf{y} = \hat{\mathbf{y}} - \mathbf{y}$$
* **في حالة دالة MSE مع دالة تنشيط عامة**:
  $$\boldsymbol{\delta}^{[L]} = (\mathbf{a}^{[L]} - \mathbf{y}) \odot {\phi^{[L]}}'(\mathbf{z}^{[L]})$$
  حيث يرمز $\odot$ لـ **جداء هادامار (Hadamard Product)**، وهو الضرب عنصراً بعنصر.

---

### 4.3 خطوة التراجع: حساب خطأ الطبقة الخفية ($\boldsymbol{\delta}^{[l]}$) انطلاقاً من ($\boldsymbol{\delta}^{[l+1]}$)
لحساب $\boldsymbol{\delta}^{[l]}$ بدلالة الطبقة اللاحقة $\boldsymbol{\delta}^{[l+1]}$، نطبق قاعدة السلسلة التفاضلية متعددة المتغيرات:
$$\delta_j^{[l]} = \frac{\partial \mathcal{L}}{\partial z_j^{[l]}} = \sum_{k=1}^{n^{[l+1]}} \frac{\partial \mathcal{L}}{\partial z_k^{[l+1]}} \frac{\partial z_k^{[l+1]}}{\partial z_j^{[l]}}$$

نعلم أن:
$$z_k^{[l+1]} = \sum_{p=1}^{n^{[l]}} W_{kp}^{[l+1]} a_p^{[l]} + b_k^{[l+1]} = \sum_{p=1}^{n^{[l]}} W_{kp}^{[l+1]} \phi^{[l]}(z_p^{[l]}) + b_k^{[l+1]}$$
باشتقاق $z_k^{[l+1]}$ بالنسبة لـ $z_j^{[l]}$:
$$\frac{\partial z_k^{[l+1]}}{\partial z_j^{[l]}} = W_{kj}^{[l+1]} \cdot {\phi^{[l]}}'(z_j^{[l]})$$
بالتعويض:
$$\delta_j^{[l]} = \sum_{k=1}^{n^{[l+1]}} \delta_k^{[l+1]} W_{kj}^{[l+1]} \cdot {\phi^{[l]}}'(z_j^{[l]}) = \left( \sum_{k=1}^{n^{[l+1]}} W_{kj}^{[l+1]} \delta_k^{[l+1]} \right) \cdot {\phi^{[l]}}'(z_j^{[l]})$$

بالصيغة المصفوفية المتجهة الشاملة:
$$\boldsymbol{\delta}^{[l]} = \left( (\mathbf{W}^{[l+1]})^T \boldsymbol{\delta}^{[l+1]} \right) \odot {\phi^{[l]}}'(\mathbf{z}^{[l]})$$

> [!tip] المعنى الهندسي لمعادلة التراجع
> تنقل المصفوفة المنقولة $(\mathbf{W}^{[l+1]})^T$ الأخطاء عكساً من عصبونات الطبقة اللاحقة إلى عصبونات الطبقة الحالية، ثم يتم تعديلها بمقدار حساسية دالة التنشيط اللحظية ${\phi^{[l]}}'(\mathbf{z}^{[l]})$.

---

### 4.4 حساب تدرجات الأوزان والإزاحات
بتطبيق قاعدة السلسلة على معاملات الطبقة $l$:
1. **تدرج مصفوفة الأوزان $\mathbf{W}^{[l]}$**:
   $$\frac{\partial \mathcal{L}}{\partial W_{jk}^{[l]}} = \frac{\partial \mathcal{L}}{\partial z_j^{[l]}} \frac{\partial z_j^{[l]}}{\partial W_{jk}^{[l]}} = \delta_j^{[l]} \cdot a_k^{[l-1]}$$
   بالصيغة المصفوفية المباشرة (جداء خارجي Outer Product):
   $$\frac{\partial \mathcal{L}}{\partial \mathbf{W}^{[l]}} = \boldsymbol{\delta}^{[l]} (\mathbf{a}^{[l-1]})^T$$
2. **تدرج متجه الإزاحة $\mathbf{b}^{[l]}$**:
   $$\frac{\partial \mathcal{L}}{\partial \mathbf{b}^{[l]}} = \boldsymbol{\delta}^{[l]}$$

---

## 5. خوارزمية التدريب المتكاملة (Algorithme Complet)

```
خوارزمية التدريب بالانتشار العكسي (Backpropagation Algorithm)
┌────────────────────────────────────────────────────────────────────────┐
│ 1. التهيـئة: تهيئة الأوزان W^[l] والإزاحات b^[l] بقيم عشوائية ذكية.    │
│ 2. لكل حقبة تدريبية (Epoch):                                           │
│    لكل دفعة بيانات (Mini-Batch):                                       │
│       أ. الانتشار الأمامي (Forward Pass):                              │
│          حساب z^[l] و a^[l] لكل l = 1, 2, ..., L وتخزينها في الذاكرة.   │
│       ب. حساب خطأ المخرج:                                              │
│          δ^[L] = a^[L] - y                                             │
│       ج. الانتشار العكسي (Backward Pass):                              │
│          لكل l من L-1 تنازلياً إلى 1:                                  │
│             δ^[l] = ((W^[l+1])^T δ^[l+1]) ⊙ ϕ'(z^[l])                 │
│       د. حساب التدرجات وتحديث المعاملات:                               │
│          W^[l] ← W^[l] - η · [ δ^[l] (a^[l-1])^T ]                     │
│          b^[l] ← b^[l] - η · δ^[l]                                     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 6. أمراض التدرجات واستراتيجيات تهيئة الأوزان (Initialisation des Poids)

### 6.1 مأزق التهيئة بالأصفار (Zero Initialization Failure)
إذا تمت تهيئة جميع الأوزان بأصفار ($\mathbf{W}^{[l]} = \mathbf{0}$):
- تنتج جميع العصبونات في نفس الطبقة نفس المخرج تماماً: $a_1^{[l]} = a_2^{[l]} = \dots$.
- تتلقى جميع العصبونات نفس التدرج تماماً وتتحدث بنفس المقدار.
- تقع الشبكة في **مشكلة التناظر (Symmetry Problem)**، وتفقد قدرتها على تعلم ميزات متنوعة وتتصرف كعصبون منفرد مهما زاد عدد عصبوناتها!

### 6.2 تلاشي وانفجار التدرجات (Vanishing & Exploding Gradients)
عند تكرار ضرب مصفوفات الأوزان عبر طبقات عديدة:
- إذا كانت القيم الذاتية للأوزان أصغر من 1، تتلاشى التدرجات أسياً نحو الصفر ($\to 0$)، وتتوقف الطبقات الأولى عن التعلم.
- إذا كانت القيم الذاتية أكبر من 1، تنفجر التدرجات نحو ما لا نهاية ($\to \infty$)، ويحدث خلل عددي في الحسابات (`NaN` / `Inf`).

### 6.3 استراتيجيات التهيئة القياسية الحديثة
للحفاظ على ثبات تباين التنشيطات والتدرجات عبر الطبقات ($\text{Var}(a^{[l]}) \approx \text{Var}(a^{[l-1]})$):

1. **تهيئة كزافييه / غلوروت (Xavier / Glorot Initialization)**:
   - مخصصة لدوال التنشيط المتشبعة متمركزة الصفر مثل **Sigmoid** و **Tanh**:
     $$W_{ij} \sim \mathcal{N}\left(0, \; \frac{2}{n_{\text{in}} + n_{\text{out}}}\right) \quad \text{أو} \quad \mathcal{U}\left(-\sqrt{\frac{6}{n_{\text{in}} + n_{\text{out}}}}, \; +\sqrt{\frac{6}{n_{\text{in}} + n_{\text{out}}}}\right)$$
2. **تهيئة هي / كايمينغ (He / Kaiming Initialization)**:
   - مخصصة لدالة **ReLU** ومشتقاتها (حيث تنعدم نصف التنشيطات للقيم السالبة):
     $$W_{ij} \sim \mathcal{N}\left(0, \; \frac{2}{n_{\text{in}}}\right) \quad \text{أو} \quad \mathcal{U}\left(-\sqrt{\frac{6}{n_{\text{in}}}}, \; +\sqrt{\frac{6}{n_{\text{in}}}}\right)$$

---

## 7. الخاتمة والربط مع المحاضرة القادمة

مكنتنا خوارزمية الانتشار العكسي من تحويل تدريب الشبكات العصبية العميقة إلى عملية مصفوفية غاية في الكفاءة والسرعة. ومع ذلك، فإن النزول التدريجي البسيط يواجه تحديات حقيقية تتعلق ببطء التقارب في الوديان المنحدرة وخطر الوقوع في فرط التخصيص (**Overfitting**).

في **[[04_Optimisation_Avancee_et_Regularisation|المحاضرة الرابعة]]**، سندرس خوارزميات التحسين التكيفية الحديثة (**Momentum, RMSProp, Adam**)، وتقنيات التنظيم والتعميم ومنع فرط التخصيص (**Dropout, Batch Normalization, Weight Decay**).
