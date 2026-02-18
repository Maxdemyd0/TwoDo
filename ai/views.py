from django.http import JsonResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .services import generate_ai_response

@login_required
def assistant_page(request: HttpRequest):
    user_message = None
    ai_response = None

    if request.method == "POST":
        user_message = request.POST.get("message")
        ai_response = generate_ai_response(user_message)

    return render(request, "ai/assistant.html", {
        "user_message": user_message,
        "ai_response": ai_response,
    })

@require_POST
@login_required
def assistant_api(request: HttpRequest) -> JsonResponse:
    message = request.POST.get("message")
    reply = generate_ai_response(message)

    return JsonResponse({"reply": reply})