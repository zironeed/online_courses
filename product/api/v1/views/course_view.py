from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course, Group
from users.models import Subscription


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    def get_queryset(self):
        if self.action in ['list']:
            return Course.objects.filter(
                subscriptions__isnull=True,
                subscriptions__user=self.request.user
            ).distinct()
        return Course.objects.all()

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""

        course = self.get_object()
        user = request.user

        if user.subscriptions.filter(course=course, is_active=True).exists():
            return Response(
                data={'detail': 'У вас уже есть подписка на этот курс'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user.balance.balance < course.price:
            return Response(
                data={'detail': 'У вас недостаточно бонусов'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                user.balance.balance -= course.price
                user.balance.save()

                Subscription.objects.create(user=user, course=course, is_active=True)

            if course.groups.count() < 10:
                for i in range(10 - course.groups.count()):
                    Group.objects.create(course=course, title=f'Группа {i + 1}')

            group = course.groups.annotate(student_count=Count('subscriptions__user')).order_by('student_count').first()
            group.subsctiptions.add(user)

        except Exception:
            return Response(
                data={'detail': 'Оплата не удалась'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            data={'detail': 'Подписка оформлена!'},
            status=status.HTTP_201_CREATED
        )
