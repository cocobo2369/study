### **📌 Soft Label과 Hard Label이란?**  
Soft Label과 Hard Label은 **딥러닝 모델이 정답(Class Label)을 표현하는 방식**입니다.  

✅ **Hard Label** → **정확한 정답 (One-Hot Encoding 방식)**  
✅ **Soft Label** → **확률 분포 기반의 정답 (Teacher Model에서 생성한 부드러운 정답)**  

이제 **왜 "Soft"와 "Hard"라는 용어를 사용하는지** 쉽게 설명해드릴게요! 😊  

---

## **✅ 1. Hard Label이란? (딱딱한 정답, Slide 90)**
### **🔹 Hard Label의 특징**
- **각 클래스(Class) 중 하나만 정답으로 지정** (One-Hot Encoding 방식).  
- 다른 클래스들은 **무조건 0**으로 표현됨.  

✅ **예제: 개 🐶 vs. 고양이 🐱 vs. 토끼 🐰**  
모델이 **"이 이미지가 개(🐶)인지 예측해야 한다"**고 가정하자.  
Hard Label은 다음과 같이 원-핫 인코딩(One-Hot Encoding)으로 표현됩니다.

```math
y_{\text{hard}} = [1, 0, 0]
```
- 개(🐶) → `1`
- 고양이(🐱) → `0`
- 토끼(🐰) → `0`

즉, **Hard Label은 "절대적인 정답"만 1로, 나머지는 0으로 처리하는 방식**입니다.  
하지만 **이 방식은 클래스 간 관계를 고려하지 않음** → 학습이 더 어려울 수 있음.  

---

## **✅ 2. Soft Label이란? (부드러운 정답, Slide 90)**
### **🔹 Soft Label의 특징**
- Hard Label과 달리, **Teacher Model이 생성한 확률 분포를 정답으로 사용**.  
- **각 클래스에 대한 확률 값이 부드럽게 표현됨.**  

✅ **예제: Soft Label로 변환한 경우**  
```math
y_{\text{soft}} = [0.8, 0.1, 0.1]
```
- 개(🐶) → `0.8`
- 고양이(🐱) → `0.1`
- 토끼(🐰) → `0.1`

이제 **정답(🐶)이 0.8로 표현되고, 다른 클래스들도 0의 확률이 아닌 일부 확률을 가짐**.  
즉, **Soft Label은 "절대적인 정답"이 아니라, 부드러운 확률 분포를 사용하여 학습하는 방식**입니다.  

---

## **✅ 3. 왜 Soft Label과 Hard Label이라는 용어를 사용할까?**
### **✔️ Hard Label이 "딱딱한 정답"인 이유**
- Hard Label은 **0 또는 1로만 표현**됩니다.  
- 즉, **딱딱하게(하드하게) 정답을 구분**합니다.  
- 클래스 간 유사도를 전혀 고려하지 않으며, 오직 "정답 vs. 오답"만 구분합니다.

✅ 예시:
```math
[1, 0, 0]  \quad  \text{(개 🐶)}
```
**→ 정답만 1, 나머지는 무조건 0 → "Hard" (단단한, 딱딱한 구조)**  

---

### **✔️ Soft Label이 "부드러운 정답"인 이유**
- Soft Label은 **확률 값이 부드럽게 분포**됩니다.  
- 0 또는 1이 아닌 **0.8, 0.1, 0.1 등으로 표현되므로 부드러운(Soft) 학습이 가능**.  
- 클래스 간 유사도를 반영하여 학습 성능이 향상될 수 있음.  

✅ 예시:
```math
[0.8, 0.1, 0.1]  \quad  \text{(개 🐶)}
```
**→ 정답(🐶)은 0.8, 다른 클래스(🐱, 🐰)도 0의 확률이 아님 → "Soft" (부드러운, 연속적인 분포)**  

---

## **✅ 4. Soft Label과 Hard Label의 차이점**
| | **Hard Label** | **Soft Label** |
|---|---|---|
| **정답 표현 방식** | 1 또는 0만 가능 | 확률 분포로 정답 표현 |
| **클래스 간 관계** | 고려하지 않음 (절대적인 정답만 반영) | 클래스 간 유사도를 반영 |
| **학습 안정성** | 데이터가 많아야 학습 가능 | 적은 데이터에서도 효과적 |
| **Teacher-Student 적용** | 사용되지 않음 | Teacher Model에서 생성한 Soft Label 사용 |
| **사용되는 곳** | 일반적인 딥러닝 학습 | Knowledge Distillation (KD) |

---

## **✅ 5. Soft Label을 활용하는 Knowledge Distillation (Slide 87)**
Knowledge Distillation에서는 **Soft Label을 사용하여 Student Model을 효과적으로 학습**시킵니다.  
이를 위해 **Softmax Temperature(온도 매개변수 \( T \))를 적용**하여 Soft Label을 생성합니다.

```math
p_T(z_i) = \frac{exp(z_i / T)}{\sum_j exp(z_j / T)}
```
- **\( T \)가 크면** → Softmax 값이 부드러워지고, 작은 확률 값도 더 반영됨.  
- **\( T \)가 작으면** → Hard Label과 유사하게 0 또는 1로 가까워짐.  

✅ **\( T \) 값 조정 예시**
- \( T = 1 \) → 일반적인 Softmax
- \( T = 5 \) → Softmax가 부드러워짐 (Soft Label 생성)
- \( T = 0.1 \) → Hard Label과 유사해짐

---

## **📌 결론**
- **Hard Label** → "딱딱한 정답" (1 또는 0으로만 표현)
- **Soft Label** → "부드러운 정답" (확률 분포 기반 정답)
- **Soft Label을 활용하면 작은 Student Model도 Teacher Model의 지식을 더 효과적으로 학습할 수 있음.**

이제 **Soft Label과 Hard Label의 개념이 확실히 이해되셨나요?** 😊  
추가 질문이 있으면 언제든지 물어봐 주세요! 🚀