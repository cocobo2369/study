# Hugging Face, DataCollatorForLanguageModeling을 활용하여 언어 모델 학습용 배치 데이터를 만드는 과정

## 🔹 전체 코드

```python
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False, return_tensors='pt')
print(dataset['train'][:1])
print(data_collator(dataset['train'][:1]['input_ids']))
```

---

## 🔹 1️⃣ `DataCollatorForLanguageModeling(...)`

```python
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
    return_tensors='pt'
)
```

✅ **의미:**  
`DataCollatorForLanguageModeling`은 언어 모델 학습을 위한 배치를 만드는 도구입니다.

### 📌 주요 인자:
- `tokenizer`: 입력 토큰 ID를 디코딩하거나 padding할 때 사용
- `mlm=False`: 마스크드 언어 모델(MLM)이 아닌 **AutoRegressive 모델 (예: GPT류)** 용
- `return_tensors='pt'`: 반환 타입을 PyTorch 텐서로 설정 (`torch.Tensor`)

---

## 🔹 2️⃣ `dataset['train'][:1]`

✅ **의미:**  
train 데이터셋의 **첫 번째 샘플 1개**를 가져옵니다. 반환은 `dict[str, list]` 형식입니다.

예시 출력:
```python
{
  'input_ids': [[101, 2057, 2024, ...]],
  'attention_mask': [[1, 1, 1, ...]]
}
```

---

## 🔹 3️⃣ `data_collator(dataset['train'][:1]['input_ids'])`

✅ **의미:**  
`DataCollatorForLanguageModeling`은 보통 `list[dict]` 또는 `list[input]`을 받습니다.  
하지만 여기서 `['input_ids']`만 넣었기 때문에 **토크나이저 정보 없이** raw token id만 넘긴 셈입니다.

이건 **문제가 발생할 수 있습니다!**  
왜냐하면 `data_collator`는 **전체 샘플(dict)**을 기대하기 때문입니다.

### 🧨 이렇게 하면 오류가 날 가능성 높음:
```python
print(data_collator(dataset['train'][:1]['input_ids']))
```

---

## ✅ 올바른 사용 방법:

```python
# 올바르게 전체 샘플(dict)을 넘기기
sample = dataset['train'][:1]
print(data_collator(sample))
```

이렇게 하면 `input_ids`, `attention_mask`, (필요시 `labels`)까지 모두 처리됩니다.

---

## 🔹 출력 예시 (AutoRegressive 모델 - GPT류)

`data_collator(sample)` 결과:

```python
{
  'input_ids': tensor([[101, 2057, 2024,  ...]]),
  'attention_mask': tensor([[1, 1, 1, ...]]),
  'labels': tensor([[101, 2057, 2024,  ...]])  # labels == input_ids (mlm=False일 경우)
}
```

---

## ✅ 요약 정리

| 코드 | 설명 |
|------|------|
| `DataCollatorForLanguageModeling(...)` | 학습에 필요한 배치를 만드는 도우미 (GPT류 or BERT류 모두 지원) |
| `mlm=False` | AutoRegressive 학습을 위한 설정 (예: GPT) |
| `dataset['train'][:1]` | 첫 번째 샘플 가져오기 |
| `data_collator(...)` | 샘플을 배치 형태로 가공. `labels`까지 추가됨 |
| ❗ 주의사항 | `['input_ids']`만 넘기면 오류 발생 가능. **샘플 전체(dict)**를 넘겨야 함 |

