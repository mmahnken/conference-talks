"""Improved versions of doctest-related directives.

The standard doctest directives are awesome, but they don't have all of the features
of code-block directives. This adds back in:

- :caption:
- :class:

It does so by registering the subclassed versions, below, under the original names.

Joel Burton <joel@joelburton.com>
"""


# BUG: allows emphasize-lines but doesn't do the emphasizing; bug 112


from docutils.parsers.rst import directives
from sphinx.directives.code import container_wrapper
from sphinx.locale import _
from sphinx.ext.doctest import DoctestDirective, TestcodeDirective, TestoutputDirective
from sphinx.util import parselinenos
from sphinx.util.nodes import set_source_info


class AllowCaptionMixin(object):
    """Mixin that adds caption option to doctest directives."""

    def run(self):
        """Call the original directive run, then add in caption, if applicable."""

        literal = super(AllowCaptionMixin, self).run()[0]

        # This code copied from sphinx.directives.code

        linespec = self.options.get('emphasize-lines')
        if linespec:
            try:
                nlines = len(self.content)
                hl_lines = [x + 1 for x in parselinenos(linespec, nlines)]
            except ValueError as err:
                document = self.state.document
                return [document.reporter.warning(str(err), line=self.lineno)]
        else:
            hl_lines = None

        literal['classes'] += self.options.get('class', [])
        extra_args = literal['highlight_args'] = {}
        if hl_lines is not None:
            extra_args['hl_lines'] = hl_lines
        if 'lineno-start' in self.options:
            extra_args['linenostart'] = self.options['lineno-start']
        set_source_info(self, literal)

        caption = self.options.get('caption')
        if caption:
            try:
                literal = container_wrapper(self, literal, caption)
            except ValueError as exc:
                document = self.state.document
                errmsg = _('Invalid caption: %s' % exc[0][0].astext())
                return [document.reporter.warning(errmsg, line=self.lineno)]

        # literal will be note_implicit_target that is linked from caption and numref.
        # when options['name'] is provided, it should be primary ID.
        self.add_name(literal)

        return [literal]


class JDoctestDirective(AllowCaptionMixin, DoctestDirective):
    """Subclass of DoctestDirective to allow caption & class options."""

    option_spec = {
        'hide': directives.flag,
        'options': directives.unchanged,
        'caption': directives.unchanged,
        'class': directives.class_option,
        'emphasize-lines': directives.unchanged,
    }


class JTestcodeDirective(AllowCaptionMixin, TestcodeDirective):
    """Subclass of TestcodeDirective to allow caption & class options."""

    option_spec = {
        'hide': directives.flag,
        'options': directives.unchanged,
        'caption': directives.unchanged,
        'class': directives.class_option,
        'emphasize-lines': directives.unchanged,
    }


class JTestoutputDirective(AllowCaptionMixin, TestoutputDirective):
    """Subclass of TestoutputDirective to allow caption & class options."""

    option_spec = {
        'hide': directives.flag,
        'caption': directives.unchanged,
        'class': directives.class_option,
        'emphasize-lines': directives.unchanged,
    }


def setup(app):
    """Re-register our directives."""

    # HACK HACK HACK
    #
    # We should be registering these with the higher-level public API --- but that issues
    # a warning about "overriding already-registered classes". Therefore, we use this
    # semi-internal registration method that skips that.
    #
    # Should this feature ever stop working, you can replace these with the more public
    # API --- you'll get that warning, but it will work.
    #
    #        app.add_directive('doctest', JDoctestDirective)
    #        app.add_directive('testcode', JTestcodeDirective)
    #        app.add_directive('testoutput', JTestoutputDirective)

    directives.register_directive(
        "doctest", app._directive_helper(JDoctestDirective, None, None))
    directives.register_directive(
        "testcode", app._directive_helper(JTestcodeDirective, None, None))
    directives.register_directive(
        "testoutput", app._directive_helper(JTestoutputDirective, None, None))
