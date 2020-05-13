# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
from pkg_resources import get_distribution


# -- Project information -----------------------------------------------------

project = "{{ cookiecutter.project_slug }}"
copyright = "Contributors of {{ cookiecutter.project_slug }}"
author = "Contributors of {{ cookiecutter.project_slug }}"

# The full version, including alpha/beta/rc tags
release = get_distribution("{{ cookiecutter.project_slug }}").version
version = ".".join(release.split(".")[:2])


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.todo",
    "sphinx.ext.doctest",
    "sphinxcontrib.katex",
]

katex_css_path = "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/katex.min.css"
katex_js_path = "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/katex.min.js"
katex_autorender_path = (
    "https://cdn.jsdelivr.net/npm/katex@0.11.1/contrib/auto-render.min.js"
)
katex_inline = [r"\(", r"\)"]
katex_display = [r"\[", r"\]"]
katex_prerender = False
katex_options = ""


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

source_suffix = ".rst"
master_doc = "index"
autosummary_generate = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

napoleon_use_ivar = True

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = True


intersphinx_mapping = {
    "https://docs.python.org/3": None,
}
