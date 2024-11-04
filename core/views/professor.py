from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Professor
from core.serializers.professor import ProfessorSerializer


class ProfessorListAPIView(APIView):
    def get_queryset(self):
        return Professor.objects.prefetch_related("department").all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProfessorSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ProfessorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfessorDetailAPIView(APIView):
    def get_queryset(self):
        return Professor.objects.prefetch_related("department").all()

    def get_object(self, pk):
        professor = self.get_queryset().get(pk=pk)
        return professor

    def get(self, request, pk):
        professor = self.get_object(pk)
        serializer = ProfessorSerializer(professor)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        professor = self.get_object(pk)
        serializer = ProfessorSerializer(professor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        professor = self.get_object(pk)
        professor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

