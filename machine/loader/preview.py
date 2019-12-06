from machine.datalistener import GetFileData


def get_head( filename, n=5 ):
    pd = GetFileData( filename )

    head = pd.head( n )

    return head


def get_tail( filename, n=5 ):
    pd = GetFileData( filename )

    tail = pd.tail( n )

    return tail


def get_lines( filename, offset=0, limit=5 ):
    pd = GetFileData( filename )

    lines = pd.iloc[ offset:offset+limit ]

    return lines

