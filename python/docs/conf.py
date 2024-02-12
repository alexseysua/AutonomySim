# -*- coding: utf-8 -*-
#
# conf.py
#
# Sphinx configuration file.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
#
# Copyright 2024 Nervosys, LLC
#

# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

import sphinx_immaterial
from autonomysim import __version__


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "AutonomySim Python API"
copyright = "Copyright © 2024 Nervosys, LLC"
author = "Nervosys"

# short X.Y version
# version = __version__
version = ""
# full version, including alpha/beta/rc tags
# release = version
release = ""

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# If your documentation needs a minimal Sphinx version, state it here.
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_immaterial",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.mathjax",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

autodoc_default_flags = ["members"]
autosummary_generate = True
autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = 4

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages. This is also used if you do content
# translation via gettext catalogs. Usually you set "language" from the
# command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
# https://jbms.github.io/sphinx-immaterial/customization.html
# see `theme.conf` for more information

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# html_theme = 'alabaster'
html_theme = "sphinx_immaterial"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {}
html_theme_options = {
    "site_url": "https://nervosys.github.io/AutonomySim",
    "repo_url": "https://github.com/nervosys/AutonomySim",
    "repo_name": "AutonomySim",
    "edit_uri": "blob/master/docs",
    "globaltoc_collapse": True,
    "toc_title_is_page_title": False,
    "version_dropdown": True,
    # "version_info": [
    #    {
    #        "version": "https://nervosys.github.io/AutonomySim",
    #        "title": "Main",
    #        "aliases": [],
    #    },
    # ],
    "features": [
        "announce.dismiss",
        "content.code.annotate",
        "content.code.copy",
        "content.tabs.link",
        # 'header.autohide',
        # 'mkdocstrings',
        "navigation.expand",
        # 'navigation.instant',
        "navigation.top",
        # 'navigation.tabs',
        # 'navigation.sections',
        "navigation.instant",
        "navigation.path",
        "navigation.footer",
        # 'navigation.tracking',
        # 'search.highlight',
        "search.suggest",
        "search.share",
        "toc.follow",
        "toc.integrate",
    ],
    "font": {
        "text": "Roboto",
        "code": "Roboto Mono",
    },
    "language": "en",
    "palette": [
        {
            "media": "(prefers-color-scheme)",
            "toggle": {
                "icon": "material/brightness-auto",
                "name": "Switch to light mode",
            },
        },
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "nervosys",
            "toggle": {
                "icon": "material/brightness-7",
                "name": "Switch to dark mode",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "toggle": {
                "icon": "material/brightness-4",
                "name": "Switch to system preference",
            },
        },
    ],
    "favicon": "media/images/rune.svg",
    "icon": {
        "logo": "material/book-open-page-variant",
        "repo": "fontawesome/brands/git-alt",
        "edit": "material/pencil",
        "view": "material/eye",
    },
    "social": [
        {
            "icon": "fontawesome/brands/github-alt",
            "link": "https://github.com/nervosys/AutonomySim",
        },
        {
            "icon": "fontawesome/brands/discord",
            "link": "https://discord.gg/x84JXYje",
        },
        {
            "icon": "fontawesome/brands/twitter",  # x-twitter, square-x-twitter must be added to sphinx-immaterial
            "link": "https://x.com/nervosys",
        },
    ],
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "AutonomySimDoc"


# -- Options for LaTeX output ------------------------------------------------

# Elements
latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "AutonomySim.tex",
        "AutonomySim Documentation",
        "Adam Erickson",
        "manual",
    ),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "AutonomySim", "AutonomySim Documentation", [author], 1)]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "AutonomySim",
        "AutonomySim Documentation",
        author,
        "AutonomySim",
        "The simulation engine for autonomous systems",
        "Miscellaneous",
    ),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
# epub_identifier = ''

# A unique identification for the text.
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ["search.html"]


# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {"https://docs.python.org/": None}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True
