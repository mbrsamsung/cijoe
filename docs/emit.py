#!/usr/bin/env python3
"""
Produce documentation for all cijoe packages
"""
from pathlib import Path
from pprint import pprint

from jinja2 import Template

from cijoe.core.resources import get_resources

DOC_ROOT_PKGS = "packages"

TEMPLATE_PKG_OVERVIEW = """.. _sec-packages:

==========
 Packages
==========

.. toctree::
   :maxdepth: 2

{% for pkg_name, script_name in packages.items() %}
   {{ pkg_name }}/index.rst
{%- endfor %}
   packaging/index.rst
"""

TEMPLATE_PKG_INDEX = """
{{ pkg_name }}
{% set pkg_name_len = pkg_name | length -%}
{{ "=" * pkg_name_len }}

These are the scripts provided in the package, they are listed by the **full**
name that you can use to refer to them in a workflow.

Scripts
-------

.. toctree::
   :maxdepth: 2
   :hidden:

{% for script_name in scripts %}
   scripts/{{ script_name }}.rst
{%- endfor %}
"""

TEMPLATE_SCRIPT_INDEX = """
{% set script_title = pkg_name + '.' + script_name -%}
{% set script_title_len = script_title | length -%}
{{ script_title }}
{{ "~" * script_title_len }}

.. automodule:: cijoe.{{ pkg_name }}.scripts.{{ script_name }}
   :members:
"""


def setup_templates():
    return {
        "pkg_overview": Template(TEMPLATE_PKG_OVERVIEW),
        "pkg_index": Template(TEMPLATE_PKG_INDEX),
        "script_index": Template(TEMPLATE_SCRIPT_INDEX),
    }


def main():
    packages = {}
    templates = setup_templates()

    for key, props in get_resources().get("scripts").items():
        pkg_name, script_name = key.split(".")
        if pkg_name not in packages:
            packages[pkg_name] = []

        packages[pkg_name].append(script_name)
        packages[pkg_name].sort()

    # Create package page
    pkgs_index_rst = Path("source") / DOC_ROOT_PKGS / "index.rst"
    pkgs_index_rst.parent.mkdir(parents=True, exist_ok=True)
    with pkgs_index_rst.open("w") as rst:
        rst.write(templates["pkg_overview"].render(packages=packages))

    for pkg_name, scripts in packages.items():
        pkg_path = Path("source") / DOC_ROOT_PKGS / pkg_name

        # Create package index
        pkg_path.mkdir(parents=True, exist_ok=True)
        pkg_index_rst = pkg_path / "index.rst"
        with pkg_index_rst.open("w") as rst:
            rst.write(templates["pkg_index"].render(pkg_name=pkg_name, scripts=scripts))

        for script_name in scripts:
            script_path = pkg_path / "scripts" / f"{script_name}.rst"

            # Create package index
            script_path.parent.mkdir(parents=True, exist_ok=True)
            with script_path.open("w") as rst:
                rst.write(
                    templates["script_index"].render(
                        pkg_name=pkg_name, script_name=script_name
                    )
                )


if __name__ == "__main__":
    main()
