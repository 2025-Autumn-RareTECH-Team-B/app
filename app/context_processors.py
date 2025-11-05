from django.utils import timezone

def season_image(request):
    current_month = timezone.localtime().month
    return {"season_image": f"img/season/{current_month}.png"}
