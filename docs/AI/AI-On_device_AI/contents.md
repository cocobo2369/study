### 📌 목차 및 페이지 안내

다음은 **삼성전자 AI 전문가 교육 - On-Device AI** 문서의 내용을 주제별로 정리한 목차입니다. 각 주제의 슬라이드 번호를 함께 안내하므로, 필요한 내용을 쉽게 찾을 수 있습니다.

---

## 1️⃣ **LLM Pruning (대규모 언어 모델 가지치기)**  
- **On-Device AI 응용 소개** - 슬라이드 1  
- **Outline (전체 개요)** - 슬라이드 2  
- **Pruning Granularities (가지치기 세분화)** - 슬라이드 3  
- **Vector-Wise Sparsity (벡터 단위 희소성)** - 슬라이드 4  
- **N:M Sparsity (N:M 희소성 개념)** - 슬라이드 5-6  
- **Taylor Expansion Analysis on Pruning Error (테일러 전개 기반 가지치기 오차 분석)** - 슬라이드 7  
- **OBD: Second-Order-based Pruning (2차 미분 기반 가지치기)** - 슬라이드 8-9  
- **Optimal Brain Surgeon (OBS, 최적 신경망 가지치기)** - 슬라이드 10-11  
- **LLM Pruning 요약** - 슬라이드 12  
- **SparseGPT (희소성 기반 GPT 최적화)** - 슬라이드 13-15  
- **Wanda (간단한 크기 기반 가지치기)** - 슬라이드 16-17  
- **Parameter-Efficient Fine-Tuning (PEFT, 효율적 파라미터 미세 조정)** - 슬라이드 18  
- **LoRA (저차원 적응 방식)** - 슬라이드 19-20  
- **SPP: Sparsity-Preserved PEFT (희소성을 유지한 미세 조정 기법)** - 슬라이드 21-23  

---

## 2️⃣ **LLM Quantization (대규모 언어 모델 양자화)**
- **LLM Quantization 개요** - 슬라이드 24  
- **Post-Training Quantization (PTQ, 사후 훈련 양자화)** - 슬라이드 25  
- **ZeroQuant (마이크로소프트의 ZeroQuant 기법)** - 슬라이드 26-28  
- **LLM.int8() (GPT-3 8비트 양자화, bitsandbytes 라이브러리)** - 슬라이드 29  
- **SmoothQuant (NVIDIA, MIT의 SmoothQuant 기법)** - 슬라이드 30-34  
    - f
- **OmniQuant (다방향 보정 양자화)** - 슬라이드 35  
- **QuaRot (회전 기반 양자화 기법)** - 슬라이드 36  
- **Weight-Only Quantization (가중치만 양자화)** - 슬라이드 37  
- **GPTQ (Generative Pretrained Transformers Quantization, GPT 전용 양자화)** - 슬라이드 38-39  
- **SpQR (희소성과 양자화를 결합한 기법)** - 슬라이드 40-42  
- **AWQ (활성화 기반 가중치 양자화)** - 슬라이드 43-45  
- **QLoRA (LoRA + Quantization 기법)** - 슬라이드 46  
- **NF4 Quantization (NormalFloat 4비트 양자화)** - 슬라이드 47  
- **Double Quantization (2중 양자화 기법)** - 슬라이드 48  
- **Distillation-Assisted Quantization (지식 증류를 활용한 양자화)** - 슬라이드 49  

---

## 3️⃣ **Efficient Inference (효율적인 추론 기법)**
- **Efficient Transformer (효율적인 트랜스포머 개요)** - 슬라이드 50  
- **Fixed Sparse Attention (고정 희소성 주의 기법: Longformer, Big Bird)** - 슬라이드 51  
- **Dynamic Sparsity - SpAtten (동적 희소성 기반 주의 기법)** - 슬라이드 52  
- **Deja Vu (맥락 기반 희소성 예측 기법)** - 슬라이드 53  
- **Conditional Computation (조건부 연산 기법)** - 슬라이드 54  
- **Speculative Decoding (추론 속도 향상을 위한 예측 기반 디코딩 기법)** - 슬라이드 55-57  
- **H2O (효율적인 KV 캐시 관리 기법)** - 슬라이드 58-59  
- **Operator Fusion (연산 최적화)** - 슬라이드 60  
- **FlashAttention (GPU 메모리 효율적 활용을 위한 FlashAttention 기법)** - 슬라이드 61-62  
- **Patch-based Inference (패치 기반 추론 기법, MobileNetV2 적용 사례)** - 슬라이드 63-66  

---

## 4️⃣ **Efficient Vision Transformer (효율적인 비전 트랜스포머)**
- **Efficient Vision Transformer 개요** - 슬라이드 67  
- **ViT (Vision Transformer 기본 개념)** - 슬라이드 68  
- **CNN vs ViT (합성곱 신경망과 비전 트랜스포머 비교)** - 슬라이드 69-70  
- **Contents (내용 개요)** - 슬라이드 71-72  
- **CvT (Convolutional Vision Transformer, CNN과 트랜스포머 결합 기법)** - 슬라이드 73  
- **CMT (Convolution Meets Transformer)** - 슬라이드 74  
- **MobileViT (애플의 모바일 친화적인 ViT 기법)** - 슬라이드 75  
- **MobileViT2 - Separable Self-Attention** - 슬라이드 76  
- **FasterViT (엔비디아의 FasterViT 기법)** - 슬라이드 77-80  
- **Alternative to MHSA (다중 헤드 자가 주의 대체 기법)** - 슬라이드 81  
- **PoolFormer (풀링 기반 트랜스포머)** - 슬라이드 82  
  - pooling은 weight가 없다. -> 모델 사이즈 줄일 수 있다
  - 결합법칙에 의해 QK 보다 KV 연산을 우선해서 매트릭스의 차원을 줄여 연산을 줄일 수 있다.
- **EfficientViT (효율적인 다중 스케일 주의 기법)** - 슬라이드 83-85  
  - RELU가 성능을 좀 떨어트리긴 한다.
    - Conv layer를 추가하여 해소

---

## 5️⃣ **Token Reduction (토큰 감소 기법)**
- **Token Reduction 개요** - 슬라이드 86  
- **Dynamic Token Pruning (동적 토큰 가지치기)** - 슬라이드 87-89  
- **Token Fusion (토큰 결합 기법)** - 슬라이드 90  
- **SPViT (토큰 선택을 활용한 비전 트랜스포머 가속화 기법)** - 슬라이드 91  
- **Not All Patches are What You Need (필요한 패치만 선택하는 기법)** - 슬라이드 92  
- **Token Merging (유사한 토큰을 병합하는 기법)** - 슬라이드 93  