from rest_framework.response import Response
from .models import Users, Todos
from rest_framework.views import APIView
from .serializers import UsersSerializer, TodosSerializer


class UsersAPI(APIView):
    def post(self, request):
        queryset = Users.objects.all()
        context = {
            "accessToken" : "abcde",
            "refreshToken" : "fedcba"
        }
        return Response(context, status=200)


class TodoListAPI(APIView):
    def get(self, request):
        email = request.GET.get("email")

        if email:
            queryset = Todos.objects.filter(user__email=email).order_by("-deadline")
            serializer = TodosSerializer(queryset, many=True)
            return Response(serializer.data, status=200)

        else:
            return Response({"error" : "Todo Not Found"}, status=400)

    def post(self, request):
        data = request.data
        user = Users.objects.get(email=data["user"])

        newTodo = Todos()
        newTodo.user = user
        newTodo.title = data["title"]
        newTodo.description = data["description"]
        newTodo.deadline = data["date"]
        newTodo.save()

        queryset = Todos.objects.filter(user__email=user).order_by("-id")
        serializer = TodosSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def put(self, request):
        data = request.data
        if data["type"] == "checked":
            todo = Todos.objects.get(id=data["id"])
            todo.isChecked = not(todo.isChecked)
            todo.save()

            return Response({"status": 200}, status=200)

        elif data["type"] == "update":
            todo = Todos.objects.get(id=data["id"])
            todo.isChecked = data["isChecked"]
            todo.title = data["title"]
            todo.description = data["description"]
            todo.deadline = data["deadline"]
            todo.save()

            todo = Todos.objects.get(id=data["id"])
            serializer = TodosSerializer(todo, many=False)
            return Response(serializer.data, status=200)


    def delete(self, request):
        data = request.data

        todo = Todos.objects.get(id=data["id"])
        todo.delete()

        return Response({"status": 200}, status=200)
