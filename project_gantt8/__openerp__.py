# -*- coding: utf-8 -*-
{
    "name": """Gantt view for Projects""",
    "summary": """Restores feature from odoo 8.0""",
    "category": "Project",
    "images": ['images/gantt_view.png'],
    "version": "1.0.0",

    "author": "IT-Projects LLC, Pavel Romanchenko",
    "website": "https://twitter.com/OdooFree",
    "license": "AGPL-3",

    "depends": [
        "project",
        "web_gantt8",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        'project_view.xml'
    ],
    "qweb": [],
    "demo": [],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "installable": True,
    "auto_install": False,
    "application": False,
}
