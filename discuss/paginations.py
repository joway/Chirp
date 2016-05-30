from rest_framework import pagination


class DiscussPagination(pagination.PageNumberPagination):
    ordering = "-create_at"
    page_size_query_param = 'page_size'
    page_size = 10
