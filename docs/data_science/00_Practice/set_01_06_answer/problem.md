제공해주신 데이터 사이언스 실전 문제풀이(119~146페이지) 내용을 깔끔하고 가독성 좋은 마크다운 형식으로 완벽하게 정리해 드립니다. 불필요한 페이지 번호나 소스 코드는 제거하고, 표와 수식은 마크다운 문법에 맞게 재구성했습니다.

---

# [Level 2] Data Science 역량강화 실전과정(Python) - 실기 대비

---

## 📝 실전 문제풀이 Set 1: 시중 TV 제품별 분석

### 1) 데이터 및 시나리오

▶ 시중 판매 중인 TV 정보를 온라인 쇼핑몰 웹페이지에서 크롤링하여 분석하고자 한다. 해당 데이터를 기반으로 각 TV의 제원은 어떠한지, 제원에 따른 평가는 어떠한지 알아보고 향후 신제품 출시에 참고하고자 한다.

* **데이터 개요:** `Xa TV.csv` (666 rows, 11 columns, UTF-8)

**[변수 상세]**

| 변수명 | 유형 | 설명 |
| --- | --- | --- |
| `Product_Name` | string | 상품명 |
| `Stars` | float | 평가 평균 점수 |
| `Ratings` | int | 평가 수 |
| `Reviews` | int | 후기 수 |
| `current_price` | int | 현재 가격 |
| `MRP` | int | 출고가 |
| `channel` | string | 판매 채널 / 공장 정보 등 |
| `Operating_system` | string | 운영체제 |
| `Picture_quality` | string | 해상도 |
| `Speaker` | string | 스피커 |
| `Frequency` | string | 주사율 |

### 2) 문제

* **필요 라이브러리:** `from sklearn.ensemble import RandomForestRegressor`

**Q01.** 주사율(Frequency)은 TV 제원 중 가격에 큰 영향을 미치는 제원이다. 그런데 데이터 수집 중 실수가 발생하여 주사율(Frequency) 값 중 일부가 해상도(Picture_quality), 스피커(Speaker) 변수에 잘못 입력된 것이 발견되었다. 세 변수에 흩어져 있는 주사율 데이터를 취합하여 전체 TV 중에서 **주사율이 60Hz인 TV는 총 몇 대 인가?**

* ※ 주사율은 2~3자리 숫자 뒤에 반드시 Hz라는 단위로 표기되어 있다.
* ※ 세 변수 모두 주사율 정보가 없을 경우 결측치로 간주하고 이를 분석에서 제외하시오. (정답 예시: 12)

**Q02.** TV의 해상도(Picture_quality)는 HD, 4K, 8K로 나뉜다. 최근 시장에 등장한 8K 제품군은 상대적으로 비싸 비교적 매출이 떨어지는 편이다. 하지만 8K 제품군 구매자가 4K 제품군 구매자 대비 얼마나 만족하고 있는지 확인해보고자 한다. **8K 제품군의 평가 평균 점수(Stars)의 평균값과 4K 제품군의 평가 평균 점수와의 평균값 차이의 절대값을 산출하시오.**

* ※ 화면 해상도는 관련 변수에서 "HD", "4K", "8K"로 찾아낼 수 있다.
* ※ 화면 해상도 정보는 "Operating_system", "channel", "Picture_quality" 변수에 흩어져 있다.
* ※ 결과는 반올림하여 소수점 둘째 자리까지 출력하시오. (정답 예시: 0.12)

**Q03.** 좋은 평가를 받는 제품의 조건을 알아보고자 한다. 이를 위해 기존 변수와 더불어 여러 파생변수를 생성 후 해당 변수를 독립변수로 하고 평가 평균 점수(Stars)를 종속변수로 하여 Random Forest 분석을 통해 좋은 평가를 받는 제품의 조건을 알아보고자 한다. 아래 절차를 수행하여 변수 중요도를 확인하고, **변수 중요도 값 중 가장 큰 값을 가진 변수명을 기술하시오.**

