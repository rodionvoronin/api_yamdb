# from django.shortcuts import get_object_or_404
# from rest_framework.filters import SearchFilter
# from rest_framework.mixins import CreateModelMixin, ListModelMixin
# from rest_framework.pagination import LimitOffsetPagination
# from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import (
    GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
)

# from api.permissions import OwnerOrReadOnly
from api.serializers import TitleSerializer, ReviewSerializer

from reviews.models import Title, Review


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
#     permission_classes = (OwnerOrReadOnly,)
#     pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer