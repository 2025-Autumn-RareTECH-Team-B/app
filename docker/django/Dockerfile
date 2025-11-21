#pythonのイメージを指定
FROM python:3.13
#オプション
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1
RUN mkdir /code
#コンテナのワークディレクトリを/codeに指定
WORKDIR /code
#ローカルのrequirements.txtをコンテナの/appフォルダ直下に置く
COPY requirements.txt ./
#pipコマンドとツールを最新にし、txtファイル内のパッケージをpipインストール
RUN pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install -r requirements.txt
#ソースコードをコンテナにコピー
COPY ./app /code/app
COPY ./manage.py /code/manage.py
COPY ./templates /code/templates
COPY ./static /code/static
#静的ファイルをまとめる
#RUN python manage.py collectstatic --noinput || true
#Gunicorn起動コマンド
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn app.wsgi:application --chdir /code/app --bind 0.0.0.0:8000 --access-logfile /var/log/app/gunicorn.log --error-logfile /var/log/app/gunicorn.log"]