---
# 출력예시
```
DataCollatorForLanguageModeling(tokenizer=PreTrainedTokenizerFast(name_or_path='./models/finetuned_model/', vocab_size=1500, model_max_length=1000000000000000019884624838656, is_fast=True, padding_side='right', truncation_side='right', special_tokens={'bos_token': '<|endoftext|>', 'eos_token': '<|endoftext|>', 'pad_token': '<|pad|>'}, clean_up_tokenization_spaces=True, added_tokens_decoder={
	0: AddedToken("<|endoftext|>", rstrip=False, lstrip=False, single_word=False, normalized=False, special=True),
	1: AddedToken("<|pad|>", rstrip=False, lstrip=False, single_word=False, normalized=False, special=True),
	2: AddedToken("<|USER|>", rstrip=False, lstrip=False, single_word=False, normalized=False, special=True),
	3: AddedToken("<|ASSISTANT|>", rstrip=False, lstrip=False, single_word=False, normalized=False, special=True),
}
), mlm=False, mlm_probability=0.15, mask_replace_prob=0.8, random_replace_prob=0.1, pad_to_multiple_of=None, tf_experimental_compile=False, return_tensors='pt')
result: {'input_ids': tensor([[   2,   38,   80,   79,   85,   70,   89,   85,  147,   74,   79,   71,
           80,   83,   78,   66,   85,   74,   80,   79,  147,   74,   84,  147,
           67,   70,   77,   80,   88,   17,  146,
...
           70,   83,   90,   17,  146,   52,   86,   70,   83,   90,   29,  297,
          122,  629,  111,  230,   99, 1403,  490,  212,  149, 1274,  161,  492,
         1080,  308,  219,  541, 1276,  173,  375,  406,  774,  531, 1080,  597,
          376,  602,  274,  500,  629, 1126,   17,  146,   36,   79,   84,   88,
           70,   83,   29,  147,    3,  489,  122,  629,  111,  230,   99, 1403,
          490,  212,  149,  376,  425,  501,  219,  808,  217,  182,  871,  629,
         1126,   17,    0,    1,    1,    1,    1,    1,    1,    1,    1,    1,
            1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,
            1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,
            1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,
            1,    1,    1,    1,    1,    1,    1,    1]]), 
            'labels': tensor([[   2,   38,   80,   79,   85,   70,   89,   85,  147,   74,   79,   71,
           80,   83,   78,   66,   85,   74,   80,   79,  147,   74,   84,  147,
           67,   70,   77,   80,   88,   17,  146,   16,   16,   16,   16,   16,
...
          376,  602,  274,  500,  629, 1126,   17,  146,   36,   79,   84,   88,
           70,   83,   29,  147,    3,  489,  122,  629,  111,  230,   99, 1403,
          490,  212,  149,  376,  425,  501,  219,  808,  217,  182,  871,  629,
         1126,   17,    0, -100, -100, -100, -100, -100, -100, -100, -100, -100,
         -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100,
         -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100,
         -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100,
         -100, -100, -100, -100, -100, -100, -100, -100]])}
```

## 🔹 코드 핵심 요약

```python
DataCollatorForLanguageModeling(
    tokenizer=PreTrainedTokenizerFast(...),
    mlm=False,
    return_tensors='pt'
)
```

### ✅ `mlm=False`:  
**GPT류 언어모델**처럼 **다음 토큰을 예측하는 방식 (AutoRegressive Language Modeling)** 을 사용한다는 의미입니다.

---

## 🔹 출력 결과 해석

출력은 다음과 같은 두 개의 key로 구성된 dictionary입니다:

```python
{
  "input_ids": Tensor([...]),
  "labels": Tensor([...])
}
```

---

### 🔸 1️⃣ `input_ids`

```python
'input_ids': tensor([[ 2, 38, 80, 79, 85, ...]])
```

✅ **의미:**  
- 실제 모델의 **입력 텍스트를 숫자로 변환한 것**
- 이 숫자는 `tokenizer`가 정의한 **vocabulary 사전의 ID**에 해당합니다.
- 예: `<|USER|> How are you today?` → `[2, 38, 80, ...]`

---

### 🔸 2️⃣ `labels`

```python
'labels': tensor([[ 2, 38, 80, 79, 85, ..., -100, -100, -100, ...]])
```

✅ **의미:**  
- 모델이 학습 중에 예측해야 하는 **정답 토큰 시퀀스**
- `input_ids`와 **초반에는 동일**하지만,
- **패딩 부분은 `-100`** 으로 처리되어 **loss 계산에서 무시됨**  
  (PyTorch에서 `CrossEntropyLoss(ignore_index=-100)`로 처리됨)

---

## 🔸 `-100`이 등장하는 이유?

`DataCollatorForLanguageModeling`은 `padding=True`로 인해 문장 길이를 맞추면서,  
패딩된 부분은 학습 시 **loss에 반영되지 않도록 `-100`으로 마킹**합니다.

예:

| input_ids | labels (loss에 사용됨) |
|-----------|------------------------|
| 85        | 85                     |
| 74        | 74                     |
| 1 (PAD)   | -100 (무시됨)          |

