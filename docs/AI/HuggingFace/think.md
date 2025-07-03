# 유사도가 가장 높은 문서 찾기
1. 쿼리 임베딩
2. 유사도

query_embedding = self.get_embedding(query)
top_1_idx = torch.argmax()

#임베딩하기

모델안에는 토크나이저가 딸려있다.
당연하지 이 토크나이저로 문서를 임베딩하니까

1. 학습
   내용 임베딩 및 학습
2. 질문
   질문 임베딩 후, 모델에 넣어 유사도 측정
3. 도출

i love pizza

i [0.1, ..., 0.222]
love [0.2, ..., 0.522]
pizza [0.11, ..., -0.52]

i 123번 단어
love 1939번 단어
pizza 9293번 단어