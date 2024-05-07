from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from apps.users.models import User
from apps.users.api.serializers import *

'''
class UserAPIView(APIView):
    # Recibe la petición GET que envia el front end
    def get(self,request):
        users = User.objects.all()
        # many para convertir a json un LISTADO de datos
        users_serializer = UserSerializer(users, many=True)
        # Se retornan los datos de la variable con el atributo data
        return Response(users_serializer.data)
'''

# Decorator that converts a function-based view into an APIView subclass. Takes a list of allowed methods for the view as an argument.
@api_view(['GET','POST']) 
def user_api_view(request):
    # Recibe la petición GET que envia el front end
    # List
    if request.method == 'GET':
        # queryset
        # Se traen valores de atributos especificos para optimizar consulta (los mismos que se van a usar en el to_representation)
        users = User.objects.all().values('id','username','email','password')
        # many para convertir a json un LISTADO de datos
        users_serializer = UserSerializer(users, many=True)
        
        '''
        # Test
        test_data = {
            'name':'ambrosio',
            'email':'empleadito@gmail.com'
        }
        
        test_user = TestUserSerializer(data=test_data,context=test_data)
        if test_user.is_valid():
            user_instance = test_user.save()
            print(user_instance)
        else:
            print(test_user.errors)
        '''
            
        # Se retornan los datos de la variable con el atributo data (diccionario con los datos) y el status adecuado para el navegador.
        return Response(users_serializer.data, status = status.HTTP_200_OK)
        # Obs: opera de la misma forma que con el APIView pero con estructura distinta.
    
    # Create    
    elif request.method == 'POST':
        # Se hace un request de datos por medio del serializer para el POST 
        user_serializer = UserSerializer(data = request.data)
        # Validation
        if user_serializer.is_valid():
            # Igual que con los forms
            user_serializer.save()
            # El atributo data puede guardar info serializada y tambien info a serializar
            return Response({'message': 'Usuario creado correctamente!'}, status=status.HTTP_201_CREATED)
        # Imprimir error correspondiente si no se cumple
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_api_view(request,pk):
    # Realizar consulta/queryset (devuelve true o false)
    user = User.objects.filter(id = pk).first()
    # if para validar consulta abreviadamente en vez de poner en cada método
    if user:
        
        # Listar/Retrieve (Individualmente)
        if request.method == 'GET':
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status.HTTP_200_OK)
        
        # Editar/Update
        elif request.method == 'PUT':
            # Se pasa user (la instancia) y el request, con lo que se sobreescribe la instancia
            user_serializer = UserSerializer(user, data = request.data)
            if user_serializer.is_valid():
                # Cuando se ejecuta este save, se llama a la funcion definida como update en serializers
                user_serializer.save()
                return Response(user_serializer.data, status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Eliminar/Delete
        elif request.method == 'DELETE':
            user = User.objects.filter(id = pk).first()
            user.delete()
            return Response({'message': 'Usuario eliminado correctamente!'}, status = status.HTTP_200_OK)
        
    return Response({'message': 'No se ha encontrado un usuario con estos datos'}, status = status.HTTP_400_BAD_REQUEST)