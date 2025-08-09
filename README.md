# rec_rajiru: らじる★らじる 聴き逃し番組ダウンローダー

## 概要

`rec_rajiru` は、NHKのラジオ聞き逃し配信サービス「らじる★らじる」の番組を簡単なコマンド操作でダウンロードし、ローカルに保存するためのコマンドラインツールです。

お気に入りのラジオ番組をいつでも好きな時に聴けるように、あなたの手元に音声ファイルとして保存します。

## 主な機能

-   **簡単な操作:** 番組を特定するための数個のIDをコマンドラインで指定するだけで、手軽に録音が開始できます。
-   **自動ファイル名生成:** `[ラジオ局名]番組名_エピソード名_配信日.m4a` のように、整理しやすく分かりやすいファイル名を自動で生成します。
-   **豊富なメタデータ:** ダウンロードした音声ファイルには、番組タイトル、アルバム名（ラジオ局名）、アーティスト名（パーソナリティ名）、番組のサブタイトルなどがメタデータとして自動的に埋め込まれます。これにより、音楽プレイヤーなどで管理がしやすくなります。
-   **柔軟な保存先:** ダウンロードしたファイルの保存先を自由に指定できます。
-   **自動化に対応:** Linuxの`cron`と組み合わせることで、毎週放送される番組などを定期的に自動でダウンロードする仕組みを簡単に構築できます。

## 動作環境

-   Python 3.x
-   Linux (cronによる自動化を想定) / Windows / macOS

## 必要な外部ツール

このツールは、内部で以下のコマンドラインツールを利用しています。あらかじめインストールしておいてください。

-   **GStreamer:** 音声ストリームを録音するために必要です。
-   **ffmpeg:** 音声ファイルにメタデータを付与するために必要です。
-   **curl:** GStreamerがHTTPストリームにアクセスするために利用します。

## インストール手順

1.  **リポジトリをクローン**

    まず、このリポジトリをローカルマシンに複製します。

    ```bash
    git clone https://github.com/qack-dev/rec_rajiru.git
    ```
    ```bash
    cd rec_rajiru
    ```

2.  **Python仮想環境の構築**

    プロジェクト用の独立したPython環境（仮想環境）を作成し、有効化します。

    ```bash
    python -m venv env
    ```

    -   **Windowsの場合:**
        ```bash
        .\env\Scripts\activate
        ```
    -   **Linux / macOS の場合:**
        ```bash
        source env/bin/activate
        ```

3.  **依存関係のインストール**

    必要なPythonパッケージをインストールします。

    ```bash
    pip install -r requirements.txt
    ```

## 基本的な使い方

番組が保存されるフォルダを、正確な番組名で、手動かコマンドで事前に作成しておきます。
-   **例）Linuxの場合:**
    ```bash
    sudo mkdir -p '/mnt/ssd/share/radio/らじる★らじる 聴き逃しサービス/なにしったのや〜？'
    ```

仮想環境に入ったまま、以下のコマンド形式でスクリプトを実行します。

```bash
python -B rec_rajiru.py <series_site_id> <corner_site_id> <artist_name> <save_path>
```

-   `<series_site_id>`: 番組のサイトID
-   `<corner_site_id>`: コーナーサイトID（基本的には01を入力）
-   `<artist_name>`: パーソナリティ名（メタデータ用）
-   `<save_path>`: 保存先の絶対パス

<series_site_id>は、 [https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/corners/new_arrivals](https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/corners/new_arrivals) から、番組タイトルで検索し、特定することができます。
番組タイトルが書いてあるところと同じ`{}`内（Pythonで言うところの辞書内）を探してください。

**実行例:**

```bash
python -B rec_rajiru.py 8Q8XG537NW 01 "岩田 マキ" "/mnt/ssd/share/radio"
```

仮想環境から抜けるコマンドは以下となります。

```bash
deactivate
```

## 高度な使い方: cronによる自動化 (Linux)

Linux環境では、`cron` を利用して番組のダウンロードを定期的に自動化することができます。これにより、毎週・毎日放送される番組を自動で録り溜めておくことが可能になります。

1.  `crontab` を編集用に開きます。

    ```bash
    sudo nano /etc/crontab
    ```

2.  ファイルの末尾に、以下のような形式で実行コマンドを追記します。

    ```bash
    # 毎週日曜日の早朝4:00に番組をダウンロードする例
    0 4 * * 0   your_user /path/to/your/rec_rajiru/env/bin/python -B /path/to/your/rec_rajiru/rec_rajiru.py G918NWNZ2V 01 "岩田 マキ" "/mnt/ssd/share/radio"
    ```

    **【重要】**
    -   `your_user` は、あなたの実際のユーザー名に置き換えてください。
    -   `/path/to/your/rec_rajiru/` の部分は、あなたが `rec_rajiru` をクローンした実際の絶対パスに必ず置き換えてください。

## ライセンス

このプロジェクトは [MIT License](LICENSE) のもとで公開されています。

## 免責事項

-   このツールは、個人的な利用の範囲内で使用してください。
-   ダウンロードしたコンテンツの取り扱いについては、著作権法を遵守してください。
-   このツールの利用によって生じたいかなる損害についても、開発者は一切の責任を負いません。
