"""Master Sphinx configuration for all areas of Fellowship.

The subdirectories (lectures, exercises, etc.) all have a `conf.py` file that Sphinx
uses for building documents. Those files import from here for 99% of the settings
and just add subfolder-specific settings.

Therefore, common changes for our setup should go here.

BE VERY CAUTIOUS ABOUT EDITING THIS FILE. Breakages here could stop people from
building documents and will affect the appearance of all built documents.
If you're not certain what you're doing, please ask.

Most of the software here precedes Hackbright; everything in the tools/ directory
is copyright (c) 2008-2014 by Joel Burton <joel@joelburton.com> and is covered
by the GNU General Public License, version 3.
"""

import os
import datetime
import subprocess
import sys
import imp
import logging

def setup(app):
    # New settings we want to refer to in the config file; these need to be declared
    app.add_config_value('revealjs_theme', 'revealjs-meggie-2017', 'env')
    app.add_config_value('revealjs_imgmath_dvipng_args', [], 'env')
    app.add_config_value('answerkey', 'ANSWERKEY' in os.environ, 'env')

    try:
        imp.find_module('pygmentslexerbabylon')
        import pygmentslexerbabylon
        app.add_lexer("jsx", pygmentslexerbabylon.BabylonLexer())
    except ImportError:
        logging.warn("Pygmentslexerbabylon missing -- required to highlight JSX.")

#########################################################################################

# These things are most likely to be overridden in those files which import
# from here

# Title of document (for books, like the handbook, change this)
project = 'Meggie'

# Appears at bottom of many documents, may amend if we whitelabel training
copyright = '%s Meggie Mahnken' % datetime.datetime.now().year

# Normally blank, but you can set this for a specific use (eg, "Disney Fellowship")
version = release = ''

# Appears as the HTML title tag for many things or at the top of docs. Can change.
html_title = 'Talks by Meggie'

# Additional HTML context to provide
html_context = {'backurl': '/'}

#########################################################################################

# Can use this to change the theme we use for the Handouts
#
# For custom Fellowships, make a new theme, subclassing our standard theme,
# and then edit the CSS and change this conf file in a branch. Or, you can
# just change the environmental variable for one-off builds in other themes.

html_theme = os.environ.get('HANDOUTS_THEME', 'light')
revealjs_theme = os.environ.get('REVEALJS_THEME', 'revealjs-meggie-2017')

# We need to pull in our Hackbright-specific Sphinx plugins and themes, so add
# our tools directory to our path. Do this in a way that's safe no matter how
# deeply this stuff is imported

sys.path.append(os.path.abspath(os.path.join(__file__, "..", "tools")))

extensions = [
    # Standard parts of Sphinx we're using

    'sphinx.ext.todo',
    'sphinx.ext.ifconfig',
    'sphinx.ext.doctest',

    # Hackbright custom writers for our slideshows and handouts

    'writers.revealjs',
    'writers.handouts',
    'writers.latex',

    # Special directives for Hackbright's build-systems
    # all prefixed with "J", for the original author, Joel Burton

    'jdirectives.newslide',  # Add new slide without a section break
    'jdirectives.incremental',  # Support for RevealJS fragments
    'jdirectives.interslide',  # Adds Reveal-only interstitial slides
    'jdirectives.speakernote',  # Adds Reveal-only speaker notes
    'sphinx.ext.graphviz',  # Sphinx's standard Graphviz directive
    'jdirectives.graphviz',  # Joel's customizations of standard Graphviz directive
    'jdirectives.required',  # break makefiles until directive is read and removed
    'jdirectives.doctest',  # our special override-doctest class

    # In addition, keep reading --- some extensions are added dynamically via
    # feature testing, below
]

# Check for graphviz
#
# About 30% of our lectures/exercises uses Graphviz--so sooner or later,
# you'll need it (see the INSTALL directions). However, some people will use
# this without graphviz. You'll get an error when you build a presentation
# that requires it; our goal here it to provide better feedback for when you
# hit that

try:
    subprocess.check_output("which dot", shell=True)

except subprocess.CalledProcessError:
    logging.warn(
        "Graphviz not installed -- required to build graphs. See INSTALL.rst      <-- READ ME")

# How will generate math equations?
#
# If we have `pdflatex` installed, we'll use that. That makes the prettiest
# math equations and doesn't require any kind of browser support. However,
# some users of our build system won't easily get LaTeX installed, so we
# have a fallback to mathjax. (Our themes include the JS support for MathJax)
# already.

try:
    subprocess.check_output("which pdflatex", shell=True)
    extensions.append('sphinx.ext.imgmath')
    logging.debug("Found imgmath; using it.")

except subprocess.CalledProcessError:
    extensions.append('sphinx.ext.mathjax')
    logging.warn("LaTeX not installed; falling back to mathjax for equations. See INSTALL.rst.")

