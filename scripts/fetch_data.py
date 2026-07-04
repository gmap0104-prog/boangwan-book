"""
네이버 오픈 API(뉴스·블로그 검색)로 책 관련 글을 수집해 data.json에 누적 저장합니다.
GitHub Actions가 6시간마다 자동 실행합니다. (직접 실행할 필요 없음)

필요한 환경변수: NAVER_CLIENT_ID, NAVER_CLIENT_SECRET
"""
import json, os, re, sys, urllib.parse, urllib.request
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

QUERY = '"나는 초등학교 보안관입니다"'   # 따옴표로 정확히 이 제목이 들어간 글만 검색
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data.json")

CLIENT_ID = os.environ.get("NAVER_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("NAVER_CLIENT_SECRET", "")

def api(endpoint: str, query: str, display: int = 50):
    url = f"https://openapi.naver.com/v1/search/{endpoint}.json?query={urllib.parse.quote(query)}&display={display}&sort=date"
    req = urllib.request.Request(url, headers={
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET,
    })
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8")).get("items", [])

def clean(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s or "").replace("&quot;", '"').replace("&amp;", "&").strip()

def to_iso_news(pubdate: str) -> str:
    try:
        return parsedate_to_datetime(pubdate).astimezone(timezone.utc).isoformat()
    except Exception:
        return datetime.now(timezone.utc).isoformat()

def to_iso_blog(postdate: str) -> str:  # 형식: YYYYMMDD
    try:
        return datetime.strptime(postdate, "%Y%m%d").replace(tzinfo=timezone.utc).isoformat()
    except Exception:
        return datetime.now(timezone.utc).isoformat()

def domain(link: str) -> str:
    try:
        host = urllib.parse.urlparse(link).netloc.replace("www.", "")
        return host
    except Exception:
        return ""

def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("NAVER_CLIENT_ID / NAVER_CLIENT_SECRET 환경변수가 없습니다.", file=sys.stderr)
        sys.exit(1)

    # 기존 데이터 불러오기 (수집된 글은 계속 보존)
    try:
        with open(DATA_PATH, encoding="utf-8") as f:
            existing = json.load(f).get("items", [])
    except Exception:
        existing = []
    by_link = {it["link"]: it for it in existing}

    added = 0
    for it in api("news", QUERY):
        link = it.get("originallink") or it.get("link", "")
        if link and link not in by_link:
            by_link[link] = {
                "type": "news", "title": clean(it.get("title")),
                "description": clean(it.get("description")),
                "link": link, "source": domain(link),
                "date": to_iso_news(it.get("pubDate", "")),
            }
            added += 1

    for it in api("blog", QUERY):
        link = it.get("link", "")
        if link and link not in by_link:
            by_link[link] = {
                "type": "blog", "title": clean(it.get("title")),
                "description": clean(it.get("description")),
                "link": link, "source": clean(it.get("bloggername")),
                "date": to_iso_blog(it.get("postdate", "")),
            }
            added += 1

    items = sorted(by_link.values(), key=lambda x: x["date"], reverse=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump({"updated": datetime.now(timezone.utc).isoformat(), "items": items},
                  f, ensure_ascii=False, indent=2)
    print(f"완료: 새 글 {added}건, 전체 {len(items)}건")

if __name__ == "__main__":
    main()
