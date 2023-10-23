from dataclasses import dataclass
from typing import Callable
from core.cast_member.application.dto import CastMemberOutput
from rest_framework import status as http_status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from core.__seedwork.infra.django_app.serializers import UUIDSerializer
from core.cast_member.application.use_cases import (
    CreateCastMemberUseCase, UpdateCastMemberUseCase, DeleteCastMemberUseCase, ListCastMemberUseCase, GetCastMemberUseCase)


class CastMemberResource(APIView):

    create_use_case: Callable[[], CreateCastMemberUseCase]
    list_use_case: Callable[[], ListCastMemberUseCase]
    get_use_case: Callable[[], GetCastMemberUseCase]
    update_use_case: Callable[[], UpdateCastMemberUseCase]
    delete_use_case: Callable[[], DeleteCastMemberUseCase]
    
    def post(self, request: Request):
        serializer = CastMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        input_param = CreateCastMemberUseCase.Input(**serializer.validated_data)
        output = self.create_use_case().execute(input_param)
        body = CastMemberResource.cast_member_to_response(output)
        
        return Response(body, status=http_status.HTTP_201_CREATED)

    def get(self, request: Request, id: str = None):
        if id:
            return self.get_object(id)
        
        input_param = ListCastMemberUseCase.Input(**request.query_params.dict())
        
        output = self.list_use_case().execute(input_param)
        
        data = CastMemberCollectionSerializer(instance=output).data
        return Response(data)
    
    def get_object(self, id: str):
        CastMemberResource.validate_id(id)
        input_param = GetCastMemberUseCase.Input(id)
        output = self.get_use_case().execute(input_param)
        body = CastMemberResource.cast_member_to_response(output)
        return Response(body)
    
    def put(self, request: Request, id: str):
        CastMemberResource.validate_id(id)
        
        serializer = CastMemberSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        
        input_param = UpdateCastMemberUseCase.Input(
            **{
                'id': id, 
                **serializer.validated_data,
            }
        )
        
        output = self.update_use_case().execute(input_param)
        body = CastMemberResource.cast_member_to_response(output)
        return Response(body)
    
    def delete(self, id: str):
        CastMemberResource.validate_id(id)
        input_param = DeleteCastMemberUseCase.Input(id=id)
        self.delete_use_case().execute(input_param)
        return Response(status=http_status.HTTP_204_NO_CONTENT)
    
    @staticmethod
    def cast_member_to_response(output: CastMemberOutput):
        serializer = CastMemberSerializer(instance=output)
        return serializer.data
    
    @staticmethod
    def validate_id(id: str):
        serializer = UUIDSerializer(data={'id': id})
        serializer.is_valid(raise_exception=True)