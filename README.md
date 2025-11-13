# 포트폴리오 코드 품질 검증기

테크 리크루터를 위한 코드 품질 분석 도구입니다. 비개발자도 이해할 수 있는 명확한 리포트를 제공하여 지원자의 코드 품질을 평가할 수 있습니다.

## 저작권

Copyright (c) 2025 Gaon. All rights reserved.

이 소프트웨어는 저작권법에 의해 보호됩니다. 무단 복제, 배포, 수정을 금지합니다.  
사용 시 반드시 출처를 명시해야 합니다.

**원본 출처**: https://github.com/Gaon/portfolio-code-analyzer

## 주요 기능

- 📊 **코드 품질 지표 분석**: 복잡도, 가독성, 구조적 품질 측정
- 🌐 **다양한 언어 지원**: Python, JavaScript, Java, TypeScript 등
- 📈 **시각적 리포트**: HTML 형식의 이해하기 쉬운 리포트 생성
- ⚠️ **이슈 감지**: 코드 스멜, 잠재적 버그, 보안 취약점 탐지
- 🎯 **스크리닝 점수**: 종합적인 코드 품질 점수 제공

## 설치 방법

```bash
pip install -r requirements.txt
```

## 사용 방법

### 기본 사용법

```bash
python analyzer.py <코드_경로>
```

### 예시

```bash
# 단일 프로젝트 분석
python analyzer.py ./candidate-portfolio

# 결과를 HTML 파일로 저장
python analyzer.py ./candidate-portfolio -o report.html

# 상세 분석 모드
python analyzer.py ./candidate-portfolio --detailed
```

## 리포트 항목

1. **종합 점수**: 0-100점 척도의 전체 코드 품질 점수
2. **코드 복잡도**: 순환 복잡도, 함수 길이 등
3. **가독성**: 네이밍, 주석, 구조적 명확성
4. **구조 품질**: 모듈화, 의존성, 아키텍처
5. **이슈 목록**: 발견된 문제점과 개선 제안

## 지원 언어

- Python (.py)
- JavaScript (.js)
- TypeScript (.ts)
- Java (.java)
- C/C++ (.c, .cpp)
- 기타 텍스트 기반 언어

## 출력 예시

분석 완료 후 다음 정보를 제공합니다:
- 종합 점수 및 등급 (A, B, C, D, F)
- 주요 강점 및 약점
- 개선 권장 사항
- 상세 분석 리포트 (HTML)

