#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# らじるらじるをGStreamerで録音

from ast import arg
import sys
import package1

RAJIRU_JSON_URL = 'https://www.nhk.or.jp/radio-api/app/v1/web/ondemand'
RADIO_TYPE = 'らじる★らじる 聴き逃しサービス'

# GStreamerで録音するコマンド(list)を作成
def make_cmd_gst(dict):
    return [
        ['gst-launch-1.0','curlhttpsrc'],
        'location=' + dict['stream_url'],
        [
            '!','hlsdemux',
            '!','decodebin',
            '!','audioconvert',
            '!','avenc_aac'
        ],
        'bitrate=' + dict['bitrate'],
        [
            '!','mp4mux',
            '!','filesink'
        ],
        'location=' + dict['filename']
    ]

# ffmpegでmetadataを追加するコマンド(list)を作成
def make_cmd_ffmpeg(dict):
    # '-metadataの後は、
    # title=タイトル
    # or album=アルバム
    # or artist=アーティスト
    # or comment=コメント
    # or ...
    return [
        'ffmpeg','-i',
        dict['filename'],
        '-metadata',
        'title=' + dict['meta_title'],
        '-metadata',
        'album=' + dict['meta_album'],
        '-metadata',
        'artist=' + dict['meta_artist'],
        '-metadata',
        'comment=' + dict['meta_comment'],
        '-c', 'copy',
        'output.' + package1.module1.select_ext(dict['media_type'])
    ]

# mvでファイルを移動するコマンド(list)を作成
def make_cmd_mv(dict):
    return [
        'mv',
        'output.' + package1.module1.select_ext(dict['media_type']),
        dict['filename']
    ]

# 'https://[^"]+\.m3u8'を探す。
def get_rajiru_stream_url(items):
    if(items['stream_url'] is None):
        return ''
    # 「.m3u8」で終わっていたら
    elif(items['stream_url'].endswith('.m3u8')):
       return items['program_title'], \
           items['onair_date'], \
           items['stream_url'], \
           items['program_sub_title']

# '4月4日(金)午後0:20放送'から'4/4'へ変換
def conv_date_rajiru(str):
    index = str.find('日')
    s = str[0:index]
    return s.replace('月','/')

def main():
    # args = ('','G918NWNZ2V','01','岩田 マキ','/mnt/ssd/share/radio')
    args = sys.argv

    # json全文
    data = package1.module1.get_json(
        RAJIRU_JSON_URL
        + '/series?site_id=' + args[1]
        + '&corner_site_id=' + args[2]
    )

    SAVE_PATH = args[4]

    # data['title']の"?"を"？"へ変更
    data['title'] = data['title'].replace("?","？")

    # jsonから抽出
    t = get_rajiru_stream_url(data['episodes'][0])

    # ファイル名に必要な要素の辞書
    filename_dict = {
        'radio_type':RADIO_TYPE,
        'title':data['title'],
        'program_title':t[0],
        'delivery_date': \
            package1.module1.conv_date( \
                conv_date_rajiru(t[1]) \
            ),
        'media_type':'sound'
    }

    # 録音用に必要な要素の辞書
    t2 = package1.module1.make_filename_list(filename_dict)

    # t2[1]の"?"を"？"へ変更
    t2[1] = t2[1].replace("?","？")

    rec_dict = {
        'stream_url':t[2],
        'filename':t2[1],
        'meta_title':t2[2],
        'meta_album':RADIO_TYPE,
        'meta_artist':args[3],
        'meta_comment':t[3],
        'bitrate':'46000',
        'media_type':filename_dict['media_type']
    }

    # 録音
    package1.module1.run_cmd( \
        package1.module1.conv_list(make_cmd_gst(rec_dict)), \
        SAVE_PATH + '/' + t2[0] \
    )
    package1.module1.run_cmd( \
        package1.module1.conv_list(make_cmd_ffmpeg(rec_dict)), \
        SAVE_PATH + '/' + t2[0] \
    )
    package1.module1.run_cmd( \
        package1.module1.conv_list(make_cmd_mv(rec_dict)), \
        SAVE_PATH + '/' + t2[0] \
    )

if __name__ == "__main__":
    main()
