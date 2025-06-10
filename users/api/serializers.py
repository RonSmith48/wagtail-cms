from rest_framework import serializers
from users.models import RemoteUser


class RemoteUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the RemoteUser mirror model.
    Exposes only our frequently-used fields, all read-only since this is a mirror.
    """
    class Meta:
        model = RemoteUser
        # fields to include in the API
        fields = [
            'id',
            'first_name',
            'last_name',
            'initials',
            'email',
            'is_staff',
            'is_superuser',
            'is_active',
            'start_date',
            'role',
            'permissions',
            'avatar',
        ]
        # mirror fields should not be editable via this endpoint
        read_only_fields = fields
