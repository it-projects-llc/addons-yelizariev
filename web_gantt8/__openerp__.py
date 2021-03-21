# -*- coding: utf-8 -*-
# Copyright (c) 2004-2015 Odoo S.A.
# Copyright 2016 Pavel Romanchenko
# Copyright 2016 Ilmir Karamov <https://it-projects.info/team/ilmir-k>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0.html).
{
    "name": """Gantt view from odoo 8""",
    "summary": """Ported view from odoo 8""",
    "category": "Hidden",
    "images": [],
    "version": "1.0.0",

    "author": "IT-Projects LLC, Pavel Romanchenko",
    "website": "https://twitter.com/OdooFree",
    "license": "AGPL-3",

    "depends": [
        "web",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        'views/web_gantt.xml',
    ],
    "qweb": [
        'static/src/xml/*.xml',
    ],
    "demo": [],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "installable": True,
    "auto_install": False,
    "application": False,
}