---

## 🔸 tokenizer 정보 (요약)

```python
PreTrainedTokenizerFast(
    name_or_path='./models/finetuned_model/',
    vocab_size=1500,
    special_tokens={
        'bos_token': '<|endoftext|>',
        'eos_token': '<|endoftext|>',
        'pad_token': '<|pad|>',
        ...
    }
)
```

✅ **사용된 토크나이저 정보**:

- **사용자 정의 특수 토큰** 포함: `<|USER|>`, `<|ASSISTANT|>` 등
- 이 토크나이저는 사용자 정의된 작은 vocab (1500개)로 사전 학습된 모델에 맞춤 설정된 것으로 보임
- `input_ids`의 시작 값 `2`는 `<|USER|>`일 가능성이 큽니다.

---

## ✅ 요약 정리

| 항목 | 내용 |
|------|------|
| `input_ids` | 텍스트가 토큰 ID로 변환된 결과 |
| `labels` | 학습 중 예측 대상인 정답 시퀀스 (패딩은 -100으로 마스킹됨) |
| `mlm=False` | GPT류 모델처럼 다음 토큰 예측 방식 사용 |
| `-100` | loss 계산에서 무시될 토큰 (패딩된 부분) |
| 특수 토큰 | `<|USER|>`, `<|ASSISTANT|>`, `<|pad|>` 등 직접 정의된 토큰 사용 중 |
---

## labels 와 input_ids

> **`labels`는 `input_ids`를 "정답으로 복사"한 것**입니다.  
> 그래서 **두 값이 처음엔 같아 보이지만**,  
> 학습 시 loss 계산에 쓰일 수 있도록 `padding` 부분이 `-100`으로 마스킹된 형태입니다.

---

## 🔸 왜 같게 복사하냐?

- 지금 설정이 `mlm=False`이기 때문에,  
  **GPT류처럼 다음 토큰을 예측하는 AutoRegressive Language Modeling** 방식을 사용합니다.

- 이 방식에선 모델에게:
  > "이 토큰들(input_ids)을 보고 다음 토큰(labels)을 예측해봐!"  
  라는 식으로 학습시키는 구조입니다.

---

## 🔸 실제 예시

```python
input_ids: [ 66, 79, 69, 147, 79, 80, 85, 147, 81, 83, ... , 1, 1, 1]
labels:    [ 66, 79, 69, 147, 79, 80, 85, 147, 81, 83, ... ,-100, -100, -100]
```

- 처음엔 둘 다 같음 ✅  
- 하지만 `padding`된 부분(`input_ids`의 `1`)은 `labels`에서 `-100`으로 바뀜 ❗

즉:

| 항목 | 의미 |
|------|------|
| `input_ids` | 모델 입력값 (토큰 ID들) |
| `labels` | 정답값. `input_ids`를 복사하되 **패딩은 `-100`으로 마스킹** |
| `-100` | `loss 계산에서 무시하라`는 뜻 (CrossEntropyLoss에서 `ignore_index=-100`) |

---

## 🔧 이게 왜 중요할까?

```python
loss_fn = nn.CrossEntropyLoss(ignore_index=-100)
```

- 이렇게 되어 있기 때문에,  
  **패딩된 위치는 학습 대상이 아니게 되고**,  
  모델은 **실제 텍스트 부분만 보고 학습**합니다.

---

## ✅ 결론

| 질문 | 답변 |
|------|------|
| `labels`는 `input_ids`의 train 결과인가요? | ❌ 훈련 결과는 아님 |
| 그럼 뭐예요? | ✅ `input_ids`를 복사한 값이며, `loss` 계산을 위해 패딩은 `-100`으로 마스킹됨 |
| 왜 이렇게 하나요? | ✅ AutoRegressive 방식 학습(GPT류)을 위해, 입력 그대로를 정답으로 삼음 |


---

# 🧠 전체 흐름도: GPT류 언어 모델 학습 데이터 흐름 (mlm=False)

