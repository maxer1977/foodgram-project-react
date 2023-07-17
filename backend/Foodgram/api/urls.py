from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TagsViewSet, IngridientsViewSet, RecieptsViewSet, IngridientsListViewSet, CustomUserViewSet #, SubscriptionsViewSet

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngridientsViewSet, basename='ingredients')
router.register('recipes', RecieptsViewSet, basename='recipes')
router.register('ingredientslist', IngridientsListViewSet, basename='ingredientslist')
router.register('users', CustomUserViewSet, basename='users_subscriptions')
# router.register(r'users/(?P<id>\d+)', CustomUserViewSet, basename='users_subscribe')
# router_v1.register(
#     r'titles/(?P<title_id>\d+)/reviews',
#     ReviewsViewSet,
#     basename='reviews'
# )
# router_v1.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentsViewSet,
#     basename='comments'
# )

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # path('user/subscriptions/', SubscriptionsViewSet.as_view({'get': 'list'}), name='subscription-list'),
    # path('users/<int:pk>/subscribe/', SubscriptionsViewSet.as_view({'post': 'create', 'delete': 'destroy'}), name='subscription-create'),
]
