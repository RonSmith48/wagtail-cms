# approval/api/serializers.py
from rest_framework import serializers
from approval.models import BusinessDocument, DocumentSignature


class DocumentSignatureSerializer(serializers.ModelSerializer):
    signer = serializers.ReadOnlyField(source='signer.username')

    class Meta:
        model = DocumentSignature
        fields = ['signer', 'signed_at', 'comment']


class BusinessDocumentSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    signatures = DocumentSignatureSerializer(many=True, read_only=True)

    class Meta:
        model = BusinessDocument
        fields = [
            'id', 'title', 'description', 'file',
            'creator', 'created_at',
            'required_signatories',
            'status', 'signatures',
        ]
        read_only_fields = ['creator', 'status', 'signatures']

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)
