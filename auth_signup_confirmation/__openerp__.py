# -*- coding: utf-8 -*-
{
    'name': 'Auth signup confirmation',
    'version': '1.0.0',
    'author': 'IT-Projects LLC',
    'website': "https://it-projects.info",
    'license': 'GPL-3',
    'depends': [
        'auth_signup',
    ],
    'data':['data/config.xml', 'views/thankyou.xml','data/email.xml'],
    'installable': True,
    'post_init_hook': 'init_auth',
}
