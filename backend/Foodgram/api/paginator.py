from rest_framework.pagination import PageNumberPagination


class CustomPaginator(PageNumberPagination):
    """Paginator для определения количества записей на странице."""

    page_size_query_param = 'limit'
    page_size = 6