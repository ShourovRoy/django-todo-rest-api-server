from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import TodoModel
from .serializers import TodoSerializer
import jwt
from django.conf import settings
# Create your views here.


class TodoView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TodoSerializer

    def get(self, request):
        token = request.headers['Authorization'].split(' ')[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        try:
            todoList = TodoModel.objects.filter(owner=user_id)
            serializer = self.serializer_class(todoList, many=True)
            return Response(serializer.data)
        except TodoModel.DoesNotExist:
            return Response({"message": "No todo list found"})

    def post(self, request):
        try:
            token = request.headers['Authorization'].split(' ')[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            data = {
                "title": request.data['title'],
                "desc": request.data['desc'],
                "category" : request.data['category'],
                "owner": user_id,
            }
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except KeyError:
            return Response({"message": "Something went wrong"})


class TodoDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TodoSerializer


    def get(self, request, pk):
        token = request.headers['Authorization'].split(' ')[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        try:
            todo = TodoModel.objects.filter(pk=pk, owner=user_id)
            serializer = self.serializer_class(todo, many=True)
            return Response(serializer.data)
        except TodoModel.DoesNotExist:
            return Response({'message': 'Todo not found'})


    def put(self, request, pk):
        token = request.headers['Authorization'].split(' ')[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        data = {
            **request.data,
            "owner": user_id,
        }
        try:
            todo = TodoModel.objects.get(pk=pk, owner=user_id)
            serializer = self.serializer_class(todo, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data": serializer.data, "message": "Todo updated"})
            return Response(serializer.errors)
        except TodoModel.DoesNotExist:
            return Response({"message": "Todo not found"})
    

    def delete(self, request, pk):
        token = request.headers['Authorization'].split(' ')[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        try:
            todo = TodoModel.objects.get(pk=pk, owner=user_id)
            todo.delete()
            return Response({"message": "Todo deleted"})
        except TodoModel.DoesNotExist:
            return Response({"message": "Todo not found"})