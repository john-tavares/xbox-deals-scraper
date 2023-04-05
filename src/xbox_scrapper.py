from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

HOST = 'https://www.xbox.com'
MAX_WAIT_TIME = 60

def create_webdriver(headless=True) -> webdriver.Firefox:
    """Cria uma instância do webdriver do Firefox"""
    options = Options()
    if headless:
        options.add_argument("-headless")
    return webdriver.Firefox(options=options)


def scrape_xbox_deals_html(locale="pt-br") -> str:
    """Acessa a página de promoções do Xbox e retorna o HTML da página"""
    url = f"{HOST}/{locale}/games/all-games?cat=onsale"

    with create_webdriver(False) as driver:
        driver.get(url)

        wait = WebDriverWait(driver, MAX_WAIT_TIME)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "m-product-placement-item")))

        html = driver.page_source
    
    return html


def extract_deal_data(deal) -> dict:
    """Extrai os dados de um deal e retorna um dicionário com os valores"""
    name = deal.find(class_="x1GameName").text
    price_old = float((deal.find("s").text).split()[-1].replace(",", "."))
    price_new = float((deal.find(class_="textpricenew").text).split()[-1].replace(",", "."))
    discount = (price_new / price_old) * 100

    deal_data = {
        'name': name,
        'price_old': price_old,
        'price_new': price_new,
        'discount': discount
    }

    return deal_data


def scrape_deals_in_page() -> pd.DataFrame:
    """Extrai os dados de todos os deals na página e imprime na tela"""

    page = scrape_xbox_deals_html()
    soup = BeautifulSoup(page, features='lxml')
    deals_html = soup.find_all(class_="m-product-placement-item")
    
    data = []
    
    for deal_html in deals_html:
        deal_data = extract_deal_data(deal_html)
        data.append(deal_data)
    
    data = pd.DataFrame(data)
    return data