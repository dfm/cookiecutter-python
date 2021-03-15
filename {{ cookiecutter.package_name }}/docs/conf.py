#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution("{{ cookiecutter.module_name }}").version
except DistributionNotFound:
    __version__ = "dev"


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    {%- if "myst-nb" in cookiecutter.docs_dependencies %}
    "myst_nb",{% endif %}
]
autodoc_mock_imports = []

project = "{{ cookiecutter.package_name }}"
copyright = "{{ cookiecutter.year }} {{ cookiecutter.author_name }}"
version = __version__
release = __version__

exclude_patterns = ["_build"]
html_static_path = ["_static"]
html_theme = "{{ cookiecutter.sphinx_theme }}"
html_title = "{{ cookiecutter.package_name }}"
html_show_sourcelink = False
html_baseurl = "https://{{ cookiecutter.module_name }}.readthedocs.io/en/latest/"
{% if cookiecutter.sphinx_theme == "sphinx_book_theme"  -%}
html_theme_options = {
    "path_to_docs": "docs",
    "repository_url": "https://github.com/{{ cookiecutter.github_project }}",
    "repository_branch": "{{ cookiecutter.default_branch }}",
    "launch_buttons": {
        "binderhub_url": "https://mybinder.org",
        "colab_url": "https://colab.research.google.com",
        "notebook_interface": "jupyterlab",
    },
    "use_edit_page_button": True,
    "use_issues_button": True,
    "use_repository_button": True,
    "use_download_button": True,
}
{%- endif %}
