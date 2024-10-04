from flask import (
    Flask, current_app, g, render_template, url_for, request,
    redirect, flash, make_response, session)
from flask_debugtoolbar import DebugToolbarExtension
from email_validator import validate_email, EmailNotValidError
from flask_mail import Mail, Message
import logging
import os

app = Flask(__name__)
#SECRET_KEYを追加
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"
#ログレベルを設定
app.logger.setLevel(logging.DEBUG)
#リダイレクトを中断しないようにする(デフォルトはTrue)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
#DebugToolbarExtensionにアプリをセットする
toolbar = DebugToolbarExtension(app)

#Mailクラスのコンフィグを設定する
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_POST"] = os.environ.get("MAIL_POST")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

#flask-mail拡張を登録
mail = Mail(app)

@app.route("/")
def index():
    return "Hello, Flaskbook!"

#メゾットとエンドポイント設定、nameの文字を表示
@app.route("/hello/<name>",
           methods=["GET","POST"],
           endpoint="hello-endpoint")
def hello(name):
    return f"hello,{name}!"

#<name>の文字をテンプレートを用いて表示
@app.route("/name/<name>")
def show_name(name):
    return render_template("index.html", name=name)

@app.route("/contact")
def contact():
    #レスポンスオブジェクトを取得
    response = make_response(render_template("contact.html"))

    #cookieを設定
    response.set_cookie("flaskbook key", "flaskbook value")

    #セッションを設定
    session["username"] = "kaede"
    return response
    return render_template("contact.html")

@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        #form属性でフォームの値を取得
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        #入力チェック
        is_valid = True

        if not username:
            flash("ユーザ名は必須です")
            is_valid = False
        
        if not email:
            flash("メールアドレスは必須です")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("メールアドレスの形式で入力してください")
            is_valid = False

        if not description:
            flash("問い合わせ内容は必須です")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))

        #メールを送る(最後)
        send_email(
            email,
            "問い合わせありがとうございました",
            "contact_mail",
            username=username,
    				description=description,
        )
        
        #問い合わせ完了エンドポイントへリダイレクト
        flash("問い合わせ内容はメールにて送信しました")
        return redirect(url_for("contact_complete"))

    return render_template("contact_complete.html")

def send_email(to, subject, template, **kwargs):
    """メールを送信する関数"""
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)

with app.test_request_context():
    # /
    print(url_for("index"))
    # /hello/world
    print(url_for("hello-endpoint", name="world"))
    # /name/kaede?page=1
    print(url_for("show_name", name="kaede", page="1"))

with app.test_request_context("/users?updated=true"):
    #trueが出力される
    print(request.args.get("updated"))