# 도서 쇼핑몰 상품 정보 자동 수집기

쇼핑몰의 상품 정보를 자동으로 모아 엑셀로 저장하는 파이썬 프로그램입니다.
크롤링 연습용으로 공개된 사이트(books.toscrape.com)를 대상으로 만든 샘플입니다.

## 기능
- 전체 50페이지, 1,000개 상품 자동 수집
- 수집 항목: 상품명, 가격, 평점, 재고, 링크
- 엑셀(`books.xlsx`)과 CSV(`books.csv`)로 저장
- 요청 실패 시 자동 재시도, 끝내 실패한 페이지는 건너뛰고 계속 진행
- 서버에 부담을 주지 않도록 요청 간격 적용

## 사용 방법
```bash
pip install -r requirements.txt
python crawler.py              # 전체 수집
python crawler.py --pages 5    # 앞 5페이지만 테스트
```
구글 Colab에서도 실행할 수 있습니다.

## 결과 예시
50페이지 전체 실행 결과: **1,000개 상품 수집**, 평균 가격 £35.07, 평균 평점 2.92

| 상품명 | 가격(£) | 평점 | 재고 |
|---|---|---|---|
| A Light in the Attic | 51.77 | 3 | In stock |
| Tipping the Velvet | 53.74 | 1 | In stock |
| Soumission | 50.10 | 1 | In stock |
| Sharp Objects | 47.82 | 4 | In stock |
| Sapiens: A Brief History of Humankind | 54.23 | 5 | In stock |

## 사용 기술
Python, requests, BeautifulSoup, pandas

## 참고
- 실제 의뢰 작업에서는 대상 사이트의 이용약관과 `robots.txt`를 먼저 확인하고, 수집이 허용된 범위에서만 진행합니다.