* `<독립변수>`
* 후기 작성 비율: 후기 수(Reviews) / 평가 수(Ratings)
* 공장 출고가(MRP)
* 할인율: 현재 판매가(current_price) / 공장 출고가(MRP)
* Netflix 제공 여부: 제공(1), 미제공(0)
* Prime Video 제공 여부: 제공(1), 미제공(0)
* 고해상도 여부: 4K 또는 8K(1), 나머지(0)


* `<종속변수>`
* 평가 평균 점수(Stars)


* ※ channel 변수에 해상도('Pixel' 문자 참조) 또는 운영체제 정보('Oper' 문자 참조)가 있는 TV는 분석에서 제외하시오.
* ※ Netflix와 Prime Video 제공 여부 변수는 channel 변수를 참고하시오.
* ※ 독립변수를 생성하면서 결측치가 생성되는 경우 해당 행을 모두 제거하시오.
* ※ 학습 대상이 되는 행 개수는 197이다.
* ※ 고해상도 여부 변수 생성은 해상도(Picture_quality) 변수만 참고하여 생성하시오.
* ※ seed는 123으로 지정하시오. (정답 예시: 고해상도여부 - 띄어쓰지 않고 문제에서 제시된 독립변수 명을 기입)

---

## 📝 실전 문제풀이 Set 2: 갤럭시 사용자 데이터 분석

### 1) 데이터 및 시나리오

▶ 디지털 기기 취급 전문업체 DigiSales는 오프라인 매장에서 갤럭시 제품군을 구매한 이력이 있는 사람들의 단말기 이용 행태를 분석하기 위해 통신사 MT로부터 익명화 처리된 고객 정보를 일부 구매하였다. 해당 데이터에서 인사이트를 뽑기 위해 다양한 분석을 해보고자 한다.

* **데이터 개요:** `galaxy_users.csv` (7032 rows, 21 columns, UTF-8)

**[변수 상세]**

| 변수명 | 유형 | 설명 |
| --- | --- | --- |
| `customerID` | string | 고객 식별자 |
| `gender` | string | 성별 |
| `Senior Citizen` | int | 시니어 여부(1: 시니어, 0: 아님) |
| `Partner` | string | 배우자 존재 여부(Yes, No) |
| `Dependents` | string | 부양가족(Yes, No) |
| `tenure` | int | 현 직장 근속 월수 |
| `PhoneService` | string | 단말 서비스 사용 여부(Yes, No) |
| `MultipleLines` | string | 다중 회선 개통 여부(Yes, No) |
| `InternetService` | string | 인터넷 사용(DSL, Fiber optic, No) |
| `OnlineSecurity` | string | 온라인 보안 서비스(Yes, No) |
| `OnlineBackup` | string | 온라인 백업 서비스(Yes, No) |
| `Device Protection` | string | 기기 보호 서비스(Yes, No) |
| `TechSupport` | string | 기술 지원 서비스(Yes, No) |
| `Streaming TV` | string | 스트리밍 지원 TV(Yes, No) |
| `Streaming Movies` | string | 영화 스트리밍 서비스(Yes, No) |
| `Contract` | string | 계약 갱신 주기 |
| `PaperlessBilling` | string | 온라인 명세서 발급 서비스(Yes, No) |
| `Payment Method` | string | 납부 방법 |
| `MonthlyCharges` | float | 월별 청구 금액 |
| `TotalCharges` | float | 누적 청구 금액 |
| `Churn` | string | 이탈 여부(Yes: 이탈, No: 잔존) |

### 2) 문제

* **필요 라이브러리:** `MinMaxScaler`, `train_test_split`, `LogisticRegression`, `f1_score`

**Q01.** 부가 서비스를 많이 사용할수록 제품 또는 브랜드에 고관여 되어있다는 가설을 세우고 분석을 하고자 한다. 이에 앞서 고객별 부가서비스 사용 현황 통계를 산출하고자 한다. **부가 서비스를 1개 사용하는 사람은 부가 서비스를 6개 사용하는 사람보다 몇 배나 많은지 계산하시오.**

