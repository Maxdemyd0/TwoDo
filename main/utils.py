from django.http import HttpRequest

def is_admin_mode(request: HttpRequest):
    return request.user.is_staff and request.session.get("admin_mode", False)