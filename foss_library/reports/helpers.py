import os
import tempfile
from textwrap import dedent

import pdfkit
from flask import render_template_string


def render_jinja_to_pdf(partial_template, prefix, **kwargs):
    # creating a temporary file to write output to
    fd, pdf_output = tempfile.mkstemp(prefix=prefix, suffix=".pdf")
    os.close(fd)

    template_string = dedent(
        """
        {% extends "pdf_reports_layout.html" %}
        {% block content %}
        {% include "?" %}
        {% endblock %}
        """
    )

    # how else to format?
    template_string = template_string.replace("?", partial_template)

    html_content = render_template_string(
        template_string,
        **kwargs,
    )

    options = {
        "page-size": "Letter",
        "margin-top": "0.75in",
        "margin-right": "0.75in",
        "margin-bottom": "0.75in",
        "margin-left": "0.75in",
        "encoding": "UTF-8",
        "enable-local-file-access": None,
    }
    pdfkit.from_string(html_content, pdf_output, options=options)

    return pdf_output
