# -*- coding: utf-8 -*-
from odoo import fields
import mimetypes
import re


class Binary(fields.Binary):

    def write(self, records, value):
        domain = [
            ('res_model', '=', records._name),
            ('res_field', '=', self.name),
            ('res_id', 'in', records.ids),
        ]
        atts = records.env['ir.attachment'].sudo().search(domain)
        if value and atts.url and atts.type == 'url' and not self.is_url(value):
            atts.write({
                'url': None,
                'type': 'binary',
            })
        if value and self.is_url(value):
            with records.env.norecompute():
                if value:
                    # update the existing attachments
                    atts.write({
                        'url': value,
                        'mimetype': mimetypes.guess_type(value)[0],
                        'datas': None,
                        'type': 'url',
                    })
                    # create the missing attachments
                    for record in (records - records.browse(atts.mapped('res_id'))):
                        atts.create({
                            'name': self.name,
                            'res_model': record._name,
                            'res_field': self.name,
                            'res_id': record.id,
                            'type': 'url',
                            'url': value,
                        })
                else:
                    atts.unlink()
        else:
            super(Binary, self).write(records, value)

    def is_url(self, value):
        return re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', value)


fields.Binary = Binary
