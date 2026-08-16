# DNME 시험 직전 1페이지

> 상세 설명: [문제유형과 모델 파라미터 총정리](00_DNME_문제유형과_모델_파라미터_총정리.md)

## 1. DNME

```text
D Data      조건 → 파생 → 인코딩 → X/y → Train/Test
N Normalize Train fit_transform, Test transform
M Modeling  모델 생성 → fit → predict
E Error     실제값과 예측값으로 채점
```

> `D에서 나누고, N에서 맞추고, M에서 배우고, E에서 채점한다.`

## 2. 기본 코드

```python
# D
X = data[cols_X].copy()
y = data['target'].copy()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=123
)

# N
scaler = MinMaxScaler()
X_train_n = scaler.fit_transform(X_train)
X_test_n = scaler.transform(X_test)

# M
model = SomeModel(문제에서_지정한_파라미터)
model.fit(X_train_n, y_train)
y_pred = model.predict(X_test_n)

# E
score = metric(y_test, y_pred)
```

## 3. 모델 한 번에 비교 — 관리 순서

| 학습 방식 | 문제 유형 | 모델·클래스 | `random_state` | 그 외 핵심 파라미터 | 학습·예측 | 마지막 답 |
|---|---|---|:---:|---|---|---|
| 비지도 | 군집 | `KMeans` | O | `n_clusters` | `fit(X)` → `predict(X)` | Silhouette 최대 |
| 지도 | 회귀 | `LinearRegression` | X | `fit_intercept` | `fit(Xtr,ytr)` → `predict(Xte)` | RMSE·R² |
| 지도 | 분류 | `LogisticRegression` | O | `C`, `max_iter`, `solver` | `fit(Xtr,ytr)` → `predict(Xte)` | F1 또는 오즈비 |
| 지도 | 분류 | `GaussianNB` | X | `var_smoothing` | `fit(Xtr,ytr)` → `predict(Xte)` | Accuracy·F1 |
| 지도 | 회귀·분류 | `DecisionTreeRegressor/Classifier` | O | `max_depth`, `min_samples_split` | `fit(Xtr,ytr)` → `predict(Xte)` | RMSE 또는 분류지표 |
| 지도 | 회귀·분류 | `RandomForestRegressor/Classifier` | O | `n_estimators`, `max_depth` | `fit(Xtr,ytr)` → `predict(Xte)` | 예측지표·중요도 |
| 지도 | 회귀·분류 | `KNeighborsRegressor/Classifier` | X | `n_neighbors`, `weights`, `metric`, `p` | `fit(Xtr,ytr)` → `predict(Xte)` | RMSE 또는 Accuracy |

> `O`는 `random_state`를 받을 수 있는 모델, `X`는 받지 않는 모델이다.

```python
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
```

```text
지도학습 fit(X, y)
K-Means  fit(X)
```

## 4. 모델별 한 줄 — 관리 순서

```text
[비지도·군집]
K-Means:        스케일링 → fit(X) → 군집 → Silhouette

[지도·회귀]
Linear:         fit(X,y) → predict → RMSE·R²

[지도·분류]
Logistic:       predict면 F1 / exp(coef_)면 오즈비
Naive Bayes:    사전확률×우도 → predict → Accuracy·F1

[지도·회귀/분류]
Tree:           한 나무, Regressor/Classifier 선택
Random Forest:  여러 나무, Regressor/Classifier 선택
k-NN:           회귀는 이웃 평균, 분류는 이웃 투표
```

## 5. 파라미터 암기

```text
random_state = 무작위 결과 고정
n_clusters   = K-Means 군집 수
n_estimators = Random Forest 나무 수
n_neighbors  = 사용할 이웃 수
C            = 규제의 역수: 클수록 규제 약함
max_iter     = 최대 반복 횟수
solver       = 계수를 찾는 계산 방법
fit_intercept = Linear Regression 절편 추정 여부
var_smoothing = Naive Bayes 분산 계산 안정화
max_depth     = Tree의 최대 깊이
weights       = k-NN 이웃의 투표·평균 가중방식
p=2           = k-NN Euclidean 거리
```

## 6. 평가 방향

```text
RMSE                    작을수록 좋음 → idxmin
F1·Accuracy·Silhouette  클수록 좋음 → idxmax
```

## 7. 스케일링

```text
거리 K 둘: k-NN, K-Means → 스케일링 중요
나무 둘: Decision Tree, Random Forest → 보통 불필요
```

```python
# Min-Max: 보통 0~1
scaler = MinMaxScaler()

# Z-score: 평균 0, 표준편차 1
scaler = StandardScaler()
```

> `Train은 fit_transform, Test는 transform.`

## 8. `train_test_split`

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    train_size=0.7,       # 또는 test_size=0.3
    random_state=123
)
```

```text
반환 순서: X_train, X_test, y_train, y_test
문제가 ID나 Xgrp로 분할 기준을 주면 Boolean 조건으로 직접 분할
```

## 9. 문제 표현 → 코드

| 표현 | 코드 |
|---|---|
| 정확히 Yes/No만 | `isin(['Yes','No'])` |
| 모든 열이 만족 | `.all(axis=1)` |
| 하나라도 만족 | `.any(axis=1)` |
| 문자열 포함 | `.str.contains()` |
| 문자열 값 추출 | `.str.extract()` |
| 그룹별 계산 | `.groupby()` |
| 종류 수 | `.nunique()` |
| 가장 큰 값의 이름 | `.idxmax()` |
| 가장 작은 값의 이름 | `.idxmin()` |
| 몫 | `//` |
| 평균 차이 | `abs(mean_A - mean_B)` |

## 10. 제출 전 체크

```text
[ ] X 변수 이름·개수 정확?
[ ] y와 ID를 X에서 제외?
[ ] y는 1차원 Series?
[ ] 분할비와 seed 정확?
[ ] Test에는 transform만 사용?
[ ] 모델 파라미터 그대로 입력?
[ ] 지도 fit(X,y), K-Means fit(X) 구분?
[ ] 평가는 metric(실제, 예측) 순서?
[ ] RMSE는 min, Score는 max?
[ ] 반올림과 버림 구분?
```

> 최종 암기: `조건을 그대로 옮기고 → DNME → Error는 최소, Score는 최대.`
