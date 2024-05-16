from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models.functions import Lower
from .models import User, Movie, Checkout
import re

# Page rendering views
class HomePageView(View):
    def get(self, request):
        return render(request, "home.html")

class AccountPageView(View):
    def get(self, request):
        return render(request, "account.html")


class MoviePageView(View):
    def get(self, request):
        return render(request, "movie.html")


class RentPageView(View):
    def get(self, request):
        return render(request, "rent_return.html")


class UserManager(View):
    def get(self, request):
        email = request.GET.get("email")
        user = User.objects.filter(email=email).first()
        if not user:
            return JsonResponse({"error": "User not found"}, status=404)
        return JsonResponse({
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }, safe=False)

    def post(self, request):
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")

        if not first_name or not last_name:
            return JsonResponse({"error": "First name and last name are required"}, status=400)

        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_pattern, email):
            return JsonResponse({"error": "Invalid email format"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"}, status=400)

        user = User.objects.create(
            first_name=first_name, last_name=last_name, email=email
        )
        return JsonResponse({
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }, safe=False)

class RentalManager(View):
    def get(self, request):
        user_id = request.GET.get("user_id")
        movie_id = request.GET.get("movie_id")
        filters = {}
        if user_id:
            filters['user_id'] = user_id
        if movie_id:
            filters['movie_id'] = movie_id
        checkouts = Checkout.objects.filter(**filters).select_related("user", "movie").order_by("movie__title")

        result = [
            {
                "user_id": co.user.id,
                "email": co.user.email,
                "movie_id": co.movie.id,
                "title": co.movie.title,
                "checkout_date": co.date,
            }
            for co in checkouts
        ]
        return JsonResponse(result, safe=False)

    def post(self, request):
        action = request.POST.get("action")
        user_id = request.POST.get("user_id")
        movie_id = request.POST.get("movie_id")

        user = User.objects.filter(id=user_id).first()
        movie = Movie.objects.filter(id=movie_id).first()

        if not user or not movie:
            return JsonResponse({"error": "Invalid user or movie ID"}, status=400)

        if action == "rent":
            if movie.stock <= 0:
                return JsonResponse({"error": "No copies in stock"}, status=400)
            if Checkout.objects.filter(user=user, movie=movie).exists():
                return JsonResponse({"error": "Movie already checked out by this user"}, status=400)
            if Checkout.objects.filter(user=user).count() >= 3:
                return JsonResponse({"error": "User has reached maximum checkout limit"}, status=400)

            Checkout.objects.create(user=user, movie=movie)
            movie.stock -= 1
            movie.save()

        elif action == "return":
            checkout = Checkout.objects.filter(user=user, movie=movie).first()
            if not checkout:
                return JsonResponse({"error": "Movie not checked out by this user"}, status=400)

            movie.stock += 1
            checkout.delete()
            movie.save()

        checkouts = Checkout.objects.filter(user=user).select_related("user", "movie")
        result = [
            {
                "user_id": co.user.id,
                "email": co.user.email,
                "movie_id": co.movie.id,
                "title": co.movie.title,
                "checkout_date": co.date,
            }
            for co in checkouts
        ]
        return JsonResponse(result, safe=False)


class MovieManager(View):
    def get(self, request):
        movies = Movie.objects.annotate(lowercase_title=Lower("title")).order_by("lowercase_title")
        movie_list = [
            {
                "movie_id": movie.id,
                "title": movie.title,
                "stock": movie.stock,
                "checked_out": movie.checked_out,
            }
            for movie in movies
        ]
        return JsonResponse(movie_list, safe=False)

    def post(self, request):
        action = request.POST.get("action")
        if action == "new":
            title = request.POST.get("title").strip()
            if not title or Movie.objects.filter(title__iexact=title).exists():
                return JsonResponse({"error": "Invalid or existing movie title"}, status=400)
            movie = Movie.objects.create(title=title, stock=1, checked_out=0)

        elif action in ["add", "remove"]:
            movie_id = request.POST.get("movie_id")
            movie = Movie.objects.filter(id=movie_id).first()
            if not movie:
                return JsonResponse({"error": "Invalid movie ID"}, status=400)
            if action == "add":
                movie.stock += 1
            elif action == "remove":
                if movie.stock <= 0:
                    return JsonResponse({"error": "No copies left to remove"}, status=400)
                movie.stock -= 1
            movie.save()

        movies = Movie.objects.annotate(lowercase_title=Lower("title")).order_by("lowercase_title")
        movie_list = [
            {
                "movie_id": movie.id,
                "title": movie.title,
                "stock": movie.stock,
                "checked_out": movie.checked_out,
            }
            for movie in movies
        ]
        return JsonResponse(movie_list, safe=False)

