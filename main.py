# BeautifulSoup 라이브러리를 이용한
# 쿠팡 웹사이트 제품 및 가격 데이터 크롤링
# 2021년 7월 16일
# 유승원 (mikeryu98@gmail.com)

from bs4 import BeautifulSoup 
import requests

# 쿠팡 페이지 정보 크롤링
def get_product(search_word, page_num):
    products = []
    prices = []

    coupang = 'https://www.coupang.com/'

    for loop in range(1, page_num+1):
        url = 'np/search?q={}&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page={}&rocketAll=false&searchIndexingToken=&backgroundColor='.format(
            search_word, loop
        )
        #print(coupang + url + '\n')

        req = requests.get(coupang + url)

        # request 정상 작동 확인
        soup = BeautifulSoup(req.text, 'html.parser')

        get_product = soup.select('#productList[data-products]')

        for product in get_product:
            products.append(product.text)
    
    print(products)
            
# input
search_word = input('검색할 상품 입력 : ')
page_num = int(input('검색 할 페이지 수 입력 : '))

get_product(search_word, page_num)
