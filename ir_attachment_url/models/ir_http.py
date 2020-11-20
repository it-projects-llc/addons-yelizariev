# Copyright 2016-2018 Ildar Nasyrov <https://it-projects.info/team/iledarn>
# Copyright 2017 Dinar Gabbasov <https://it-projects.info/team/GabbasovDinar>
# Copyright 2016-2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
import base64
import hashlib
import mimetypes
import os
import re

from odoo import models
from odoo.exceptions import AccessError
from odoo.http import STATIC_CACHE, request
from odoo.modules.module import get_module_path, get_resource_path
from odoo.tools import consteq, pycompat
from odoo.tools.mimetypes import guess_mimetype


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def binary_content(
        cls,
        xmlid=None,
        model="ir.attachment",
        id=None,
        field="datas",
        unique=False,
        filename=None,
        filename_field="datas_fname",
        download=False,
        mimetype=None,
        default_mimetype="application/octet-stream",
        access_token=None,
        env=None,
    ):  # pylint: disable=redefined-builtin
        """ Get file, attachment or downloadable content

        If the ``xmlid`` and ``id`` parameter is omitted, fetches the default value for the
        binary field (via ``default_get``), otherwise fetches the field for
        that precise record.

        :param str xmlid: xmlid of the record
        :param str model: name of the model to fetch the binary from
        :param int id: id of the record from which to fetch the binary
        :param str field: binary field
        :param bool unique: add a max-age for the cache control
        :param str filename: choose a filename
        :param str filename_field: if not create an filename with model-id-field
        :param bool download: apply headers to download the file
        :param str mimetype: mintype of the field (for headers)
        :param str default_mimetype: default mintype if no mintype found
        :param str access_token: optional token for unauthenticated access
                                 only available  for ir.attachment
        :param Environment env: by default use request.env
        :returns: (status, headers, content)
        """
        env = env or request.env
        # get object and content
        obj = None
        if xmlid:
            obj = env.ref(xmlid, False)
        elif id and model in env.registry:
            obj = env[model].browse(int(id))

        # obj exists
        if not obj or not obj.exists() or field not in obj:
            return (404, [], None)

        # access token grant access
        if model == "ir.attachment" and access_token:
            obj = obj.sudo()
            if not consteq(obj.access_token or u"", access_token):
                return (403, [], None)

        # check read access
        try:
            last_update = obj["__last_update"]
        except AccessError:
            return (403, [], None)

        status, headers, content = None, [], None

        # attachment by url check
        module_resource_path = None
        if model == "ir.attachment" and obj.type == "url" and obj.url:
            url_match = re.match(
                r"^/(\w+)/(.+)$", obj.url
            )  # pylint: disable=anomalous-backslash-in-string
            if url_match:
                module = url_match.group(1)
                module_path = get_module_path(module)
                module_resource_path = get_resource_path(module, url_match.group(2))
                if module_path and module_resource_path:
                    module_path = os.path.join(
                        os.path.normpath(module_path), ""
                    )  # join ensures the path ends with '/'
                    module_resource_path = os.path.normpath(module_resource_path)
                    if module_resource_path.startswith(module_path):
                        with open(module_resource_path, "rb") as f:
                            content = base64.b64encode(f.read())
                        last_update = pycompat.text_type(  # noqa: F841
                            os.path.getmtime(module_resource_path)
                        )

            if not module_resource_path:
                module_resource_path = obj.url

            if not content:
                status = 301
                content = module_resource_path
        # redefined: begin
        elif (
            model == "ir.attachment"
            and obj.type == "binary"
            and obj.url
            and any(obj.url.startswith(x) for x in ("http://", "https://",))
        ):
            status = 301
            content = obj.url
        # redefined: end
        else:
            content = obj[field] or ""

        # filename
        if not filename:
            if filename_field in obj:
                filename = obj[filename_field]
            if not filename and module_resource_path:
                filename = os.path.basename(module_resource_path)
            if not filename:
                filename = "{}-{}-{}".format(obj._name, obj.id, field)

        # mimetype
        mimetype = "mimetype" in obj and obj.mimetype or False
        if not mimetype:
            if filename:
                mimetype = mimetypes.guess_type(filename)[0]
            if not mimetype and getattr(env[model]._fields[field], "attachment", False):
                # for binary fields, fetch the ir_attachement for mimetype check
                attach_mimetype = env["ir.attachment"].search_read(
                    domain=[
                        ("res_model", "=", model),
                        ("res_id", "=", id),
                        ("res_field", "=", field),
                    ],
                    fields=["mimetype"],
                    limit=1,
                )
                mimetype = attach_mimetype and attach_mimetype[0]["mimetype"]
            if not mimetype:
                mimetype = guess_mimetype(
                    base64.b64decode(content), default=default_mimetype
                )

        # extension
        _, existing_extension = os.path.splitext(filename)
        if not existing_extension:
            extension = mimetypes.guess_extension(mimetype)
            if extension:
                filename = "{}{}".format(filename, extension)

        headers += [("Content-Type", mimetype), ("X-Content-Type-Options", "nosniff")]

        # cache
        etag = bool(request) and request.httprequest.headers.get("If-None-Match")
        retag = (
            '"%s"' % hashlib.md5(pycompat.to_text(content).encode("utf-8")).hexdigest()
        )
        status = status or (304 if etag == retag else 200)
        headers.append(("ETag", retag))
        headers.append(
            ("Cache-Control", "max-age=%s" % (STATIC_CACHE if unique else 0))
        )

        # content-disposition default name
        if download:
            headers.append(("Content-Disposition", cls.content_disposition(filename)))
        return (status, headers, content)
