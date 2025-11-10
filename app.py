from scraper import scrape_books
import database

def main():
    database.create_table()

    while True:
        print("\n----- 博客來 LLM 書籍管理系統 -----")
        print("1. 更新書籍資料庫")
        print("2. 查詢書籍")
        print("3. 離開系統")
        print("---------------------------------")
        choice = input("請選擇操作選項 (1-3): ").strip()

        # 更新
        if choice == "1":
            print("開始從網路爬取最新書籍資料...")
            books = scrape_books()
            total = len(books)
            count = database.insert_books(books)
            print(f"資料庫更新完成！共爬取 {total} 筆資料，新增了 {count} 筆新書記錄。")

        # 查詢
        elif choice == "2":
            while True:
                print("\n--- 查詢書籍 ---")
                print("a. 依書名查詢")
                print("b. 依作者查詢")
                print("c. 返回主選單")
                print("---------------")
                sub = input("請選擇查詢方式 (a-c): ").strip().lower()

                if sub == "a":
                    keyword = input("請輸入關鍵字: ").strip()
                    results = database.query_books_by_title(keyword)

                elif sub == "b":
                    keyword = input("請輸入關鍵字: ").strip()
                    results = database.query_books_by_author(keyword)

                elif sub == "c":
                    break

                else:
                    print("無效選項，請重新輸入。")
                    continue

                # 顯示
                if results:
                    print("\n====================")
                    for r in results:
                        print(f"書名：{r['title']}")
                        print(f"作者：{r['author']}")
                        print(f"價格：{r['price']}")
                        print("---")
                    print("====================")
                else:
                    print("查無資料。")

        # === 離開系統 ===
        elif choice == "3":
            print("感謝使用，系統已退出。")
            break

        # === 無效選項 ===
        else:
            print("無效選項，請重新輸入。")


if __name__ == "__main__":
    main()
