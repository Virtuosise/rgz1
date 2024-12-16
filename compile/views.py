import json
import io
import sys
from django.http import JsonResponse
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from .models import task,User
from rest_framework.views import APIView
from rest_framework.response import Response
import pdb

@csrf_exempt  # Важно: используйте это с осторожностью в продакшн-режиме
def execute_code(request):
    if request.method == 'POST':
        try:
            # Получаем код из запроса
            body = json.loads(request.body)
            code = body.get('code')

            if not code:
                return JsonResponse({'error': 'No code provided'}, status=400)

            # Создаем объект StringIO для захвата вывода
            output_capture = io.StringIO()

            # Перенаправляем стандартный вывод в StringIO
            sys.stdout = output_capture

            # Выполнение кода в локальном пространстве
            try:
                exec(code)
                # Получаем захваченный вывод
                output = output_capture.getvalue()
                return JsonResponse({'output': output.strip()})  # Возвращаем вывод программы

            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

            finally:
                # Восстанавливаем стандартный вывод, чтобы он снова выводился в консоль
                sys.stdout = sys.__stdout__

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid method'}, status=405)


class create_task(APIView):
    def post(self, request):
        try:
            body = json.loads(request.body)
            name = body.get('name')
            description = body.get('description')
            input_data = body.get('inputData')
            output_data = body.get('outputData')

            # Проверка на обязательные поля
            if not name or not description or not input_data or not output_data:
                return Response({'error': 'Missing fields in the request body'}, status=400)

            # Создание задачи
            task.objects.create(
                name = name,
                description=description, 
                input_data=input_data, 
                output_data=output_data
            )

            return Response({'message': 'Task created successfully'}, status=201)

        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return Response({'error': f'Error: {str(e)}'}, status=500)

    # Если вы хотите использовать GET метод, можно добавить его для получения задач:
    def get(self, request):
        tasks = task.objects.all()  # Получаем все задачи
        tasks_data = [{'name': task.name, 
                       'description': task.description, 
                       'input_data': task.input_data, 
                       'output_data': task.output_data, 
                       'date_create' : task.date_create,
                       'is_choice': task.is_choice} for task in tasks]
        return Response({'tasks': tasks_data}, status=200)
    
    def delete(self, request):
        #pdb.set_trace()
        body = json.loads(request.body)
        description = body.get('description')
        tsk = task.objects.filter(description = description).first()

        if tsk:
            task.objects.filter(description = description).delete()
            return Response(status = 200)
        return Response({'error' : 'error'})

class Registration(APIView):
    def post(self,request):
        #pdb.set_trace()
        body = json.loads(request.body)
        name = body.get('name')
        password = body.get('password')
        is_admin = body.get('isAdmin')
        email = body.get('email')

        if not name or not password or not email:
            return Response({'error': 'Missing fields in the request body'}, status=400)
        
        exists = User.objects.filter(email=email).exists()

        if exists:
            return Response({'error': 'This user already exists'}, status=400)

        User.objects.create(
            name=name, 
            password=password, 
            is_admin=is_admin,
            email = email,
        )

        return Response({'message': 'User created successfully'}, status=201)

    def get(self,request):
        all_users = User.objects.all()
        user = [{'name': users.name, 'password': users.password, 'isAdmin': users.is_admin, 'email' : users.email,} for users in all_users]
        return Response({'tasks': user}, status=200)
    

class Login(APIView):
    def post(self,request):
        body = json.loads(request.body)
        name = body.get('name')
        password = body.get('password')
        email = body.get('email')

        if not name or not password or not email:
            return Response({'error': 'Missing fields in the request body'}, status=400)
        
        user = User.objects.filter(email=email).first()

        if user:
            return Response({'isAdmin' : user.is_admin},status = 200)

        return Response({'error': 'This user does not exist'}, status=400)
    

    