* ※ 부가서비스 대상 변수: OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, Streaming TV, Streaming Movies
* ※ 부가서비스 변수의 범주가 "Yes"인 경우 1로, "No"는 0으로 간주한다.
* ※ 부가서비스 변수에 "Yes" 또는 "No"가 아닌 다른 범주가 있는 경우 해당 행은 제거 후 분석하시오.
* ※ 정답은 반올림하여 소수점 첫째 자리까지 출력하시오. (정답 예시: 1.2)

**Q02.** 여러 변수간 상관관계를 확인하고자 한다. **현 직장 근속 월수(tenure), 월별 청구 금액(MonthlyCharges), 통신사 사용 월수 간 피어슨 상관분석을 실시하고 그 결과 중 상관계수 절대값이 가장 높은 것을 확인하시오.**

* ※ 통신사 사용 월수는 총 청구금액(TotalCharges)을 월별 청구금액(MonthlyCharges)으로 나눈 값의 몫으로 한다.
* ※ 정답은 반올림하여 소수점 셋째 자리까지 출력하시오. (정답 예시: 0.123)

**Q03.** 고객 이탈여부(Churn)를 종속변수로 하는 모델을 만들어보고자 한다. 데이터 분할 후 정규화를 실시하여 로지스틱 회귀분석을 실시하고 해당 모델을 기준점 삼아 모델을 개선하고자 한다. **주어진 독립변수를 활용하여 F1-score로 모델을 평가하시오.**

* `<독립변수>`: 시니어 여부, 파트너 존재 여부, 부양가족 존재 여부, 현 직장 근속 개월 수, 월별 청구 금액, 누적 청구 금액, 온라인 보안 서비스, 온라인 백업 서비스, 기기 보호 서비스, 기술 지원 서비스, 영화 스트리밍 서비스, 온라인 명세서 발급 서비스
* `<종속변수>`: 고객 이탈여부
* ※ 범주형 변수의 범주가 "Yes"인 경우 1로, "No"인 경우 0으로 치환하며, 나머지 범주는 -1로 치환하시오.
* ※ 학습 및 평가 데이터 세트 분할비는 7:3으로 하시오.
* ※ Min-Max 정규화를 실시하며(모든 변수 대상), 평가 데이터 세트는 학습 데이터 세트 기반으로 정규화 하시오.
* ※ seed는 123으로 고정하시오.
* ※ 정답은 반올림하여 소수점 둘째 자리까지 출력하시오. (정답 예시: 0.12)

---

### 💡 실전문제 핵심 요약 (Set 01 ~ 02)

* **Set 01:** 텍스트 처리 관련 메서드 용법 숙지, 다중 변수 데이터 통합, `.apply()` 및 `lambda` 함수 활용, 반복 작업으로 인한 잔실수 주의
* **Set 02:** 범주형 변수의 값 치환, `.apply()` 및 `lambda`를 사용한 신규 변수 생성, 학습/평가 데이터 정규화 절차 유의, seed 설정 유의

---

## 📝 실전 문제풀이 Set 3: 시중 스마트폰 상세 정보

### 1) 데이터 및 시나리오

▶ 신입사원 김모씨는 신규 스마트폰 스펙 기획 업무를 보조하기 위해 온라인 디지털 마켓 사이트에서 판매 중인 스마트폰 데이터를 수집하여 이를 분석하고 백데이터로 활용하기로 결심하였다.

* **데이터 개요:** `Xa mobiles.csv` (430 rows, 11 columns, UTF-8)

**[변수 상세]**

| 변수명 | 유형 | 설명 |
| --- | --- | --- |
| `screen_size` | string | 화면 크기 |
| `ROM` | int | 저장 공간 용량 |
| `RAM` | int | RAM 용량 |
| `num_rear_camera` | int | 후면 카메라 개수 |
| `num_front_camera` | int | 전면 카메라 개수 |
| `battery_capacity` | int | 배터리 용량 |
| `ratings` | float | 평가 점수 평균 |
| `num_of_ratings` | int | 평가 개수 |
| `sales_price` | int | 판매가격 |
| `discount_percent` | float | 할인율 |
| `sales` | float | 판매 지수 |

### 2) 문제