```
┌────────────────────────┐
│ 1. 원본 텍스트 데이터    │   예: "오늘 날씨 어때?"
└────────────┬───────────┘
             ↓
┌────────────────────────┐
│ 2. Tokenizer 적용       │
│  → input_ids 생성       │
│  예: [66, 79, 84, 88, …]│
└────────────┬───────────┘
             ↓
┌───────────────────────────────────────┐
│ 3. DataCollatorForLanguageModeling   │
│  ▶ input_ids → padding 적용          │
│  ▶ labels = input_ids.copy()         │
│  ▶ labels에서 padding 부분은 -100    │
│                                       │
│  📌 출력:                             │
│  input_ids: [66, 79, 84, 88, 1, 1, 1] │
│  labels:     [66, 79, 84, 88, -100…]  │
└────────────┬──────────────────────────┘
             ↓
┌────────────────────────┐
│ 4. 모델 Forward         │
│  → logits 출력          │
│  shape: [batch, seq_len, vocab] │
└────────────┬───────────┘
             ↓
┌──────────────────────────────┐
│ 5. Loss 계산 (CrossEntropy)  │
│  ▶ labels의 -100은 무시됨     │
│  ▶ 나머지 토큰은 다음 토큰을 예측 │
└──────────────────────────────┘
```

---

## 🔎 예시를 간단히 풀어보면:

| 원본 텍스트        | 오늘 날씨 어때? |
|-------------------|-----------------|
| `input_ids`       | `[66, 79, 84, 88, 70, 83, 17, 1, 1, 1]` |
| `labels`          | `[66, 79, 84, 88, 70, 83, 17, -100, -100, -100]` |

→ 모델은 `66`을 보고 `79`를 예측하고,  
→ `79`를 보고 `84`를 예측하고, …  
→ `1`은 padding이라 무시됩니다 (`-100`).

---

## ✅ 흐름 핵심 요약

| 단계 | 설명 |
|------|------|
| Tokenizer | 텍스트를 숫자로 바꿈 (`input_ids`) |
| Collator  | 학습 가능한 배치 구성 (`input_ids` + `labels`) |
| Model     | 토큰 시퀀스를 보고 다음 토큰 예측 |
| Loss      | `labels` 기준으로 정답 비교. `-100`은 무시 |

---

💯 네! **완벽하게 정확한 이해**예요.  
`DataCollatorForLanguageModeling`의 주요 목적은 바로 그거예요:

---

## ✅ 핵심 요약

> `DataCollatorForLanguageModeling`은  
> 👉 **`input_ids`를 그대로 `labels`로 복사한 뒤**,  
> 👉 **패딩 위치는 `-100`으로 바꿔서**  
> 👉 **loss 계산 시 무시되게 만들기 위해** 사용됩니다.

---

## 🔎 왜 `-100`으로 바꾸는가?

PyTorch의 `CrossEntropyLoss`는 기본적으로 다음처럼 설정돼 있어요:

```python
nn.CrossEntropyLoss(ignore_index=-100)
```

즉, `labels` 값 중 `-100`은 **loss 계산 대상에서 제외**됩니다.

그래서:

```python
input_ids: [ 66, 79, 84, 88, 1, 1 ]
labels:     [ 66, 79, 84, 88, -100, -100 ]
```

위처럼 되면, 모델은 **앞쪽 4개 토큰까지만** 학습하고  
나머지 패딩은 무시하게 됩니다.

---

## 🔸 왜 굳이 `labels`를 따로 만들어서 넘겨줄까?

GPT류 모델은 "다음 토큰을 예측"해야 하므로, `input_ids`와 `labels`가 거의 동일하지만,
**loss 계산 시 무시할 위치만 달라야 하기 때문**입니다.

---

## 📌 보충 설명: `mlm=False`일 때

- `mlm=False`: AutoRegressive (GPT류)
- `labels = input_ids.copy()` 후, `padding → -100`

---

## 📌 보충 설명: `mlm=True`일 때

- `mlm=True`: Masked Language Modeling (BERT류)
- `labels`는 랜덤으로 일부 토큰만 복사되고, 나머지는 -100  
  (즉, **일부 토큰만 예측하고, 나머지는 무시**)

---

## ✅ 결론

| 역할 | 설명 |
|------|------|
| `input_ids` | 모델 입력값 |
| `labels` | 정답. 대부분 `input_ids`와 동일하지만, **패딩은 -100** |
| `-100` | loss에서 무시되도록 설정 |
| 목적 | "패딩은 학습에 쓰이지 않도록" 보장하는 자동 처리 장치 |

---