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
import os
import sys

sys.path.insert(0, os.path.abspath("../.."))


# -- Project information -----------------------------------------------------

project = "Maha"
copyright = "2021, Mohammad Al-Fetyani"
author = "Mohammad Al-Fetyani"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx_copybutton",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx.ext.todo",
    "sphinx.ext.doctest",
    "autoapi.extension",
]

autoapi_type = "python"
autoapi_dirs = ["../../maha"]
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]
autoapi_add_toctree_entry = False
autoapi_python_class_content = "both"
autoapi_template_dir = "_autoapi_templates"
autoapi_keep_files = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# Automatically generate stub pages when using the .. autosummary directive
autosummary_generate = True
add_module_names = False

# generate documentation from type hints
autodoc_typehints = "description"
autoclass_content = "both"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_autoapi_templates"]
highlight_language = "python"

copybutton_prompt_text = ">>> "
# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_static_path = ["_static"]

html_theme = "furo"

html_theme_options = {
    "light_css_variables": {
        "color-content-foreground": "#232B35",
        "color-background-primary": "#FCF5EE",
        "color-background-secondary": "#F9F0E9",
        "color-background-border": "#F5DBBF",
        "color-sidebar-background": "#F8EBDB",
        "color-brand-content": "#35A5F3",
        "color-brand-primary": "#0073ED",
        "color-background-hover": "#F7E7D1",
        "color-link": "#E5525C",
        "color-link--hover": "#FF2433",
        "color-inline-code-background": "#F8EBDB",
        "color-highlighted-background": "#F5DBBF",
    },
    "dark_css_variables": {
        "color-content-foreground": "#ffffffd9",
        "color-background-primary": "#131416",
        "color-background-border": "#303335",
        "color-sidebar-background": "#1a1c1e",
        "color-brand-content": "#2196f3",
        "color-brand-primary": "#87c2a5",
        "color-link": "#E5525C",
        "color-link--hover": "#FF2433",
        "color-inline-code-background": "#383838",
    },
}
html_title = "Maha"
pygments_style = "default"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".


members_to_watch = [
    "function",
]