* **필요 라이브러리:** `MinMaxScaler`, `train_test_split`, `KNeighborsRegressor`, `mean_squared_error`

**Q01.** 판매지수(sales)를 기준으로 이상치라고 판단되는 제품을 '주목받는 제품'이라고 판단하고 해당 제품들의 성능지표를 산출하시오. **산출된 성능지표의 평균은 얼마인가?**

* `<성능지표 계산식>`:  $E = \frac{ROM}{32} + \frac{RAM}{2} + \text{카메라 개수} + \frac{battery\_capacity}{1000}$
* ※ 카메라 개수 = num_rear_camera + num_front_camera
* ※ 이상치는 평균으로부터 2표준편차보다 큰 값으로 정의한다.
* ※ 결과는 반올림하여 소수점 둘째 자리까지 계산하시오. (정답 예시: 0.12)

**Q02.** 판매 지수(sales)와 가장 상관관계가 높은 변수를 찾고자 한다. 배터리 용량, 평가 점수 평균, 평가 개수, 판매 가격, 할인율 변수와 판매 지수를 피어슨 상관분석을 실시하였을 때, **상관계수의 절대값이 가장 큰 변수의 상관계수는 얼마인가?**

* ※ 후면 카메라가 1개인 제품은 제외하시오.
* ※ 결과는 반올림하여 소수점 둘째 자리까지 출력하시오. (정답 예시: 0.12)

**Q03.** 판매 지수(sales)를 예측하기 위해 k-NN 알고리즘을 사용하고, 이웃의 개수를 변화하면서 가장 성능이 좋은 모델을 확보하려 한다. **RMSE를 기준으로 가장 성능이 좋은 모델을 확인하고 해당 모델의 k(이웃 개수)를 구하라.**

* `<독립변수>`: 판매 지수를 제외한 모든 변수
* `<종속변수>`: 판매 지수
* ※ 명목형 독립변수는 One Hot Encoding을 실시하시오. (학습에 사용하는 독립변수 개수는 14개)
* ※ 분할비는 8:2, Min-Max 정규화 실시, seed 123.
* ※ 최근접 이웃은 3, 5, 7, 9, 11개를 사용하시오. (정답 예시: 7)

---

## 📝 실전 문제풀이 Set 4: 디지털프라자 매출 데이터

### 1) 데이터 및 시나리오

▶ 디지털프라자 A지점에서 연휴 직전에 대대적인 할인 행사를 진행했다. 예상보다 많은 손님이 방문했고, 발생한 매출 데이터를 취합하여 향후 발송할 판촉물 컨텐츠를 기획하고자 한다. (1행 = 물품 1개 구매 내역)

* **데이터 개요:** `Xa sales_pos.csv` (550068 rows, 11 columns, UTF-8)

**[변수 상세]**

| 변수명 | 유형 | 설명 |
| --- | --- | --- |
| `user` | int | 고객 식별자 |
| `prod` | string | 상품 식별자 |
| `gender` | string | 성별 |
| `age_group` | string | 연령대 |
| `job` | int | 직업 구분 |
| `city` | string | 도시 유형 구분 |
| `marital` | int | 결혼 여부(1: 결혼) |
| `prod_cat1` | int | 상품 카테고리(1차) |
| `prod_cat2` | int | 상품 카테고리(2차) |
| `prod_cat3` | int | 상품 카테고리(3차) |
| `purchase` | int | 결제 금액 |

### 2) 문제

* **필요 라이브러리:** `MinMaxScaler`, `KMeans`, `silhouette_score`

**Q01.** 상품별 매출액(purchase)을 합산하여 그 매출액이 가장 큰 상품을 확인하고, **해당 상품을 가장 많이 구매하는 직업(job)을 확인하시오.**

* ※ 직업 확인 시 상품 구매 개수를 기준으로 확인하시오. 결과는 job 변수의 번호를 출력. (정답 예시: 1)

**Q02.** 결혼 여부(marital)에 따라 구매하는 물품 종류 차이를 확인하고자 한다. 비교적 신혼부부가 많은 26-35세 그룹을 대상으로 각 고객의 구매물품 카테고리 개수를 산출하고, **결혼여부별로 그 평균값의 차이를 산출하시오.**