# Safely see if matplotlib and scipy are installed and, if so, add Sphinx
# extension for it
#
# We use matplotlib and scipy to draw charts and business graphs.
#
# Over time, we'll no doubt use more of it, and everyone will need it --- but for
# now (Nov 2015), this will allow people w/o matplotlib  or scipy to build the
# 98% of our talks that don't rely on it. (As a test case, the comp-sci-ds
# lecture has a graph in it)
#
# For unknown reasons, we need to do this in an odd way, by using the imp module
# rather than doing a more traditional import. For some reason, that nukes sphinx
# finding other writers---perhaps sphinx somehow relies on imports not having failed?
# In any event, while a less conventional way to write this, it works. -- Joel

try:
    imp.find_module('matplotlib')
    extensions.append('matplotlib.sphinxext.plot_directive')

except ImportError:
    # You don't have matplotlib installed, but you're probably still a good person
    extensions.append("jdirectives.noplot")
    logging.warn(
        "Matplotlib not installed; skipping drawing charts. See INSTALL.rst       <-- READ ME")

try:
    imp.find_module('scipy')

except ImportError:
    # You don't have scipy installed, but you're probably still a good person
    logging.warn(
        "Scipy not installed; skipping drawing charts. See INSTALL.rst       <-- READ ME")

# RST Prolog
#
# This stuff is added to every RST file before it's processed

# Colors; you'll also need to add CSS classes to your theme if you want these
# colors to actually appear, of course. You'll also need to edit the LaTeX
# writer to get them to appear in PDFs.

_colors = """
.. role:: red
.. role:: green
.. role:: orange
.. role:: tan
.. role:: blue
.. role:: cmd
.. role:: white
.. role:: gray
.. role:: comment
.. role:: gone
.. role:: inv-red
.. role:: text-heavy
"""

# Additional symbols to include
#
# Be cautious about just adding things here; not all symbols appear in all fonts
# nor will some obscure ones work in LaTeX

# We use some of these to make our curriculum more agile and to help make the
# py2->py3 easier:
#
# |py|      - unstylized name of python executable:    python         or  python3
# |pyi|     - emphasized-name:                         `python`       or  `python3`
# |pycmd|   - as command, for inside console blocks    `python`:cmd:  or  `python3`:cmd:
# |pyname|  - not as exec, but friendly name           Python         or  Python 3

# PY3: make sure these get changed for Python 3 :)

_symbols = """
.. |nbsp|      unicode:: U+000A0 .. NONBREAKING SPACE
.. |rarr|      unicode:: U+02192 .. RIGHTWARDS ARROW
.. |larr|      unicode:: U+02190 .. LEFTWARDS ARROW
.. |darr|      unicode:: U+02193 .. DOWNWARDS ARROW
.. |lrarr|     unicode:: U+02194 .. LEFT RIGHT ARROW
.. |plus|      unicode:: U+0002B .. PLUS SIGN
.. |times|     unicode:: U+000D7 .. MULTIPLICATION SIGN
.. |check|     unicode:: U+02713 .. CHECK MARK
.. |approx|    unicode:: U+02248 .. ALMOST EQUAL TO
.. |sub2|      unicode:: U+02082 .. SUBSCRIPT 2
.. |super2|    unicode:: U+000B2 .. SUPERSCRIPT 2
.. |spades|    unicode:: U+02660 .. SPADES
.. |hearts|    unicode:: U+02665 .. HEARTS
.. |diamonds|  unicode:: U+02666 .. DIAMONDS
.. |clubs|     unicode:: U+02663 .. CLUBS
.. |py|        replace:: python
.. |pyi|       replace:: `python`
.. |pycmd|     replace:: `python`:cmd:
.. |ipy|       replace:: python
.. |ipyi|      replace:: `python`:cmd:
.. |ipycmd|    replace:: `python`:cmd:
.. |ipyname|   replace:: Python
.. |editor|    replace:: subl
.. |editori|   replace:: `subl`
.. |editcmd|   replace:: `subl`:cmd:
.. |editorname|  replace:: Sublime Text
.. |pip|       replace:: pip
.. |pipi|      replace:: `pip`
.. |pipcmd|    replace:: `pip`:cmd:
.. |venv|      replace:: virtualenv
.. |venvi|     replace:: `virtualenv`
.. |venvcmd|   replace:: `virtualenv`:cmd:
"""

# A new role for raw output that should only appear in HTML, and a
# directive that causes a linebreak <br> to appear only in revealjs
# This is useful for when we have a long line that we don't need to break in
# handouts-html or LaTeX, but looks better broken in RevealJS. Note: the
# handouts CSS needs to make this display:none

_reveal_br = """
.. role:: raw-reveal(raw)
   :format: html
.. |reveal-br| replace:: :raw-reveal:`<br>`
"""

# Concatenate that, the only thing that matters is what appears in rst_prolog itself
rst_prolog = _colors + _reveal_br
rst_epilog = _symbols

# General options; these are pretty standard. Don't change!

templates_path = ['_templates']
master_doc = 'index'
html_show_sourcelink = False
html_show_sphinx = False
html_use_index = False
html_domain_indices = False
html_scaled_image_link = False
html_copy_source = False
html_add_permalinks = ""
pygments_style = 'sphinx'
html_theme_path = [
    os.path.abspath(os.path.join(__file__, '..', 'tools', 'themes'))
]

