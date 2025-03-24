# **학습이 끝난 파인튜닝 모델을 불러와서(prompt 기반으로)** 응답 생성

---

## 📌 전체 흐름 요약

```
1. 파인튜닝된 모델 로드
2. 토크나이저 로드
3. 응답 생성 (generate)
4. 결과 출력
```

---

## 🔹 1️⃣ 파인튜닝 모델 로드

```python
model = AutoModelForCausalLM.from_pretrained(
    path_finetuned_model,
    device_map=device_map
)
```

### ✅ 해석

- `AutoModelForCausalLM`: GPT류 **텍스트 생성 모델** 클래스
- `from_pretrained(path)`: 저장된 모델 디렉토리에서 **가중치 + 설정** 로드
- `device_map=device_map`: GPU/CPU 자동 배치 (예: `'auto'` 또는 `{'': 'cpu'}`)

---

## 🔹 2️⃣ 토크나이저 로드

```python
tokenizer = AutoTokenizer.from_pretrained(
    path_finetuned_model,
    device_map=device_map
)
```

### ✅ 해석

- 모델 학습 시 사용된 **동일한 토크나이저 설정**을 불러옴
- `path_finetuned_model` 안에 있는 `tokenizer_config.json`, `vocab.json`, `merges.txt` 등을 읽어옴
- `device_map`은 일반적으로 `tokenizer`에는 필요하지 않지만, 무시되더라도 에러는 나지 않음

---

## 🔹 3️⃣ 응답 생성

```python
response = generate_response(prompt, model, tokenizer)
```

### ✅ 해석

- `generate_response()`는 아마도 커스텀 함수로,
- `prompt`를 넣어서 **모델이 생성한 텍스트를 반환**하는 역할을 합니다.
- 내부에서는 대체로 아래와 같은 작업이 이뤄질 거예요:

```python
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
```

---

## 🔹 4️⃣ 출력

```python
print("response(after training):", response)
```

✅ 학습된 모델이 생성한 응답을 출력합니다.

---

## ✅ 전체 정리

| 단계 | 설명 |
|------|------|
| 🔹 모델 로드 | `AutoModelForCausalLM.from_pretrained(...)` |
| 🔹 토크나이저 로드 | `AutoTokenizer.from_pretrained(...)` |
| 🔹 응답 생성 | `generate_response(prompt, model, tokenizer)` |
| 🔹 결과 출력 | 파인튜닝된 모델의 응답 확인 |

---

## 💡 추가 팁

- `generate_response()` 함수 내부를 한번 확인해보면,  
  `max_new_tokens`, `temperature`, `do_sample` 같은 **생성 옵션**도 조절할 수 있어요.
  
- 예를 들어, 아래처럼 설정할 수 있습니다:

```python
model.generate(
    input_ids,
    max_new_tokens=100,
    temperature=0.8,
    do_sample=True,
    top_k=50
)
```