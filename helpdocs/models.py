# helpdocs/models.py
from django.conf import settings
from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
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


class HelpPage(Page):
    identifier = models.CharField(
        max_length=100,
        unique=True,
        help_text="Used as the lookup key in your frontend dialogs"
    )
    body = RichTextField()
    # ← NEW FIELD: extra departments that can see this page
    additional_departments = models.JSONField(
        default=list,
        blank=True,
        help_text="List of other department slugs (from user.role) that can see this page."
    )

    content_panels = Page.content_panels + [
        FieldPanel('identifier'),
        FieldPanel('body', classname="full"),
        FieldPanel('additional_departments'),
    ]

    class Meta:
        verbose_name = "Help Page"
        verbose_name_plural = "Help Pages"
