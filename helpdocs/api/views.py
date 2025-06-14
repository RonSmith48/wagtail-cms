# helpdocs/api/views.py
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from helpdocs.models import HelpPage, HowToIndexPage
from helpdocs.api.serializers import HelpPageSerializer, HowToIndexSerializer


class HelpPageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    /helpdocs/help/<id>/
    """
    queryset = HelpPage.objects.all()
    serializer_class = HelpPageSerializer
    lookup_field = 'identifier'         # ← match your model’s `identifier`
    lookup_url_kwarg = 'id'
    permission_classes = [IsAuthenticated]

    # optionally restrict to users with an “editor” role
    def get_permissions(self):
        perms = super().get_permissions()
        # you could swap in a custom IsEditor permission
        return perms


class HowToIndexViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HowToIndexSerializer   # write this to nest your sections
    lookup_field = 'slug'                 # or however you identify guides

    def get_queryset(self):
        qs = HowToIndexPage.objects.prefetch_related('children')
        # if power-user wants all guides:
        if self.request.query_params.get('all_depts') == 'true':
            return qs

        # otherwise, only guides owned by or opted-into the user's dept:
        user_dept = getattr(self.request.user, 'role', None)
        return qs.filter(
            Q(owner__department=user_dept) |
            Q(additional_departments__contains=[user_dept])
        ).distinct()
