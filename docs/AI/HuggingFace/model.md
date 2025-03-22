
## 🔹 1. 기본 호출 형태
`embedding = self.model(token_ids)` 이 한 줄은 HuggingFace의 트랜스포머 모델에서 **가장 핵심적인 부분** 중 하나입니다.  
이 한 줄을 제대로 이해하면, BERT 기반 모델의 동작을 훨씬 잘 이해할 수 있습니다.

```python
outputs = self.model(token_ids)
```

여기서 `self.model`은 HuggingFace에서 `AutoModel.from_pretrained(...)`으로 불러온 모델입니다.  
예: `bert-base-uncased`, `distilbert-base-uncased`, `roberta-base` 등

이 모델은 `token_ids`를 입력받으면 다양한 **출력값(Output)** 을 튜플 또는 `ModelOutput` 객체 형태로 반환합니다.

---

## 🔸 2. 리턴 타입 (출력)

### ✅ 대부분의 `AutoModel` 기반 모델은 다음과 같은 형태를 리턴합니다:

```python
BaseModelOutput(
    last_hidden_state=...,
    hidden_states=...,         # (옵션)
    attentions=...             # (옵션)
)
```

### 또는 튜플처럼 사용할 수 있어서 아래처럼도 됩니다:

```python
outputs = self.model(token_ids)
outputs[0]  # last_hidden_state
```

---

## 🔹 3. 주요 리턴 값 설명

| 이름 | 형태 | 설명 |
|------|------|------|
| `last_hidden_state` | `[batch_size, seq_len, hidden_size]` | 각 토큰의 임베딩 벡터 (예: BERT는 768차원),hidden_states의 마지막 list 원소 |
| `pooler_output` | `[batch_size, hidden_size]` | `[CLS]` 토큰만 뽑아 처리한 전체 문장 대표 벡터 (일부 모델에만 존재) |
| `hidden_states` | list of tensors | 각 레이어별 hidden state들 (옵션, `output_hidden_states=True` 시) |
| `attentions` | list of tensors | 각 레이어별 어텐션 행렬들 (옵션, `output_attentions=True` 시) |

---

## 🔸 예시: `bert-base-uncased` 모델 기준

```python
from transformers import AutoTokenizer, AutoModel
import torch

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

text = "Hello world"
tokens = tokenizer(text, return_tensors="pt")

with torch.no_grad():
    outputs = model(**tokens)
```

### 출력 구조 확인
```python
print(outputs.keys())  
# => odict_keys(['last_hidden_state', 'pooler_output'])

print(outputs.last_hidden_state.shape)  
# => torch.Size([1, 3, 768])  
# 1: 배치 크기, 3: 토큰 개수 ([CLS], hello, world), 768: 히든 사이즈
```

---

## 🔹 4. 실무에서는 어떻게 활용?

### 🔸 토큰 단위 임베딩 → 평균 풀링
```python
token_embeddings = outputs.last_hidden_state  # shape: [1, seq_len, hidden_size]
sentence_embedding = token_embeddings.mean(dim=1)  # shape: [1, hidden_size]
```

### 🔸 [CLS] 토큰 임베딩만 사용
```python
cls_embedding = outputs.last_hidden_state[:, 0, :]  # shape: [1, hidden_size]
```

### 🔸 Pooler Output 사용
```python
pooled_output = outputs.pooler_output  # shape: [1, hidden_size]
```

※ 단, 일부 모델(DistilBERT, RoBERTa 등)은 `pooler_output`이 없을 수 있습니다.

---

## ✅ 정리 요약

| 코드 | 설명 |
|------|------|
| `outputs = model(token_ids)` | 모델에 토큰화된 입력을 넣음 |
| `outputs[0]` 또는 `outputs.last_hidden_state` | 각 토큰별 임베딩 결과 |
| `outputs.pooler_output` | 전체 문장을 대표하는 벡터 (일부 모델만 지원) |
| `outputs.hidden_states` | 모든 레이어의 중간 상태 (옵션) |
| `outputs.attentions` | 모든 어텐션 가중치 행렬 (옵션) |


---

# model 출력값 중 hidden_states 와 last_hidden_state 비교

| 항목 | 의미 | 언제 쓰나 |
|------|------|-----------|
| `last_hidden_state` | **마지막 레이어**의 출력 (토큰별 벡터) | 일반적인 문장 임베딩, 분류, NER 등 |
| `hidden_states` | **모든 레이어의 출력** 리스트 | 중간 레이어 분석, 튜닝, Layer-wise Attention 등 |

