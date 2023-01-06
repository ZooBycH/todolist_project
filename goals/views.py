from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters, generics
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal, GoalComment, Board
from goals import serializers
from goals.permissions import BoardPermissions, GoalCategoryPermissions, GoalPermissions, GoalCommentPermissions


class GoalCategoryCreateView(generics.CreateAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated, GoalCategoryPermissions]
    serializer_class = serializers.GoalCategoryCreateSerializer


class GoalCategoryListView(generics.ListAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["board"]
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title']

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user, is_deleted=False
        )


class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = serializers.GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated, GoalCategoryPermissions]

    def get_queryset(self):
        return GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class GoalCreateView(generics.CreateAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated, GoalPermissions]
    serializer_class = serializers.GoalCreateSerializer


class GoalListView(generics.ListAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ['due_date', 'priority']
    ordering = ['priority', 'due_date']
    search_fields = ['title']

    def get_queryset(self):
        return Goal.objects.filter(category__board__participants__user=self.request.user).exclude(
            status=Goal.Status.archived)


class GoalView(generics.RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = serializers.GoalSerializer
    permission_classes = [permissions.IsAuthenticated, GoalPermissions]

    def get_queryset(self):
        return Goal.objects.filter(category__board__participants__user=self.request.user)

    def perform_destroy(self, instance):
        instance.status = Goal.Status.archived
        instance.save()
        return instance


class GoalCommentCreateView(generics.CreateAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated, GoalCommentPermissions]
    serializer_class = serializers.GoalCommentCreateSerializer


class GoalCommentListView(generics.ListAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.GoalCommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
    ]
    filterset_fields = ['goal']
    ordering = ['-created']

    def get_queryset(self):
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)


class GoalCommentView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = serializers.GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated, GoalCommentPermissions]

    def get_queryset(self):
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)


class BoardCreateView(generics.CreateAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.BoardCreateSerializer


class BoardView(generics.RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]
    serializer_class = serializers.BoardSerializer

    def get_queryset(self):
        # Обратите внимание на фильтрацию – она идет через participants
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):
        # При удалении доски помечаем ее как is_deleted,
        # «удаляем» категории, обновляем статус целей
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance


class BoardListView(generics.ListAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]
    serializer_class = serializers.BoardListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['title']

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)
