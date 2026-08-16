import json
from pathlib import Path
from uuid import uuid4


ROOT = Path(__file__).resolve().parent


def markdown(source):
    return {
        "cell_type": "markdown",
        "id": uuid4().hex[:8],
        "metadata": {},
        "source": source.splitlines(keepends=True),
    }


def code(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": uuid4().hex[:8],
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


def write_notebook(relative_path, cells):
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": ".venv",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.7.12",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path.write_text(
        json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )


fill_in_intro = """# 01~06 코드 빈칸 채우기 테스트

기존 실전문제와 오답노트에서 반복해서 헷갈린 코드를 다시 구성한 테스트입니다.

- `____`를 올바른 코드로 바꾸세요.
- 각 세트는 독립적으로 실행할 수 있습니다.
- 정답은 `answers/01_06_fill_in_answer.ipynb`에 있습니다.
- 먼저 정답을 보지 않고 작성한 뒤, 결과의 shape와 최종값까지 확인하세요.
"""


fill_in_questions = [
    markdown(fill_in_intro),
    markdown("""## Set 1 — 문자열 추출과 Random Forest

핵심: 문자열 열 결합, 정규식 추출, OR 검색, 1차원 y, 변수 중요도
"""),
    code(r'''import pandas as pd
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv('../../dataset/TV.csv')
df['spec_text'] = df[['Picture_quality', 'Speaker', 'Frequency']].agg(' '.join, axis=1)

df['refresh_rate'] = df['spec_text'].str.____(
    r'(?P<refresh_rate>\d{2,3})\s*Hz',
    expand=____
)

df['high_quality'] = df['Picture_quality'].str.____(
    r'4K____8K',
    na=False
).astype(int)

df['review_ratio'] = df['Reviews'] / df['Ratings']
df['price_ratio'] = df['current_price'] / df['MRP']
model_df = df.dropna(subset=['review_ratio', 'price_ratio']).copy()

cols_X = ['review_ratio', 'MRP', 'price_ratio', 'high_quality']
X = model_df[cols_X]
y = model_df____'Stars'____

model = RandomForestRegressor(random_state=123)
model.____(X, y)

importance = pd.Series(model.____, index=cols_X)
display(importance.____())
'''),
    markdown("""## Set 2 — 정확한 범주 검사와 상관행렬

핵심: `isin`, 행 단위 all, 몫, 자기상관 제외, Series y
"""),
    code(r'''import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv('../../dataset/galaxy_users.csv')
service_cols = [
    'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
    'TechSupport', 'StreamingTV', 'StreamingMovies'
]

valid = df[service_cols].____(['Yes', 'No']).____(axis=1)
base = df.loc[____valid].copy()
base[service_cols] = base[service_cols].____({'Yes': 1, 'No': 0}).astype(int)
base['service_count'] = base[service_cols].____(axis=1)
base['used_month'] = base['TotalCharges'] ____ base['MonthlyCharges']

corr_abs = base[['tenure', 'MonthlyCharges', 'used_month']].corr().____()
np.fill_diagonal(corr_abs.____, 0)
display(corr_abs.max().____())

X = base[['tenure', 'MonthlyCharges', 'TotalCharges', 'service_count']]
y = base____'Stars'____ if 'Stars' in base.columns else base['Churn']
'''),
    markdown("""## Set 3 — 이상치, OHE, k-NN RMSE

핵심: 상위 이상치, 명시적 더미화, train 기반 정규화, RMSE 최소화
"""),
    code(r'''import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error

df = pd.read_csv('../../dataset/mobiles.csv')

upper = df['sales'].____() + 2 * df['sales'].____()
focus = df.loc[df['sales'] ____ upper].copy()

X = df.drop(columns='sales').copy()
y = df['sales']
X = pd.____(X, columns=____'screen_size'____, drop_first=False)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=123
)

scaler = MinMaxScaler()
X_train_scaled = scaler.____(X_train)
X_test_scaled = scaler.____(X_test)

rmse_by_k = {}
for k in [3, 5, 7, 9, 11]:
    model = KNeighborsRegressor(n_neighbors=k)
    model.fit(X_train_scaled, y_train)
    pred = model.predict(X_test_scaled)
    rmse_by_k[k] = mean_squared_error(y_test, pred) ____ 0.5

rmse = pd.Series(rmse_by_k)
display(rmse.____())
'''),
    markdown("""## Set 4 — 고객 단위 Named Aggregation과 군집평가

핵심: `first`, `nunique`, `sum`, 식별자 제외, OHE, Silhouette score
"""),
    code(r'''import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

df = pd.read_csv('../../dataset/sales_pos.csv')

df_user = df.groupby('user').agg(
    gender=('gender', '____'),
    age_group=('age_group', '____'),
    job=('job', '____'),
    city=('city', '____'),
    marital=('marital', '____'),
    prod_count=('prod', '____'),
    total_purchase=('purchase', '____')
)

df_user['gender'] = df_user['gender'].____({'M': 1, 'F': 0})
df_user['age_group'] = pd.to_numeric(
    df_user['age_group'].str.____(r'(\d+)', expand=False)
)
X = pd.get_dummies(df_user, columns=____'job', 'city'____)

scaler = MinMaxScaler()
X_scaled = scaler.____(X)

model = KMeans(n_clusters=7, random_state=123, n_init=10)
labels = model.____(X_scaled)
score = silhouette_score(____, ____)
display(round(score, 2))
'''),
    markdown("""## Set 5 — 그룹별 상관계수, 군집 라벨, 조건 분할

핵심: GroupBy apply, StandardScaler, 최적 k 라벨, modulo 분할, RMSE
"""),
    code(r'''import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, mean_squared_error
from sklearn.tree import DecisionTreeRegressor

df = pd.read_csv('../../dataset/card_cust.csv')
base = df.copy()
base['MINIMUM_PAYMENTS'] = base['MINIMUM_PAYMENTS'].____(
    base['MINIMUM_PAYMENTS'].____()
)

corr_by_tenure = base.groupby('TENURE').____(
    lambda group: group['BALANCE'].____(group['CREDIT_LIMIT'])
)

X = base.drop(columns='CUST_ID').copy()
X_scaled = StandardScaler().____(X)

scores = {}
labels_by_k = {}
for k in range(2, 6):
    labels = KMeans(n_clusters=k, random_state=1234).____(X_scaled)
    scores[k] = silhouette_score(X_scaled, labels)
    labels_by_k[k] = labels

best_k = pd.Series(scores).____()
X['cluster'] = labels_by_k[____]

train = base.loc[base['CUST_ID'] % 4 ____ 0].copy()
test = base.loc[base['CUST_ID'] % 4 ____ 0].copy()
model = DecisionTreeRegressor(random_state=1234)
'''),
    markdown("""## Set 6 — 문자형 결측치, 마지막 기준범주, Odds Ratio, Accuracy

핵심: `select_dtypes`, `dropna(subset)`, 마지막 더미열 제거, `exp(coef)`, 혼동행렬
"""),
    code(r'''import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv('../../dataset/edu_enrollees.csv')
base = df.drop(columns=['city', 'company_size', 'company_type']).copy()

object_cols = base.____(include='object').columns
base = base.____(subset=object_cols).copy()
base = base.loc[____base['experience'].isin(['>20', '<1'])].copy()
base['experience'] = base['experience'].astype(____)

dummy = pd.get_dummies(base['gender'], prefix='gender')
dummy = dummy.iloc[:, ____].copy()  # 사전순 마지막 열 제외

target_rate = base.groupby('relevant_experience')['target'].____()

categorical_cols = [
    'gender', 'relevant_experience', 'enrolled_university',
    'education_level', 'major_discipline', 'last_new_job'
]
numeric_cols = ['city_development_index', 'experience', 'training_hours']
job2 = pd.get_dummies(
    base[numeric_cols + categorical_cols + ['target', 'Xgrp']],
    columns=categorical_cols,
    drop_first=____
)
X = job2.drop(columns=['target', 'Xgrp'])
y = job2['target']
model = LogisticRegression(C=100000, max_iter=1000, solver='liblinear', random_state=123)
model.fit(X, y)

odds_ratio = pd.Series(np.____(model.coef_[0]), index=X.columns)
answer = np.____(odds_ratio.max() * 100) / 100

train = job2.loc[job2['Xgrp'] ____ 'train'].copy()
test = job2.loc[job2['Xgrp'] ____ 'test'].copy()
knn = KNeighborsClassifier(n_neighbors=5, metric='____')
'''),
]


fill_in_answers = [
    markdown("""# 01~06 코드 빈칸 채우기 정답

빈칸만 확인하지 말고 각 코드가 반환하는 객체의 타입과 shape도 함께 확인하세요.
"""),
    markdown("## Set 1 정답"),
    code(r'''import pandas as pd
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv('../../dataset/TV.csv')
df['spec_text'] = df[['Picture_quality', 'Speaker', 'Frequency']].agg(' '.join, axis=1)
df['refresh_rate'] = df['spec_text'].str.extract(
    r'(?P<refresh_rate>\d{2,3})\s*Hz', expand=False
)
df['high_quality'] = df['Picture_quality'].str.contains(r'4K|8K', na=False).astype(int)
df['review_ratio'] = df['Reviews'] / df['Ratings']
df['price_ratio'] = df['current_price'] / df['MRP']
model_df = df.dropna(subset=['review_ratio', 'price_ratio']).copy()
cols_X = ['review_ratio', 'MRP', 'price_ratio', 'high_quality']
X = model_df[cols_X]
y = model_df['Stars']
model = RandomForestRegressor(random_state=123)
model.fit(X, y)
importance = pd.Series(model.feature_importances_, index=cols_X)
display(importance.idxmax())
'''),
    markdown("## Set 2 정답"),
    code(r'''import numpy as np
import pandas as pd

df = pd.read_csv('../../dataset/galaxy_users.csv')
service_cols = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
valid = df[service_cols].isin(['Yes', 'No']).all(axis=1)
base = df.loc[valid].copy()
base[service_cols] = base[service_cols].replace({'Yes': 1, 'No': 0}).astype(int)
base['service_count'] = base[service_cols].sum(axis=1)
base['used_month'] = base['TotalCharges'] // base['MonthlyCharges']
corr_abs = base[['tenure', 'MonthlyCharges', 'used_month']].corr().abs()
np.fill_diagonal(corr_abs.values, 0)
display(corr_abs.max().max())
y = base['Churn']
'''),
    markdown("## Set 3 정답"),
    code(r'''import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error

df = pd.read_csv('../../dataset/mobiles.csv')
upper = df['sales'].mean() + 2 * df['sales'].std()
focus = df.loc[df['sales'] > upper].copy()
X = pd.get_dummies(df.drop(columns='sales'), columns=['screen_size'], drop_first=False)
y = df['sales']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
rmse_by_k = {}
for k in [3, 5, 7, 9, 11]:
    model = KNeighborsRegressor(n_neighbors=k)
    model.fit(X_train_scaled, y_train)
    pred = model.predict(X_test_scaled)
    rmse_by_k[k] = mean_squared_error(y_test, pred) ** 0.5
display(pd.Series(rmse_by_k).idxmin())
'''),
    markdown("## Set 4 정답"),
    code(r'''import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

df = pd.read_csv('../../dataset/sales_pos.csv')
df_user = df.groupby('user').agg(
    gender=('gender', 'first'), age_group=('age_group', 'first'),
    job=('job', 'first'), city=('city', 'first'), marital=('marital', 'first'),
    prod_count=('prod', 'nunique'), total_purchase=('purchase', 'sum')
)
df_user['gender'] = df_user['gender'].replace({'M': 1, 'F': 0})
df_user['age_group'] = pd.to_numeric(
    df_user['age_group'].str.extract(r'(\d+)', expand=False)
)
X = pd.get_dummies(df_user, columns=['job', 'city'])
X_scaled = MinMaxScaler().fit_transform(X)
model = KMeans(n_clusters=7, random_state=123, n_init=10)
labels = model.fit_predict(X_scaled)
score = silhouette_score(X_scaled, labels)
display(round(score, 2))
'''),
    markdown("## Set 5 정답"),
    code(r'''import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

df = pd.read_csv('../../dataset/card_cust.csv')
base = df.copy()
base['MINIMUM_PAYMENTS'] = base['MINIMUM_PAYMENTS'].fillna(base['MINIMUM_PAYMENTS'].mean())
corr_by_tenure = base.groupby('TENURE').apply(
    lambda group: group['BALANCE'].corr(group['CREDIT_LIMIT'])
)
X = base.drop(columns='CUST_ID').copy()
X_scaled = StandardScaler().fit_transform(X)
scores, labels_by_k = {}, {}
for k in range(2, 6):
    labels = KMeans(n_clusters=k, random_state=1234).fit_predict(X_scaled)
    scores[k] = silhouette_score(X_scaled, labels)
    labels_by_k[k] = labels
best_k = pd.Series(scores).idxmax()
X['cluster'] = labels_by_k[best_k]
train = base.loc[base['CUST_ID'] % 4 != 0].copy()
test = base.loc[base['CUST_ID'] % 4 == 0].copy()
'''),
    markdown("## Set 6 정답"),
    code(r'''import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

df = pd.read_csv('../../dataset/edu_enrollees.csv')
base = df.drop(columns=['city', 'company_size', 'company_type']).copy()
object_cols = base.select_dtypes(include='object').columns
base = base.dropna(subset=object_cols).copy()
base = base.loc[~base['experience'].isin(['>20', '<1'])].copy()
base['experience'] = base['experience'].astype(int)
dummy = pd.get_dummies(base['gender'], prefix='gender')
dummy = dummy.iloc[:, :-1].copy()
target_rate = base.groupby('relevant_experience')['target'].mean()
categorical_cols = [
    'gender', 'relevant_experience', 'enrolled_university',
    'education_level', 'major_discipline', 'last_new_job'
]
numeric_cols = ['city_development_index', 'experience', 'training_hours']
job2 = pd.get_dummies(
    base[numeric_cols + categorical_cols + ['target', 'Xgrp']],
    columns=categorical_cols,
    drop_first=True
)
X = job2.drop(columns=['target', 'Xgrp'])
y = job2['target']
model = LogisticRegression(C=100000, max_iter=1000, solver='liblinear', random_state=123)
model.fit(X, y)
odds_ratio = pd.Series(np.exp(model.coef_[0]), index=X.columns)
answer = np.floor(odds_ratio.max() * 100) / 100
train = job2.loc[job2['Xgrp'] == 'train'].copy()
test = job2.loc[job2['Xgrp'] == 'test'].copy()
'''),
]


write_notebook("fill_in/01_06_fill_in_test.ipynb", fill_in_questions)
write_notebook("answers/01_06_fill_in_answer.ipynb", fill_in_answers)


def applied_intro(set_no, title, dataset, final_rows):
    return [
        markdown(f'''# 응용 모의고사 Set {set_no} — {title}

- 데이터: `{dataset}`
- 난이도: 기존 Set 01~06과 유사
- 구성: **공통 전처리 → Q1 통계 → Q2 상관분석 → Q3 모델링**
- 모든 문항은 공통 전처리 결과를 이어서 사용합니다.
- 전처리 완료 후 데이터는 **{final_rows:,}행**이어야 합니다. 행 수가 다르면 다음 문제로 넘어가기 전에 전처리를 확인하세요.

정답 노트북은 `../answers/`에 있습니다.'''),
    ]


applied_sets = []


# ---------------------------------------------------------------------------
# Applied Set 1: TV product data
# ---------------------------------------------------------------------------
q1_cells = applied_intro(1, "문자열 추출과 상품 분석", "TV.csv", 197) + [
    markdown(r'''## 공통 전처리

1. `Picture_quality`, `Speaker`, `Frequency`를 문자열로 연결하여 `spec_text`를 만드세요.
2. `spec_text`에서 `Hz` 앞의 2~3자리 숫자를 추출하여 숫자형 `refresh_rate`를 만드세요.
3. `channel`에 `Pixel` 또는 `Oper`가 들어간 행은 제외하세요. 결측치는 포함하지 않는 것으로 처리합니다.
4. 다음 파생변수를 만드세요.
   - `review_ratio = Reviews / Ratings`
   - `price_ratio = current_price / MRP`
   - `Netflix`: `channel`에 Netflix가 있으면 1, 아니면 0
   - `PrimeVideo`: `channel`에 Prime Video가 있으면 1, 아니면 0
   - `high_quality`: `Picture_quality`에 `4K` 또는 `Ultra HD`가 있으면 1, 아니면 0
5. 무한대를 결측치로 바꾸고 `refresh_rate`, `review_ratio`, `price_ratio` 중 하나라도 결측인 행을 제거하세요.'''),
    code(r'''import numpy as np
import pandas as pd

df = pd.read_csv('../../dataset/TV.csv')
# 공통 전처리 코드를 작성하세요.
'''),
    markdown(r'''## Q1

`refresh_rate >= 60`인 상품의 평균 `Stars`에서 `refresh_rate < 60`인 상품의 평균 `Stars`를 빼세요. 결과는 소수점 둘째 자리까지 반올림하세요.'''),
    code("# Q1 풀이"),
    markdown(r'''## Q2

`Stars`, `refresh_rate`, `MRP`, `current_price`의 피어슨 상관계수를 구하세요. `Stars`와 나머지 세 변수 중 절댓값 기준 상관계수가 가장 큰 변수명과 **부호를 보존한 상관계수**를 구하고, 계수는 소수점 셋째 자리까지 반올림하세요.'''),
    code("# Q2 풀이"),
    markdown(r'''## Q3

다음 변수를 사용하여 `Stars`를 예측하는 `RandomForestRegressor(random_state=321)`를 전체 데이터에 학습하세요.

`review_ratio`, `MRP`, `price_ratio`, `Netflix`, `PrimeVideo`, `high_quality`, `refresh_rate`

학습 후 변수 중요도가 가장 큰 변수명을 구하세요.'''),
    code("# Q3 풀이"),
]

a1_cells = applied_intro(1, "정답 — 문자열 추출과 상품 분석", "TV.csv", 197) + [
    markdown("## 공통 전처리 정답"),
    code(r'''import numpy as np
import pandas as pd

df = pd.read_csv('../../dataset/TV.csv')
base = df.copy()
spec_cols = ['Picture_quality', 'Speaker', 'Frequency']
base['spec_text'] = base[spec_cols].fillna('').astype(str).agg(' '.join, axis=1)
base['refresh_rate'] = pd.to_numeric(
    base['spec_text'].str.extract(r'(\d{2,3})\s*Hz', expand=False),
    errors='coerce'
)
exclude = base['channel'].str.contains(r'Pixel|Oper', na=False)
base = base.loc[~exclude].copy()
base['review_ratio'] = base['Reviews'] / base['Ratings']
base['price_ratio'] = base['current_price'] / base['MRP']
base['Netflix'] = base['channel'].str.contains('Netflix', na=False).astype(int)
base['PrimeVideo'] = base['channel'].str.contains('Prime Video', na=False).astype(int)
base['high_quality'] = base['Picture_quality'].str.contains(r'4K|Ultra HD', na=False).astype(int)
base = base.replace([np.inf, -np.inf], np.nan)
base = base.dropna(subset=['refresh_rate', 'review_ratio', 'price_ratio']).copy()
assert len(base) == 197
display(base.head())'''),
    markdown("## Q1 정답"),
    code(r'''high_mean = base.loc[base['refresh_rate'] >= 60, 'Stars'].mean()
low_mean = base.loc[base['refresh_rate'] < 60, 'Stars'].mean()
answer_q1 = round(high_mean - low_mean, 2)
display(answer_q1)  # -0.05'''),
    markdown("## Q2 정답"),
    code(r'''corr = base[['Stars', 'refresh_rate', 'MRP', 'current_price']].corr(method='pearson')
stars_corr = corr['Stars'].drop(index='Stars')
answer_var_q2 = stars_corr.abs().idxmax()
answer_coef_q2 = round(stars_corr.loc[answer_var_q2], 3)
display(answer_var_q2, answer_coef_q2)  # current_price, 0.184'''),
    markdown("## Q3 정답"),
    code(r'''from sklearn.ensemble import RandomForestRegressor

features = ['review_ratio', 'MRP', 'price_ratio', 'Netflix',
            'PrimeVideo', 'high_quality', 'refresh_rate']
X = base[features]
y = base['Stars']
model = RandomForestRegressor(random_state=321)
model.fit(X, y)
importance = pd.Series(model.feature_importances_, index=features)
answer_q3 = importance.idxmax()
display(importance.sort_values(ascending=False), answer_q3)  # price_ratio'''),
]
applied_sets.append((1, "tv_preprocessing", q1_cells, a1_cells))


# ---------------------------------------------------------------------------
# Applied Set 2: customer churn
# ---------------------------------------------------------------------------
q2_cells = applied_intro(2, "서비스 전처리와 이탈 예측", "galaxy_users.csv", 5512) + [
    markdown(r'''## 공통 전처리

1. 다음 여섯 서비스 열의 값이 모두 정확히 `Yes` 또는 `No`인 행만 남기세요.
   `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`
2. 여섯 열을 `Yes=1`, `No=0`으로 변환하고 합계인 `service_count`를 만드세요.
3. `used_month = tenure // 12`를 만드세요.
4. `Partner`, `Dependents`, `PaperlessBilling`, `Churn`도 `Yes=1`, `No=0`으로 변환하세요.'''),
    code(r'''import numpy as np
import pandas as pd

df = pd.read_csv('../../dataset/galaxy_users.csv')
# 공통 전처리 코드를 작성하세요.
'''),
    markdown("## Q1\n\n`service_count >= 4`인 고객 수를 `service_count <= 1`인 고객 수로 나누고 소수점 둘째 자리까지 반올림하세요."),
    code("# Q1 풀이"),
    markdown(r'''## Q2

`tenure`, `MonthlyCharges`, `used_month`, `TotalCharges`의 모든 변수 쌍에 대해 피어슨 상관계수를 구하세요. 자기 자신과의 상관계수는 제외하고 절댓값이 가장 큰 계수를 소수점 셋째 자리까지 반올림하세요.'''),
    code("# Q2 풀이"),
    markdown(r'''## Q3

아래 변수를 사용해 `Churn`을 예측하세요.

`SeniorCitizen`, `Partner`, `Dependents`, `tenure`, `MonthlyCharges`, `TotalCharges`, `service_count`, `PaperlessBilling`

- `train_test_split(test_size=0.25, random_state=321, stratify=y)`
- `MinMaxScaler`는 학습 데이터에만 `fit`
- `LogisticRegression(max_iter=1000)`
- 테스트 데이터의 F1 score를 소수점 둘째 자리까지 반올림'''),
    code("# Q3 풀이"),
]

a2_cells = applied_intro(2, "정답 — 서비스 전처리와 이탈 예측", "galaxy_users.csv", 5512) + [
    markdown("## 공통 전처리 정답"),
    code(r'''import numpy as np
import pandas as pd

df = pd.read_csv('../../dataset/galaxy_users.csv')
base = df.copy()
service_cols = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                'TechSupport', 'StreamingTV', 'StreamingMovies']
valid = base[service_cols].isin(['Yes', 'No']).all(axis=1)
base = base.loc[valid].copy()
base[service_cols] = base[service_cols].replace({'Yes': 1, 'No': 0})
base['service_count'] = base[service_cols].sum(axis=1)
base['used_month'] = base['tenure'] // 12
binary_cols = ['Partner', 'Dependents', 'PaperlessBilling', 'Churn']
base[binary_cols] = base[binary_cols].replace({'Yes': 1, 'No': 0})
assert len(base) == 5512
display(base.head())'''),
    markdown("## Q1 정답"),
    code(r'''many = (base['service_count'] >= 4).sum()
few = (base['service_count'] <= 1).sum()
answer_q1 = round(many / few, 2)
display(answer_q1)  # 1.03'''),
    markdown("## Q2 정답"),
    code(r'''cols = ['tenure', 'MonthlyCharges', 'used_month', 'TotalCharges']
corr_abs = base[cols].corr(method='pearson').abs()
np.fill_diagonal(corr_abs.values, 0)
answer_q2 = round(corr_abs.max().max(), 3)
display(corr_abs, answer_q2)  # 0.989'''),
    markdown("## Q3 정답"),
    code(r'''from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

features = ['SeniorCitizen', 'Partner', 'Dependents', 'tenure',
            'MonthlyCharges', 'TotalCharges', 'service_count', 'PaperlessBilling']
X = base[features]
y = base['Churn']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=321, stratify=y
)
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)
pred = model.predict(X_test_scaled)
answer_q3 = round(f1_score(y_test, pred), 2)
display(answer_q3)  # 0.58'''),
]
applied_sets.append((2, "churn_preprocessing", q2_cells, a2_cells))


# ---------------------------------------------------------------------------
# Applied Set 3: mobile products
# ---------------------------------------------------------------------------
q3_cells = applied_intro(3, "파생변수와 KNN 회귀", "mobiles.csv", 390) + [
    markdown(r'''## 공통 전처리

1. 후면 카메라 수 `num_rear_camera`가 1인 제품을 제외하세요.
2. 다음 파생변수를 만드세요.

`performance = (RAM + ROM) / (num_rear_camera + num_front_camera)`'''),
    code(r'''import numpy as np
import pandas as pd

df = pd.read_csv('../../dataset/mobiles.csv')
# 공통 전처리 코드를 작성하세요.
'''),
    markdown("## Q1\n\n`performance`가 평균+표준편차보다 큰 제품들의 `discount_percent` 평균을 소수점 셋째 자리까지 반올림하세요."),
    code("# Q1 풀이"),
    markdown(r'''## Q2

`sales`와 `ratings`, `num_of_ratings`, `sales_price`, `discount_percent`, `performance` 각각의 피어슨 상관계수를 구하세요. 절댓값이 가장 큰 변수명과 부호를 보존한 계수를 구하고 계수는 소수점 둘째 자리까지 반올림하세요.'''),
    code("# Q2 풀이"),
    markdown(r'''## Q3

`sales`를 예측하는 KNN 회귀 모델을 만드세요.

- 입력 변수: `ratings`, `num_of_ratings`, `sales_price`, `discount_percent`, `performance`, `screen_size`
- `screen_size`는 원-핫 인코딩
- `train_test_split(test_size=0.25, random_state=321)`
- `MinMaxScaler`는 학습 데이터에만 `fit`
- 이웃 수 후보: `[2, 4, 6, 8, 10]`
- 각 모델의 RMSE를 비교하여 최적 이웃 수를 구하세요.'''),
    code("# Q3 풀이"),
]

a3_cells = applied_intro(3, "정답 — 파생변수와 KNN 회귀", "mobiles.csv", 390) + [
    markdown("## 공통 전처리 정답"),
    code(r'''import numpy as np
import pandas as pd

df = pd.read_csv('../../dataset/mobiles.csv')
base = df.loc[df['num_rear_camera'] != 1].copy()
base['performance'] = (
    (base['RAM'] + base['ROM'])
    / (base['num_rear_camera'] + base['num_front_camera'])
)
assert len(base) == 390
display(base.head())'''),
    markdown("## Q1 정답"),
    code(r'''cut = base['performance'].mean() + base['performance'].std()
answer_q1 = round(base.loc[base['performance'] > cut, 'discount_percent'].mean(), 3)
display(answer_q1)  # 0.098'''),
    markdown("## Q2 정답"),
    code(r'''features = ['ratings', 'num_of_ratings', 'sales_price',
            'discount_percent', 'performance']
sales_corr = base[['sales'] + features].corr()['sales'].drop(index='sales')
answer_var_q2 = sales_corr.abs().idxmax()
answer_coef_q2 = round(sales_corr.loc[answer_var_q2], 2)
display(answer_var_q2, answer_coef_q2)  # num_of_ratings, 0.95'''),
    markdown("## Q3 정답"),
    code(r'''from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import MinMaxScaler

features = ['ratings', 'num_of_ratings', 'sales_price',
            'discount_percent', 'performance', 'screen_size']
X = pd.get_dummies(base[features], columns=['screen_size'])
y = base['sales']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=321
)
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
rmse_by_k = {}
for k in [2, 4, 6, 8, 10]:
    model = KNeighborsRegressor(n_neighbors=k)
    model.fit(X_train_scaled, y_train)
    pred = model.predict(X_test_scaled)
    rmse_by_k[k] = mean_squared_error(y_test, pred) ** 0.5
answer_q3 = pd.Series(rmse_by_k).idxmin()
display(pd.Series(rmse_by_k), answer_q3)  # 2'''),
]
applied_sets.append((3, "mobile_preprocessing", q3_cells, a3_cells))


# ---------------------------------------------------------------------------
# Applied Set 4: point-of-sale customer aggregation
# ---------------------------------------------------------------------------
q4_cells = applied_intro(4, "고객 집계와 군집화", "sales_pos.csv", 5891) + [
    markdown(r'''## 공통 전처리

1. `prod_cat1`, `prod_cat2`, `prod_cat3`의 결측치를 0으로 채운 뒤 정수형, 이어서 문자열로 바꾸세요.
2. 세 카테고리 열을 `-`로 연결하여 `prod_cat`을 만드세요.
3. `user`별로 다음과 같이 집계하여 고객 단위 데이터 `base`를 만드세요.
   - `gender`, `age`, `job`, `city`, `marital`: `first`
   - `prod_count`: `prod`의 고유값 수
   - `category_count`: `prod_cat`의 고유값 수
   - `total_purchase`: `purchase`의 합계
   - `transaction_count`: 행 수
   - `avg_purchase`: `purchase`의 평균'''),
    code(r'''import numpy as np
import pandas as pd

df = pd.read_csv('../../dataset/sales_pos.csv')
# 공통 전처리 코드를 작성하세요.
'''),
    markdown("## Q1\n\n`city`별 `category_count` 평균을 구한 후 최댓값에서 최솟값을 빼고 소수점 둘째 자리까지 반올림하세요."),
    code("# Q1 풀이"),
    markdown(r'''## Q2

`total_purchase`와 `prod_count`, `category_count`, `avg_purchase`의 피어슨 상관계수를 구하세요. 절댓값이 가장 큰 변수명과 부호를 보존한 계수를 구하고 계수는 소수점 셋째 자리까지 반올림하세요.'''),
    code("# Q2 풀이"),
    markdown(r'''## Q3

고객을 K-Means로 군집화하세요.

1. `gender`: M=1, F=0으로 변환
2. `age`: 나이 구간 문자열에서 첫 번째 숫자를 추출해 숫자형으로 변환
3. `job`, `city`: 원-핫 인코딩
4. 나머지 입력 변수: `marital`, `prod_count`, `category_count`, `total_purchase`, `transaction_count`, `avg_purchase`
5. 전체 입력 변수를 `MinMaxScaler`로 변환
6. `KMeans(random_state=321, n_init=10)`, 군집 수 후보 `[3, 4, 5, 6]`

실루엣 점수가 가장 높은 군집 수와 그 점수를 소수점 셋째 자리까지 반올림하여 구하세요.'''),
    code("# Q3 풀이"),
]

a4_cells = applied_intro(4, "정답 — 고객 집계와 군집화", "sales_pos.csv", 5891) + [
    markdown("## 공통 전처리 정답"),
    code(r'''import numpy as np
import pandas as pd

df = pd.read_csv('../../dataset/sales_pos.csv')
work = df.copy()
category_cols = ['prod_cat1', 'prod_cat2', 'prod_cat3']
work[category_cols] = work[category_cols].fillna(0).astype(int).astype(str)
work['prod_cat'] = work[category_cols].agg('-'.join, axis=1)
base = work.groupby('user').agg(
    gender=('gender', 'first'),
    age=('age_group', 'first'),
    job=('job', 'first'),
    city=('city', 'first'),
    marital=('marital', 'first'),
    prod_count=('prod', 'nunique'),
    category_count=('prod_cat', 'nunique'),
    total_purchase=('purchase', 'sum'),
    transaction_count=('purchase', 'size'),
    avg_purchase=('purchase', 'mean')
).reset_index()
assert len(base) == 5891
display(base.head())'''),
    markdown("## Q1 정답"),
    code(r'''city_mean = base.groupby('city')['category_count'].mean()
answer_q1 = round(city_mean.max() - city_mean.min(), 2)
display(city_mean, answer_q1)  # 22.48'''),
    markdown("## Q2 정답"),
    code(r'''features = ['prod_count', 'category_count', 'avg_purchase']
purchase_corr = base[['total_purchase'] + features].corr()['total_purchase'].drop('total_purchase')
answer_var_q2 = purchase_corr.abs().idxmax()
answer_coef_q2 = round(purchase_corr.loc[answer_var_q2], 3)
display(answer_var_q2, answer_coef_q2)  # prod_count, 0.979'''),
    markdown("## Q3 정답"),
    code(r'''from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler

model_df = base.drop(columns='user').copy()
model_df['gender'] = model_df['gender'].replace({'M': 1, 'F': 0})
model_df['age'] = pd.to_numeric(
    model_df['age'].str.extract(r'(\d+)', expand=False), errors='coerce'
)
X = pd.get_dummies(model_df, columns=['job', 'city'])
X_scaled = MinMaxScaler().fit_transform(X)
scores = {}
for k in [3, 4, 5, 6]:
    labels = KMeans(n_clusters=k, random_state=321, n_init=10).fit_predict(X_scaled)
    scores[k] = silhouette_score(X_scaled, labels)
answer_k_q3 = pd.Series(scores).idxmax()
answer_score_q3 = round(scores[answer_k_q3], 3)
display(pd.Series(scores), answer_k_q3, answer_score_q3)  # 3, 0.238'''),
]
applied_sets.append((4, "customer_aggregation", q4_cells, a4_cells))


# ---------------------------------------------------------------------------
# Applied Set 5: credit-card customers
# ---------------------------------------------------------------------------
q5_cells = applied_intro(5, "그룹별 상관과 군집·회귀", "card_cust.csv", 980) + [
    markdown(r'''## 공통 전처리

1. `MINIMUM_PAYMENTS`의 결측치를 해당 열의 평균으로 채우세요.
2. `TENURE >= 8`인 고객만 남기세요.
3. `payment_ratio = PAYMENTS / (BALANCE + 1)`을 만드세요.'''),
    code(r'''import numpy as np
import pandas as pd

df = pd.read_csv('../../dataset/card_cust.csv')
# 공통 전처리 코드를 작성하세요.
'''),
    markdown(r'''## Q1

`TENURE`별로 `PAYMENTS`와 `CREDIT_LIMIT`의 피어슨 상관계수를 구하세요. 상관계수의 절댓값이 가장 큰 `TENURE`와 **부호를 보존한 계수**를 구하고 계수는 소수점 둘째 자리까지 반올림하세요.'''),
    code("# Q1 풀이"),
    markdown(r'''## Q2

`CUST_ID`를 제외한 모든 변수를 `StandardScaler`로 변환하고, `KMeans(random_state=321, n_init=10)`로 군집화하세요.

- 군집 수 후보: `[2, 3, 4, 5]`
- 실루엣 점수가 가장 높은 군집 수를 선택
- 선택된 군집별 원본 `CASH_ADVANCE` 평균을 구한 뒤, 가장 큰 평균을 소수점 둘째 자리까지 반올림'''),
    code("# Q2 풀이"),
    markdown(r'''## Q3

`CUST_ID % 5 != 0`을 학습 데이터, `CUST_ID % 5 == 0`을 평가 데이터로 사용하세요. `CUST_ID`와 목표변수 `PURCHASES`를 제외한 모든 열로 `DecisionTreeRegressor(random_state=321)`를 학습하고, 평가 데이터 RMSE를 소수점 둘째 자리까지 반올림하세요.'''),
    code("# Q3 풀이"),
]

a5_cells = applied_intro(5, "정답 — 그룹별 상관과 군집·회귀", "card_cust.csv", 980) + [
    markdown("## 공통 전처리 정답"),
    code(r'''import numpy as np
import pandas as pd

df = pd.read_csv('../../dataset/card_cust.csv')
base = df.copy()
base['MINIMUM_PAYMENTS'] = base['MINIMUM_PAYMENTS'].fillna(
    base['MINIMUM_PAYMENTS'].mean()
)
base = base.loc[base['TENURE'] >= 8].copy()
base['payment_ratio'] = base['PAYMENTS'] / (base['BALANCE'] + 1)
assert len(base) == 980
display(base.head())'''),
    markdown("## Q1 정답"),
    code(r'''corr_by_tenure = base.groupby('TENURE').apply(
    lambda group: group['PAYMENTS'].corr(group['CREDIT_LIMIT'])
)
answer_tenure_q1 = corr_by_tenure.abs().idxmax()
answer_coef_q1 = round(corr_by_tenure.loc[answer_tenure_q1], 2)
display(corr_by_tenure, answer_tenure_q1, answer_coef_q1)  # 10, 0.93'''),
    markdown("## Q2 정답"),
    code(r'''from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

X = base.drop(columns='CUST_ID')
X_scaled = StandardScaler().fit_transform(X)
scores, labels_by_k = {}, {}
for k in [2, 3, 4, 5]:
    labels = KMeans(n_clusters=k, random_state=321, n_init=10).fit_predict(X_scaled)
    scores[k] = silhouette_score(X_scaled, labels)
    labels_by_k[k] = labels
best_k = pd.Series(scores).idxmax()
clustered = base.copy()
clustered['cluster'] = labels_by_k[best_k]
cash_mean = clustered.groupby('cluster')['CASH_ADVANCE'].mean()
answer_q2 = round(cash_mean.max(), 2)
display(pd.Series(scores), best_k, cash_mean, answer_q2)  # k=2, 1332.76'''),
    markdown("## Q3 정답"),
    code(r'''from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor

train = base.loc[base['CUST_ID'] % 5 != 0].copy()
test = base.loc[base['CUST_ID'] % 5 == 0].copy()
features = base.columns.difference(['CUST_ID', 'PURCHASES'])
model = DecisionTreeRegressor(random_state=321)
model.fit(train[features], train['PURCHASES'])
pred = model.predict(test[features])
answer_q3 = round(mean_squared_error(test['PURCHASES'], pred) ** 0.5, 2)
display(answer_q3)  # 569.59'''),
]
applied_sets.append((5, "card_preprocessing", q5_cells, a5_cells))


# ---------------------------------------------------------------------------
# Applied Set 6: education enrollees, shared preprocessing like the original
# ---------------------------------------------------------------------------
q6_cells = applied_intro(6, "단계형 전처리와 분류", "edu_enrollees.csv", 7439) + [
    markdown(r'''## 공통 전처리

아래 순서대로 전처리하세요.

1. `city`, `company_size`, `company_type` 열 제거
2. 문자열(object) 열 가운데 결측치가 있는 행 제거
3. `experience`가 `>20`, `<1`인 행 제거 후 정수형 변환
4. `last_new_job`이 `>4`, `never`인 행 제거 후 정수형 변환
5. `education_level`이 `Primary School`인 행 제거
6. `education_level`을 `Graduate=1`, `Masters=2`, `Phd=3`으로 변환
7. `gender`가 `Other`인 행 제거
8. `target`은 정수형으로 변환'''),
    code(r'''import numpy as np
import pandas as pd

df = pd.read_csv('../../dataset/edu_enrollees.csv')
# 공통 전처리 코드를 작성하세요.
'''),
    markdown("## Q1\n\n`gender`별 `target` 평균을 구하고, 여성의 평균을 남성의 평균으로 나눈 값을 소수점 둘째 자리까지 반올림하세요."),
    code("# Q1 풀이"),
    markdown(r'''## Q2

아래 규칙으로 로지스틱 회귀용 데이터를 만드세요.

- `gender`, `relevant_experience`, `enrolled_university`, `major_discipline`: 각 열의 범주를 **사전순으로 정렬했을 때 첫 범주를 기준 범주로 제거**하여 원-핫 인코딩
- 나머지 입력 변수: `city_development_index`, `education_level`, `experience`, `last_new_job`, `training_hours`
- 목표변수: `target`
- `LogisticRegression(C=100000, max_iter=1000, solver='liblinear', random_state=321)`

전체 데이터로 모델을 학습하고 오즈비가 가장 큰 변수명과 오즈비를 구하세요. 오즈비는 반올림하지 말고 소수점 셋째 자리에서 버림하여 둘째 자리까지 표시하세요.'''),
    code("# Q2 풀이"),
    markdown(r'''## Q3

Q2에서 만든 입력 데이터에 원본의 `Xgrp`을 붙여 `train`과 `test`를 나누세요.

- `MinMaxScaler`는 train에만 `fit`
- `KNeighborsClassifier(n_neighbors=7, metric='euclidean')`
- 테스트 정확도를 소수점 둘째 자리까지 반올림'''),
    code("# Q3 풀이"),
]

a6_cells = applied_intro(6, "정답 — 단계형 전처리와 분류", "edu_enrollees.csv", 7439) + [
    markdown("## 공통 전처리 정답"),
    code(r'''import numpy as np
import pandas as pd

df = pd.read_csv('../../dataset/edu_enrollees.csv')
base = df.drop(columns=['city', 'company_size', 'company_type']).copy()
object_cols = base.select_dtypes(include='object').columns
base = base.dropna(subset=object_cols).copy()
base = base.loc[~base['experience'].isin(['>20', '<1'])].copy()
base['experience'] = base['experience'].astype(int)
base = base.loc[~base['last_new_job'].isin(['>4', 'never'])].copy()
base['last_new_job'] = base['last_new_job'].astype(int)
base = base.loc[base['education_level'] != 'Primary School'].copy()
base['education_level'] = base['education_level'].replace(
    {'Graduate': 1, 'Masters': 2, 'Phd': 3}
)
base = base.loc[base['gender'] != 'Other'].copy()
base['target'] = base['target'].astype(int)
assert len(base) == 7439
display(base.head())'''),
    markdown("## Q1 정답"),
    code(r'''target_rate = base.groupby('gender')['target'].mean()
answer_q1 = round(target_rate.loc['Female'] / target_rate.loc['Male'], 2)
display(target_rate, answer_q1)  # 0.94'''),
    markdown("## Q2 정답"),
    code(r'''from sklearn.linear_model import LogisticRegression

categorical = ['gender', 'relevant_experience',
               'enrolled_university', 'major_discipline']
numeric = ['city_development_index', 'education_level', 'experience',
           'last_new_job', 'training_hours']
dummy_parts = []
for col in categorical:
    categories = sorted(base[col].unique())
    dummy = pd.get_dummies(base[col], prefix=col)
    dummy = dummy.drop(columns=f'{col}_{categories[0]}')
    dummy_parts.append(dummy)
X = pd.concat([base[numeric]] + dummy_parts, axis=1)
y = base['target']
model = LogisticRegression(
    C=100000, max_iter=1000, solver='liblinear', random_state=321
)
model.fit(X, y)
odds_ratio = pd.Series(np.exp(model.coef_[0]), index=X.columns)
answer_var_q2 = odds_ratio.idxmax()
answer_or_q2 = np.floor(odds_ratio.max() * 100) / 100
display(odds_ratio.sort_values(ascending=False), answer_var_q2, answer_or_q2)
# relevant_experience_No relevant experience, 2.17'''),
    markdown("## Q3 정답"),
    code(r'''from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler

job = X.copy()
job['target'] = y
job['Xgrp'] = base['Xgrp']
train = job.loc[job['Xgrp'] == 'train'].copy()
test = job.loc[job['Xgrp'] == 'test'].copy()
X_train = train.drop(columns=['target', 'Xgrp'])
y_train = train['target']
X_test = test.drop(columns=['target', 'Xgrp'])
y_test = test['target']
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
knn = KNeighborsClassifier(n_neighbors=7, metric='euclidean')
knn.fit(X_train_scaled, y_train)
pred = knn.predict(X_test_scaled)
answer_q3 = round(accuracy_score(y_test, pred), 2)
display(answer_q3)  # 0.75'''),
]
applied_sets.append((6, "education_preprocessing", q6_cells, a6_cells))


for set_no, slug, question_cells, answer_cells in applied_sets:
    write_notebook(f"applied/{set_no:02d}_{slug}_test.ipynb", question_cells)
    write_notebook(f"answers/{set_no:02d}_{slug}_answer.ipynb", answer_cells)


readme = '''# 01~06 복습 모의고사

기존 `01~06_question.ipynb`와 `error_notes`를 토대로 만든 추가 연습 자료입니다.

## 구성

- `fill_in/01_06_fill_in_test.ipynb`: 오답노트 핵심 문법을 복습하는 코드 빈칸 문제
- `applied/01_*_test.ipynb` ~ `06_*_test.ipynb`: 공통 전처리를 포함한 신규 응용 문제
- `answers/01_06_fill_in_answer.ipynb`: 빈칸 문제 정답
- `answers/01_*_answer.ipynb` ~ `06_*_answer.ipynb`: 응용 문제 정답 및 실행 코드

## 추천 순서

1. 빈칸 테스트를 답을 보지 않고 풉니다.
2. 응용 문제에서는 먼저 공통 전처리의 최종 행 수가 맞는지 확인합니다.
3. Q1~Q3을 차례로 해결합니다.
4. 정답 노트북과 코드뿐 아니라 중간 객체의 형태와 인덱스도 비교합니다.

정답 숫자는 제공된 데이터와 `random_state`를 기준으로 검산되어 있습니다.
'''
(ROOT / 'README.md').write_text(readme, encoding='utf-8')
