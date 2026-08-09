모델 예측
1. 독립변수, 종속변수 각각 train, test로 나누기
- train : test  =  n : 1 -n

2. 정규화 시
   - X_train  --> fit_transform
   - X_test --> transform
   - 최대값과 최소값을 알고 정규화 -> train
   - 최대값과 최소값을 모르는 상태로 해야함 -> test

### 모델예측 DNME(Data-Normalization-Modeling-Error)

#### D(Data 분할하기)

```python
X = {}
y = {}
X_trained,X_tested,y_trained,y_tested = train_test_split(X,y, test_size = {}, random_state = {})
```

#### N(Normalization, 생략가능)

```python
scaler = {}
X_trained_scaled = scaler.fit_trasform(X_trained)
X_tested_scaled = scaler.transform(X_tested)
```

#### M(Modeling)

```python
model = {}
model.fit(X_trained_scaled, y_train)
pred = model.predict(X_test_scaled)
```

- 모델 별 fit, predict 쓰는 법
-  지도학습 모델:
    - fit(X_train, y_train)
    - predict(X_test)
- 비지도 군집 모델 KMeans:
    - fit_predict(X)
    - fit(X) 후 predict(X)

- 정규화 Scaler:
  - Train = fit_transform()
  - Test = transform()

| 모델/도구                   | 추천 사용 방식                                    | 이유                   |
| ----------------------- | ------------------------------------------- | -------------------- |
| `KMeans`                | `fit_predict(X)` 가능                         | 정답 y 없이 군집 번호를 바로 얻음 |
| `KNeighborsRegressor`   | `fit(X_train, y_train)` 후 `predict(X_test)` | 지도학습이라 y 필요          |
| `KNeighborsClassifier`  | `fit(X_train, y_train)` 후 `predict(X_test)` | 지도학습이라 y 필요          |
| `LogisticRegression`    | `fit(X_train, y_train)` 후 `predict(X_test)` | 지도학습                 |
| `DecisionTreeRegressor` | `fit(X_train, y_train)` 후 `predict(X_test)` | 지도학습                 |
| `MinMaxScaler`          | Train은 `fit_transform`, Test는 `transform`   | Test 기준을 새로 학습하면 안 됨 |
| `StandardScaler`        | Train은 `fit_transform`, Test는 `transform`   | 동일                   |



#### E(Error)
```python
rmse = mean_sqaure_error(y_test,pred)**0.5
```

---


### 상관계수
```python
df.corr(method = 'pearson')['columns'].drop['columns']
```
---
## 데이터 확인하기

### 열안에 어떤 데이터가 있는지 검증하기
``` python
display(df_q2['age_group'].apply(type).value_counts())
display(df_q2['age_group'].unique())

```
### 특정 열 안의 데이터의 타입 확인하기
#### 1. dataframe 전체 열 데이터 타입
```python
df.dtypes
```

```text
job        int64
name      object
score    float64
mixed     object
dtype: object
```

#### 2. 특정 열의 데이터 타입
```python
df['열'].dtype
```
```text
dtype('int64')
```

#### 3. 특정 열 내 각 데이터들의 데이터 타입
- dtype이 문자열이라고 해놓고 딴 값이 들어 있을 수 있으니!
```python
df['열'].apply(type).value_counts()
```
apply(함수이름)
```
<class 'int'>         1
<class 'str'>         1
<class 'float'>       1
<class 'NoneType'>    1
Name: count, dtype: int64
```

### reset_index(name = 'xxx')
- series 결과를 xxx 이름의 열로 만들고 전체를 dataframe으로 바꿈

---
## loc
| 코드                       | 결과        |
| ------------------------ | --------- |
| `df['target']`           | Series    |
| `df['target'].loc[조건]`   | Series    |
| `df['target'].loc[0]`    | 값 하나      |
| `df[['target']]`         | DataFrame |
| `df[['target']].loc[조건]` | DataFrame |
df['열']      → Series
df[['열']]    → DataFrame

#### dataframe['col'].isin([리스트])

# 행 제거
## 어떤 값이 있는 행 제거

# 데이터프레임에서 조건을 만족하는 행의 개수를 구할 때 .sum() 을 쓰는 이유는 조건 만족으 true,false인 시리즈로 반환되기때문에 true 개수를 더한 것임

# 비율--> 데이터가 0,1 의 값으로 이루어져있으면 평균을 구하면 1의 비율이 된다.

## df.drop(columns = ['열들'])
## df.dropna()
## df[].dropna()
## df.dropna(subset=['열들'])

# fit(xtrain, ytrain)

# 제일 많이 틀린다! 문자열 매칭에 isin을 쓰는건 기억하는데 리스트!! isin([])

# df.values array 로 만들어줌 --> diagonal().sum() 가능 대각선만 뽑아 더하기

