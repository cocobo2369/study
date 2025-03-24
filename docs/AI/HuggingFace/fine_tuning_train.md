# Hugging Face의 `Trainer`를 사용해서 GPT류 언어모델을 학습(fine-tuning)

## 📌 전체 흐름 요약

```
1. DataCollator 구성
2. 훈련 설정 정의 (TrainingArguments)
3. Trainer 객체 생성
4. 학습 시작
5. 모델 저장
```

---

## 🔹 1️⃣ `DataCollatorForLanguageModeling`

```python
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
    return_tensors='pt'
)
print(data_collator)
print('result:', data_collator(dataset['train']['input_ids'][:1]))
```

### ✅ 해석

- `tokenizer`를 이용해서 학습용 배치를 만들어주는 도우미
- `mlm=False`: GPT류 **AutoRegressive** 학습 방식 (다음 토큰 예측)
- `return_tensors='pt'`: PyTorch 텐서로 반환
- `input_ids`만 넘기면 안 되고, `dict` 형태로 넘겨야 함 → 이 부분은 실수 가능성 있음 ⚠️

### 🔎 이 코드는 아래처럼 수정하는 것이 정확합니다:

```python
sample = dataset['train'][:1]  # {'input_ids': ..., 'attention_mask': ...}
print('result:', data_collator(sample))
```

---

## 🔹 2️⃣ `TrainingArguments`

```python
training_args = TrainingArguments(
    output_dir='tmp',
    do_train=True,
    do_eval=False,
    learning_rate=7e-4,
    per_device_train_batch_size=4,
    num_train_epochs=100,
    use_cpu=True,
    report_to='none'
)
```

### ✅ 해석

- `output_dir='tmp'`: 결과, 로그, 모델 등을 저장할 디렉토리
- `do_train=True`: 학습을 수행함
- `do_eval=False`: 평가(validation)는 수행하지 않음
- `learning_rate=7e-4`: 학습률 (GPT류 모델에선 일반적으로 조금 높을 수 있음 → 학습이 불안정할 수 있음)
- `per_device_train_batch_size=4`: 배치 사이즈
- `num_train_epochs=100`: 전체 학습 에폭 수
- `use_cpu=True`: GPU 대신 CPU로 학습 (⚠️ 느림)
- `report_to='none'`: 로그를 외부 툴(wandb, tensorboard 등)에 기록하지 않음

---

## 🔹 3️⃣ Trainer 생성 및 학습 실행

```python
trainer = Trainer(
    model,
    train_dataset=dataset['train'],
    args=training_args,
    data_collator=data_collator
)

trainer.train()
```

### ✅ 해석

- `Trainer` 객체를 만들고,
- `train_dataset`을 사용하여 학습 시작!
- `data_collator`를 통해 각 배치가 자동으로 구성됨

---

## 🔹 4️⃣ 모델 저장

```python
trainer.save_model(path_finetuned_model)
```

✅ 학습이 끝난 모델을 `path_finetuned_model` 경로에 저장합니다.

---

## ✅ 전체 정리 요약

| 단계 | 설명 |
|------|------|
| `data_collator` | `input_ids` → `labels` 자동 생성 (패딩은 `-100` 처리) |
| `TrainingArguments` | 학습 세팅 정의 (학습률, 에폭 수, 디바이스 등) |
| `Trainer` | 모델 학습 담당 객체 |
| `train()` | 학습 수행 |
| `save_model()` | 파인튜닝된 모델 저장 |

---

## ⚠️ 주의할 점

- `data_collator(dataset['train']['input_ids'][:1])`는 **실행 시 오류 가능성** 높음  
  → `input_ids`만 넘기면 안 되고, 전체 샘플(dict)을 넘겨야 함.

올바른 형태:
```python
sample = dataset['train'][:1]
print(data_collator(sample))
```

네! 정확히 말해서,  
> ✅ **"훈련된 모델을 저장한다" = "가중치(Weights)를 저장한다"**  
는 것이 맞습니다.  
하지만 **가중치만 저장하는 건 아니고**, 다음과 같은 **모델 구성 요소 전체**가 저장됩니다:

---

## 📦 `Trainer.save_model()` 또는 `model.save_pretrained()` 시 저장되는 항목

| 항목 | 설명 |
|------|------|
| `pytorch_model.bin` | ✅ **모델의 학습된 가중치 (Weights)** |
| `config.json`       | 모델 구조 (예: hidden size, num_layers 등) |
| `tokenizer_config.json`, `vocab.json`, `merges.txt` | 토크나이저 관련 파일들 (BPE 방식인 경우) |
| `special_tokens_map.json` | BOS, EOS, PAD 토큰 정보 등 |
| `training_args.bin` (옵션) | `Trainer`로 학습했다면 학습 설정 정보 |

---

# 훈련된 모델을 저장한다는 것은.

## 🔎 가중치란?

모델 학습에서 "가중치"는 곧 **뉴럴 네트워크가 학습한 모든 값(행렬)**을 의미합니다.

예:

- Linear Layer: `y = Wx + b`  
  → 여기서 학습된 `W`, `b`가 "가중치"입니다.
- Transformer에서는:
  - Self-Attention 쿼리/키/값 행렬
  - FFN 내부의 Weight
  - LayerNorm, Bias 등 모두 포함

---

## ✅ 모델을 저장하면 무엇을 재사용할 수 있나?

저장된 모델은 `from_pretrained()`으로 다시 로드 가능하며,  
> 👉 **다시 학습하거나**  
> 👉 **추론에 사용하거나**  
> 👉 **다른 프롬프트에 적용하거나**  
모두 가능합니다.

---

## 🔄 요약

| 질문 | 답변 |
|------|------|
| 훈련된 모델 저장 = 가중치 저장인가요? | ✅ 네, 가중치 저장이 핵심입니다. |
| 그것만 저장되나요? | ❌ 아니요, 구조(config), 토크나이저 등도 함께 저장됩니다. |
| 저장된 모델로 뭘 할 수 있나요? | ✅ 다시 불러와서 추론/재학습/응답 생성 가능 |

---

필요하시면 `save_model()` 이후 어떻게 `from_pretrained()`으로 연결되는지도 함께 보여드릴게요!  
아니면 모델만 저장하고 토크나이저는 따로 저장하는 방법도 알려드릴 수 있어요 😄