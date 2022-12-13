from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, permissions

from goals.models.comments import GoalComment
from goals.permissions import CommentPermissions
from goals.serislizers.comments import GoalCommentSerializer, GoalCommentCreateSerializer


class GoalCommentCreateView(generics.CreateAPIView):
    model = GoalComment
    permission_classes = [
        permissions.IsAuthenticated,
        CommentPermissions
    ]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(generics.ListAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_fields = ['goal']
    ordering = ['-id']

    def get_queryset(self):
        return GoalComment.objects.filter(
            goal__category__board__participants__user=self.request.user
        )


class GoalCommentView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        CommentPermissions
    ]

    def get_queryset(self):
        return GoalComment.objects.filter(
            goal__category__board__participants__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance
