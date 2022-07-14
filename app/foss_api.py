import datetime
import glob
import json
import os
import time
from collections import OrderedDict

import requests

url = "http://localhost:8081"

# 初期設定
def set_token_folder(access_token_json):
    token = get_access_token(0, "fossology_python_token", access_token_json)
    return token, make_folder(token)

# アクセストークンの獲得
def get_access_token(token_num, token_name, access_token_json):
    # FOSSologyに送信する情報
    headers = {'Content-Type':'application/json'}
    body = {
        "username":"fossy",
        "password":"fossy",
        "token_scope":"write"
    }
    today = datetime.date.today()
    expire_date = today + datetime.timedelta(days=30)

    # API接続の実行
    next_num = token_num + 1
    body["token_expire"] = str(expire_date)
    body["token_name"] = token_name + str(next_num)
    result = requests.post(url + '/repo/api/v1/tokens', headers=headers, data=json.dumps(body)).json()

    # 次のアクセストークンを作るための情報を入れてトークンの内容を保存
    body["token_nummber"] = next_num
    body["token"] = result["Authorization"]
    with open(access_token_json, 'w') as f:
        json.dump(body, f, indent=4)

    # トークンを返す
    return result["Authorization"]

# 作業用フォルダをFOSSology上に作成
def make_folder(token):
    # FOSSologyに送信する情報
    headers = {
        'Content-Type': 'application/json',
        'parentFolder': '1',
        'folderName': 'fossology_python',
        'folderDescription': 'folder create test via REST API by python',
        'Authorization': token
    }

    # API接続の実行
    result = requests.post(url + '/repo/api/v1/folders', headers=headers).json()
    # folderのIDを返す
    return result["message"]

# 作業用フォルダのIDを取得
def get_folderID(token):
    # FOSSologyに送信する情報
    headers = {'Authorization':token}

    # API接続の実行
    result = requests.get(url + '/repo/api/v1/folders', headers=headers).json()
    for folder in list(result):
        print(folder)
        if folder["name"] == "fossology_python":
            return folder["id"]
    return 0

# アクセストークンの確認or取得
def take_access_token(access_token_dict, access_token_json):
    # 有効期限と今日を取得
    token_expire_date = datetime.datetime.strptime(access_token_dict["token_expire"], '%Y-%m-%d').date()
    today = datetime.date.today()

    # 期限が切れていた時
    if token_expire_date <= today:
        return get_access_token(access_token_dict["token_num"], access_token_dict["token_name"], access_token_json)
    # 期限が切れてなかった時
    else:
        return access_token_dict["token"]

# POST  ファイル
def upload_copyright(token, copyright_file, folderID):
    # FOSSologyに送信する情報
    headers = {
        'folderId': folderID,
        'uploadDescription': 'Upload from python',
        'public': 'public',
        'Authorization': token
    }

    # API接続の実行
    with open(copyright_file, 'rb') as file:
        result = requests.post(url + '/repo/api/v1/uploads', headers=headers, files={'fileInput': file}).json()
    return str(result["message"])

# 解析依頼
def analyze_copyright(uploadId, token, folderID):
    # FOSSologyに送信する情報
    headers = {
        'folderId': folderID,
        'uploadId': uploadId,
        'Authorization': token,
        'Content-Type': 'application/json',
    }
    body = {
        "analysis": {
            "bucket": True,
            "copyright_email_author": True,
            "ecc": True,
            "keyword": True,
            "mime": True,
            "monk": True,
            "nomos": True,
            "package": True
            },
        "decider": {
            "nomos_monk": True,
            "bulk_reused": True,
            "new_scanner": True
            }
    }

    # API接続の実行
    # 結果を受けて出力すればテスト可能
    requests.post(url + '/repo/api/v1/jobs', headers=headers, data=json.dumps(body))

def get_spdx(uploadId, token, copyright_spdx):
    # FOSSologyに送信する情報
    headers = {
        'uploadId': uploadId,
        'reportFormat': 'spdx2tv',
        'Authorization': token,
    }

    # API接続の実行
    result = requests.get(url + '/repo/api/v1/report', headers=headers).json()

    # SPDX生成を待つ
    time.sleep(5)
    headers = {
        'Authorization': token,
        'accept': 'text/plain'
    }

    # API接続の実行
    result = requests.get(url + '/repo/api/v1/report/' + str(result['message']).rsplit('/',1)[1], headers=headers)
    with open(copyright_spdx, mode='w', encoding='utf-8') as f:
        f.write(str(result.text))

# FOSSologyAPIを用いて解析
def foss_api(copyright_file, copyright_spdx):
    # ローカルに保存していたアクセストークン情報を見に行く
    access_token_json = r"./access_token.json"
    with open(access_token_json) as f:
        access_token_dict = json.load(f)

    # アクセストークンが空（初期状態）の場合
    if access_token_dict == {}:
        token, folderID = set_token_folder(access_token_json)
    else:
        token = take_access_token(access_token_dict, access_token_json)
        folderID = get_folderID(token)

    folderID = str(folderID)
    uploadId = upload_copyright(token, copyright_file, folderID)
    time.sleep(5)
    analyze_copyright(uploadId, token, folderID)
    time.sleep(5)
    get_spdx(uploadId, token, copyright_spdx)
