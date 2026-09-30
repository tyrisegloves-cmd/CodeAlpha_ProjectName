from django.contrib.auth import get_user_model
from django.db.models import Count

def sidebar(request):
    if not request.user.is_authenticated:
        return {}
    skip = set(request.user.following.values_list("following_id", flat=True)) | {request.user.id}
    users = get_user_model().objects.exclude(id__in=skip).annotate(nf=Count("followers")).order_by("-nf", "username")[:4]
    return {"suggestions": users}
