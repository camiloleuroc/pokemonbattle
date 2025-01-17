from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.middleware.csrf import get_token
from django.db import connection
import pandas as pd
from .models import Test_Table_One
import json

def get_data(request):

    if request.method == 'GET':
        df = pd.read_sql_query("""SELECT * FROM enerbit_test_table_one""", con=connection)

        return JsonResponse({'data':df.to_dict(), 'CSRF':get_token(request)})
    return HttpResponse("Error", status=300)

def insert_data(request):

    if request.method == 'POST':

        data = json.loads(request.body)

        name = data.get('name', '')
        description = data.get('description', '')
        value = data.get('value', 0)
        state = data.get('state', False)

        print(name)
        print(description)
        print(value)
        print(state)

        Test_Table_One.objects.create(name=name, description=description, value=int(value), state=state)

        return HttpResponse("OK", status=200)
    return HttpResponse("Error", status=300)