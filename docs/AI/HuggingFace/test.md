# Contents
## 1. get_embedding
## 2. build_docs_embedding
## 3. retrieve_doc에서 유사도 값 변경

# 1. training_data.jsonl
{  
    "text":  
    "<|USER|>  
    Context information is below.  \n---------------------
    \n갤럭시 링  
    \n두께 2.6mm  
    \n재질 Titanium  
    \n무게 2.3g  
    \n---------------------  
    \nGiven the context information and not prior knowledge, answer the query.  
    \nQuery: 삼성 갤럭시 링 홍보문구를 스펙 고려해서 한문장으로 만들어 주세요.  
    \nAnswer:   
    <|ASSISTANT|>  
    삼성 갤럭시 링으로 미래를 손에 쥐세요.  
    <|endoftext|>"  
}

# 2.질문 3개
> 1. embedding 구현에서 pooler_output
> 2. 
## 1. embedding 관련한 구현
> 1. text   
>    I love pizza
> 2. tokenization   
>    1) 101   - [CLS] : 문장의 결과 값, CLS는 고정된 값을 지님
>    2) 1045  - i  
>    3) 2293  - love  
>    4) 10733 - pizza  
>    5) 102   - [SEP] : 문장의 끝을 의미하는 값, SEP는 고정 값을 지님
> 3. embedding : tokenized text
>    1) 101   - [CLS] - [v0,v1 ... ,vN]
>    2) 1045  - i     - [v0,v1 ... ,vN]
>    3) 2293  - love  - [v0,v1 ... ,vN]
>    4) 10733 - pizza - [v0,v1 ... ,vN]
>    5) 102   - [SEP] - [v0,v1 ... ,vN]
> 4. embedding : sentence 
>    - 101   - [CLS] - [v0,v1 ... ,vN] 자체
>    - 2), 3), 4) 를 연산(ex 평균)

### 1. text

### 2. tokenization
```python
{ 
    input_ids,
    attention_mask,
    token_type_ids
}
=
self.tokenizer(text, return_tensors='pt', padding=True)
# text가 batch(여러문장)이면 padding=True 시 문장최대길이에 맞추기 위해 padding을 넣어주게 됨 
tokenized_text : 
{'input_ids': tensor([[     0,      6, 193074,  48905,  11747,    363,  54099, 137647,    190,
         195049,   1022,    201, 210257,   1022,  11585,    617,   2866, 234252,
           8934, 134448, 208422,  22436,   1381,    841,      6,      2]]),
 'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         1, 1]])
}
```

## 2. embedding : tokenized text
### 리턴 값
| 이름 | 형태 | 설명 |
|------|------|------|
| `last_hidden_state` | `[batch_size, seq_len, hidden_size]` | 각 토큰의 임베딩 벡터 (예: BERT는 768차원),hidden_states의 마지막 list 원소 |
| `pooler_output` | `[batch_size, hidden_size]` | `[CLS]` 토큰만 뽑아 처리한 전체 문장 대표 벡터 (일부 모델에만 존재) |
| `hidden_states` | list of tensors | 각 레이어별 hidden state들 (옵션, `output_hidden_states=True` 시) |
| `attentions` | list of tensors | 각 레이어별 어텐션 행렬들 (옵션, `output_attentions=True` 시) |

```
model_output=self.model(**tokenized_text)
# 와 동일:
self.model(input_ids=tokenized_text["input_ids"], attention_mask=tokenized_text["attention_mask"])
```

## 3. embedding : sentence 
```
embedding=model_output.pooler_output

documents_embeddings: tensor([[-0.5421, -0.8164,  0.8235,  ...,  0.3320,  0.7494,  0.0085],
        [ 0.0000,  0.0000,  0.0000,  ...,  0.0000,  0.0000,  0.0000],
        [ 0.0000,  0.0000,  0.0000,  ...,  0.0000,  0.0000,  0.0000],
        [ 0.0000,  0.0000,  0.0000,  ...,  0.0000,  0.0000,  0.0000],
        [ 0.0000,  0.0000,  0.0000,  ...,  0.0000,  0.0000,  0.0000]],
       grad_fn=<CopySlices>)
```
# 질문
```python
    def build_docs_embedding(self):
        ### Q A-2) 작성 필요
        #1. 도큐먼트 개수
        #2. 도큐먼트 내 문장 개수
        #3. 임베딩

        #쿼리가 제품명에 한해서 뽑으라 할 수도 있다.
        #documents_embeddings = self.get_embedding([doc.split('\n')[0] for doc in self.documents])

        documents_embeddings = torch.zeros([len(self.documents), self.model.config.hidden_size])
        for i, doc in enumerate(self.documents):
          documents_embeddings[i] = self.get_embedding(doc)
          print("documents_embeddings:", documents_embeddings)
        return documents_embeddings
```