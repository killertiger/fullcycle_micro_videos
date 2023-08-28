from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

@api_view()
def hello_world(request: Request):
    return Response({'message': 'API is working'})