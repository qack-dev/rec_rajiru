#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import subprocess
from datetime import datetime

# その番組のjsonを取得する。
def get_json(url):
    try:
        req = requests.get(url)
        req.raise_for_status()  # ステータスコードが200番台でない場合にエラーを発生させる
        return req.json()       # .json()メソッドで直接デコードする
    except requests.exceptions.RequestException as e:
        print(f"HTTPリクエスト中にエラーが発生しました: {e}")
        return None
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSONのデコードに失敗しました: {e}")
        return None

# コマンドを実行
def run_cmd(items, path):
    # コマンドを表示
    print('Running command:')
    print(items)
    print('cwd = ' + path)
    # 実行
    print('Run!')
    subprocess.run(items, cwd=path)

# 映像ありかなしかで拡張子を変える。
def select_ext(str):
    if str == 'sound':
        return 'm4a'
    elif str == 'movie':
        return 'mp4'

# 2次元配列を1次元配列へ変換
def conv_list(items):
    items2 = []
    # 要素をループ
    for item in items:
        # 要素がlistなら
        if isinstance(item, list):
            items2.extend(item)
        # 要素が文字列か数字なら
        elif isinstance(item, (str, int)):
            items2.append(item)
    return items2

# SAVE_PATH配下で作るファイル名を作る。
# output:((相対パス), (ファイル名), (タイトル))
def make_filename_list(d):
    # 変数宣言
    tmp1 = ''
    tmp2 = ''
    tmp3 = ''
    # 「音泉」なら
    if d['radio_type'] == '音泉':
        tmp1 = d['radio_type'] + '/' + d['title']
        tmp3 = d['title'] \
            + '_【' + d['program_title'] + '】' \
            + '_' + d['delivery_date']
        tmp2 = '[' + d['radio_type'] + ']' \
            + tmp3 \
            + '.' + select_ext(d['media_type'])
    # 「らじる★らじる」なら
    elif d['radio_type'] == 'らじる★らじる 聴き逃しサービス':
        tmp1 = d['radio_type'] + '/' + d['title']
        tmp3 = d['title'] + '_' + d['program_title'] \
            + '_' + d['delivery_date']
        tmp2 = '[' + d['radio_type'] + ']' \
            + tmp3 \
            + '.' + select_ext(d['media_type'])
    else:
        tmp1 = '録音'
        tmp2 = 'output.m4a'
        tmp3 = 'output'
    return [tmp1, tmp2, tmp3]

# 'y/m'を'yyyymmdd'へ変換する。
def conv_date(str):
    try:
        # 今の'y/m/d'(文字列)
        date_slash = f"{datetime.today().year}/{str}"
        # 文字列をdatetimeに変換
        dt = datetime.strptime(date_slash, '%Y/%m/%d')
        # '%Y%m%d'形式に変換
        return dt.strftime('%Y%m%d')
    except ValueError:
        return '00000000'
