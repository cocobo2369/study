## **📌 Knowledge Distillation (지식 증류) 관련 슬라이드 상세 설명 (Slide 83~103)**  

Knowledge Distillation(KD, 지식 증류)는 **큰 모델(Teacher)에서 작은 모델(Student)로 지식을 전달하는 기법**입니다.  
이 기법을 사용하면 **경량화된 모델도 큰 모델과 유사한 성능을 유지하면서 효율적으로 학습할 수 있습니다.**  

---

## **✅ 1. Knowledge Distillation 개요 (Slide 83~85)**
### **🔹 (1) Knowledge Distillation이란?**
- 원래 딥러닝 모델은 **큰 모델(Teacher)**이 더 좋은 성능을 보입니다.  
- 하지만 **온디바이스 AI**에서는 **작은 모델(Student)이 필요**합니다.  
- **지식 증류(KD)**는 Teacher 모델에서 학습한 지식을 Student 모델로 전달하여, **작은 모델이 큰 모델의 성능을 따라잡도록 하는 기법**입니다.  

---

### **🔹 (2) Knowledge Distillation의 기본 개념**
✅ **Teacher Model (T) → Student Model (S)로 지식 전달**  
✅ **Soft Target (부드러운 정답, Soft Label)을 이용해 Student를 학습**  
✅ **온디바이스 환경에서 작은 모델을 고성능으로 최적화**  

---

## **✅ 2. Knowledge Distillation의 공식 (Slide 87)**
### **✅ Softmax 기반 지식 증류 공식**
일반적인 Softmax 함수는 다음과 같이 정의됩니다.

```math
p(z_i) = \frac{exp(z_i)}{\sum_j exp(z_j)}
```

하지만 Knowledge Distillation에서는 **Softmax Temperature(온도 조절 매개변수 \(T\))**를 사용하여 Soft Label을 생성합니다.

```math
p_T(z_i) = \frac{exp(z_i / T)}{\sum_j exp(z_j / T)}
```

- 여기서 \( T \)는 **온도(Temperature) 매개변수**입니다.  
- **\( T \)가 크면 Softmax가 더 부드러워지고, 작은 확률 값도 더 잘 반영됨.**  
- Softmax를 부드럽게 만들면, **모델이 더 많은 정보를 학습할 수 있음**.  

---

### **✅ Knowledge Distillation Loss (손실 함수)**
KD에서는 **Teacher와 Student의 확률 분포를 맞추는 KL Divergence(쌍방향 정보 거리)를 손실 함수로 사용**합니다.

```math
L_{\text{KD}} = \alpha L_{\text{CE}} + (1 - \alpha) T^2 KL(p_T^T, p_T^S)
```
- **\( L_{\text{CE}} \)**: 일반적인 Cross Entropy Loss (기본 정답과 Student의 예측 비교)
- **\( KL(p_T^T, p_T^S) \)**: Teacher와 Student의 확률 분포 차이를 최소화하는 KL Divergence Loss
- **\( \alpha \)**: Cross Entropy와 KD Loss 간의 가중치 조절 값
- **\( T \)**: Temperature (온도 매개변수)

---

## **✅ 3. Soft Label vs. Hard Label (Slide 90)**
**Teacher Model에서 Soft Label을 생성하여 Student Model을 학습**합니다.

✅ **Hard Label (일반적인 학습 방법)**  
- Cross Entropy를 사용하여 정답 라벨과 예측값을 직접 비교.  
- 예제) 🐶 (개) → `[1, 0, 0]` (원-핫 인코딩)  

✅ **Soft Label (Knowledge Distillation에서 사용)**  
- Teacher Model의 출력 분포를 학습.  
- 예제) 🐶 (개) → `[0.8, 0.1, 0.1]` (소프트 라벨)  

**Soft Label의 장점**  
- Hard Label보다 **추론 과정에서 더 많은 정보(클래스 간 관계)를 반영**할 수 있음.  
- Student Model이 Teacher Model의 **지식 구조를 더 효과적으로 학습 가능**.  

---

## **✅ 4. Knowledge Distillation의 주요 유형 (Slide 91~100)**
### **🔹 (1) Response-based KD (응답 기반 지식 증류, Slide 91)**
- **Teacher Model의 최종 출력 값(logits)을 Student Model이 학습**하는 방식.  
- 가장 기본적인 KD 방법으로, **Softmax Temperature 조절을 통해 Teacher의 Soft Label을 학습**.  

✅ **특징**  
- 구현이 간단하고 학습이 빠름.  
- 하지만 내부 Feature 정보는 활용하지 못함.  

---

### **🔹 (2) Feature-based KD (특징 기반 지식 증류, Slide 92)**
- **Teacher의 중간 Feature Map을 Student가 따라하도록 학습**.  
- Teacher의 Layer 출력을 **Hint Layer(힌트 레이어)**로 활용하여 Student가 학습할 수 있도록 함.  

✅ **특징**  
- Teacher의 내부 표현을 그대로 전달할 수 있어 성능 향상 가능.  
- 하지만 Student의 구조가 Teacher와 유사해야 하므로 **구조 제약이 존재**.  

---

### **🔹 (3) Matching Intermediate Features (Slide 93~95)**
- Teacher와 Student의 **중간 Feature Map을 정렬(Matching)하여 학습**.  
- 예를 들어, **Teacher의 중간 Layer에서 나오는 Feature를 Student가 그대로 복사하도록 유도**.  

✅ **적용 사례**  
- CNN에서 **Feature Map을 비교하여 Student가 Teacher의 Feature 표현을 학습**.  
- **R-CNN, MobileNet 같은 모델에서 자주 사용됨**.  

---

### **🔹 (4) Matching Sparsity Patterns (Slide 97)**
- **Teacher와 Student가 같은 활성화 패턴을 따르도록 학습**.  
- ReLU 활성화 이후의 **희소성(Sparsity) 패턴을 맞추는 방식**.  

✅ **적용 사례**  
- SparseNet, MobileNet 등의 **경량 모델 최적화에 활용**.  

---

## **✅ 5. Transformer 모델을 위한 Knowledge Distillation (Slide 101~103)**
- 최근 **BERT, GPT 같은 Transformer 모델에서도 KD가 활용됨**.  
- **Transformer 기반 KD 기법은 주로 Feature-based KD와 Attention-based KD로 구성됨**.  

✅ **MobileBERT (Slide 101)**
- BERT의 경량화 버전.  
- Teacher와 Student의 Feature Map 크기를 맞추고, Attention 정보를 함께 학습.  

✅ **Pruning + KD (Slide 103)**
- **Pruning으로 모델 크기를 줄인 후, KD를 적용하여 성능을 회복하는 방식**.  
- 경량 모델의 성능을 높이는 강력한 기법.  

---

## **📌 결론**
✅ **Teacher Model의 Soft Label을 활용하여 작은 Student Model을 학습시키는 기법**  
✅ **Softmax Temperature와 KL Divergence를 사용하여 Teacher의 확률 분포를 Student가 학습**  
✅ **Feature Matching, Response Matching, Sparsity Matching 등의 다양한 방법 활용 가능**  
✅ **MobileBERT, Pruned LLM 같은 경량화된 AI 모델에 필수적인 기술**  