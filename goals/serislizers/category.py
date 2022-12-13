from rest_framework import serializers

from core.serializers import UserSerializer
from goals.models.boards import Board, BoardParticipant
from goals.models.category import GoalCategory


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'

    def validate_board(self, value: Board):
        if value.is_deleted:
            raise serializers.ValidationError('Not allowed in deleted category')
        if not BoardParticipant.objects.filter(
                board=value,
                role__in=[
                    BoardParticipant.Role.owner,
                    BoardParticipant.Role.writer,
                ],
                user=self.context['request'].user
        ).exists():
            raise serializers.ValidationError('You must be owner or writer')
        return value


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user', 'board')

        def update(self, instance, validated_data):
            board = validated_data.get('board')
            if instance.board.id != board:
                raise serializers.ValidationError('Cannot change board of category')
            return super().update(instance, validated_data)
