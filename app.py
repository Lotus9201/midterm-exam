from scraper import scrape_books
import database

def main():
    database.create_table()

    while True:
        print("\n=== 博客來 LLM 書籍管理系統 ===")
        print("1. 更新書籍資料庫")
        print("2. 查詢書籍")
        print("3. 離開")
        choice = input("請輸入選項 (1/2/3): ").strip()

        if choice == "1":
            print("開始抓取最新書籍資料...")
            books = scrape_books()
            count = database.insert_books(books)
            print(f"成功存入 {count} 筆新書資料。")

        elif choice == "2":
            print("\n查詢方式：")
            print("1. 依書名")
            print("2. 依作者")
            print("3. 返回主選單")
            sub = input("請輸入選項 (1/2/3): ").strip()

            if sub == "1":
                keyword = input("請輸入書名關鍵字: ").strip()
                results = database.query_books_by_title(keyword)
            elif sub == "2":
                keyword = input("請輸入作者關鍵字: ").strip()
                results = database.query_books_by_author(keyword)
            else:
                continue

            if results:
                for r in results:
                    print(f"書名: {r['title']}, 作者: {r['author']}, 價格: {r['price']}")
            else:
                print("查無資料。")

        elif choice == "3":
            print("離開系統。")
            break
        else:
            print("選項錯誤，請重新輸入。")

if __name__ == "__main__":
    main()
