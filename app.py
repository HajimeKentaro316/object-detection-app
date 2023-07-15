#API用のimport文
import requests
# If you are using a Jupyter Notebook, uncomment the following line.
# %matplotlib inline
import matplotlib.pyplot as plt
import json
from PIL import Image
from io import BytesIO
import os
import sys

#streamlit用のimport文
import pandas as pd
import streamlit as st
import altair as alt

#環境変数を確認する関数
def get_certificate() :
    if 'COMPUTER_VISION_KEY' in os.environ:  #OSの環境変数にCOMPUTER_VISION_KEYの値が設定されている場合
        subscription_key = os.environ['COMPUTER_VISION_KEY']  #subscription_keyにその値を代入
    else:
        #エラー処理を出力する。
        print("\nSet the COMPUTER_VISION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
        #プログラムを強制終了させる。
        sys.exit()

    if 'COMPUTER_VISION_ENDPOINT' in os.environ:  #OSの環境変数にCOMPUTER_VISION_ENDPOINTが設定されている場合
        endpoint = os.environ['COMPUTER_VISION_ENDPOINT']  #endpointに値を代入
    return subscription_key, endpoint

#################################################################

#streamlitの表示内容の作成
st.title('物体検出アプリ')
st.sidebar.write("""
# 画像のURLから物体検出                 
""")

#画像URLをimage_urlという変数にセットする。
image_url = st.sidebar.text_input('画像URLを入力',"https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Shiba_inu_taiki.jpg/250px-Shiba_inu_taiki.jpg")


#URLから物体検出のアルゴリズムを関数として記述
def get_data():
    #環境変数の設定確認
    subscription_key, endpoint = get_certificate()
    # Computer Visionの解析エンドポイントのURLをセットする。(エンドポイント＝API連携するためのURL)
    analyze_url = endpoint + "vision/v3.1/analyze"

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
    #戻り値にimageとimage_captionを格納
    return image, image_caption

if not image_url:
    st.error('画像URLを入力してください')
else:   
    #関数の戻り値をresultに格納
    result = get_data()
    #image,image_urlにそれぞれ戻り値を格納。
    image, image_caption = result

    #画像をstreamlit上に表示する。
    st.image(image)

    #画像のキャプションをstraemlit上に表示する。
    st.write(f"""
    ## {image_caption}
    """)

############################################################
st.sidebar.write("""
# ローカルファイルの画像から物体検出                 
""")

#ローカルファイルから物体検出を行うアルゴリズム
uploaded_file = st.sidebar.file_uploader('画像をローカルファイルから選択してください',type=['jpg','png'])

#ローカルファイルから物体検出を行う関数
def get_data_Local() :
    #環境変数の設定確認
    subscription_key, endpoint = get_certificate()
    analyze_url = endpoint + "vision/v3.1/analyze"

    # 画像をバイトで読み込む
    image_data = uploaded_file.getvalue()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
            'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Categories,Description,Color'}
    response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data)

    # The 'analysis' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.
    analysis = response.json()
    print(json.dumps(analysis, indent = 2))
    image_caption = analysis["description"]["captions"][0]["text"].capitalize()

    #画像を表示する。
    #requests.get()を使用して指定したURLから画像データを取得し、
    #BytesIOを使用して画像データをバイトストリームとして読み込みます。(API関係なく単純に画像をURLから取得している)
    #その後、Image.open()を使用してバイトストリームから画像オブジェクトを作成します。これにより、画像がメモリに読み込まれます。
    image = Image.open(BytesIO(image_data))
    #戻り値にimageとimage_captionを格納
    return image, image_caption

if uploaded_file is not None :
    #image,image_urlにそれぞれ戻り値を格納。
    image_local, image_caption_local = get_data_Local()

    #画像をstreamlit上に表示する。
    st.image(image_local)

    #画像のキャプションをstraemlit上に表示する。
    st.write(f"""
    ## {image_caption_local}
    """)
else :
    # ファイルがアップロードされなかった場合
    st.sidebar.write("ファイルがアップロードされていません")


# #検出結果を表示する。
# plt.imshow(image)
# plt.axis("off")
# #画像の分析結果のメッセージを表示する。
# _ = plt.title(image_caption, size="x-large", y=-0.1)
# plt.show()