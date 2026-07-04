# 『나는 초등학교 보안관입니다』 기사·리뷰 모음 사이트

컴퓨터를 켜놓을 필요 없이, 6시간마다 자동으로 새 기사와 블로그 리뷰를 수집해
보여주는 무료 웹사이트입니다. (GitHub Pages + GitHub Actions + 네이버 오픈 API)

## 준비물 (모두 무료)
1. GitHub 계정 — https://github.com
2. 네이버 개발자센터 API 키 — https://developers.naver.com

## 1단계: 네이버 API 키 발급 (5분)
1. https://developers.naver.com 접속 → 네이버 로그인
2. 상단 **Application → 애플리케이션 등록** 클릭
3. 애플리케이션 이름: 아무거나 (예: `book-tracker`)
4. 사용 API: **검색** 선택
5. 환경 추가: **WEB 설정** 선택, 웹 서비스 URL에 `http://localhost` 입력
6. 등록하면 **Client ID**와 **Client Secret**이 나옵니다 → 메모해 두세요

## 2단계: GitHub 저장소 만들기
1. GitHub에서 **New repository** → 이름 예: `boangwan-book` → **Public** → Create
2. 이 폴더의 파일 전부를 업로드합니다
   - 웹에서: 저장소 페이지 → **Add file → Upload files** → 폴더째 끌어다 놓기
   - 주의: `.github/workflows/update.yml` 은 숨김 폴더라서 웹 업로드에서 빠질 수 있어요.
     빠졌다면 **Add file → Create new file** 에서 파일명을
     `.github/workflows/update.yml` 로 입력하고 내용을 붙여넣으면 됩니다.

## 3단계: API 키 등록
1. 저장소의 **Settings → Secrets and variables → Actions → New repository secret**
2. 두 개를 등록:
   - Name: `NAVER_CLIENT_ID` / Value: (1단계에서 받은 Client ID)
   - Name: `NAVER_CLIENT_SECRET` / Value: (Client Secret)

## 4단계: 웹사이트 켜기 (GitHub Pages)
1. **Settings → Pages**
2. Source: **Deploy from a branch**, Branch: **main**, 폴더: **/ (root)** → Save
3. 1~2분 뒤 `https://아이디.github.io/boangwan-book/` 주소가 생깁니다
4. 이 주소를 고모부께 보내드리면 끝!

## 5단계: 자동 수집 확인
- **Actions** 탭 → "기사·리뷰 자동 수집" → **Run workflow** 버튼으로 즉시 한 번 실행해 보세요
- 이후에는 6시간마다 알아서 돌아갑니다 (컴퓨터 꺼놔도 됨)

## 자주 묻는 것
- **비용?** 전부 무료입니다. 네이버 검색 API는 하루 25,000회까지 무료인데
  이 사이트는 하루 8회만 씁니다.
- **교보문고/YES24 리뷰는?** 서점들은 리뷰 자동 수집을 공식적으로 허용하지 않아서,
  페이지 상단 버튼으로 바로가기를 제공합니다. 블로그 리뷰는 자동 수집됩니다.
- **수집 주기를 바꾸려면?** `.github/workflows/update.yml`의 `cron` 값을 수정하세요.
  예: `"0 0 * * *"` = 하루 1회
