# Retrieval as K-nearest neighbor search
- 유사도로 찾는다.
- 유클라디안, 맨해튼 등
- 양이 많으면 느려진다 --> 전처리를 생각한다.

## psudo code
1-NN algorithm
```
init distance = 무한대
init distance 측정 문서 = null
query 문서 = 0

for i = 1~N
    d = 비교 거리(xi, query 문서)
    d < distance
    distance 측정문서 = xi
    distance = d
return distance 측정문서 = xi

```

# TF-IDF 
> TF−IDF(t)=TF(t)×IDF(t)  
자주 등장하면서도 희귀한 단어일수록 값이 높아짐
> 자주 나오는 단어는 중요하다 --> TF(단어빈도)  
하지만 일반적인 단어는 덜 중요하다 -->IDF(문서빈도 역수)
## TF(Term Frequency)
> TF(t) = t 단어의 개수/전체 단어 개수
    - 전체 단어 중에 t가 얼마나 많이 차지하는가?

## IDF(Inverser Document Frequency)
> IDF(t) = log(전체 문서 수/(단어 t가 나온 문서 수 + 1))
    - t가 나온 문서 수가 얼마나 적은가?
    - t의 희귀성을 위함

# distance metrics
## 유클라디안 거리
- 가까운 정도 -> 유사도
- 차원이 커진다 -> 비교할 특징이 많아진다 -> 특징의 가중치를 달리하여 거리를 잴 수 있다
    - weight을 0으로 두어 feature를 선별적으로 사용할 수 있다

## 코사인 유사도-정규화