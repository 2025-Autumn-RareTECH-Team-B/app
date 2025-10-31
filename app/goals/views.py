from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

def goals_index(request, user_id=None):
    if not request.user.is_authenticated:
        return redirect("login")  # or settings.LOGIN_URL

    # /goals/   → 自分の一覧
    # /goals/1/ → 指定ユーザーの一覧
    target_user = request.user if user_id is None else get_object_or_404(User, pk=user_id)

    # ここで target_user のゴールを取得してテンプレへ
    ctx = {"profile_user": target_user}
    return render(request, "home.html", ctx)


def goals_create(request):
    return render(request, 'goal_create.html')
    