from django.http import HttpRequest
from django.shortcuts import redirect, render

waiting_list: list[dict[str, str]] = []


def welcome(request: HttpRequest):
    if request.method == "POST":
        name = request.POST.get("name")
        if not name:
            request.session["errors"] = ["You need to set your name first."]
            return redirect("/error")
        response = redirect("/")
        response.set_cookie("name", name)
        return response

    return render(request, "pooque/welcome.html")


def index(request: HttpRequest):
    if request.method == "POST":
        name = request.COOKIES.get("name")
        action = request.POST.get("action")

        if not name or not action:
            request.session["errors"] = ["We can't find your name or action."]
            return redirect("/error")

        waiting_list.append({"name": name, "action": action})

        return redirect("/")

    is_already_joined = any(
        person
        for person in waiting_list
        if person["name"] == request.COOKIES.get("name")
    )
    return render(
        request,
        "pooque/index.html",
        {"waiting_list": waiting_list, "is_already_joined": is_already_joined},
    )


def done(request: HttpRequest):
    global waiting_list
    new_waiting_list = [
        person
        for person in waiting_list
        if person["name"] != request.COOKIES.get("name")
    ]
    waiting_list = new_waiting_list
    return redirect("/")


def error(request: HttpRequest):
    errors = request.session.get("errors", [])
    request.session["errors"] = []
    return render(request, "pooque/error.html", {"errors": errors})
