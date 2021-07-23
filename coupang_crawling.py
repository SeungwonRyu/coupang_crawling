# BeautifulSoup 라이브러리를 이용한
# 쿠팡 웹사이트 제품 및 가격 데이터 크롤링
# 2021년 7월 16일 ~
# 유승원 (mikeryu98@gmail.com)


# -------------------- Libraries --------------------
# 웹 페이지 구문분석
from bs4 import BeautifulSoup 
from urllib.parse import quote
import requests

# DB 연결
import pymysql as db


# -------------------- Functions --------------------
# 제품 정보 크롤링
def get_product(search_word, page_num):
    result = []

    coupang = 'https://www.coupang.com/'

    for loop in range(1, page_num+1):
        url = 'np/search?q={}&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page={}&rocketAll=false&searchIndexingToken=&backgroundColor='.format(
            quote(search_word), loop
        )
        
        req = requests.get(coupang + url, headers={"User-Agent": "Mozilla/5.0"})

        if req.ok:
            html = req.text
            soup = BeautifulSoup(html, 'lxml')

            # 1page 36products
            products = soup.select('li.search-product')  

            for product in products:
                names = product.select('div.name')
                prices = product.select('strong.price-value')

                for name in names:
                    result.append(name.text)

                for price in prices:
                    result.append(price.text)

    return result

# 제품 정보 출력
def print_product(product_list):
    for i in range(0, len(product_list)):
        if i%2==0:
            print('제품명: ', product_list[i])
        else:
            print('가격: ', product_list[i], '\n')

# 데이터 베이스 저장
def connect_db(search_word, product_list):
    
    # 검색어의 테이블이 존재하는지 확인
    cursor.execute('SHOW TABLES LIKE \'' + search_word + '\';')
    if len(cursor.fetchall()) == 0:
        cursor.execute(
            'CREATE TABLE ' + search_word + ' (`index` INT AUTO_INCREMENT, `product_name` VARCHAR(200), `price` VARCHAR(50), PRIMARY KEY(`index`)) DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;'
        )

        for i in range(0, len(product_list), 2):
            cursor.execute('INSERT INTO ' + search_word + ' (product_name, price) VALUES (\'' + product_list[i] + '\', \'' + product_list[i+1] + '\');')
            connect.commit()

    else:
        for i in range(0, len(product_list), 2):
            cursor.execute('INSERT INTO ' + search_word + ' (product_name, price) VALUES (\'' + product_list[i] + '\', \'' + product_list[i+1] + '\');')
            connect.commit()

# -------------------- Run --------------------
# DB 연결
connect = db.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        passwd = '1117',
        db = 'coupang',
        charset = 'utf8'
    )
    
# 딕셔너리 형태 커서 설정
cursor = connect.cursor(db.cursors.DictCursor)

# input
print('--------- 쿠팡 제품 검색 ---------')
search_word = input('  검색할 상품 입력 : ')
page_num = int(input('  검색 할 페이지 수 입력 : '))

connect_db(search_word, get_product(search_word, page_num))
