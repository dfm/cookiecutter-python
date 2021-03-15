#!/usr/bin/env python

# Inspired by:
# https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/

import codecs
import os
import re

{% if cookiecutter.pybind11_extensions %}from pybind11.setup_helpers import Pybind11Extension, build_ext
{% endif -%}
from setuptools import find_packages, setup

# PROJECT SPECIFIC

NAME = "{{ cookiecutter.package_name }}"
PACKAGES = find_packages(where="src")
META_PATH = os.path.join(
    "src", "{{ cookiecutter.module_name }}", "__init__.py"
)
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
]
INSTALL_REQUIRES = [
{%- if cookiecutter.required_dependencies %}
{%- for req in cookiecutter.required_dependencies.split(',') %}
    "{{ req.strip() }}",{% endfor %}
{%- endif %}
]
EXTRA_REQUIRE = {
    "docs": [
    {%- for req in cookiecutter.docs_dependencies.split(',') %}
        "{{ req.strip() }}",{% endfor %}
    ],
    {%- if cookiecutter.optional_dependencies %}
    "all": [
    {%- for req in cookiecutter.optional_dependencies.split(',') %}
        "{{ req.strip() }}",{% endfor %}
    ],
    {%- endif %}
    {%- if cookiecutter.test_dependencies %}
    "test": [
    {%- for req in cookiecutter.test_dependencies.split(',') %}
        "{{ req.strip() }}",{% endfor %}
    ],
    {%- endif %}
}
{% if cookiecutter.pybind11_extensions %}
{%- if cookiecutter.include_dirs %}
include_dirs = [
{%- for dirname in cookiecutter.include_dirs.split(',') %}
    "{{ dirname.strip() }}",{% endfor %}
]
{%- endif %}
ext_modules = [
{%- for ext in cookiecutter.pybind11_extensions.split(',') %}
    Pybind11Extension(
        "{{ ext.strip() }}",
        ["src/{{ ext.strip().replace('.', '/') }}.cpp"],
        {% if cookiecutter.include_dirs %}include_dirs=include_dirs,
        {% endif -%}
        language="c++",
    ),{% endfor %}
]
{%- endif %}

# END PROJECT SPECIFIC


HERE = os.path.dirname(os.path.realpath(__file__))


def read(*parts):
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


def find_meta(meta, meta_file=read(META_PATH)):
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta), meta_file, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


if __name__ == "__main__":
    setup(
        name=NAME,
        use_scm_version={
            "write_to": os.path.join(
                "src",
                "{{ cookiecutter.module_name }}",
                "{{ cookiecutter.module_name }}_version.py"
            ),
            "write_to_template": '__version__ = "{version}"\n',
        },
        author=find_meta("author"),
        author_email=find_meta("email"),
        maintainer=find_meta("author"),
        maintainer_email=find_meta("email"),
        url=find_meta("uri"),
        license=find_meta("license"),
        description=find_meta("description"),
        long_description=read("README.md"),
        long_description_content_type="text/markdown",
        packages=PACKAGES,
        package_dir={"": "src"},
        include_package_data=True,
        python_requires=">={{ cookiecutter.minimum_python_version }}",
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRA_REQUIRE,
        classifiers=CLASSIFIERS,
        zip_safe=False,
        {%- if cookiecutter.pybind11_extensions %}
        ext_modules=ext_modules,
        cmdclass={"build_ext": build_ext},{% endif %}
    )
