# helpdocs/api/serializers.py
from rest_framework import serializers
from helpdocs.models import HelpPage, HowToIndexPage, HowToSectionPage


class HelpPageSerializer(serializers.ModelSerializer):
    # read the raw stream_data, not HTML
    body = serializers.CharField(read_only=True)

    class Meta:
        model = HelpPage
        fields = ['identifier', 'title', 'body']
        lookup_field = 'identifier'


class HowToSectionSerializer(serializers.ModelSerializer):
    """
    Serializes each “chapter” or step in a guide,
    including a JSON‐serialised version of the StreamField.
    """
    body = serializers.SerializerMethodField()

    class Meta:
        model = HowToSectionPage
        # Use the Wagtail slug + title from Page, and the body stream
        fields = ['slug', 'title', 'body']

    def get_body(self, obj):
        # Return the raw JSON blocks for your StreamField
        return obj.body.stream_data  # :contentReference[oaicite:0]{index=0}


class HowToIndexSerializer(serializers.ModelSerializer):
    """
    Serializes a guide index page and nests its section pages.
    """
    sections = serializers.SerializerMethodField()

    class Meta:
        model = HowToIndexPage
        # slug + title from Page, then our nested `sections`
        fields = ['slug', 'title', 'sections']

    def get_sections(self, obj):
        # Grab the direct children of this index that are HowToSectionPage
        children = (
            obj
            .get_children()
            .type(HowToSectionPage)   # only section pages
            .specific()               # cast to the concrete model
        )
        return HowToSectionSerializer(children, many=True, context=self.context).data
