

# JSON 데이터셋을 불러와서, 토크나이저를 적용해 전처리하는 과정

## 🔹 1️⃣ JSON 데이터셋 불러오기

```python
dataset = DatasetDict.from_json({'train': path_json_dataset})
```

✅ **해석:**

- `path_json_dataset`에 있는 JSON 파일을 불러와서 **"train"이라는 이름의 데이터셋으로 구성**합니다.
- 결과적으로 `dataset`은 다음과 같은 구조가 됩니다:

```python
DatasetDict({
  'train': Dataset({
    features: ['text'],
    num_rows: N
  })
})
```

📌 `DatasetDict`는 `train`, `test`, `validation` 등의 세트를 가진 딕셔너리 형태의 데이터셋입니다.

---

## 🔹 2️⃣ 데이터 출력 (불러온 후)

```python
print('dataset:', dataset)
```

✅ **해석:**

- 전체 데이터셋 정보를 출력합니다.
- 출력 예시:
```python
dataset: DatasetDict({
  train: Dataset({
    features: ['text'],
    num_rows: 1000
  })
})
```

---

## 🔹 3️⃣ 토크나이저 적용 (map)

```python
dataset = dataset.map(
    lambda x: tokenizer(
        x["text"], truncation=True, padding=True, max_length=512
    ),
    batched=True,
    remove_columns=dataset["train"].column_names
)
```

✅ **해석:**

- 각 샘플의 `"text"` 컬럼에 대해 토크나이저를 적용해 **모델 학습에 맞는 입력 포맷(`input_ids`, `attention_mask`)**으로 변환합니다.
- `truncation=True`: 512 토큰 초과 시 자르기
- `padding=True`: 길이가 짧은 문장은 512까지 패딩
- `remove_columns`: `"text"`와 같은 원래 컬럼은 제거하고, **새로운 토큰화 결과만 남김**

예:  
```python
Before: {'text': "Hello world"}
After: {'input_ids': [...], 'attention_mask': [...]}
```

---

## 🔹 4️⃣ 처리 후 데이터 출력

```python
print('after map, dataset:', dataset)
```

✅ **해석:**

- 토크나이징 후 변경된 데이터셋을 출력합니다.
- 출력 예시:
```python
after map, dataset: DatasetDict({
  train: Dataset({
    features: ['input_ids', 'attention_mask'],
    num_rows: 1000
  })
})
```

---

## ✅ 전체 흐름 요약

| 단계 | 설명 |
|------|------|
| JSON 로딩 | JSON 파일을 Hugging Face의 `DatasetDict` 형식으로 불러옴 |
| 텍스트 전처리 | `"text"` 필드를 `tokenizer`로 처리해 `input_ids`, `attention_mask` 생성 |
| 원본 제거 | `remove_columns` 옵션으로 `"text"` 제거 |
| 상태 출력 | 처리 전과 후의 데이터셋 상태를 확인함 |

---