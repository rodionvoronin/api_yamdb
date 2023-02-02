from django.shortcuts import get_object_or_404
# from rest_framework.filters import SearchFilter
# from rest_framework.mixins import CreateModelMixin, ListModelMixin
# from rest_framework.pagination import LimitOffsetPagination
# from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import (
    GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
)

# from api.permissions import OwnerOrReadOnly
from api.serializers import TitleSerializer, CommentSerializer

from reviews.models import Title, Review


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
#     permission_classes = (OwnerOrReadOnly,)
#     pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
#    permission_classes = (OwnerOrReadOnly,)

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)