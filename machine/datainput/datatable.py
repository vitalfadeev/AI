from datetime import datetime
from django_datatables_view.base_datatable_view import BaseDatatableView


class DTView(BaseDatatableView):
    """
    Base class for View for using with jQuery.DataTable
    Return JSON
    """
    model = None
    columns = []
    order_columns = []
    datetime_format = "%Y-%m-%d %H:%M"

    def initialize(self, *args, **kwargs):
        super(DTView, self).initialize(*args, **kwargs)
        # fix jQuery.DataTable parameters class detection
        self.pre_camel_case_notation = False


    def render_column(self, row, column, *args, **kwargs):
        res =  super(DTView, self).render_column(row, column, *args, **kwargs)
        value = getattr(row, column)

        # fix datetime field render
        if isinstance(value, datetime):
            return value.strftime(self.datetime_format)
        else:
            return res


class DtFileView(BaseDatatableView):
    """
    Base class for View for using with jQuery.DataTable
    Return JSON
    """
    model = None
    columns = []
    order_columns = []
    datetime_format = "%Y-%m-%d %H:%M"

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        # fix jQuery.DataTable parameters class detection
        self.pre_camel_case_notation = False


    def render_column(self, row, column, *args, **kwargs):
        res =  super().render_column(row, column, *args, **kwargs)
        value = getattr(row, column)

        # fix datetime field render
        if isinstance(value, datetime):
            return value.strftime(self.datetime_format)
        else:
            return res

