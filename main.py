import requests
# If you are using a Jupyter Notebook, uncomment the following line.
# %matplotlib inline
import matplotlib.pyplot as plt
import json
from PIL import Image
from io import BytesIO
import os
import sys

# Add your Computer Vision key and endpoint to your environment variables.

if 'COMPUTER_VISION_KEY' in os.environ:  #OSの環境変数にCOMPUTER_VISION_KEYの値が設定されている場合
    subscription_key = os.environ['COMPUTER_VISION_KEY']  #subscription_keyにその値を代入
else:
    #エラー処理を出力する。
    print("\nSet the COMPUTER_VISION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    #プログラムを強制終了させる。
    sys.exit()

if 'COMPUTER_VISION_ENDPOINT' in os.environ:  #OSの環境変数にCOMPUTER_VISION_ENDPOINTが設定されている場合
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']  #endpointに値を代入

# Computer Visionの解析エンドポイントのURLをセットする。(エンドポイント＝API連携するためのURL)
analyze_url = endpoint + "vision/v3.1/analyze"

#画像URLをimage_urlという変数にセットする。
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Shiba_inu_taiki.jpg/250px-Shiba_inu_taiki.jpg"

#HTTPリクエストヘッダーにheaders変数の値をセットし、
#paramsでは、解析のために要求するビジュアル機能を選択する。
#dataでは、urlという変数に画像のURLをセットする。
headers = {'Ocp-Apim-Subscription-Key': subscription_key}
params = {'visualFeatures': 'Categories,Description,Color'}
data = {'url': image_url}
#POST通信でリクエストしたデータをresponseとして受け取る。
#引数には、API連携するためのURL(analyze_url),リクエストヘッダーに書き込む情報(headers),
#ビジュアル解析の機能の設定(params),jsonはresponseで返ってくる作られた情報の内容を辞書型として指定する。
response = requests.post(analyze_url, headers=headers,
                         params=params, json=data)
response.raise_for_status()

#analysisにレスポンスの結果をjson形式で格納する。
analysis = response.json()
#jsonをターミナル上で出力する。「indent=2」は辞書型のレイアウトをきれいにするためのもの
print(json.dumps(response.json(),indent=2))
#image_captionに画像の分析結果のメッセージを格納する。
image_caption = analysis["description"]["captions"][0]["text"].capitalize()

#画像を表示する。
#requests.get()を使用して指定したURLから画像データを取得し、
#BytesIOを使用して画像データをバイトストリームとして読み込みます。(API関係なく単純に画像をURLから取得している)
#その後、Image.open()を使用してバイトストリームから画像オブジェクトを作成します。これにより、画像がメモリに読み込まれます。
image = Image.open(BytesIO(requests.get(image_url).content))
plt.imshow(image)
plt.axis("off")
#画像の分析結果のメッセージを表示する。
_ = plt.title(image_caption, size="x-large", y=-0.1)
plt.show()