# GitHub Pages 설정 가이드

## GitHub Pages 활성화 방법

### 1단계: 저장소 설정

1. GitHub 저장소로 이동: https://github.com/annie-recruit/Portfolio-code-analyzer
2. **Settings** 탭 클릭
3. 왼쪽 메뉴에서 **Pages** 클릭

### 2단계: Pages 설정

1. **Source** 섹션에서:
   - Branch: `main` 선택
   - Folder: `/ (root)` 선택
2. **Save** 버튼 클릭

### 3단계: 배포 확인

- 몇 분 후 다음 주소에서 접근 가능:
  - `https://annie-recruit.github.io/Portfolio-code-analyzer/`

### 4단계: 커스텀 도메인 (선택사항)

- Settings → Pages → Custom domain에서 도메인 설정 가능

## 파일 구조

GitHub Pages가 작동하려면 다음 파일들이 필요합니다:

- ✅ `index.html` - 메인 웹 페이지
- ✅ `.nojekyll` - Jekyll 처리 비활성화 (이미 생성됨)

## 업데이트 방법

코드를 수정한 후:

```bash
git add .
git commit -m "Update web interface"
git push origin main
```

GitHub Pages는 자동으로 업데이트됩니다 (몇 분 소요).

## 문제 해결

### 페이지가 표시되지 않는 경우

1. Settings → Pages에서 배포 상태 확인
2. Actions 탭에서 배포 로그 확인
3. `index.html`이 루트 디렉토리에 있는지 확인
4. `.nojekyll` 파일이 있는지 확인

### Pyodide 로딩이 느린 경우

- 첫 로딩 시 Pyodide 라이브러리 다운로드로 인해 시간이 걸릴 수 있습니다
- 이후 방문 시 캐시되어 더 빠르게 로드됩니다

