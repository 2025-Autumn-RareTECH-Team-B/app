#pythonのイメージを指定
FROM python:3.13
#オプション
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir /code
#コンテナのワークディレクトリを/codeに指定
WORKDIR /code
#ローカルのrequirements.txtをコンテナの/codeフォルダ直下に置く
COPY requirements.txt /code/
#pipコマンドとツールを最新にし、txtファイル内のパッケージをpipインストール
RUN pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install -r requirements.txt
#ソースコードをコンテナにコピー
COPY . /code/

