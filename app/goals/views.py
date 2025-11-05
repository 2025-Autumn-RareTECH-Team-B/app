from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .models import GoalsModel
from datetime import date
import random

User = get_user_model()


def goals_index(request, user_id=None):
    if not request.user.is_authenticated:
        return redirect("login")  # or settings.LOGIN_URL

    # /goals/   → 自分の一覧
    # /goals/1/ → 指定ユーザーの一覧
    target_user = request.user if user_id is None else get_object_or_404(User, pk=user_id)

    # ここで target_user のゴールを取得してテンプレへ
    ctx = {
        "profile_user": target_user,
        "message": random.choice([
        "お疲れさまです🌙",
        "コツコツ進めましょう🐰",
        "頑張っててえらいよ✨",
        "できることから、ひとつずつ。",
        ])
        }
     # 今の状態ではただ年齢の昇順に全部のgoalsを受け取ってるだけ
    goals = GoalsModel.objects.filter(user=request.user).order_by("limit_age")
    birthday = request.user.birthday

    # 計算結果を各goalに紐づけてcontextに渡す
    # goals_with_ageに空の配列を設定
    goals_with_age = []
    for goal in goals:
        limit_age = goal.limit_age
        # limit_ageの満年齢を計算
        future_age = limit_age.year - birthday.year - ((limit_age.month, limit_age.day) < (birthday.month, birthday.day))
        # 表示用の月（例: "4月"）
        future_month = f"{limit_age.month}月"
        # 配列に代入
        goals_with_age.append({
            "id": goal.id,
            "title": goal.title,
            "limit_age": goal.limit_age,
            "future_age": future_age,
            "future_month": future_month,
            "is_done": goal.is_done,
        })
    return render(request, "goals/home.html", {"goals": goals_with_age,"message": ctx["message"]})


def goals_create(request):
    # ---- GET(最初の表示) ----
    if request.method == "GET":
        return render(request, 'goals/goal_create.html')
    # ---- POST（長期目標入力）----
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        limit_age_str = request.POST.get("limit_age")  # HTMLのinput type="date" で受け取る
        ctx = {"title": title, "limit_age_str": limit_age_str}
        # ---- 空欄チェック ----
        if not title:
            messages.error(request, "タイトルは必須です。")
            return render(request, "goals/goal_create.html", ctx)
        # ---- 文字数制限 ----
        if len(title) > 128:
            messages.error(request, "タイトルは128文字以内にしてください。")
            return render(request, "goals/goal_create.html", ctx)
        # ---- 期限の空欄チェック ----
        if not limit_age_str:
            messages.error(request, "期限を必ず設定してください。")
            return render(request, "goals/goal_create.html", ctx)
        # ---- 期限の形式チェック ----
        if limit_age_str:
            try:
                limit_age = datetime.strptime(limit_age_str, "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, "日付の形式が正しくありません。")
                return render(request, "goals/goal_create.html", ctx)
        # ---- 過去は設定できない ----
        today = timezone.localtime().date()
        if limit_age < today:
            messages.error(request, "過去の日付は選択できません。")
            return render(request, "goals/goal_create.html", ctx)

        # バリデーションOKなら保存
        goal = GoalsModel.objects.create(
            user=request.user,
            title=title,
            limit_age=limit_age,
        )
        messages.success(request, "目標を登録しました！")
        return redirect("goals:home")
    
    
def goal_edit(request, goal_id):
    goal = get_object_or_404(GoalsModel, id=goal_id, user=request.user)
    today = timezone.localdate()

    # ---- GET（最初の表示） ----
    if request.method == "GET":
       
        # CBに保存されているものを表示
        ctx = {"goal": goal, "title": goal.title, "limit_date": goal.limit_age.isoformat(),}
        return render(request, "goals/goal_edit.html", ctx)
		
	# ---- POST（送信されたとき） ----
    # strip() = 前後の空白スペース・改行を消す
    title = request.POST.get("title", "").strip()
    limit_date_str = request.POST.get("limit_date", "").strip()
    
    ctx = {"goal": goal, "title": title, "limit_date": limit_date_str}
    
    # ---- 空欄チェック ----
    if not title or not limit_date_str:
        messages.error(request, "タイトルと期限を入力してください")
        return render(request, "goals/goal_edit.html", ctx)

    # ---- 日付形式チェック ----
    try:
        limit_date = date.fromisoformat(limit_date_str)
    except ValueError:
        messages.error(request, "期限の日付形式が正しくありません。")
        return render(request, "goals/goal_edit.html", ctx)

    #（今日より過去の日付はだめ）
    if limit_date < today:
        messages.error(request, "今日以降の日付を選んでください")
        return render(request, "goals/goal_edit.html", ctx)

    # userの誕生日から期限日を設定
    birthday = request.user.birthday
    age_at_limit = (
    limit_date.year - birthday.year
    - ((limit_date.month, limit_date.day) < (birthday.month, birthday.day))
    )


    # 18歳以上80歳未満
    if not (18 <= age_at_limit <= 80):
        messages.error(request, "期限日に18〜80歳の範囲になるよう設定してください。")
        return render(request, "goals/goal_edit.html", ctx)

    # ---- 保存 ----
    goal.title = title
    goal.limit_age = limit_date
    goal.save()


    messages.success(request, "長期目標を更新しました")
    return redirect("goals:home")    
				
				
def goal_delete(request, goal_id):
    # goal取得
    goal = get_object_or_404(GoalsModel, id=goal_id, user=request.user)

		#---- POST（送信されたとき） ----
    if request.method == "POST":
        goal.delete()
        messages.success(request, "長期目標を削除しました。")
        return redirect("goals:home")

    # ---- GET ----
    return render(request, "goals/goal_delete.html", {"goal": goal})
    
