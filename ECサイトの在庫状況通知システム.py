import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

#通知先のLINE特定用アクセストークン
access_token = "非公開"

#メソッド
def send_line_message(message):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "message": message
    }

    response = requests.post(url, headers=headers, data=payload)
    print(response.text)

#クラス
class Goods:
    URL = ""
    name = ""

    def __init__(self, URL, name):
        self.URL = URL
        self.name = name

#メイン処理
def lambda_function():
    #判別用文字列
    judge_string = "カートに入れる"

    #webスクレイピング対象URL一覧
    goods_list = [
        Goods("非公開", "非公開"),
        Goods("非公開", "非公開")
    ]

    #ブラウザのオプション
    options = Options()
    #ブラウザを非表示で起動する
    options.add_argument("--headless")

    #ブラウザ起動
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    #要素が見つかるまで最大10秒待つ
    driver.implicitly_wait(10)

    for goods in goods_list:
        driver.get(goods.URL)
        #要素が見つかるまで最大10秒待つ
        driver.implicitly_wait(10)

        #ブラウザのHTMLを取得
        soup = BeautifulSoup(driver.page_source, features="html.parser")
        #特定のテキストを持つ<button>タグを全て列挙
        target_button_tags = soup.find_all("button", text=judge_string)

        send_line_message("テスト")

        #販売未定
        if len(target_button_tags) == 0:
            continue
        #エラー
        if len(target_button_tags) >= 2:
            # メッセージを送信
            send_line_message("\n判別用文字列が重複して存在するため自動判断不可\nプログラムの修正と商品ページの確認が必要\n現在の判別用文字列「" + judge_string + "」")
            continue
        #販売開始
        send_line_message("\n販売開始\n「" + goods.name + "」\n購入急げ")

    #ブラウザを閉じる
    driver.quit()

lambda_function()