---

## 🔹 1. `last_hidden_state`

```python
outputs.last_hidden_state  # 또는 outputs[0]
```

- Transformer의 **가장 마지막 인코더 레이어**의 출력값입니다.
- 형태:
  ```python
  [batch_size, seq_len, hidden_size]
  ```

- 예: `"I love pizza"` → `[1, 5, 768]`
- 이걸 활용해서 문장 임베딩을 만들거나, [CLS] 토큰을 뽑거나, 토큰 분류 등에 사용합니다.

---

## 🔹 2. `hidden_states`

```python
outputs.hidden_states
```

- Transformer의 **모든 레이어의 출력값**을 담은 **리스트**입니다.
- 보통 다음과 같이 구성돼요:
  ```
  [
    embedding_output,          # 입력 임베딩 (레이어 0)
    encoder_layer_1_output,    # 레이어 1
    encoder_layer_2_output,    # 레이어 2
    ...
    encoder_layer_N_output     # 마지막 레이어
  ]
  ```

- 길이: `num_hidden_layers + 1`  
  예: BERT-base는 레이어 12개 → 리스트 길이 13

- 각 아이템의 shape: `[batch_size, seq_len, hidden_size]`

---

## 🔍 예시로 비교

```python
from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased", output_hidden_states=True)

inputs = tokenizer("I love pizza", return_tensors="pt")
outputs = model(**inputs)

last = outputs.last_hidden_state              # [1, 5, 768]
all_layers = outputs.hidden_states            # 리스트 (길이 13), 각 [1, 5, 768]
first_layer = outputs.hidden_states[1]        # 1번째 레이어 출력
final_layer = outputs.hidden_states[-1]       # 마지막 레이어 출력 == last_hidden_state
```

✅ 즉, `last_hidden_state == hidden_states[-1]` 입니다.

---

## 📌 언제 뭘 써야 할까?

| 목적 | 추천 |
|------|------|
| 문장 임베딩 | `last_hidden_state` + 평균 / CLS |
| 토큰 분류 (NER 등) | `last_hidden_state` |
| 특정 레이어 출력 보고 싶을 때 | `hidden_states[i]` |
| 중간 레이어 분석 / 가중합 | `hidden_states` 전체 활용 |
| layer-wise attention, probing | `hidden_states` 필요 |

---

## ✅ 요약 정리

| 항목 | last_hidden_state | hidden_states |
|------|-------------------|----------------|
| 내용 | 마지막 레이어 출력 | 모든 레이어 출력 리스트 |
| 타입 | Tensor | List[Tensor] |
| shape | `[B, T, H]` | `[L+1] × [B, T, H]` |
| 활용 | 문장 벡터, 분류 등 | 중간 분석, 레이어 합성 등 |

---

## 🔹 `hidden_size`란?

> Transformer 계열 모델에서 `hidden_size`는 **모델 내부에서 사용하는 임베딩 벡터의 차원 수**, 즉 **각 단어(토큰) 또는 문장이 표현되는 벡터의 크기**입니다.

---

## 📌 예를 들어:

| 모델 이름 | hidden_size (벡터 차원 수) |
|-----------|----------------------------|
| `bert-base-uncased` | 768 |
| `bert-large-uncased` | 1024 |
| `distilbert-base-uncased` | 768 |
| `roberta-base` | 768 |
| `gpt2` | 768 |
| `gpt2-medium` | 1024 |

👉 즉, `"I love pizza"`라는 문장을 모델에 넣으면 각 토큰은 **768차원의 벡터**로 표현됩니다.  
(이 768은 BERT의 `hidden_size`)

---

## 🔸 어디에 쓰이냐?

- 각 토큰의 의미 표현 (hidden state)
- 문장 임베딩 구성 (평균, [CLS], pooler 등)
- 문서 벡터 저장 (`build_docs_embedding()`에서 사용)
- 검색, 분류, 생성 등 모든 다운스트림 작업의 기본 단위

---

## 🔍 코드에서 확인하는 방법

```python
model.config.hidden_size
```

👉 모델의 `config` 객체에 정의되어 있어요.

---

## ✅ 결론

> `hidden_size`는 모델이 표현하는 벡터의 크기이며, 단어 또는 문장의 의미를 담는 기본 단위입니다.**  
> 이 값이 클수록 더 풍부한 표현이 가능하지만, 계산량도 많아져요.

---