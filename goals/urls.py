from django.urls import path

from goals.views import goal, category, comments, boards

urlpatterns = [
    path('goal/create', goal.GoalCreateView.as_view(), name='goal_create'),
    path('goal/list', goal.GoalListView.as_view(), name='goal_list'),
    path('goal/<pk>', goal.GoalView.as_view(), name='goal_pk'),
    path('goal_category/create', category.GoalCategoryCreateView.as_view(), name='category_create'),
    path('goal_category/list', category.GoalCategoryListView.as_view(), name='category_list'),
    path('goal_category/<pk>', category.GoalCategoryView.as_view(), name='category_pk'),
    path('goal_comment/create', comments.GoalCommentCreateView.as_view(), name='comment_create'),
    path('goal_comment/list', comments.GoalCommentListView.as_view(), name='comment_list'),
    path('goal_comment/<pk>', comments.GoalCommentView.as_view(), name='comment_pk'),
    path('board/create', boards.BoardCreateView.as_view(), name='board_create'),
    path('board/list', boards.BoardListView.as_view(), name='board_list'),
    path('board/<pk>', boards.BoardView.as_view(), name='board_pk'),
]


