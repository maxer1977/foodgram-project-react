from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CustomUserViewSet,
    IngridientsListViewSet,
    IngridientsViewSet,
    RecieptsViewSet,
    TagsViewSet,
)

app_name = "api"

router = DefaultRouter()
router.register("tags", TagsViewSet, basename="tags")
router.register("ingredients", IngridientsViewSet, basename="ingredients")
router.register("recipes", RecieptsViewSet, basename="recipes")
router.register("ingredientslist", IngridientsListViewSet, basename="ingredientslist")
router.register("users", CustomUserViewSet, basename="users_subscriptions")

urlpatterns = [
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
