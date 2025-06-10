from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel

class HowToIndexPage(Page):
    """Container page for a multi‐step guide."""
    subpage_types = ['helpdocs.HowToSectionPage']
    parent_page_types = ['home.HomePage']  # or wherever you mount docs

class HowToSectionPage(Page):
    """One “chapter” or step in the guide."""
    parent_page_types = ['helpdocs.HowToIndexPage']
    body = StreamField([
        # rich text with inline images & links
        ('paragraph', blocks.RichTextBlock(features=[
            'bold', 'italic', 'link', 'image'
        ])),
        # standalone images (with captions, resizing, etc.)
        ('image', ImageChooserBlock()),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
