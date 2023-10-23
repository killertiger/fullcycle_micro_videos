from django.urls import path
from .api import CastMemberResource


def __init_cast_member_resource():
    cast_member_container = container.cast_member
    return {
        'create_use_case': cast_member_container.use_case_create_cast_member,
        'list_use_case': cast_member_container.use_case_list_cast_member,
        'get_use_case': cast_member_container.use_case_get_cast_member,
        'update_use_case': cast_member_container.use_case_update_cast_member,
        'delete_use_case': cast_member_container.use_case_delete_cast_member,
    }


urlpatterns = [
    path('cast-members/', CastMemberResource.as_view(
        **__init_cast_member_resource()
    )),
    path('cast-members/<id>/', CastMemberResource.as_view(
        **__init_cast_member_resource()
    )),
]
