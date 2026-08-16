"""Reorder chapters 1-8 to the textbook's actual section sequence."""

from collections import OrderedDict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "교재정리"


CONFIG = {
    1: [
        ("1. 개요", ["1. 통계분석의 정의와 목적", "2. 기술통계와 추론통계"], "기술통계는 현재 데이터를 요약하고, 추론통계는 표본으로 모집단을 판단한다."),
        ("2. 모집단과 표본", ["3. 모집단·표본·모수·통계량"], "모집단의 숫자는 모수, 표본의 숫자는 통계량이다."),
        ("3. 관련 기호", ["4. 통계 기호"], "모평균 μ-표본평균 x̄, 모표준편차 σ-표본표준편차 s를 짝으로 외운다."),
        ("4. 데이터의 이해", ["5. 데이터·데이터 포인트·데이터셋", "6. 변수", "7. 수치형과 범주형 데이터"], "행은 관측 한 건, 열은 변수 하나다. 숫자 모양이라고 반드시 수치형은 아니다."),
        ("5. 측정 척도", ["8. 측정 척도"], "명-순-등-비: 구분, 순서, 간격, 절대 0의 순서로 정보가 하나씩 늘어난다."),
    ],
    2: [
        ("1. 통계량 개요", ["통계량의 개요와 종류"], "통계량은 표본의 함수이며 표본이 바뀌면 값도 바뀐다."),
        ("2. 기술통계량", [], "기술통계량은 위치·변이·모양의 세 축으로 분포를 요약한다."),
        ("3. 위치 통계량", ["중심경향", "분위수", "계산 예시"], "평균은 전체 값, 중앙값은 가운데 위치, 최빈값은 가장 잦은 값이다."),
        ("4. 변이 통계량", ["산포"], "범위는 양 끝, IQR은 가운데 50%, 표준편차는 평균 주변의 퍼짐이다."),
        ("5. 모양 통계량", ["분포의 모양"], "왜도는 좌우 치우침, 첨도는 꼬리와 극단값의 정도다."),
        ("6. 통계량의 선형 연산", ["선형변환의 영향", "두 변수의 결합 요약"], "더하기는 평균만 이동하고, 곱하기 a는 분산을 a²배 한다."),
    ],
    3: [
        ("1. 개요", ["원시자료를 정리하는 이유"], "표는 정확한 값, 그래프는 전체 패턴을 빠르게 보여 준다."),
        ("2. 도수분포표", ["빈도표와 교차표"], "도수는 개수, 상대도수는 비율, 누적도수는 이전 구간까지의 합이다."),
        ("3. 분할표", [], "셀도수-주변도수-총도수를 구분하고 비교 기준이 행인지 열인지 확인한다."),
        ("4. 데이터 시각화", ["데이터 시각화의 목적과 분류"], "변수 개수와 자료형을 먼저 보고 그래프를 고른다."),
        ("5. 일변량 그래프", ["그래프 선택", "사분위수와 상자그림"], "범주는 막대·원, 수치 분포는 히스토그램·상자그림이다."),
        ("6. 이변량 그래프", ["다변량 표현"], "수치-수치는 산점도, 시간 흐름은 선, 범주 조합은 복합·누적 막대다."),
    ],
    4: [
        ("1. 개요", ["확률의 세 가지 해석"], "고전은 경우의 수, 빈도는 반복 비율, 주관은 정보에 따른 믿음이다."),
        ("2. 기본 개념", ["기본 용어"], "시행의 개별 결과가 outcome, 결과들을 묶은 집합이 event다."),
        ("3. 표본공간과 사건", ["표본공간의 종류"], "표본공간은 가능한 결과 전체, 사건은 그 부분집합이다."),
        ("4. 확률의 공리와 성질", ["확률 공리"], "0≤P(A)≤1, P(S)=1, 서로소 사건 확률은 더한다."),
    ],
    5: [
        ("1. 독립성", ["독립성과 조건부확률"], "독립이면 조건을 알아도 확률이 변하지 않고 교집합은 곱이다."),
        ("2. 조건부확률", [], "조건 B가 새 표본공간이 되므로 P(A∩B)를 P(B)로 나눈다."),
        ("3. 확률의 기본 계산 법칙", ["곱셈법칙과 전확률법칙", "포함배제 원리"], "합집합은 더하고 중복 교집합을 빼며, 연속 단계는 조건부확률을 곱한다."),
        ("4. 전확률의 법칙", ["확률나무로 계산하기"], "같은 결과로 모이는 모든 경로의 확률을 더한다."),
        ("5. 베이즈 정리", ["베이즈 정리"], "사후확률은 우도×사전확률을 전체 증거확률로 나눈 값이다."),
    ],
    6: [
        ("1. 확률변수", ["확률질량함수"], "확률변수는 결과를 숫자에 대응시키는 함수다."),
        ("2. 확률함수", [], "PMF는 한 점의 확률, PDF는 밀도, CDF는 이하 누적확률이다."),
        ("3. 베르누이 분포", ["주요 분포"], "한 번의 성공/실패가 베르누이, 성공확률은 p다."),
        ("4. 이항분포", [], "같은 p의 독립 베르누이 시행 n번에서 성공 횟수를 센다."),
        ("5. 포아송분포", ["분포 선택", "분포 사이의 근사"], "일정 구간의 희귀사건 횟수이며 평균과 분산이 모두 λ다."),
    ],
    7: [
        ("1. 확률함수 복습", ["확률밀도함수와 누적분포함수"], "연속분포의 확률은 PDF 높이가 아니라 구간 아래 면적이다."),
        ("2. 균등분포", ["균일분포"], "구간 안의 밀도가 일정하고 평균은 양 끝의 중간이다."),
        ("3. 정규분포", ["정규분포"], "μ가 중심, σ가 폭을 정하며 표준화하면 N(0,1)이다."),
        ("4. t분포", ["t-분포"], "모표준편차를 모를 때 쓰며 자유도가 커지면 정규분포에 가까워진다."),
        ("5. 지수분포", ["지수분포"], "포아송 사건 사이 대기시간이며 무기억성을 가진다."),
        ("6. 감마분포", ["감마분포"], "여러 포아송 사건이 생길 때까지의 대기시간으로 지수분포를 확장한다."),
        ("7. 카이제곱분포", ["카이제곱분포", "F-분포"], "카이제곱은 분산, F는 두 분산의 비에 연결된다."),
    ],
    8: [
        ("1. 추론통계 개요", [], "표본의 불확실성을 수치화해 모집단의 모수에 대해 판단한다."),
        ("2. 추정", [], "하나의 값이면 점추정, 범위와 신뢰수준을 제시하면 구간추정이다."),
        ("3. 중심극한정리", ["표본분포와 중심극한정리"], "표본이 충분히 크면 표본평균의 분포가 정규분포에 가까워진다."),
        ("4. 표본분포", ["평균·비율·분산의 표본분포"], "표본분포는 원자료가 아니라 통계량을 반복 계산한 분포다."),
        ("5. 점추정", ["점추정과 구간추정"], "좋은 추정량은 불편성·일치성·효율성을 살핀다."),
        ("6. 구간추정", [], "추정치 ± 임계값×표준오차 구조를 먼저 외운다."),
    ],
}


