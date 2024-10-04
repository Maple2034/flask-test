from pathlib import Path
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

#SQLAlchemyをインスタンス化
db = SQLAlchemy()

csrf = CSRFProtect()

#create_app関数を作成
def create_app():
  #flaskインスタンス生成
  app = Flask(__name__)
  #アプリのコンフィグを設定
  app.config.from_mapping(
    SECRET_KEY="2AZSMss3p5QPbcY2hBsJ",
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    #SQLのコンソールログに出力する設定
    SQLALCHEMY_ECHO=True,
    WTF_CSRF_SECRET_KEY="AuwzyszU5sugKN7KZs6f",
  )

  #SQLAlchemyとアプリを連携
  db.init_app(app)
  #Migrateと”
  Migrate(app, db)

  csrf.init_app(app)


  #crudパッケージからviwesをimport
  from apps.crud import views as crud_views

  #register_blueprintを使いviewsｍｐcrudをアプリへ登録
  app.register_blueprint(crud_views.crud, url_prefix="/crud")

  return app
