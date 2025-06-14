# business_docs/models.py
from django.db import models
from django.conf import settings


class BusinessDocument(models.Model):
    """
    A user‐created document (form, plan, etc.) that
    must be signed off by one or more approvers.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='business_docs/')
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_docs',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # A list of usernames or role-slugs who *must* sign
    required_signatories = models.JSONField(
        default=list,
        help_text="List of user.role or username values required to sign off."
    )

    class STATUS(models.TextChoices):
        DRAFT = 'D', 'Draft'
        PENDING = 'P', 'Pending Signatures'
        COMPLETE = 'C', 'Fully Signed'
        REJECTED = 'R', 'Rejected'

    status = models.CharField(
        max_length=1,
        choices=STATUS.choices,
        default=STATUS.DRAFT,
        db_index=True
    )

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class DocumentSignature(models.Model):
    """
    One signature on a BusinessDocument.
    """
    document = models.ForeignKey(
        BusinessDocument,
        related_name='signatures',
        on_delete=models.CASCADE
    )
    signer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    signed_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ('document', 'signer')
