from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from . import models, serializer
# Create your views here.
@api_view(['GET'])
def api_message(req):
    return Response({"Message" : "Sucessfully Displayed API"})



@api_view(['GET'])
def get_all_todo(req):
    all_todos = models.todo.objects.all()
    serilize_todo = serializer.TodoSerializer(all_todos , many=True)
    return Response(serilize_todo.data , status=status.HTTP_200_OK)


@api_view(['POST'])
def add_todo(req):
    data = req.data
    # serlize data to send
    serilize_data_to_send = serializer.TodoSerializer(data=data)
    if serilize_data_to_send.is_valid():
        serilize_data_to_send.save()
        return Response(serilize_data_to_send.data , status=status.HTTP_201_CREATED) 
    return Response(serilize_data_to_send.errors , status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT' , 'GET'])
def edit_view(req, todo_id):
    try:
        if req.method == "PUT":
            data_to_send = req.data
            get_todo_from_database = models.todo.objects.get(id=todo_id)
            todo_serialize_compare = serializer.TodoSerializer(get_todo_from_database, data_to_send)
            if todo_serialize_compare.is_valid():
                todo_serialize_compare.save()
            return Response(todo_serialize_compare.data , status=status.HTTP_202_ACCEPTED)
        if req.method == "GET":
            get_single_todo = models.todo.objects.get(id=todo_id)
            seralize_data = serializer.TodoSerializer(get_single_todo)
            return Response(seralize_data.data , status=status.HTTP_200_OK)
    except models.todo.DoesNotExist:
        return Response({"message" : "Todo Does Not Exisit"})
        

@api_view(['DELETE'])
def delete_todo(req, todo_id):
        try:
            get_todo_to_delete  = models.todo.objects.get(id=todo_id)
            get_todo_to_delete.delete()
            return Response({'Message': 'Succesfully Deleted Todo'})
        except models.todo.DoesNotExist:
             return Response({"message" : "Todo Does Not Exisit"})