* ※ 구매 물품 카테고리 개수 산출에는 prod_cat1, 2, 3을 사용하며 결측치는 0으로 대치한다.
* ※ 카테고리 처리 예시: `prod_cat1=1, 2=2, 3=0` -> `1-2-0`
* ※ 정답은 절대값을 반올림하여 소수점 둘째 자리까지 출력하시오. (정답 예시: 0.12)

**Q03.** 고객 5891명을 군집화하여 마케팅 전략을 수립하고자 한다. 제시된 변수(성별, 구매 상품 종류수, 나이, 직업, 총 구매금액, 도시, 결혼 여부)를 대상으로 **k-means 군집분석(K=7)을 실시했을 때 Silhouette score를 산출하시오.**

* ※ 성별 변수는 M=1, F=0으로 변환, 나이는 순서형(0~6)으로 변환, 직업과 도시는 One Hot Encoding.
* ※ 사용 변수는 총 29개이며 MinMax 정규화 후 분석. seed는 123. (정답 예시: 0.12)

---

## 📝 실전 문제풀이 Set 5: 신용카드 고객정보 분석

### 1) 데이터 및 시나리오

▶ 삼성카드의 비식별화된 고객 데이터를 활용하여 통합 분석을 위한 선제 분석을 수행한다.

* ※ 분석 전 '기한 내 최소 지불 금액(MINIMUM_PAYMENTS)' 결측값(Null)을 각 컬럼 평균값으로 대체하고, 이를 `base` 객체로 지칭하여 문제 풀이에 사용한다.
* **데이터 개요:** `Xa card_cust.csv` (1000 rows, 18 columns, UTF-8)

**[주요 변수 상세]**
`BALANCE`(잔고), `PURCHASES`(구매총액), `ONEOFF_PURCHASES`(일시불), `CASH_ADVANCE`(현금서비스), `CREDIT_LIMIT`(한도), `TENURE`(이용기간) 등 18개 변수 구성.

### 2) 문제

* **필요 라이브러리:** `StandardScaler`, `KMeans`, `silhouette_score`, `DecisionTreeRegressor`

**Q01.** (`base` 사용) 연간 평균 잔고액(BALANCE)과 신용카드 서비스 이용기간(TENURE) 간의 관계를 파악하고자 한다. **신용카드 서비스 이용기간(TENURE) 별로 연간 평균 잔고액(BALANCE)과 신용카드 한도(CREDIT_LIMIT) 간 피어슨 상관분석을 실시하고, 이 중 가장 큰 상관계수를 구하시오.**

* ※ 정답은 반올림하여 소수점 둘째 자리까지 출력하시오.

**Q02.** (`base` 사용) 일시불 구매 금액이 높은 고객군 도출을 위해 '고객 ID' 제외 17개 변수를 Z-score 표준화 후 K-means 군집 분석(K=2~5 중 실루엣 점수가 가장 높은 최적의 K)을 수행한다. **군집 별 일시불 구매 총액(ONEOFF_PURCHASES)의 평균 중 가장 큰 값은 얼마인가?** (정규화하지 않은 원본 기준, seed=1234)

**Q03.** (`base` 사용) '고객 ID'가 4의 배수가 아닌 데이터를 Train, 4의 배수인 데이터를 Test Set으로 분할한다. Train Set으로 의사결정나무 회귀모델(종속: 일시불 구매 총액)을 학습하고 Test Set을 예측한다. **이때 예측 성능을 평가하는 Measure B(RMSE)를 계산한 값은?**

* $B = \left( \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2 \right)^{\frac{1}{2}}$
* ※ 정답은 반올림하여 소수점 둘째 자리까지 출력, seed=1234.

---

## 📝 실전 문제풀이 Set 6: 교육 수강자 분석

# set 6

## 1) 데이터 및 시나리오

### 교육 수강자 분석

> 삼성전자 임직원의 체계적인 커리어 패스 설계를 위해 데이터 분석과 같은 Hard Skill 역량과 Soft Skill 역량을 조화롭게 함양하기 위해 HRD 부서의 조프로는 전산팀의 협조를 받아 데이터를 확보하였다.

