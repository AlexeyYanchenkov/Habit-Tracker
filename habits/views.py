from rest_framework import viewsets, permissions
from .models import Habit
from .serializers import HabitSerializer
from .permissions import IsOwnerOrReadOnlyPublic
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny


class HabitViewSet(viewsets.ModelViewSet):
    """CRUD представление привычек пользователя"""

    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnlyPublic]

    def get_queryset(self):
        if self.action == 'list':
            # Для списка привычки текущего пользователя, упорядоченные по id
            return Habit.objects.filter(user=self.request.user).order_by('id')
        elif self.action == 'public_list':
            return Habit.objects.filter(is_public=True).order_by('id')
        # Для retrieve, update, delete - возвращаем все привычки (доступ ограничен permission-ами)
        return Habit.objects.all()

    def perform_create(self, serializer):
        # Автоматическая привязка пользователя
        serializer.save(user=self.request.user)

class PublicHabitListView(ListAPIView):
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    permission_classes = [AllowAny]