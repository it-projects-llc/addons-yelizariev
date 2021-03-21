# -*- coding: utf-8 -*-
{
    'name': "Task Search Custom",
    'summary': """Searching for tasks includes "Messages" and "Description" fields""",
    'author': "IT-Projects LLC, Ilmir Karamov",
    'license': 'LGPL-3',
    'website': "https://twitter.com/OdooFree",
    'version': '1.1.0',
    'category': 'Project',
    'images': ['images/task_search.png'],
    'depends': ['project'],
    'data': [
        'views/project_task_search_custom.xml',
    ],
    'installable': True
}