※ 분석을 수행하기 전, 상기 데이터를 이용하여 아래의 전처리를 수행하시오.

- **단계 1:** 분석에 사용하지 않을 `city`, `company_size`, `company_type` 컬럼을 제거하시오.
- **단계 2:** 각 문자형 변수에 결측치가 하나라도 존재하는 행은 모두 제거하시오.
- **단계 3:** `experience` 변수 값이 `'>20'` 또는 `'<1'`이 있는 행을 제거하고 `experience` 변수의 유형을 정수로 변환하시오.
- **단계 4:** `last_new_job` 변수의 값이 `'>4'` 또는 `'never'`인 행을 제거하고 해당 변수의 유형을 정수로 변환하시오.

전처리 수행 이후 행 개수는 **7,522**이며 전처리가 완료된 데이터를 `base` 객체로 지정하고 이를 사용하여 문제를 풀이하시오.

### 데이터 개요

| 파일명 | 행 | 열 | 인코딩 |
|---|---:|---:|---|
| `edu_enrollees.csv` | 19158 | 15 | UTF-8 |

---

## 1) 데이터 및 시나리오

### 변수 상세

| 변수명 | 유형 | 설명 |
|---|---|---|
| `enrollee_id` | int | 수료자 ID |
| `city` | string | 도시 코드 |
| `city_development_index` | float | 도시 발전 지표 |
| `gender` | string | 성별 |
| `relevant_experience` | string | 관련 분야 경험 여부 |
| `enrolled_university` | string | 수강 과목명 |
| `education_level` | string | 학력 |
| `major_discipline` | string | 전공 |
| `experience` | string | 경력 |
| `company_size` | string | 현 직장 직원 수 |

### 변수 상세

| 변수명 | 유형 | 설명 |
|---|---|---|
| `company_size` | string | 현 직장 직원 수 |
| `company_type` | string | 현 직장 유형 |
| `last_new_job` | string | 전 직장 근속연수 |
| `training_hours` | int | 수료 시간 |
| `target` | int | 전배 희망 여부 `(0: 비희망, 1: 희망)` |
| `Xgrp` | string | Train/Test Set 구분 |

---

## 2) 문제

### 필요 라이브러리 함수 및 클래스 목록

| 목록 |
|---|
| `from sklearn.linear_model import LogisticRegression` |
| `from sklearn.neighbors import KNeighborsClassifier` |

---

### Q01.

`base`를 사용하여 관련 분야 경험 여부(`relevant_experience`)에 따른 전배 희망 여부(`target`)를 기술통계량으로 확인하고자 한다.

관련 분야 경험이 없는 수료자 중 전배를 희망하는 수료자의 비율을 **A**,  
관련 분야 경험이 있는 수료자 중 전배를 희망하는 수료자의 비율을 **B**라 할 때,  
**A/B를 구하시오.**

※ 관련 경험이 없는 사람은 `relevant_experience` 변수의 값이 `'No relevant experience'`인 사람으로 정의한다.  
※ 관련 경험이 있는 사람은 `relevant_experience` 변수의 값이 `'Has relevant experience'`인 사람으로 정의한다.  
※ 정답은 반올림하여 소수점 둘째 자리까지 출력하시오. `(정답 예시: 0.12)`

---

### Q02.

`base`를 사용하여 전배 희망 여부(`target`)에 영향을 주는 변수들을 확인하고자 한다.  
다음 절차에 따라 로지스틱 회귀분석을 수행하고 질문에 답하시오.

#### 단계 1

`gender`, `relevant_experience`, `enrolled_university`, `education_level`, `major_discipline` 변수로부터 더미 변수들을 생성한다.

단, 각 변수로부터 더미 변수를 생성할 때 마지막으로 등장하는 범주는 제외하도록 한다.

여기서 마지막으로 등장하는 범주란, 각 컬럼의 값을 사전 순으로 나열하였을 때 마지막으로 등장하는 값이다.