## 각 문자형 변수에 결측치가 하나라도 존재하는 행은 모두 제거하시오.
```python
cols_obj = df.select_dtypes(include='object').columns
df_drop_obj_na = df.dropna(subset=cols_obj).copy()
```


# 결측치
| 목적                   | 코드                                       |
| -------------------- | ---------------------------------------- |
| 한 열 결측치 여부           | `df['col'].isna()`                       |
| 한 열에 결측치 하나라도 있는지    | `df['col'].isna().any()`                 |
| 한 열 결측치 개수           | `df['col'].isna().sum()`                 |
| 여러 열 결측치 개수          | `df[cols].isna().sum()`                  |
| 여러 열 중 하나라도 결측치 있는 행 | `df[cols].isna().any(axis=1)`            |
| 결측치 있는 행만 보기         | `df.loc[df[cols].isna().any(axis=1), :]` |


# columns의 data type
| 코드                          | 대상            | 결과            |
| --------------------------- | ------------- | ------------- |
| `df['experience'].dtype`    | Series 한 열    | 자료형 하나        |
| `df[['experience']].dtypes` | DataFrame 한 열 | Series 형태 자료형 |
| `df.dtypes`                 | 전체 DataFrame  | 컬럼별 자료형       |

# columns 찾기
| 목적            | 코드                                               |
| ------------- | ------------------------------------------------ |
| 특정 컬럼 존재 여부   | `'col' in df.columns`                            |
| 여러 컬럼이 모두 있는지 | `set(cols).issubset(df.columns)`                 |
| 없는 컬럼 찾기      | `[col for col in cols if col not in df.columns]` |
| 전체 컬럼 보기      | `df.columns.tolist()`                            |

# Series 만들기
pd.Series(array, index=[])

# accuracy score
- crosstab은 두 개의 Series/array를 한 줄씩 짝지어서 조합별 개수를 세는 함수
```python
from sklearn.metrics import accuracy_score
round(accuracy_score(y_true = y_test, y_pred = y_pred), 2)
```

# df['새로만들열'] = array,series 는 가능하다.
## df['새로만들열'] = df['열'](series) 가능
    - series 는 col이 한개인 dataframe도 동일 취급
## df['새로만들열'] = df(dataframe) 불가능 


# Q2-2. OOO 을 표준화 변환 실시하고 변환된 변수에 접미사 "_S"를 붙이시오.
```python
df_q2_nor = pd.DataFrame(arr_q2_nor, columns = df_q2.columns)
df_q2_nor = df_q2_nor.add_suffix("_S")
df_q2_nor.head(2)
```


# 정규화는 X만!-특별할때 y!
- fit은 Train에서만 한다.
| 상황         | 정규화 대상      |
| ---------- | ----------- |
| KNN 회귀     | X만          |
| KNN 분류     | X만          |
| KMeans 군집  | X만          |
| 로지스틱 회귀    | X만          |
| 선형회귀/릿지/라쏘 | 보통 X만       |
| y까지 정규화    | 문제에서 명시할 때만 |
- 여기서 중요한 건 Test는 fit 하면 안 된다야.
- 왜냐하면 모델은 Train 데이터로 공부했잖아.
- 그러면 Test 데이터도 Train에서 배운 기준으로 변환해야 공정해.
- MinMaxScaler의 fit은 min과 max를 찾는 것이다.
```python
scaler.fit(X_train)
X_train_n = scaler.transform(X_train)
X_test_n = scaledr.transform(X_test)

X_train_n = scaler.fit_transform(X_train)
X_test_n = scaledr.transform(X_test)
```

## “모든 변수를 대상으로 정규화”
- "X_train" 안에 들어간 모든 독립변수를 정규화하라는 뜻
- y_train은 정규화하지 않는다.
- X = 독립변수들(train,test)
- Y = 종속변수(train), 정답(test)
    | 문제 문장           | 해석                    |
    | --------------- | --------------------- |
    | 모든 변수를 대상으로 정규화 | X에 포함된 모든 독립변수 정규화    |
    | 모든 연속형 변수를 정규화  | 숫자형 X 변수만 정규화         |
    | 종속변수도 정규화       | 이때만 y도 정규화            |
    | target도 정규화     | 이때만 y도 정규화            |
    | 모든 데이터를 정규화     | 보통 그래도 X만, 단 문맥 확인 필요 |

# axis = 1은 당연하게 생각하면 된다. 축을 바꾸고 싶으면 axis를 생각하기
- df.sum() --> 당연히 열 내의 합이다.
- df.sum(axis = 1) --> 행의 합이된다.

# all --> 행들의 모든 조건이 true일 때 true를 출력하는 series이다.
```python
df[cols].isna(['a','b']).all(axis=1) #모든 행이 true
df[cols].isna(['a','b']).all(axis=0) #열내의 모든 값이 true
```

# 정확히 원하는 값만. isin([]), 문자열이면 str.contains()