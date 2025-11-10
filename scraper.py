import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_books():
    """
    使用 Selenium 爬取博客來 LLM 書籍資料（全部分頁）。
    回傳書籍列表，每本書為 dict: title, author, price, discount_rate, link
    """
    # Headless 模式
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    keyword = "LLM"
    total_pages = 3  # 總共三頁
    books = []

    for page in range(1, total_pages + 1):
        url = f"https://search.books.com.tw/search/query/cat/1/sort/1/v/1/spell/3/ms2/ms2_1/page/{page}/key/{keyword}"
        print(f"正在爬取第 {page} 頁...")
        driver.get(url)

        try:
            # 等待頁面載入
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.table-searchbox div.table-td"))
            )
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            items = soup.select("div.table-searchbox div.table-td")

            for item in items:
                # 書名與連結
                a_tag = item.select_one("h4 a")
                title = a_tag.text.strip() if a_tag else "查無資料"
                link = "https:" + a_tag.get("href") if a_tag and a_tag.get("href") else "查無資料"

                # 作者
                author_tags = item.select("p.author a")
                author = ", ".join([a.text.strip() for a in author_tags]) if author_tags else "查無資料"

                # 價格處理
                price_ul = item.select_one("ul.price.clearfix")
                price_text = price_ul.text.strip() if price_ul else ""
                price_digits = re.findall(r"\d+", price_text)

                if len(price_digits) >= 2:
                    # 有折扣：
                    discount_rate = int(price_digits[0])
                    discount_price = int(price_digits[1])
                elif len(price_digits) == 1:
                    # 無折扣
                    discount_rate = 100
                    discount_price = int(price_digits[0])
                else:
                    discount_rate = 0
                    discount_price = 0

                books.append({
                    "title": title,
                    "author": author,
                    "price": discount_price,
                    "discount_rate": discount_rate,
                    "link": link
                })

        except Exception as e:
            print(f"第 {page} 頁抓取錯誤: {e}")
            continue

    driver.quit()
    return books


# 測試
if __name__ == "__main__":
    result = scrape_books()
    print(f"\n共抓取 {len(result)} 本書\n")
    for b in result[:8]:  
        print(f"書名: {b['title']}\n作者: {b['author']}\n價格: {b['price']} 元 ({b['discount_rate']} 折)\n連結: {b['link']}\n")