SUPPLEMENT = {
    1: ["10. 보강 내용", "11. 핵심 점검"],
    2: ["표준화 점수", "보강: 통계량 선택 가이드", "체크포인트"],
    3: ["보강: 좋은 시각화의 원칙", "경험적 누적분포함수", "왜곡을 만드는 표현", "체크포인트"],
    4: ["조건부확률과 독립", "베르누이 시행", "보강: 확률과 우도", "확률변수와 기대값", "독립과 조건부 독립", "체크포인트"],
    5: ["경우의 수", "보강: 진단검사 해석", "체크포인트"],
    6: ["보강: 포아송 가정", "체크포인트"],
    7: ["보강: 밀도와 확률의 차이", "분포 관계 한눈에 보기", "체크포인트"],
    8: ["가설검정", "대표 검정 선택", "다중검정", "효과크기", "보강: 자주 하는 오해", "체크포인트"],
}


def parse(path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = lines[0]
    source = next(line for line in lines if line.startswith("> 원본 PDF 범위:"))
    body_start = next((i + 1 for i, line in enumerate(lines) if line == "<!-- TOC END -->"), 1)
    sections = OrderedDict()
    current = None
    for line in lines[body_start:]:
        if line.startswith("## "):
            current = line[3:]
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    return title, source, sections


def append_section(out, label, content, show_subheading):
    if show_subheading:
        out.extend(["### " + label, ""])
    while content and not content[0].strip():
        content = content[1:]
    while content and not content[-1].strip():
        content = content[:-1]
    out.extend(content)
    out.append("")


def main():
    for chapter, groups in CONFIG.items():
        path = next(NOTES.glob("{:02d}_*.md".format(chapter)))
        title, source, sections = parse(path)
        out = [title, "", source + " · 원문 순서 재편집", "", "<!-- TOC START -->", "<!-- TOC END -->", ""]
        used = set()
        for group_title, labels, memory in groups:
            out.extend(["## " + group_title, "", "> **암기 한 줄:** " + memory, ""])
            present = [label for label in labels if label in sections]
            for label in present:
                append_section(out, label, list(sections[label]), len(present) > 1 or label != group_title)
                used.add(label)

        supplements = [label for label in SUPPLEMENT[chapter] if label in sections and label not in used]
        if supplements:
            out.extend(["## 보충 학습", "", "> 원문 1~마지막 이론 절을 모두 학습한 뒤 보는 확장 내용이다.", ""])
            for label in supplements:
                append_section(out, label, list(sections[label]), True)
                used.add(label)

        problem = next((label for label in sections if "교재 확인문제" in label), None)
        if problem:
            out.extend(["## 교재 문제와 해설", "", "> 문제는 원문 단원 말미의 출제 순서대로 정리했다.", ""])
            append_section(out, problem, list(sections[problem]), False)
            used.add(problem)

        remaining = [label for label in sections if label not in used and label != "목차"]
        if remaining:
            out.extend(["## 추가 보충", ""])
            for label in remaining:
                append_section(out, label, list(sections[label]), True)

        path.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
        print(path.name)


if __name__ == "__main__":
    main()
