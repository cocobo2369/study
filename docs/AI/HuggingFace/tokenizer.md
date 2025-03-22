# ✅ `self.tokenizer(...)`

`self.tokenizer(...)`는 HuggingFace의 `AutoTokenizer`를 기반으로 동작하며,  
입력 문장을 **모델이 이해할 수 있는 숫자(Tensor)** 형태로 변환해주는 매우 중요한 전처리 도구입니다.

---

## ✅ 1. 기본 사용 예시

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
inputs = tokenizer("I love pizza", return_tensors="pt")

print(inputs)
```

---

## 🧠 2. 반환값

dictionary 로 리턴

### 1. input_ids  
   - 각각의 토큰이 모델이 이해할 수 있는 정수 ID로 변환된 것
   - 모델 내부의 토큰 사전에 따라 매핑

### 2. attention_mask
  - 각 토큰이 실제 단어인지(1), 아니면 패딩인지(0) 구분  
    → 문장이 짧을 경우 패딩은 0이 되고, 무시됨

### 3. token_type_ids
   - 문장 구분용 (문장 A: 0, 문장 B: 1)  
     → BERT에서 두 문장을 비교할 때 사용됨 (단일 문장일 땐 전부 0)

---

## 📦 3. 반환 값 예시
```plaintext
"I love pizza" → [CLS] i love pizza [SEP]
                 ↓     ↓   ↓    ↓     ↓
input_ids      [101, 1045,2293,10733,102]
attention_mask [  1,    1,   1,    1,  1]
token_type_ids [  0,    0,   0,    0,  0]
```

```python
inputs =
{
  'input_ids': tensor([[  101,  1045,  2293, 10733,   102]]),
  'attention_mask': tensor([[   1,     1,     1,     1,     1]]),
  'token_type_ids': tensor([[   0,     0,     0,     0,     0]])
}
```

| 순서 | 토큰 문자열 | `input_ids` | `attention_mask` | `token_type_ids` | 의미 |
|------|--------------|--------------|------------------|------------------|------|
| 0    | `[CLS]`      | `101`        | `1`              | `0`              | 문장 시작 토큰 |
| 1    | `i`          | `1045`       | `1`              | `0`              | 첫 단어 |
| 2    | `love`       | `2293`       | `1`              | `0`              | 두 번째 단어 |
| 3    | `pizza`      | `10733`      | `1`              | `0`              | 세 번째 단어 |
| 4    | `[SEP]`      | `102`        | `1`              | `0`              | 문장 종료 토큰 |


---

## 🔧 4. 자주 쓰는 추가 옵션들

```python
tokenizer(
    "I love pizza",
    return_tensors="pt",
    padding=True,
    truncation=True,
    max_length=16,
    return_attention_mask=True
)
```

| 옵션 | 설명 |
|------|------|
| `padding` | 길이 맞춤용 (자동으로 0 패딩 추가) |
| `truncation` | 너무 긴 문장은 자름 |
| `max_length` | 최대 토큰 길이 제한 |
| `return_tensors` | PyTorch("pt") 또는 TensorFlow("tf") 형식 지정 |

---

## 🎯 6. 전체 시각 요약



---

## 💡 7. 응용 팁

- 두 문장을 비교할 경우:
  ```python
  tokenizer("I love pizza", "You hate pizza", return_tensors="pt")
  ```
  → token_type_ids가 0과 1로 나뉘어져 나옵니다.

- 토큰 ID를 다시 문자열로 복원하려면:
  ```python
  tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
  ```
  → `['[CLS]', 'i', 'love', 'pizza', '[SEP]']`

---

## ✅ 결론

> `self.tokenizer(...)`는 자연어를 숫자로 바꿔주는 핵심 도구입니다.  
> 이 값들만 있으면 모델에 바로 넣어도 작동하고, 검색・분류・생성 같은 다양한 작업에 쓸 수 있어요! 🔥

---

더 궁금한 게 있거나, 토큰화 과정을 시각화해서 이미지처럼 보고 싶으시면 말씀 주세요! 😄