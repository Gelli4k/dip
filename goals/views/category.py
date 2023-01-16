from rest_framework import generics, filters, permissions
from rest_framework.pagination import LimitOffsetPagination

from goals.models.category import GoalCategory
from goals.permissions import GoalCategoryPermissions
from goals.serislizers.category import GoalCategoryCreateSerializer, GoalCategorySerializer


class GoalCategoryCreateView(generics.CreateAPIView):
    """ Создание категории для цели"""
    model = GoalCategory
    permission_classes = [
        permissions.IsAuthenticated,
        GoalCategoryPermissions
    ]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(generics.ListAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title', 'board']

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user,
            is_deleted=False,
        )


class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [
        permissions.IsAuthenticated,
        GoalCategoryPermissions
    ]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user,
            is_deleted=False,
        )

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance
