# 課題１ 難易度★★☆☆☆
# 会社名以外の項目を取得して画面にprint文で表示してみましょう。

# 課題２ 難易度★★★☆☆
# for文を使って、１ページ内の３つ程度の項目（会社名、年収など）を取得できるように改造してみましょう

# 課題３ 難易度★★★☆☆
# ２ページ目以降の情報も含めて取得できるようにしてみましょう

# 課題４ 難易度★★☆☆☆
# 任意のキーワードをコンソール（黒い画面）から指定して検索できるようにしてみましょう

# 課題５ 難易度★★★★☆
# 取得した結果をpandasモジュールを使ってCSVファイルに出力してみましょう

# 課題６ 難易度★★☆☆☆
# エラーが発生した場合に、処理を停止させるのではなく、スキップして処理を継続できるようにしてみましょう
# (try文)

# 課題７ 難易度★★☆☆☆
# 処理の経過が分かりやすいようにログファイルを出力してみましょう
# ログファイルとは：ツールがいつどのように動作したかを後から確認するために重要なテキストファイルです。 
# ライブラリを用いることもできますが、テキストファイルを出力する処理で簡単に実現できるので、試してみましょう。 (今何件目、エラー内容、等を表示)

import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd



# Chromeを起動する関数
def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)



# main処理
def main():
    search_keyword =input("検索ワードを要求 >>> ")
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver('chromedriver', False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')
    time.sleep(5)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')

    # 検索窓に入力
    driver.find_element_by_class_name("topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    # ページ終了まで繰り返し取得
    exp_company_list = []
    

    count = 0
    j = 0
    while j < 1:
        # 会社単位での全ブロック要素を取得
        company_lists = driver.find_elements_by_class_name("cassetteRecruit__content")

        for e in company_lists:
            # 途中で使用、初期化
            i = 0
            detail_list = []
            column_list = []
            exp_column_list = []

            # 検索結果の一番上の会社名を取得
            name = e.find_element_by_class_name("cassetteRecruit__name")
            content_names = e.find_elements_by_class_name("tableCondition__head")
            content_lists = e.find_elements_by_class_name("tableCondition__body")
            print("----------")
            print("会社名")
            print(name.text.partition("|")[0])
            column_list.extend(["会社名"])
            detail_list.extend([name.text.partition("|")[0]])
            print("")
            while i < len(content_names):
                print(content_names[i].text)
                print(content_lists[i].text + "\n")
                column_list.extend([content_names[i].text])
                detail_list.extend([content_lists[i].text])
                i += 1
            print("----------\n")

            exp_column_list.extend([column_list])
            exp_company_list.extend([detail_list])

            # ログ出力
            with open('log.txt', 'a') as log:
                count += 1
                log.write('{}件目を書き込み完了\n'.format(count))
        time.sleep(10)

        # ログの整形
        with open('log.txt', 'a') as log:
            count += 1
            log.write('----------\n'.format(count))


        try:
            driver.get(str(driver.find_element_by_class_name("iconFont--arrowLeft").get_attribute("href")))
        except:
            j = 1
            # print(exp_column_list)
            break
    
    df = pd.DataFrame(exp_company_list, columns = exp_column_list)
    df.to_csv('result.csv')

    driver.quit()



# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
