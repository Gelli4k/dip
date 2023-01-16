from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, permissions
from rest_framework.pagination import LimitOffsetPagination

from goals.models.goal import Goal
from goals.permissions import GoalPermissions
from goals.serislizers.goal import GoalCreateSerializer, GoalSerializer
from goals.views.filters import GoalDateFilter


class GoalCreateView(generics.CreateAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalListView(generics.ListAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination
    serializer_class = GoalSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ['-priority', 'due_date']
    ordering = ['-priority', 'due_date']
    search_fields = ['title']

    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user=self.request.user
        ).exclude(status=Goal.Status.archived
                  )


class GoalView(generics.RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        GoalPermissions
    ]

    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.status = Goal.Status.archived
        instance.save()
        return instance
