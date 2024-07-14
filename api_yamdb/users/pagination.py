from rest_framework.pagination import PageNumberPagination

from reviews.constants import MAX_PAGE_SIZE, PAGE_SIZE, PAGE_SIZE_QUERY_PARAM


class UserPagination(PageNumberPagination):
    """Класс пагинации для UserViewSet."""

    page_size = PAGE_SIZE
    page_size_query_param = PAGE_SIZE_QUERY_PARAM
    max_page_size = MAX_PAGE_SIZE
