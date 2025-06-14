# approval/api/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from approval.models import BusinessDocument, DocumentSignature
from .serializers import BusinessDocumentSerializer, DocumentSignatureSerializer


class BusinessDocumentViewSet(viewsets.ModelViewSet):
    """
    /business-docs/ → List, Create, Retrieve, Update (title/desc/file),
    /business-docs/{id}/sign/ → add a signature
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BusinessDocumentSerializer
    queryset = BusinessDocument.objects.all()

    @action(detail=True, methods=['post'])
    def sign(self, request, pk=None):
        doc = self.get_object()
        signer = request.user

        # prevent duplicates
        if doc.signatures.filter(signer=signer).exists():
            return Response({"detail": "Already signed."},
                            status=status.HTTP_400_BAD_REQUEST)

        sig = DocumentSignature.objects.create(
            document=doc,
            signer=signer,
            comment=request.data.get('comment', '')
        )

        # Recompute doc.status here (or signal)
        required = set(doc.required_signatories)
        done = set(s.signer.role for s in doc.signatures.all())
        if required.issubset(done):
            doc.status = doc.STATUS.COMPLETE
        else:
            doc.status = doc.STATUS.PENDING
        doc.save()

        return Response(DocumentSignatureSerializer(sig).data)
