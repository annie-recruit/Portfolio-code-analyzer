# GitHub 업로드 가이드

## 1단계: GitHub에서 저장소 생성

1. https://github.com 에 로그인
2. 우측 상단의 "+" 버튼 클릭 → "New repository" 선택
3. 저장소 이름 입력 (예: `portfolio-code-analyzer`)
4. Public 또는 Private 선택
5. **"Initialize this repository with a README" 체크 해제** (이미 로컬에 파일이 있으므로)
6. "Create repository" 클릭

## 2단계: 원격 저장소 연결 및 푸시

GitHub에서 저장소를 생성하면 나오는 URL을 사용하여 다음 명령어를 실행하세요:

```bash
cd C:\Users\Gaon\portfolio-code-analyzer

# 원격 저장소 추가 (YOUR_USERNAME을 본인 GitHub 사용자명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/portfolio-code-analyzer.git

# 또는 SSH를 사용하는 경우
# git remote add origin git@github.com:YOUR_USERNAME/portfolio-code-analyzer.git

# 메인 브랜치를 main으로 변경 (GitHub 기본값)
git branch -M main

# GitHub에 푸시
git push -u origin main
```

## 빠른 실행 스크립트

GitHub 저장소를 생성한 후, 아래 명령어를 실행하세요:

```bash
cd C:\Users\Gaon\portfolio-code-analyzer
git remote add origin https://github.com/YOUR_USERNAME/portfolio-code-analyzer.git
git branch -M main
git push -u origin main
```

**주의**: `YOUR_USERNAME`을 본인의 GitHub 사용자명으로 변경하세요!

