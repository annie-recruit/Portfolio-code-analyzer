# 사용 가이드

## 빠른 시작

### 1. 기본 사용법

```bash
# 단일 파일 분석
python analyzer.py candidate_code.py

# 디렉토리 전체 분석
python analyzer.py ./candidate-portfolio

# 리포트 파일 지정
python analyzer.py ./candidate-portfolio -o candidate_report.html
```

### 2. 상세 분석 모드

```bash
python analyzer.py ./candidate-portfolio --detailed
```

상세 모드에서는 발견된 모든 이슈를 콘솔에 출력합니다.

## 리포트 해석 가이드

### 종합 점수 (0-100점)

- **90-100점 (A등급)**: 우수한 코드 품질
- **80-89점 (B등급)**: 양호한 코드 품질
- **70-79점 (C등급)**: 보통 수준, 개선 필요
- **60-69점 (D등급)**: 개선이 시급함
- **0-59점 (F등급)**: 심각한 문제 존재

### 주요 지표

1. **코드 복잡도**
   - 평균 복잡도가 5 이하: 양호
   - 평균 복잡도가 5-10: 주의 필요
   - 평균 복잡도가 10 이상: 개선 필요

2. **이슈 심각도**
   - **HIGH (심각)**: 구문 오류, 보안 취약점 등 즉시 수정 필요
   - **MEDIUM (중간)**: 코드 스멜, 긴 함수 등 개선 권장
   - **LOW (낮음)**: 스타일 개선 사항

### 스크리닝 기준 제안

#### 우수한 후보자 (A-B등급)
- 종합 점수 80점 이상
- 심각한 이슈 없음
- 적절한 코드 구조와 가독성

#### 보통 후보자 (C등급)
- 종합 점수 70-79점
- 일부 개선 사항 존재
- 기본적인 코딩 능력은 있으나 경험 부족 가능

#### 개선 필요 후보자 (D-F등급)
- 종합 점수 60점 미만
- 다수의 심각한 이슈
- 기본적인 코딩 규칙 미준수

## 실제 사용 시나리오

### 시나리오 1: GitHub 저장소 분석

```bash
# 저장소 클론 후 분석
git clone https://github.com/candidate/repo.git
python analyzer.py ./repo -o candidate_report.html
```

### 시나리오 2: 여러 후보자 비교

```bash
# 후보자별 리포트 생성
python analyzer.py ./candidate1 -o candidate1_report.html
python analyzer.py ./candidate2 -o candidate2_report.html
python analyzer.py ./candidate3 -o candidate3_report.html
```

### 시나리오 3: 특정 프로젝트만 분석

```bash
# 특정 디렉토리만 분석
python analyzer.py ./candidate-portfolio/backend -o backend_report.html
python analyzer.py ./candidate-portfolio/frontend -o frontend_report.html
```

## 주의사항

1. **코드 컨텍스트 고려**: 이 도구는 코드 품질만 측정합니다. 비즈니스 로직의 적절성은 별도로 평가해야 합니다.

2. **언어별 차이**: Python, JavaScript 등 언어별로 분석 정확도가 다를 수 있습니다.

3. **프로젝트 규모**: 작은 프로젝트와 큰 프로젝트의 점수 기준이 다를 수 있으니 상대적 비교를 권장합니다.

4. **포트폴리오 특성**: 학습용 프로젝트와 프로덕션 코드의 기준이 다를 수 있습니다.

