# BeautifulSoup 라이브러리를 이용한
# 쿠팡 웹사이트 제품 및 가격 데이터 크롤링
# 2021년 7월 16일 ~ 17일
# 유승원 (mikeryu98@gmail.com)

from urllib import request
from bs4 import BeautifulSoup 
#from urllib.request import urlopen
from urllib.parse import quote
import requests

# 쿠팡 페이지 정보 크롤링
def get_product(search_word, page_num):
    products = []
    prices = []

    coupang = 'https://www.coupang.com/'

    for loop in range(1, page_num+1):
        url = 'np/search?q={}&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page={}&rocketAll=false&searchIndexingToken=&backgroundColor='.format(
            quote(search_word), loop
        )
        
        req = requests.get(coupang + url, headers={"User-Agent": "Mozilla/5.0"})

        if req.ok:
            html = req.text
            soup = BeautifulSoup(html, 'lxml')

            get_product = soup.select('#productList')

            for product in get_product:
                products.append(product.text)

        # html = urlopen(coupang + url)
        # soup = BeautifulSoup(html, 'lxml')

        # products = soup.find('div', class_='name')

        # for product in products:
        #     products.append(product.text)
        
# input
search_word = input('검색할 상품 입력 : ')
page_num = int(input('검색 할 페이지 수 입력 : '))

get_product(search_word, page_num)
