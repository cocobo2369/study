정규화
    - overfitting 제거
    - 속도 증가
    - 분도 균일


# On-device AI를 위해 한 거
1. 없애고 -> 가중치 없애기 pruning
2. 줄이고 -> 메모리 줄이기 quantization
3. 모방하고 -> LLM 모방   Knowledge Distillation








## **📌 1. On-Device AI 개요 (On-Device AI Overview)**
- **On-Device AI** (온디바이스 AI) → **Edge AI, AI on local devices**
- **DNN (Deep Neural Networks)** → **심층 신경망**
- **CNN (Convolutional Neural Networks)** → **합성곱 신경망**
- **Transformer** → **트랜스포머 모델**
- **LLM (Large Language Models)** → **대형 언어 모델**
- **Multi-modal LLM** → **멀티모달 대형 언어 모델**
- **LLM Operations** → **대형 언어 모델 연산**
  - **Prefill phase** → **사전 채우기 단계**
  - **Decode phase** → **디코딩 단계**
  - **Masked GEMM** → **마스킹된 행렬 연산**
  - **KV Cache** → **키-값 캐시**
- **AI 모델 크기 문제** (AI Model Size Challenges) → **Model scaling issues, memory bottlenecks**
- **Computing Power** (연산 성능) → **Processing capabilities (GPU, TPU, NPU, PIM)**
- **Cloud AI vs. On-Device AI** → **클라우드 AI vs. 온디바이스 AI**
- **On-Device AI PC** → **AI 가속 노트북 (Snapdragon X, Intel Core Ultra, AMD Ryzen AI, Apple M4)**
- **Smartphone AI** → **스마트폰 AI 모델 (메모리 & 연산 성능 비교)**
- **AI 모델 계산량** (AI Model Computation) → **Parameters, Activations, FLOPs**
- **LLM Inference** → **대형 언어 모델 추론 최적화**
- **On-Device AI Enablers** → **온디바이스 AI 지원 기술 (하드웨어, 프레임워크, 모델 경량화)**

---

## **📌 2. 모델 경량화 기법 (Model Optimization Techniques)**
### **🔹 (1) Network Pruning (네트워크 가지치기)**
- **Pruning 개념** (Pruning Concept) → **Removing redundant weights**
- **Pruning 종류** (Types of Pruning) → **Magnitude-based, Structured, Iterative**
- **Fine-tuning** (미세 조정) → **Restoring accuracy after pruning**
- **Pruning Granularities** (가지치기 세분화) → **Fine-grained vs. Coarse-grained**
- **Parameter Selection** (매개변수 선택) → **Choosing less important weights**
- **Sparse Matrix** (희소 행렬) → **Compressed Sparse Row (CSR), Compressed Sparse Column (CSC)**
- **Sparse Architecture** (희소 아키텍처) → **Input Sparsity, Weight Sparsity**

### **🔹 (2) Quantization (양자화)**
- **Quantization 개념** (Quantization Concept) → **Reducing data precision**
- **Numeric Data Types** (수치 데이터 타입) → **FP32 → FP16 → INT8 → INT4 → Binary**
- **Static vs. Dynamic Quantization** → **정적 vs. 동적 양자화**
- **Learned Quantization** (학습된 양자화) → **Training-based optimal quantization**
- **Uniform vs. Non-Uniform Quantization** → **균등 vs. 비균등 양자화**
- **Linear Quantization** (선형 양자화) → **Scaling-based quantization**
- **Asymmetric vs. Symmetric Quantization** → **비대칭 vs. 대칭 양자화**
- **Per-Channel Weight Quantization** → **채널별 가중치 양자화**
- **Post-Training Quantization (PTQ)** → **사전 학습 후 양자화**
- **Quantization-Aware Training (QAT)** → **양자화 인식 학습**
- **Gradient Handling** (기울기 처리) → **Straight Through Estimator (STE)**

### **🔹 (3) Knowledge Distillation (지식 증류)**
- **KD 개념** (Knowledge Distillation Concept) → **Transferring knowledge from teacher to student model**
- **Soft Label vs. Hard Label** → **소프트 라벨 vs. 하드 라벨**
- **Response-based KD** → **출력값 정렬 방식 증류**
- **Feature-based KD** → **특징 기반 증류**
- **Matching Patterns** → **희소성, 관계 정보 정렬**
- **KD for Transformer** → **MobileBERT, IB-BERT**

---

## **📌 3. 최신 On-Device AI 기술 (Latest On-Device AI Technologies)**
- **Small LLMs** → **경량 대형 언어 모델 (Gemma, Llama3.2, MobileLLM, Phi-3.5)**
- **Google Gemini** → **안드로이드 AI Core, Gemini Nano**
- **Llama.cpp** → **CPU+GPU 하이브리드 모델 실행**
- **MLC-LLM** → **경량 모델 최적화 프레임워크**
- **EdgeTPU & Hailo-8** → **온디바이스 AI 가속기**
- **Model Compression Techniques** → **모델 압축 및 최적화**