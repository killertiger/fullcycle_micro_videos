from django.db import models

from core.cast_member.domain.value_objects import CastMemberType

# Create your models here.
class CastMemberModel(models.Model):
    DIRECTOR = CastMemberType.Type.DIRECTOR.value
    ACTOR = CastMemberType.Type.ACTOR.value
    
    TYPES_CHOICES = [
        (DIRECTOR, 'Diretor'),
        (ACTOR, 'Ator')
    ]
    
    id = models.UUIDField(primary_key=True, editable=True)
    name = models.CharField(max_length=255)
    cast_member_type = models.PositiveSmallIntegerField(
        choices=TYPES_CHOICES
    )
    created_at = models.DateTimeField()
    
    class Meta:
        db_table = 'cast_members'