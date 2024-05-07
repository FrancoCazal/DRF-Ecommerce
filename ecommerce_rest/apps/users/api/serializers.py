from rest_framework import serializers
from apps.users.models import User

# Convierte una instancia de un modelo en django y la convierte en una estructura de json
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
    # Función que maneja los datos del diccionario que le llega en la consulta. Por defecto retorna un diccionario.
    # Sirve para: listar atributos especificos de objetos, mostrar el nombre distinto de una clave sin modificar nada.
    def to_representation(self, instance):
        # Esto llama a la automatización de asignar clave y valor según sea la consulta.
        #data = super().to_representation(instance) 
        #print(data)
        
        # Personalizando lo que se desea retornar: campos específicos
        return {
            'id': instance['id'], # Corchetes porque en el api se tiene .values o sea es un vector.
            'username': instance['username'], # Si fuera un diccionario (solo .all()) se haría instance.username
            'correo_electrónico': instance['email'],
            'password': instance['password']
        }
        # De esta forma se puede usar un solo serializador para crear, actualizar y listar (para listar esta el to_representation).
        
'''
# Este modelo conjuntamente con sus funciones se hace a modo de prueba para entender como funciona automáticamente el ModelSerializer.
# Si se define un serializer personalizado com este, se ejecutan los métodos definidos en él en el orden establecido.
# Si no encuentra tales métodos, ejecuta automáticamente los mismos pero predeterminados en la librería.
# Capa extra en la cual se pueden validar los valores, ya que la view debería tratar solo la info validada.
class TestUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length = 200)
    email = serializers.EmailField()
    
    # Funciones que se definen para validaciones de campos específicos, se entregan los values por orden cargado.
    def validate_name(self,value):
        # custom validation
        if 'developer' in value:
            # Se carga esto en el atributo errors llamado desde la api
            raise serializers.ValidationError('Error, no puede existir un usuario con ese nombre')
        
        print(self.context)
        return value
    
    def validate_email(self, value):
        # custom validation 2
        if value == '':
            raise serializers.ValidationError('Tiene que indicar un correo')
        
        # Se validan los errores independientemente en cada campo para que se muestre un informe de error detallado.
        # Se valida el valor por medio de la funcion previamente definida.
        
#        if self.validate_name(self.context['name']) in value:
#            raise serializers.ValidationError('El email no puede contener el nombre')
        
        return value
    
    # Si no hay funciones definidas de validación, se ejecuta esta que valida todo.
    def validate(self,data):
        return data
    
    # Luego de pasar por los procesos anteriores, se ejecuta automaticamente un proceso intermedio el cual es este
    # Los datos despues de validarse se almacenan en la variable validated_data
    # Esta funcion se activa para guardar un objeto en la db
    def create(self,validated_data):
        # Con esta línea se guarda el objeto en la db
        return User.objects.create(**validated_data)
    
    # Esta funcion se ejecuta automaticamente y sin necesidad que se defina cuando se usa un ModelSerializer y el metodo HTTP es PUT.
    def update(self, instance, validated_data):
        # La instance es user
        instance.name = validated_data.get('name',instance.name)
        instance.email = validated_data.get('email',instance.email)
        instance.save()
        return instance
    
    # Si es un serializer save interactua con la db pero si es un view save interactua con el serializer, que es esta funcion.
    # Definir esta funcion puede servir para por ej enviar un correo despues del registro de un usuario o para que no se guarde
    # info en la db, para manejar datos volatiles.
    #def save(self, **args):
       # print("HOLAAAAAAAAAAAA")
'''