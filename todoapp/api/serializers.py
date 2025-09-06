from rest_framework import serializers 
from todo.models import ToDo 
 
class TodoSerializer(serializers.ModelSerializer): 
    created = serializers.ReadOnlyField() 
    completed = serializers.ReadOnlyField() 
 
    class Meta: 
        model = ToDo 
        fields = ['id', 'title', 'memo', 'created', 'completed'] 

class TodoToggleCompleteSerializer(serializers.ModelSerializer):

    class Meta: 
        model = ToDo
        fields = [] #Thanks to this I almost didn't finish this tutorial teacher thank you T_T #losingMyMind