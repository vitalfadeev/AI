def read( request ):
    """ Read data from DB
        HTTP params:
            'from_id'   0     Start ID.
            'format'    csv   Ouyput format: csv | xls | json | xml
        :return: file
    """
    from_id = request.args.get("from_id", None)
    format  = request.args.get("format", FORMAT_CSV)

    # read data from DB to [[],[],]
    data = ProcessRead(ExportLinesAfterPrimaryKey=from_id, FormatOutput=format)
    if format == FORMAT_CSV:
        return Response(
            data,
            mimetype="text/csv",
            headers={"Content-disposition":"attachment; filename={}.csv".format(settings.TABLENAME)})

    elif format == FORMAT_XLS:
        return Response(
            data,
            mimetype="application/xls",
            headers={"Content-disposition":"attachment; filename={}.xls".format(settings.TABLENAME)})

    elif format == FORMAT_XLSX:
        return Response(
            data,
            mimetype="application/xlsx",
            headers={"Content-disposition":"attachment; filename={}.xlsx".format(settings.TABLENAME)})

    elif format == FORMAT_JSON:
        return Response(
            data,
            mimetype="application/json",
            headers={"Content-disposition":"attachment; filename={}.json".format(settings.TABLENAME)})

    elif format == FORMAT_XML:
        return Response(
            data,
            mimetype="application/xml",
            headers={"Content-disposition":"attachment; filename={}.xml".format(settings.TABLENAME)})

    else:
        raise Exception("unsupported")
