### プロジェクトタイトル  
***
Habi(ハビ)
### ロゴ画像  
<img width="350" height="300" alt="image" src="https://github.com/user-attachments/assets/ce620792-ec90-40a7-9ab6-8ef76b6dfe9d" />  

### プロジェクト概要
***
**Habi**は、人生の長期的な目標や夢を小さなステップに分け、  
日常の中で「小さな達成感」を積み重ねながら目標を実現するための**人生設計アプリ**です。  
忙しい日々の中でも、自分のペースで目標や夢に近づける設計になっています。
### 必要条件
***
- Python 3.10 以上  
- Django 5.2  
- MySQL 8.0 以上
- AWS EC2 環境（Linux）
### 開発環境構築手順  
***仮想環境（venv）を使用する場合***
***
###### リポジトリをクローン
`$ git clone https://github.com/2025-Autumn-RareTECH-Team-B/app.git`

###### ディレクトリへ移動
`$ cd app`

###### 仮想環境を作成・有効化
`$ python -m venv venv`  
`$ source venv/bin/activate`

###### 依存パッケージをインストール
`$ pip install -r requirements.txt`

###### DBマイグレーション
`$ python manage.py migrate`

###### 開発サーバー起動
`$ python manage.py runserver`  

もしくは、Docker を使用して環境を構築しても問題ありません。
### 環境変数設定（.env）
***
Djangoで使用する環境変数を、プロジェクト直下に `.env` ファイルとして作成してください。
###### Django設定
`SECRET_KEY=django-insecure-your-secret-key`

###### DB設定
`DB_NAME=app`  
`DB_USER=testuser`  
`DB_PASSWORD=testuser`

>※ MySQLをDockerで構築する場合は、
>以下の変数を docker-compose.yml 内で指定してください。
>###### MySQL設定
>`MYSQL_ROOT_PASSWORD=root`  
>`MYSQL_DATABASE=app`  
>`MYSQL_USER=testuser`  
>`MYSQL_PASSWORD=testuser`  