"""Sphinx writer/translator for RevealJS, a browser slideshow."""

from docutils import nodes
from docutils.nodes import SkipNode
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.writers.html import SmartyPantsHTMLTranslator as HTMLTranslator

__author__ = "Joel Burton <joel@joelburton.com>"


class RevealJSTranslator(HTMLTranslator):
    """Translator for Sphinx structure -> RevealJS HTML structure.

    Overrides Sphinx HTML translator, particularly to handle section-structuring in the manner
    that RevealJS requires ("<section>" blocks for slides, etc.)
    """

    _dl_fragment = 0   # What # fragment are we in definition list?

    def _new_slide(self, node):
        """Adds a new slide, allowing for revealjs options."""

        # Get revealjs options so we can add them to section element

        options = []

        attr_to_html_attr = {
            'transition': 'data-transition',
            'transition-speed': 'data-transition-speed',
            'class': 'class',
        }

        for attr, html_attr in attr_to_html_attr.items():
            if node.attributes.get(attr):
                options.append("%s='%s'" % (html_attr, node.attributes.get(attr)))

        # If the background is an image, we need to add it to the images the builder is
        # tracking --- otherwise, it won't get copied into the build directory's images
        # folder and things won't work

        background = node.attributes.get('background')
        background_option = ""

        if background:
            # Assume it's not an image (it's a color) and set normally
            background_option = "data-background='%s'" % background

            if "." in background:
                _, upper_ext = background.upper().rsplit(".", 1)
                if upper_ext in ['JPG', 'PNG', 'GIF', 'SVG']:
                    background_option = "data-background='_images/%s'" % background
                    self.builder.images[background] = background

        # Add the section with options

        self.body.append("<section %s %s>" % (' '.join(options), background_option))

    def visit_section(self, node):
        """Handle starting a section.

        The input structure has two levels: the overall section surrounding all of the material
        and the section for each slide. We omit the overall section (we don't want or need
        any wrapper elements) and emit a <section> for each slide.
        """

        self.section_level += 1

        # If this is a new slide, add it (don't do this for sub-slide sections)
        if self.section_level in [2, 3]:
            self._new_slide(node)

    def depart_section(self, node):
        """Close sections.

        We didn't create any structure for sections other than slide-level, so only close those.
        """

        self.section_level -= 1

        # Close the slide (but don't do this for sub-slide sections)
        if self.section_level in [1, 2]:
            self.body.append("</section>")

    def visit_title(self, node):
        """Handle section titles in slide-aware wy."""

        # We don't want to print the overall deck title here
        if self.section_level == 1:
            raise SkipNode

        # If this is the top of second-level section, wrap in <section>...
        if self.section_level == 2:
            self.body.append(self.starttag(node, 'section'))

        return HTMLTranslator.visit_title(self, node)

    def depart_title(self, node):
        """Handle leaving section titles in a slide-away way."""

        HTMLTranslator.depart_title(self, node)

        # If this is the end of a second-level section, close our <section>
        if self.section_level == 2:
            self.body.append("</section>")

    def visit_sidebar(self, node):
        """These should never appear in slides."""

        raise SkipNode

    def visit_warning(self, node):
        """These should never appear in slides."""

        raise SkipNode

    def visit_note(self, node):
        """These should never appear in slides."""

        raise SkipNode

    def visit_admonition(self, node):
        """These should never appear in slides."""

        raise SkipNode

    def visit_topic(self, node):
        """These should never appear in slides."""

        raise SkipNode

    def visit_interslide(self, node):
        """Interslides should make a new slide (but there's no header, etc.)

        If our parent is a normal slide, close it.

        In any case, start a new slide for the interslide.
        """

        if self.section_level > 2:
            self.body.append("</section>")
        self._new_slide(node)

    def depart_interslide(self, node):
        """Close an interslide.

        If this is a top-level interslide (ie, our parent is a section, not a slide)
        we need to close the interslide itself.

        If our parent was a slide, we closed that slide to make the interslide,
        so when the translator "closes" the parent slide, that will actually be us--so
        we don't want to close this here.
        """

        if self.section_level == 2:
            self.body.append("</section>")

    def should_be_compact_paragraph(self, node):
        """Can this text be 'compacted' into a non-paragraph?

        Sphinx will try to 'compact' text into not being a paragraph when possible.
        For example, fore:

          - hello

          - there

          - reader

        It realizes that since those are simple lines, it doesn't need to put
        <p> tags around the text inside the <li> tags---whereas for::

          - hello

          - there

          - reader

            I love readers!

        It would need to keep paragraphs inside the <li> tags.

        We often put text inside containers for incremental-appearance, like this:

          The answer is:

          .. container:: one-incremental

            Forty-two

        Seeing just a simple thing inside the container, Sphinx wouldn't wrap it
        in a paragraph, just <div>. This makes for ugly line breaks.

        Therefore, when we're directly inside a container, we should never
        compact paragraphs. Otherwise, follow Sphinx's rules.
        """

        if isinstance(node.parent, nodes.container):
            if 'non-paragraph' not in node.parent.attributes['classes']:
                return False
        return HTMLTranslator.should_be_compact_paragraph(self, node)

    def visit_speakernote(self, node):
        self.body.append("<aside class='notes'>")

    def depart_speakernote(self, node):
        self.body.append("</aside>")

    # Definition lists: you can put item-incremental on a DL and it
    # will make the terms/definitions appear one-by-one (the term and definition
    # together)
    #
    # To do this, we need to put a matching fragment-index on each term/def pair,
    # so we need to keep track of this state.

    def visit_definition_list(self, node):
        """Visit definition list.

        If this is an incremental DL, keep track of start of fragements.
        """

        if 'dl-fragment' in node['classes']:
            self._dl_fragment = 1
        return HTMLTranslator.visit_definition_list(self, node)

    def visit_term(self, node):
        """Visit definition list term.

        If this is an incremental DL, add fragment & count to it.
        """

        if self._dl_fragment:
            self.body.append('<dt class="fragment" data-fragment-index=%s>' % self._dl_fragment)
        else:
            self.body.append("<dt>")

    def visit_definition(self, node):
        """Visit definition list definition.

        If this is an incremental DL, add fragment & count to it.
        """

        if self._dl_fragment:
            self.body.append('<dd class="fragment" data-fragment-index=%s>' % self._dl_fragment)
            self._dl_fragment += 1
        else:
            self.body.append("<dd>")

    def depart_definition_list(self, node):
        """End a definition list.

        Reset the fragment count (which would have been >0 if this was an incremental
        DL.
        """

        self._dl_fragment = 0
        return HTMLTranslator.depart_definition_list(self, node)




class RevealJSBuilder(StandaloneHTMLBuilder):
    """Builder for making RevealJS using Sphinx."""

    name = 'revealjs'

    def init(self):
        """Use our custom translator."""

        self.config.html_theme = self.config.revealjs_theme
        self.config.pngmath_dvipng_args = self.config.revealjs_pngmath_dvipng_args
        self.config.html_translator_class = 'writers.revealjs.RevealJSTranslator'

        return StandaloneHTMLBuilder.init(self)

    def finish(self):
        """Skip all the stuff around building additional pages, etc."""

        self.info()

        self.copy_image_files()
        self.copy_download_files()
        self.copy_static_files()
        self.copy_extra_files()
        self.write_buildinfo()


def setup(app):
    app.add_builder(RevealJSBuilder)
