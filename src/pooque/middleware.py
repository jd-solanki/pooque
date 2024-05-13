from django.http import HttpRequest
from django.shortcuts import redirect

public_pages = [
    ("/favicon.ico", ["GET"]),
    ("/welcome", ["GET", "POST"]),
]


def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request: HttpRequest):
        print("Middleware called...", request.path, request.method)
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = get_response(request)

        if any(
            [
                request.path.startswith(path) and request.method in methods
                for path, methods in public_pages
            ]
        ):
            print("public route")
            return response

        print("Checking cookie...", request.COOKIES.get("name"))
        if not request.COOKIES.get("name"):
            print("Redirecting to /welcome")
            return redirect("/welcome")

        return response

    return middleware