예를 들어, `col` 변수의 범주가 `['A', 'C', 'B', 'B', 'C', 'A']`의 값을 가진다면 사전 상의 마지막 값인 `C`가 제외된다.

#### 단계 2

단계 1에서 생성한 더미 변수와 `city_development_index`, `experience`, `last_new_job`, `training_hours`, `target`, `Xgrp` 변수를 결합하여 새로운 데이터셋을 구성한다.

- 데이터셋명: `job2`
- 이 데이터셋은 문제 3에서도 활용

이 때, `target`, `Xgrp`를 제외한 데이터셋의 컬럼은 아래 순서에 따르도록 한다.

1. `city_development_index`
2. `experience`
3. `last_new_job`
4. `training_hours`
5. `gender`의 더미 변수
6. `relevant_experience`의 더미 변수
7. `enrolled_university`의 더미 변수
8. `education_level`의 더미 변수
9. `major_discipline`의 더미 변수

#### 단계 3

단계 2에서 구성한 데이터셋 `job2`로 다음 조건에 따라 상수항(`Intercept`)이 포함된 로지스틱 회귀분석을 수행한다.

- 종속 변수: `target`
- 독립 변수(총 16개): `target`과 `Xgrp`를 제외한 나머지 변수
- 회귀식에 포함되는 독립 변수의 순서를 컬럼의 순서와 일치시킨다.

**상수항을 제외한 나머지 변수들에 대한 Odds Ratio 중 가장 큰 값을 기술하시오.**

$$
x_i \text{의 Odds Ratio}
=
\frac{
odds(P(Y=1|x_1,\cdots,x_i+1,\cdots,x_n))
}{
odds(P(Y=1|x_1,\cdots,x_i,\cdots,x_n))
}
$$

※ `LogisticRegression()` 클래스의 인자 `C`는 `100000`, `max_iter=1000`, `solver='liblinear'`으로 지정하시오.  
※ `LogisticRegression()` 클래스의 인자 `random_state`는 `123`으로 지정하시오.  
※ 정답은 소수점 셋째 자리에서 버림하여 둘째 자리까지 출력하시오. `(정답 예시: 0.12)`

---

### Q03.

`job2`를 이용하여 전체 데이터를 Train과 Test Set으로 나누고, Train Set으로 학습한 모델을 Test Set에 적용하여 모델을 평가하고자 한다.

다음 절차에 따라 분석을 수행하고 질문에 답하시오.

#### 단계 1

2단계에서 구성한 데이터셋 `job2`에서 `Xgrp` 컬럼의 값이 `'train'`인 경우 Train Set으로, `'test'`인 경우 Test Set으로 정의하여 분할한다.

#### 단계 2

아래 가이드에 따라 Train Set으로 K-NN 분류 모델을 학습하고, 이 모델을 Test Set에 적용한다.

- 종속 변수: 전배 희망 여부(`target`)
- 독립 변수(총 16개): 전배 희망 여부(`target`)와 Train/Test set 구분 변수(`Xgrp`)를 제외한 모든 변수
- Euclidean 거리 기준 가장 가까운 5개 데이터의 전배 희망 여부(`target`)를 활용하여 예측

#### 단계 3

예측 결과를 바탕으로 아래 정의된 지표 **A**를 계산하여 기술하시오.

$$
A =
\frac{
(\# \text{ of true positive}) + (\# \text{ of true negative})
}{
(\# \text{ of total data})
}
$$

※ 정답은 반올림하여 소수점 둘째 자리까지 출력하시오. `(정답 예시: 0.12)`

---

## 💡 문제 답안 (정답표)

### [실기 주관식]

*(Pandas 2, sklearn 1.2.2 기준)*

| 세트 | Q01 | Q02 | Q03 |
| --- | --- | --- | --- |
| **Set 01** | 510 | 0.38 | 할인율 |
| **Set 02** | 3.4 | 0.999 | 0.55 |
| **Set 03** | 11.01 | 0.95 | 3 |
| **Set 04** | 4 | 0.13 | 0.18 |
| **Set 05** | 0.95 | 3946.19 | 1039.2 |
| **Set 06** | 1.77 | 1.67 | 0.71 |