# Don't build RST files in the directories

exclude_patterns = ['_build', 'rubric', 'skit.rst', '**/rubric', '**/skit', '**/*-demo', 'meta'] # , 'solution/*']

# When we use dvipng to make equations, how should they appear?

revealjs_imgmath_dvipng_args = ['-gamma', '1.5', '-D', '275']
pngmath_dvipng_args = ['-gamma', '1.5', '-D', '125']
pngmath_add_tooltips = False

# LaTeX styles

latex_logo = os.path.abspath(os.path.join(__file__, "..", "tools", "themes", "latex-hackbright", 'hb-logo.pdf'))
latex_elements = {
    'pointsize': '12pt',
    'releasename': '',
    'date': '',
    'fontpkg': '\\usepackage[default,osfigures,scale=0.95]{opensans} \\usepackage{inconsolata}',
    'figure_align': 'H',
    'preamble': """
\\usepackage{amssymb}% http://ctan.org/pkg/amssymb   % needed for checkmark character
\\usepackage{soul}                                   % needed for st (strikeout)

\\definecolor{red}{RGB}{221, 0, 0}
\\definecolor{green}{RGB}{51, 187, 51}
\\definecolor{orange}{RGB}{255, 136, 0}
\\definecolor{tan}{RGB}{170, 136, 85}
\\definecolor{blue}{RGB}{34, 136, 204}
\\definecolor{gray}{RGB}{102, 102, 102}

\\DeclareUnicodeCharacter{2190}{$\\leftarrow$}
\\DeclareUnicodeCharacter{2194}{$\\leftrightarrow$}
\\DeclareUnicodeCharacter{2248}{$\\approx$}
\\DeclareUnicodeCharacter{2713}{$\\checkmark$}

% \\floatplacement{figure}{H} % figures should stick to their text
% \\floatplacement{literal-block}{H} % same with literal-blocks
    """
}
latex_show_urls = 'footnote'
latex_docclass = {
    'manual': 'report',
    'howto': 'article',
}
# There are too many chapters to write them out; use numbers instead
latex_elements['fncychap'] = r'\usepackage[Sonny]{fncychap}'


# Graphviz defaults

graphviz_dot_args = ['-Gmargin=0.2',   # less whitespace around graphs for PDFs!
                     '-Nfontname=Helvetica',   # because we're hipsters
                     '-Gfontname=Helvetica',
                     '-Efontname=Helvetica',
                     '-Npenwidth=0.5']
graphviz_output_format = 'svg'

# Matplotlib defaults (don't show the links to the source code or different formats of graphs)

plot_html_show_source_link = False
plot_html_show_formats = False
plot_formats = ['png', 'pdf']

# Don't whinge about broken links to flask servers that aren't running

linkcheck_ignore = [r'http://localhost:', r'http://127\.0\.0\.1']
linkcheck_anchors = False


epub_author = "Joel Burton"
epub_lanauge = "en"
epub_publisher = "Hackbright Academy"
epub_theme_options = {'footer': False}

# Oh my god, this is the worst hack ever --- but stupidly, the matplotlib people
# seem to have forgotten to put classes on the LaTeX output for their plot command.
# Bug filled in their tracker, but for now, let's monkey patch:

if 'matplotlib.sphinxext.plot_directive' in extensions:
    from matplotlib.sphinxext import plot_directive

    plot_directive.TEMPLATE = """
{{ source_code }}

{{ only_html }}

   {% if source_link or (html_show_formats and not multi_image) %}
   (
   {%- if source_link -%}
   `Source code <{{ source_link }}>`__
   {%- endif -%}
   {%- if html_show_formats and not multi_image -%}
     {%- for img in images -%}
       {%- for fmt in img.formats -%}
         {%- if source_link or not loop.first -%}, {% endif -%}
         `{{ fmt }} <{{ dest_dir }}/{{ img.basename }}.{{ fmt }}>`__
       {%- endfor -%}
     {%- endfor -%}
   {%- endif -%}
   )
   {% endif %}

   {% for img in images %}
   .. figure:: {{ build_dir }}/{{ img.basename }}.png
      {% for option in options -%}
      {{ option }}
      {% endfor %}

      {% if html_show_formats and multi_image -%}
        (
        {%- for fmt in img.formats -%}
        {%- if not loop.first -%}, {% endif -%}
        `{{ fmt }} <{{ dest_dir }}/{{ img.basename }}.{{ fmt }}>`__
        {%- endfor -%}
        )
      {%- endif -%}

      {{ caption }}
   {% endfor %}

{{ only_latex }}

   {% for img in images %}
   {% if 'pdf' in img.formats -%}
   .. image:: {{ build_dir }}/{{ img.basename }}.pdf
      {% for option in options -%}
      {{ option }}
      {% endfor %}
   {% endif -%}
   {% endfor %}

{{ only_texinfo }}

   {% for img in images %}
   .. image:: {{ build_dir }}/{{ img.basename }}.png
      {% for option in options -%}
      {{ option }}
      {% endfor %}

   {% endfor %}
"""


