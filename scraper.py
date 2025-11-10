import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_books():
    """
    使用 Selenium 爬取博客來 LLM 書籍資料（全部分頁）。
    回傳書籍列表，每本書為 dict: title, author, price, link
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
        driver.get(url)

        try:
            # 等待書籍載入
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.table-searchbox div.table-td"))
            )
            time.sleep(0.5)

            # 滑到底部
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)

            items = driver.find_elements(By.CSS_SELECTOR, "div.table-searchbox div.table-td")

            for item in items:
                # 書名
                try:
                    a_tag = item.find_element(By.CSS_SELECTOR, "h4 a")
                    title = a_tag.text.strip()
                    link = a_tag.get_attribute("href")
                except:
                    title = "查無資料"
                    link = "查無資料"

                # 作者
                try:
                    author_tags = item.find_elements(By.CSS_SELECTOR, "p.author a")
                    author = ", ".join([a.text.strip() for a in author_tags]) if author_tags else "查無資料"
                except:
                    author = "查無資料"

                # 價格
                try:
                    price_tag = item.find_element(By.CSS_SELECTOR, "span.price")
                    price_text = price_tag.text
                    price_digits = re.findall(r"\d+", price_text)
                    price = int(price_digits[-1]) if price_digits else 0
                except:
                    price = 0

                books.append({
                    "title": title,
                    "author": author,
                    "price": price,
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
    print(f"共抓取 {len(result)} 本書")
    for b in result[:5]:  # 只顯示前 5 本測試
        print(f"{b['title']} | {b['author']} | {b['price']}")
