from rest_framework import renderers


class CSVRenderer( renderers.BaseRenderer ):
    media_type = 'text/csv'
    format = 'csv'

    def render(self, data, media_type=None, renderer_context=None):
        return data


class XLSRenderer( renderers.BaseRenderer ):
    media_type = 'application/xls'
    format = 'xls'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data


class XLSXRenderer( renderers.BaseRenderer ):
    media_type = 'application/xlsx'
    format = 'xlsx'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data


class XMLRenderer( renderers.BaseRenderer ):
    media_type = 'application/xml'
    format = 'xml'
    charset = None

    def render(self, data, media_type=None, renderer_context=None):
        return data


