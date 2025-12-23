from rest_framework import decorators, generics, viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Course, Subject
from .serializers import (
    CourseSerializer,
    CourseWithContentsSerializer,
    SubjectSerializer,
)


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class CourseEnrollView(generics.GenericAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        course = self.get_object()
        enrolled = course.students.filter(id=request.user.id).exists()
        if not enrolled:
            course.students.add(request.user)
            enrolled = True
        return Response({'enrolled': enrolled})


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @decorators.action(detail=True, methods=['get'])
    def contents(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = CourseWithContentsSerializer(course)
        return Response(serializer.data)
