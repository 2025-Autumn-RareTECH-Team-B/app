from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from datetime import date, timedelta
import re
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


# Djangoが使っているUserモデルを取得
User = get_user_model()

#season_img_for_monthという関数にmonth: int（整数）を文字列で返す
def season_img_for_month(month: int) -> str:
    return f"img/season/{month:02}.png"

# -----------------------
#   ログイン画面
# -----------------------
@require_http_methods(["GET", "POST"])
def login(request):

    # ---- GET（最初の表示） ----
    if request.method == "GET":
        return render(request, "login.html")

    # ---- POST（ログイン送信） ----
    email = request.POST.get("email", "").strip().lower()
    password = request.POST.get("password", "")

    # ---- 空欄チェック ----
    if not email or not password:
        messages.error(request, "メールアドレスとパスワードを入力してください")
        return render(request, "login.html", {"email": email})

    # ---- 認証 ----
    user = authenticate(request, email=email, password=password)

    # ---- 失敗 ----
    if user is None:
        messages.error(request, "メールアドレスまたはパスワードが正しくありません。")
        return render(request, "login.html", {"email": email})

    # ---- 成功（ログイン）----
    auth_login(request, user)
    return redirect("goals:home", user_id=request.user.id)

# -----------------------
#   サインアップ（新規登録）
# -----------------------
@require_http_methods(["GET", "POST"])
def signup(request):

    # 今月の画像を表示
    month_now=timezone.localdate().month
    season_img = season_img_for_month(month_now)

    # ---- GET（最初の表示） ----
    if request.method == "GET":
       return render(request, "signup.html",{"season_img":season_img})

    # ---- POST（送信されたとき） ----

    # strip() = 前後の空白スペース・改行を消す
    # lower() = アルファベットをすべて小文字に変換する
    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip().lower()

    # 送信されたパスワード
    password1 = request.POST.get("password1", "")
    password2 = request.POST.get("password2", "")

    # 生の誕生日文字列（例: '2024-10-10'）
    b_raw = request.POST.get("birthday", "")

    # メールアドレスの正規表現（pattern）
    # ユーザー名部分：英数字と「_ . + -」を1文字以上
    # ＠
    # ドメイン名部分：英数字と「-」を1文字以上
    # . （ドット）
    # ドメイン後半：英数字「-」「.」を1文字以上
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # エラーになって再表示した時のために入力内容を保持
    ctx = {"name": name, "email": email, "birthday": b_raw, "season_img": season_img}

    # ---- 空欄チェック ----
    if not name or not email or not password1 or not password2:
        messages.error(request, "空のフォームがあります")
        return render(request, "signup.html", ctx)

    # ---- パスワード一致チェック ----
    if password1 != password2:
        messages.error(request, "パスワードは一致しません")
        return render(request, "signup.html", ctx)

    # ---- メールアドレス形式チェック ----
    if not re.match(pattern, email):
        messages.error(request, "メールアドレスの形式になっていません")
        return render(request, "signup.html", ctx)

    # ---- メールアドレス重複チェック ----
    if User.objects.filter(email=email).exists():
        messages.error(request, "このメールアドレスは登録済みです")
        return render(request, "signup.html", ctx)

    # ---- 誕生日のパース処理 ----
    # データベースに保存するときの birthday の初期値を None にする
    # （未入力の場合はこれをそのまま保存する）
    birthday = None

    # ユーザーが誕生日を選択している場合（=b_raw が "" ではない場合）
    # もしユーザーが誕生日を入力していた場合だけ処理する
    if b_raw:
        try:
            # 文字列 → date型に変換
            birthday = date.fromisoformat(b_raw)

            # 今日の日付（基準）
            today = timezone.localdate()

            # 許可する範囲
            min_date = today - timedelta(days=365 * 120)  # 120歳まで
            max_date = today  # 未来日はNG

            # ---- 範囲チェック ----
            if birthday > max_date:
                messages.error(request, "未来の日付は選択できません。")
                return render(request, "signup.html", ctx)

            if birthday < min_date:
                messages.error(request, "誕生日が古すぎます（120歳以上は登録できません）。")
                return render(request, "signup.html", ctx)

        except ValueError:
            messages.error(request, "誕生日の形式を正しく選択してください。")
            return render(request, "signup.html", ctx)

    else:
        # 未入力の場合は None のままでOK
        birthday = None

    # --------------------------
    #      ユーザー新規作成
    # --------------------------
    new_user = User(
        username=name,
        email=email,
    )

    # Userモデルに birthday フィールドがある場合のみセットする
    if hasattr(new_user, "birthday"):
        new_user.birthday = birthday

    # パスワードをハッシュ化して保存する
    new_user.set_password(password1)

    # データベースに登録！
    new_user.save()

    # 登録完了 → ログイン画面へリダイレクト
    messages.success(request, "登録が完了しました。ログインしてください。")
    return redirect("login")

# -----------------------
#   ログアウト画面
# -----------------------

@require_http_methods(["POST"])
def logout(request):
	auth_logout(request)
	messages.success(request, "ログアウトしました。")
	return redirect('login')
  

def profile_edit(request):
    return render(request, 'profile_edit.html')
