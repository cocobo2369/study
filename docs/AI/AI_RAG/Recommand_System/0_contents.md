### 📌 **목차 및 내용 요약**
---
### **📖 1. Introduction (p.3)**
- 추천 시스템의 개요 및 정의
- 개인화된 추천과 비개인화된 추천의 차이
- 실제 사례: 쿠팡, 넷플릭스 추천 시스템 예시

---
### **📖 2. Classical Recommendation Methods (p.7-22)**
#### **✅ Utility Matrix & Rating Collection**
- 사용자와 아이템 간의 선호도를 표현하는 행렬
- 명시적(Explicit) 및 암묵적(Implicit) 피드백을 통한 데이터 수집

#### **✅ Content-Based Filtering (p.11-14)**
- 아이템 프로필을 기반으로 추천 (예: 영화 장르, 감독, 배우 등)
- 아이템 특징 벡터화 및 딥러닝 활용 가능
- **장점:** 사용자 개별 선호 반영, 신규 아이템 추천 가능
- **단점:** 유저 프로필 필요, 과적합(overspecialization) 문제 발생 가능

#### **✅ Collaborative Filtering (p.15-22)**
- 사용자-사용자 또는 아이템-아이템 간의 유사성을 활용한 추천
- **사용자 기반(User-User) 협업 필터링:**
  - 유사한 사용자를 찾아 선호도를 예측
  - 유사도 측정 방법: 자카드 유사도, 코사인 유사도 등
- **아이템 기반(Item-Item) 협업 필터링:**
  - 유사한 아이템을 찾아 추천
  - 아이템 특성이 명확하여 사용자 기반보다 신뢰성 높음
- **장점:** 콘텐츠 정보 불필요, 단순한 계산으로도 좋은 성능
- **단점:** 신규 아이템 추천 불가, 인기 있는 아이템만 추천하는 경향

---
### **📖 3. Latent Factor Models (p.25-34)**
#### **✅ Latent Factor 모델 개념**
- 유틸리티 행렬의 숨겨진 요인을 찾아 추천에 활용
- 행렬 분해(Matrix Factorization)를 통한 유저/아이템 특징 벡터 학습

#### **✅ UV Decomposition**
- 유틸리티 행렬 \( R \) 을 두 개의 행렬 \( U \) 와 \( V \) 로 분해
- \( U \) 와 \( V \) 의 내적으로 새로운 추천 점수 예측 가능

#### **✅ Neural Collaborative Filtering (NCF)**
- 기존 선형 행렬 분해의 한계를 극복하기 위해 신경망 도입
- 비선형성 활용하여 사용자-아이템 상호작용을 더 정교하게 모델링

#### **✅ Bayesian Personalized Ranking (BPR)**
- 명시적 점수가 아닌 암묵적 피드백을 다룰 때 활용
- 특정 아이템을 선호하는 정도를 순위 학습 방식으로 학습

---
### **📖 4. Sequential Recommendation Models (p.36-44)**
#### **✅ Sequential Recommendation 개념**
- 사용자의 과거 행동을 기반으로 다음 행동 예측
- 시간 순서(time-series) 및 그래프 구조 활용 가능

#### **✅ RNN 기반 추천**
- LSTM을 이용하여 순차적 사용자 패턴 학습
- \( N \)-way 분류 문제로 변환하여 예측 수행

#### **✅ Loss Function**
- 크로스 엔트로피 손실(Cross-Entropy Loss) 사용
- 아이템 개수가 많을 경우 Negative Sampling 활용 가능

---
### **📖 5. Summary (p.45-46)**
- 추천 시스템의 중요성 강조
- 협업 필터링이 가장 일반적인 방식
- 딥러닝 기반 모델이 발전하며 더 정교한 추천 가능

---
### 📌 **정리**
✅ **추천 시스템의 기본 개념**  
✅ **전통적인 추천 방식 (Content-Based, Collaborative Filtering)**  
✅ **잠재 요인 모델 (Latent Factor Models, Matrix Factorization, Neural CF)**  
✅ **순차 추천 모델 (Sequential Recommendation, RNN 기반 예측)**  