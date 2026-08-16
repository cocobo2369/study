# 6개 실전문제 유형과 모델 파라미터 총정리 — DNME

> 기준 파일: `00_Practice/00_trying/02`의 `01_question.ipynb` ~ `06_questions.ipynb`  
> 목적: 문제를 읽자마자 유형을 판별하고, 모델 생성 → `fit` → `predict` → 평가까지 막힘없이 작성하기

시험 직전에는 [DNME 시험 직전 1페이지](01_DNME_시험직전_1페이지.md)를 먼저 보고, 이해가 필요한 항목만 이 상세본에서 찾아본다.

원본 풀이: [Set 1](01_question.ipynb) · [Set 2](02_question.ipynb) · [Set 3](03_question.ipynb) · [Set 4](04_question.ipynb) · [Set 5](05_question.ipynb) · [Set 6](06_questions.ipynb)

## 목차

1. [먼저 외울 전체 지도](#1-먼저-외울-전체-지도)
2. [6개 세트 18문항 유형표](#2-6개-세트-18문항-유형표)
3. [DNME를 정확히 쓰는 법](#3-dnme를-정확히-쓰는-법)
4. [`train_test_split` 완전 정리](#4-train_test_split-완전-정리)
5. [정규화와 표준화](#5-정규화와-표준화)
6. [모델 체계와 파라미터·fit·predict 비교](#6-모델-체계와-파라미터fitpredict-비교)
7. [모델 체계 순서별 시험 코드](#7-모델-체계-순서별-시험-코드)
8. [비모델링 문제 유형](#8-비모델링-문제-유형)
9. [실전 함정과 확인 순서](#9-실전-함정과-확인-순서)
10. [시험 직전 암기장](#10-시험-직전-암기장)

---

## 1. 먼저 외울 전체 지도

### 모델링 문제의 기본 뼈대

```text
D: Data       X/y 선택 → 범주형 변환 → Train/Test 분할
N: Normalize  Train으로 fit → Train은 fit_transform → Test는 transform
M: Modeling   모델 생성 → model.fit(X_train, y_train) → model.predict(X_test)
E: Error      실제값과 예측값으로 지표 계산
```

> **암기:** `D에서 나누고, N에서 맞추고, M에서 배우고, E에서 채점한다.`

### DNME가 항상 네 단계 모두 필요한 것은 아니다

| 문제 | D | N | M | E |
|---|---|---|---|---|
| K-Means | X만 필요, y 없음 | 매우 중요 | `fit`, `predict` | `silhouette_score` |
| Linear Regression | 필요 | 조건에 따라 | `fit`, `predict` | RMSE, R² |
| Logistic Regression | 필요 | 문제에서 요구 | `fit`, 필요 시 `predict` | F1 또는 `exp(coef_)` |
| Naive Bayes | 필요 | 모델 종류에 따라 | `fit`, `predict` | Accuracy, F1 |
| Decision Tree 회귀·분류 | 필요 | 보통 불필요 | `fit`, `predict` | RMSE 또는 분류지표 |
| Random Forest 회귀·분류 | 필요 | 보통 불필요 | `fit`, 필요 시 `predict` | 예측지표 또는 중요도 |
| k-NN 회귀·분류 | 필요 | 매우 중요 | `fit`, `predict` | RMSE 또는 Accuracy |

> **핵심:** `N`이 비어도 DNME가 틀린 것이 아니다. 문제에서 정규화를 요구하지 않거나 모델이 스케일에 둔감하면 생략한다.

---

## 2. 6개 세트 18문항 유형표

### 한눈에 보는 문제 분류

| 세트 | 문항 | 문제 유형 | 핵심 도구 | 마지막에 구할 것 |
|---:|---:|---|---|---|
| 1 | Q1 | 여러 열 문자열 통합·정규식 추출 | 문자열 합치기, `str.extract()` | 60Hz 개수 |
| 1 | Q2 | 문자열 조건별 평균 비교 | `str.contains()`, `loc`, `mean()` | 두 평균 차이의 절댓값 |
| 1 | Q3 | 파생변수 + Random Forest 회귀 | `RandomForestRegressor` | 가장 큰 변수 중요도 이름 |
| 2 | Q1 | 유효 범주 필터 + 행별 합계 | `isin`, `all(axis=1)`, `sum(axis=1)` | 빈도 비율 |
| 2 | Q2 | 파생변수 + 상관분석 | `//`, `corr()`, 대각선 제거 | 최대 절대 상관계수 |
| 2 | Q3 | 이진분류 전체 DNME | Min-Max, 로지스틱 회귀 | F1-score |
| 3 | Q1 | 이상치 조건 + 파생지표 | 평균, 표준편차, Boolean 조건 | 이상치 집단 지표 평균 |
| 3 | Q2 | 조건 제외 + 상관분석 | `loc`, `corr()['sales']` | 최대 절대 상관계수 |
| 3 | Q3 | 후보 k 반복 비교 | k-NN 회귀, RMSE | RMSE가 가장 작은 k |
| 4 | Q1 | 2단계 집계 | `groupby().sum()`, `value_counts()` | 최대 매출 상품의 최다 구매 직업 |
| 4 | Q2 | 고객 단위 고유 개수 집계 | 결측 대체, 문자열 결합, `nunique()` | 결혼 여부별 평균 차이 |
| 4 | Q3 | 고객 단위 집계 + 군집화 | OHE, Min-Max, K-Means | Silhouette score |
| 5 | Q1 | 그룹별 상관분석 | `groupby().apply()`, `corr()` | 그룹 중 최대 상관계수 |
| 5 | Q2 | 최적 군집 수 탐색 | StandardScaler, K-Means 반복 | 최적 군집의 원자료 평균 최댓값 |
| 5 | Q3 | 조건 기반 분할 + 회귀 | 결정나무 회귀 | RMSE |
| 6 | Q1 | 그룹별 비율 비교 | `groupby`, 평균 또는 빈도/개수 | 두 비율의 비 |
| 6 | Q2 | 더미변수 + 로지스틱 해석 | `LogisticRegression`, `exp(coef_)` | 최대 오즈비 |
| 6 | Q3 | 지정 열 기반 분할 + k-NN 분류 | `KNeighborsClassifier` | 정확도 |

### 문제를 읽고 5초 안에 유형 찾기

| 문제의 표현 | 바로 떠올릴 것 |
|---|---|
| “몇 개인가” | Boolean 조건의 `.sum()` 또는 `value_counts()` |
| “평균 차이” | 집단별 `.mean()` 후 `abs(A - B)` |
| “가장 상관관계가 큰” | `corr().abs()`, 자기상관 1 제외 |
| “변수 중요도” | Random Forest `feature_importances_` |
| “오즈비” | 로지스틱 `np.exp(model.coef_)` |
| “예측 성능” | `predict()` 후 실제값과 지표 계산 |
| “최적 k” | 후보 k 반복 → 지표 저장 → `idxmin()` 또는 `idxmax()` |
| “군집” | y 없음, 스케일링 → K-Means → Silhouette |
| “~별로” | `groupby()`를 먼저 의심 |

---

## 3. DNME를 정확히 쓰는 법

## D — Data

### D에서 해야 할 일

1. 원본을 복사한다.
2. 문제 조건대로 행을 포함·제외한다.
3. 파생변수를 만든다.
4. 범주형 변수를 숫자로 바꾼다.
5. X와 y를 나눈다.
6. 필요하면 Train/Test를 나눈다.

```python
work = base.copy()

X = work[cols_X].copy()
y = work['target'].copy()       # 종속변수 1개는 Series

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=123
)
```

### X와 y 암기

```text
X = 문제를 풀기 위해 보는 정보 = 독립변수 = feature
y = 맞혀야 하는 정답          = 종속변수 = target
```

- `X`는 여러 열이므로 보통 DataFrame이다.
- `y`가 한 열이면 `df['target']`처럼 Series로 만든다.
- `df[['target']]`은 2차원 DataFrame이므로 불필요한 경고가 날 수 있다.

### D 단계의 가장 흔한 실수

- 문제에 적힌 독립변수를 하나 빠뜨리거나 비슷한 변수를 잘못 넣는다.
- y 또는 ID를 X에 포함한다.
- 범주형 문자열을 숫자로 바꾸지 않고 모델에 넣는다.
- `dropna()` 또는 조건 필터 후 `.copy()`를 하지 않는다.
- 파생변수의 `/`와 `//`를 혼동한다.
- `pd.get_dummies()` 후 열 개수와 열 순서를 확인하지 않는다.

> **D 암기:** `조건 → 파생 → 인코딩 → X/y → 분할`.

## N — Normalize

```python
scaler = MinMaxScaler()
X_train_n = scaler.fit_transform(X_train)
X_test_n = scaler.transform(X_test)
```

```text
fit       = 기준을 배운다.
transform = 배운 기준으로 바꾼다.
```

> **N 암기:** `Train은 fit_transform, Test는 transform.`

### 왜 Test에 `fit_transform()`을 쓰면 안 되는가

Test의 최소·최대 또는 평균·표준편차를 미리 알게 되므로 데이터 누수가 발생한다. 시험 데이터는 아직 보지 못한 미래 데이터처럼 취급해야 한다.

## M — Modeling

```python
model = 모델클래스(문제에서 지정한 파라미터)
model.fit(X_train_n, y_train)
y_pred = model.predict(X_test_n)
```

```text
생성자 파라미터 = 모델의 학습 규칙을 정한다.
fit(X, y)       = X와 정답 y의 관계를 학습한다.
predict(X)      = 학습된 규칙으로 새 X의 답을 만든다.
```

## E — Error 또는 Evaluation

```python
score = 평가함수(y_test, y_pred)
```

| 문제 | 지표 | 선택 방향 |
|---|---|---|
| 회귀 오차 | RMSE | 작을수록 좋음 |
| 이진분류 | F1-score | 클수록 좋음 |
| 분류 정확도 | Accuracy | 클수록 좋음 |
| 군집 | Silhouette score | 클수록 좋음 |
| 변수 중요도 | `feature_importances_` | 가장 큰 변수 선택 |
| 오즈비 | `np.exp(coef_)` | 문제에서 요구한 최댓값 선택 |

> **E 암기:** `Error는 작게, Score는 크게.`

---

## 4. `train_test_split` 완전 정리

### 기본형

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=123
)
```

### 반환 순서

```text
입력: X, y
출력: X_train, X_test, y_train, y_test
      └─ X 두 개 ─┘  └─ y 두 개 ─┘
```

> **암기:** `큰 X 둘, 작은 y 둘 / 각각 train 먼저 test 나중`.

### 주요 파라미터

| 파라미터 | 의미 | 문제 예시 |
|---|---|---|
| `test_size=0.3` | Test를 30%로 지정 | 세트 2 Q3의 7:3 |
| `train_size=0.7` | Train을 70%로 지정 | `test_size=0.3`과 같은 의미 |
| `train_size=0.8` | Train을 80%로 지정 | 세트 3 Q3의 8:2 |
| `random_state=123` | 무작위 분할 결과 고정 | seed 123 |
| `stratify=y` | y의 클래스 비율을 비슷하게 유지 | 문제에서 요구하거나 불균형 분류 시 고려 |
| `shuffle=True` | 분할 전 데이터를 섞음 | 기본값 |

### `random_state`의 의미

- 점수를 높이는 숫자가 아니다.
- 같은 데이터와 같은 seed이면 같은 행이 Train/Test에 들어가도록 고정한다.
- 문제에 seed가 있으면 정확히 그 값을 사용한다.

### `train_test_split`을 사용하지 않는 분할

문제가 분할 규칙을 직접 주면 Boolean 조건으로 나눈다.

```python
# 세트 5 Q3: ID가 4의 배수인지로 분할
train = base.loc[base['CUST_ID'] % 4 != 0].copy()
test  = base.loc[base['CUST_ID'] % 4 == 0].copy()

# 세트 6 Q3: Xgrp 값으로 분할
train = job2.loc[job2['Xgrp'] == 'train'].copy()
test  = job2.loc[job2['Xgrp'] == 'test'].copy()
```

> **시험 원칙:** 문제에서 분할 기준을 직접 지정하면 `train_test_split`을 쓰지 않는다.

---

## 5. 정규화와 표준화

### Min-Max 정규화

```python
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
X_train_n = scaler.fit_transform(X_train)
X_test_n = scaler.transform(X_test)
```

$$x' = \frac{x-x_{min}}{x_{max}-x_{min}}$$

- 일반적으로 값을 0~1 범위에 맞춘다.
- 세트 2 로지스틱 회귀, 세트 3 k-NN 회귀, 세트 4 K-Means에서 사용했다.

### Z-score 표준화

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_n = scaler.fit_transform(X)
```

$$z = \frac{x-\bar{x}}{s}$$

- 평균 0, 표준편차 1에 가깝게 맞춘다.
- 세트 5 Q2 K-Means에서 문제 조건으로 사용했다.

### 어떤 모델에 특히 필요한가

| 모델 | 스케일링 | 이유 |
|---|---|---|
| k-NN | 매우 중요 | 거리로 이웃을 정함 |
| K-Means | 매우 중요 | 거리로 군집과 중심을 정함 |
| 로지스틱 회귀 | 권장·문제 조건 우선 | 최적화 안정성과 규제의 공정성 |
| 의사결정나무 | 보통 불필요 | 값의 순서와 분할점 사용 |
| Random Forest | 보통 불필요 | 여러 나무의 분할을 사용 |

> **암기:** `거리를 쓰는 K 둘(k-NN, K-Means)은 반드시 스케일을 의심한다.`

### 군집화에서 Train/Test가 없는 경우

세트 4·5의 K-Means는 전체 고객을 군집화하므로 다음처럼 전체 X에 적합한다.

```python
X_n = scaler.fit_transform(X)
```

이는 평가 데이터 정보를 누출한 것이 아니라, 애초에 별도의 Test Set 없이 전체 대상을 군집화하라는 문제이기 때문이다.

---

## 6. 모델 체계와 파라미터·fit·predict 비교

### 관리 순서

```text
모델
├─ 비지도학습
│  └─ 군집
│     └─ K-Means
└─ 지도학습
   ├─ 회귀
   │  └─ Linear Regression
   ├─ 분류
   │  ├─ Logistic Regression
   │  └─ Naive Bayes
   └─ 회귀·분류 공용
      ├─ Tree
      │  ├─ Decision Tree
      │  └─ Random Forest
      └─ k-NN
         ├─ KNeighborsRegressor
         └─ KNeighborsClassifier
```

> **암기:** `비지도는 K-Means 하나, 지도는 회귀·분류·공용 세 갈래.`

### 6개 실전 세트 출제 여부

| 학습 | 목적 | 모델 | 6개 세트 출제 |
|---|---|---|---|
| 비지도 | 군집 | K-Means | 세트 4 Q3, 세트 5 Q2 |
| 지도 | 회귀 | Linear Regression | 직접 출제 없음·체계 보충 |
| 지도 | 분류 | Logistic Regression | 세트 2 Q3, 세트 6 Q2 |
| 지도 | 분류 | Naive Bayes | 직접 출제 없음·체계 보충 |
| 지도 | 회귀·분류 | Decision Tree | 회귀: 세트 5 Q3 |
| 지도 | 회귀·분류 | Random Forest | 회귀 중요도: 세트 1 Q3 |
| 지도 | 회귀·분류 | k-NN | 회귀: 세트 3 Q3, 분류: 세트 6 Q3 |

### 모델 전체 비교
- random_state 사용(로/케이민/트 - 초코민토!)
    - 로지스틱 회귀
    - 케이민즈
    - 트리류

| 학습 방식 | 문제 유형 | 모델 | 클래스 | `random_state` | 그 외 핵심 파라미터 | `fit` | `predict` 뒤 대표 평가 |
|---|---|---|---|:---:|---|---|---|
| 비지도 | 군집 | K-Means | `KMeans` | O | `n_clusters` | `fit(X)` | Silhouette |
| 지도 | 회귀 | 선형회귀 | `LinearRegression` | X | `fit_intercept` | `fit(X,y)` | RMSE, R² |
| 지도 | 분류 | 로지스틱 회귀 | `LogisticRegression` | O | `C`, `max_iter`, `solver` | `fit(X,y)` | F1, Accuracy, 오즈비 |
| 지도 | 분류 | 나이브베이즈 | `GaussianNB` | X | `var_smoothing` | `fit(X,y)` | F1, Accuracy |
| 지도 | 회귀·분류 | 의사결정나무 | `DecisionTreeRegressor/Classifier` | O | `max_depth`, `min_samples_split` | `fit(X,y)` | 회귀 RMSE / 분류 F1 |
| 지도 | 회귀·분류 | 랜덤포레스트 | `RandomForestRegressor/Classifier` | O | `n_estimators`, `max_depth` | `fit(X,y)` | 예측지표, 중요도 |
| 지도 | 회귀·분류 | k-NN | `KNeighborsRegressor/Classifier` | X | `n_neighbors`, `weights`, `metric`, `p` | `fit(X,y)` | 회귀 RMSE / 분류 Accuracy |

> `O`는 해당 클래스가 `random_state` 파라미터를 받을 수 있음을, `X`는 받지 않음을 뜻한다. 시험에서는 `O`인 모델이라도 문제에서 seed를 지정했을 때 그 값을 넣는 것을 우선한다.

### `fit`, `predict`, 속성의 차이

```python
# 지도학습: 정답 y가 있다.
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# 비지도학습 K-Means: 정답 y가 없다.
model.fit(X_scaled)
cluster = model.predict(X_scaled)
```

| 원하는 답 | 필요한 흐름 |
|---|---|
| 새 값 예측 | `fit` → `predict` |
| Random Forest 변수 중요도 | `fit` → `feature_importances_` |
| Logistic 오즈비 | `fit` → `np.exp(coef_)` |
| K-Means 군집 번호 | `fit` → `predict` 또는 `fit_predict` |

> **암기:** `지도는 fit(X,y), 비지도 군집은 fit(X).`

---

## 7. 모델 체계 순서별 시험 코드

## 7.1 비지도학습 → 군집 → K-Means

### 고정된 군집 수

세트 4 Q3 유형이다.

```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

model = KMeans(n_clusters=7, random_state=123)
cluster = model.fit_predict(X_n)

score = silhouette_score(X_n, cluster)
```

- `n_clusters`: 만들 군집 수
- `random_state`: 초기 중심 선택 고정
- y가 없으므로 `fit(X)`다.
- `silhouette_score(X, cluster)`는 클수록 군집이 잘 분리된 것이다.

### 최적 군집 수

세트 5 Q2 유형이다.

```python
scores = {}
labels = {}

for k in [2, 3, 4, 5]:
    model = KMeans(n_clusters=k, random_state=1234)
    cluster = model.fit_predict(X_n)
    scores[k] = silhouette_score(X_n, cluster)
    labels[k] = cluster

best_k = pd.Series(scores).idxmax()
raw_data['cluster'] = labels[best_k]
answer = raw_data.groupby('cluster')['ONEOFF_PURCHASES'].mean().max()
```

> **암기:** `정규화로 군집, Silhouette로 k 선택, 원자료로 군집 해석.`

## 7.2 지도학습 → 회귀 → Linear Regression

6개 세트에는 직접 나오지 않았지만 회귀의 기준 모델이다.

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

model = LinearRegression(fit_intercept=True)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

rmse = mean_squared_error(y_test, y_pred) ** 0.5
r2 = r2_score(y_test, y_pred)
```

- `fit_intercept=True`: 절편을 추정한다.
- `model.coef_`: 각 독립변수의 회귀계수
- `model.intercept_`: 절편
- 연속형 y를 예측한다.

> **암기:** `선형회귀 = 연속 y, 계수 해석, RMSE·R² 평가.`

## 7.3 지도학습 → 분류 → Logistic Regression

### 클래스 예측과 F1

세트 2 Q3 유형이다.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score

model = LogisticRegression(random_state=123)
model.fit(X_train_n, y_train)
y_pred = model.predict(X_test_n)

f1 = f1_score(y_test, y_pred)
```

### 계수 해석과 오즈비

세트 6 Q2 유형이다.

```python
model = LogisticRegression(
    C=100000,
    max_iter=1000,
    solver='liblinear',
    random_state=123
)
model.fit(X, y)

odds_ratio = pd.Series(np.exp(model.coef_[0]), index=X.columns)
answer = odds_ratio.max()
```

```text
C            규제의 역수: 클수록 규제 약함
max_iter     최대 반복 횟수
solver       계수를 찾는 계산 방법
random_state 무작위 과정의 결과 고정
```

> **암기:** `Logistic은 이름은 회귀지만 목적은 분류, exp(계수)는 오즈비.`

## 7.4 지도학습 → 분류 → Naive Bayes

6개 세트에는 직접 나오지 않았지만 분류 체계에 함께 둔다.

```python
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

model = GaussianNB(var_smoothing=1e-9)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
```

- `GaussianNB`: 연속형 특성이 클래스별 정규분포를 따른다고 가정
- `var_smoothing`: 분산이 0에 가까울 때 계산을 안정화
- `random_state`가 없다.

자료형에 따른 대표 선택:

| 데이터 | 모델 |
|---|---|
| 연속형 수치 | `GaussianNB` |
| 단어 빈도·횟수 | `MultinomialNB` |
| 0/1 존재 여부 | `BernoulliNB` |

> **암기:** `Naive Bayes = 사전확률 × 특성별 우도, 특성은 조건부 독립이라고 단순화.`

## 7.5 지도학습 → 회귀·분류 → Tree

### Decision Tree

```python
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier

# 연속형 y
reg = DecisionTreeRegressor(max_depth=None, random_state=1234)
reg.fit(X_train, y_train)
pred_reg = reg.predict(X_test)

# 범주형 y
clf = DecisionTreeClassifier(max_depth=None, random_state=1234)
clf.fit(X_train, y_train)
pred_clf = clf.predict(X_test)
```

세트 5 Q3은 `DecisionTreeRegressor(random_state=1234)`와 RMSE를 사용한다.

```text
max_depth         나무의 최대 깊이
min_samples_split 노드를 나누기 위한 최소 표본 수
min_samples_leaf  잎에 남겨야 하는 최소 표본 수
random_state      무작위 결과 고정
```

### Random Forest

```python
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

reg = RandomForestRegressor(n_estimators=100, random_state=123)
reg.fit(X_train, y_train)
pred_reg = reg.predict(X_test)

clf = RandomForestClassifier(n_estimators=100, random_state=123)
clf.fit(X_train, y_train)
pred_clf = clf.predict(X_test)
```

세트 1 Q3처럼 변수 중요도만 물으면 `predict()`는 필요 없다.

```python
model = RandomForestRegressor(random_state=123)
model.fit(X, y)

importance = pd.Series(model.feature_importances_, index=X.columns)
answer = importance.idxmax()
```

```text
n_estimators 여러 나무의 개수
max_depth    각 나무의 최대 깊이
random_state 부트스트랩·특성 선택 결과 고정
n_jobs       병렬 계산에 사용할 작업 수
```

> **Tree 암기:** `Decision Tree 한 그루, Random Forest 여러 그루의 투표·평균.`

## 7.6 지도학습 → 회귀·분류 → k-NN

### k-NN Regression

세트 3 Q3 유형이다.

```python
from sklearn.neighbors import KNeighborsRegressor

scores = {}
for k in [3, 5, 7, 9, 11]:
    model = KNeighborsRegressor(n_neighbors=k)
    model.fit(X_train_n, y_train)
    y_pred = model.predict(X_test_n)
    scores[k] = mean_squared_error(y_test, y_pred) ** 0.5

best_k = pd.Series(scores).idxmin()
```

### k-NN Classification

세트 6 Q3 유형이다.

```python
from sklearn.neighbors import KNeighborsClassifier

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train_n, y_train)
y_pred = model.predict(X_test_n)

accuracy = accuracy_score(y_test, y_pred)
```

```text
n_neighbors 사용할 이웃 수
weights     uniform이면 동등 투표, distance면 가까운 이웃에 큰 가중치
metric      거리 계산 방법
p=2         Minkowski 거리에서 Euclidean
```

- 회귀는 이웃 y의 평균, 분류는 이웃 클래스의 투표를 사용한다.
- 무작위 학습이 아니므로 `random_state`가 없다.
- 거리에 민감하므로 정규화가 중요하다. 단, 시험 답은 문제의 지시를 우선한다.

> **k-NN 암기:** `같은 이웃, 숫자는 평균하여 회귀, 범주는 투표하여 분류.`

---

## 8. 비모델링 문제 유형

## 8.1 문자열이 여러 열에 흩어진 유형

```python
cols = ['Picture_quality', 'Speaker', 'Frequency']

combined = df[cols].fillna('').agg(' '.join, axis=1)
hz = combined.str.extract(r'(\d{2,3})\s*Hz', expand=False)
answer = (hz == '60').sum()
```

- 문자열을 합칠 때 공백을 넣어 경계가 섞이지 않게 한다.
- `str.contains()`는 존재 여부, `str.extract()`는 실제 값을 추출한다.
- 추출 결과 `'60'`은 문자열이다.

> **암기:** `있는지 contains, 뽑을 때 extract.`

## 8.2 정확한 범주만 허용하는 유형

```python
valid = df[service_cols].isin(['Yes', 'No']).all(axis=1)
work = df.loc[valid].copy()

work[service_cols] = work[service_cols].replace({
    'Yes': 1,
    'No': 0
})

work['count'] = work[service_cols].sum(axis=1)
freq = work['count'].value_counts()
answer = freq.loc[1] / freq.loc[6]
```

- `str.contains('No')`는 `No internet service`도 포함하므로 이 문제에서는 틀린 접근이다.
- 모든 열이 유효해야 하므로 `.all(axis=1)`이다.

> **암기:** `정확한 값은 isin, 전부 만족은 all(axis=1).`

## 8.3 상관계수 최댓값

### y와 다른 변수들의 상관만 비교

```python
corr = df[cols + ['sales']].corr(method='pearson')['sales']
corr = corr.drop(index='sales').abs()
answer = corr.max()
name = corr.idxmax()
```

### 모든 변수 쌍을 비교

```python
corr = df[cols].corr(method='pearson').abs()
np.fill_diagonal(corr.values, 0)
answer = corr.max().max()
```

자기 자신과의 상관은 항상 1이므로 반드시 제거한다.

> **암기:** `타깃 한 열이면 drop(target), 전체 행렬이면 대각선 0.`

## 8.4 이상치 유형

세트 3 Q1은 “평균으로부터 2 표준편차보다 큰 값”을 찾는다.

```python
mean = df['sales'].mean()
std = df['sales'].std()

cond = (df['sales'] - mean) > 2 * std
outlier = df.loc[cond].copy()
```

문제가 “평균에서 2 표준편차 이상 떨어진 값”이라고 하면 양쪽 꼬리이므로 절댓값을 쓴다.

```python
cond = (df['sales'] - mean).abs() > 2 * std
```

> **시험 원칙:** `큰 값`은 오른쪽 꼬리, `떨어진 값`은 양쪽 꼬리.

## 8.5 2단계 `groupby` 유형

세트 4 Q1처럼 “최대 상품을 찾고, 그 상품에서 다시 최다 직업을 찾는” 문제다.

```python
sales_by_product = df.groupby('prod')['purchase'].sum()
best_product = sales_by_product.idxmax()

answer = (
    df.loc[df['prod'] == best_product, 'job']
      .value_counts()
      .idxmax()
)
```

```text
1차 집계: 어떤 상품인가?
2차 집계: 그 상품 안에서 어떤 직업인가?
```

## 8.6 고객 단위 집계

거래 행을 고객 한 명당 한 행으로 바꾸는 유형이다.

```python
customer = df.groupby('user').agg(
    gender=('gender', 'first'),
    age_group=('age_group', 'first'),
    job=('job', 'first'),
    city=('city', 'first'),
    marital=('marital', 'first'),
    kind=('prod', 'nunique'),
    purchase=('purchase', 'sum')
)
```

| 집계 | 사용 상황 |
|---|---|
| `'first'` | 고객별로 고정된 성별·직업·도시 |
| `'nunique'` | 구매한 서로 다른 상품 종류 수 |
| `'sum'` | 고객별 총 구매금액 |
| `'mean'` | 고객별 평균값 |

> **암기:** `고객 특성 first, 종류 nunique, 금액 sum.`

---

## 9. 실전 함정과 확인 순서

### 전처리 함정

1. `replace()`, `astype()`, `drop()` 결과는 다시 대입한다.
2. 부분 문자열과 정확한 범주를 구분한다.
3. 결측치를 0으로 바꾸라는지, 평균으로 바꾸라는지, 행을 제거하라는지 확인한다.
4. `/`는 일반 나눗셈, `//`는 몫이다.
5. `and`, `or` 대신 Series 조건은 `&`, `|`를 쓴다.
6. `str.contains('4K|8K')`에서 `|`는 정규식 OR이다.
7. 그룹 집계 전 데이터 단위가 거래인지 고객인지 확인한다.

### 모델링 함정

1. X에 y, ID, Train/Test 구분 열을 넣지 않는다.
2. 단일 y는 Series로 만든다.
3. Train/Test를 나눈 뒤 정규화한다.
4. Test에는 `transform()`만 한다.
5. 모델에 넣은 X와 평가 때 넣는 X의 열 순서가 같아야 한다.
6. 문제에서 지정한 seed와 파라미터를 그대로 쓴다.
7. 문제에서 요구하지 않은 파라미터를 임의로 바꾸지 않는다.
8. k-NN·K-Means는 스케일을 먼저 확인한다.
9. 지도학습 `fit`에는 y가 필요하고 K-Means에는 y가 없다.

### 평가 함정

1. 평가함수는 대부분 `(실제값, 예측값)` 순서다.
2. RMSE는 작을수록 좋으므로 `idxmin()`이다.
3. F1·Accuracy·Silhouette는 클수록 좋으므로 `idxmax()`다.
4. 상관행렬에서는 자기상관 1을 제외한다.
5. 반올림과 버림을 구분한다.

```python
# 반올림
round(value, 2)

# 양수에서 소수 둘째 자리까지 버림
np.floor(value * 100) / 100
```

### 제출 전 10초 검사

```text
[ ] 행 개수와 열 개수가 문제의 힌트와 같은가?
[ ] X 변수 이름과 개수가 정확한가?
[ ] y가 Series인가?
[ ] 분할 비율과 seed가 정확한가?
[ ] scaler를 Train에만 fit했는가?
[ ] 모델 파라미터를 그대로 옮겼는가?
[ ] fit의 X/y와 predict의 X가 올바른가?
[ ] 평가함수 입력이 실제값, 예측값 순서인가?
[ ] min을 찾을지 max를 찾을지 확인했는가?
[ ] 반올림 자릿수와 버림 조건이 맞는가?
```

---

## 10. 시험 직전 암기장

### DNME 한 줄

```text
D 조건·파생·인코딩·분할
N Train fit_transform / Test transform
M 생성 → fit → predict
E 실제와 예측을 채점
```

### 모델 한 줄 — 관리 순서

```text
[비지도·군집]
K-Means:             fit(X) → 군집번호 → Silhouette 최대

[지도·회귀]
Linear Regression:   fit(X,y) → predict → RMSE·R²

[지도·분류]
Logistic 분류:       fit → predict → F1
Logistic 해석:       fit → exp(coef_) → 오즈비
Naive Bayes:         fit → predict → Accuracy·F1

[지도·회귀/분류 공용]
Decision Tree:       Regressor는 RMSE / Classifier는 분류지표
Random Forest:       여러 나무 예측 / feature_importances_
k-NN:                Regressor는 이웃 평균 / Classifier는 이웃 투표
```

### 방향 한 줄

```text
오차(RMSE)는 최소
점수(F1·Accuracy·Silhouette)는 최대
```

### 스케일링 한 줄

```text
거리 K 둘(k-NN, K-Means)은 스케일링.
나무 둘(Tree, Random Forest)은 보통 생략.
```

### 가장 재사용하기 좋은 DNME 템플릿

```python
# D: Data
X = data[cols_X].copy()
y = data['target'].copy()

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=123
)

# N: Normalize
scaler = MinMaxScaler()
X_train_n = scaler.fit_transform(X_train)
X_test_n = scaler.transform(X_test)

# M: Modeling
model = SomeModel(problem_parameters)
model.fit(X_train_n, y_train)
y_pred = model.predict(X_test_n)

# E: Evaluation
answer = metric(y_test, y_pred)
```

> 마지막 암기: **“문제 조건이 기본 상식보다 우선한다. 변수·분할·정규화·seed·평가지표를 문제 그대로 옮긴다.”**
