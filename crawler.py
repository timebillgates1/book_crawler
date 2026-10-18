"""도서 쇼핑몰 상품 정보 수집기 (연습용 사이트 books.toscrape.com 대상 샘플)

사용법:
    python crawler.py              # 50페이지 전체(1,000권)
    python crawler.py --pages 5    # 앞 5페이지만 테스트
결과: books.xlsx, books.csv
"""
import argparse
import re
import time
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
HEADERS = {"User-Agent": "Mozilla/5.0 (portfolio sample crawler)"}


def fetch(url, retries=3, timeout=10):
    """실패하면 잠깐 쉬었다가 최대 retries번 다시 시도해요."""
    for attempt in range(1, retries + 1):
        try:
            res = requests.get(url, headers=HEADERS, timeout=timeout)
            if res.status_code == 404:
                return None            # 페이지가 없으면 끝난 것으로 봐요
            res.raise_for_status()
            res.encoding = "utf-8"
            return res.text
        except requests.RequestException as e:
            print(f"  재시도 {attempt}/{retries}: {e}")
            time.sleep(1.5 * attempt)
    raise RuntimeError(f"요청 실패: {url}")


def parse_page(html, page_url):
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for item in soup.select("article.product_pod"):
        link = item.h3.a
        price_text = item.select_one("p.price_color").text
        rating_word = item.select_one("p.star-rating")["class"][1]
        rows.append({
            "상품명": link["title"],
            "가격(£)": float(re.sub(r"[^\d.]", "", price_text)),
            "평점": RATING_MAP.get(rating_word),
            "재고": item.select_one("p.availability").text.strip(),
            "링크": urljoin(page_url, link["href"]),
        })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=int, default=50)
    ap.add_argument("--delay", type=float, default=0.5, help="요청 간격(초)")
    args = ap.parse_args()

    all_rows, failed = [], []
    for page in range(1, args.pages + 1):
        url = BASE_URL.format(page)
        try:
            html = fetch(url)
        except RuntimeError as e:
            print(f"{page}페이지 건너뜀: {e}")
            failed.append(page)
            continue
        if html is None:
            print(f"{page}페이지 없음, 종료")
            break
        rows = parse_page(html, url)
        all_rows += rows
        print(f"{page}페이지 완료 ({len(rows)}개)")
        time.sleep(args.delay)

    df = pd.DataFrame(all_rows)
    df.to_excel("books.xlsx", index=False)
    df.to_csv("books.csv", index=False, encoding="utf-8-sig")
    print(f"총 {len(df)}개 저장 완료 (실패한 페이지: {failed or '없음'})")


if __name__ == "__main__":
    main()
