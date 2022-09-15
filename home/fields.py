from wagtail.core.blocks.field_block import BooleanBlock
from wagtail.core.blocks.field_block import CharBlock
from wagtail.core.blocks.field_block import PageChooserBlock
from wagtail.core.blocks.field_block import RichTextBlock
from wagtail.core.blocks.struct_block import StructBlock


class SlideshowBlog(StructBlock):
    latest_blog_post = BooleanBlock(required=False)
    blog_post = PageChooserBlock(page_type="blog.BlogPage", required=False)


class SlideshowPage(StructBlock):
    image_chooser = BooleanBlock()
    page = PageChooserBlock()


class SlideshowFreeform(StructBlock):
    image_chooser = BooleanBlock()
    headline = CharBlock()
    description = RichTextBlock()
    read_more = PageChooserBlock()
