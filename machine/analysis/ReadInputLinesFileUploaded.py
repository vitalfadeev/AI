import xml.etree.ElementTree as ET
import pandas as pd


def GetDataFrameFromFileData(file):
    """
    :param file: Any valid string path is acceptable. The string could be a URL.
                 Valid URL schemes include http, ftp, s3, and file.
                 For file URLs, a host is expected. A local file could be: file://localhost/path/to/table.csv.
                 If you want to pass in a path object, pandas accepts any os.PathLike.
                 By file-like object, we refer to objects with a read() method,
                 such as a file handler (e.g. via builtin open function) or StringIO.
    """

    # Get file name
    if isinstance(file, str):
        filename = file
    else:
        filename = file.name

    # Read csv file and convert to pandas data frame
    if filename.endswith('csv'):
        data_frame = pd.read_csv(file)

    # Read xls file and convert to pandas data frame
    elif filename.endswith('xls'):
        data_frame = pd.read_excel(file)

    # Read xlsx file and convert to pandas data frame
    elif filename.endswith('xlsx'):
        data_frame = pd.read_excel(file)

    # Read json file and convert to pandas data frame
    elif filename.endswith('json'):
        data_frame = pd.read_json(file, orient='records')

    # Read xml file and convert to pandas data frame
    elif filename.endswith('xml'):
        # If file is a url - open the url and read.
        if isinstance(file, str):
            file = open(file).read()

        # If file is a file-like object - just read it
        else:
            file = file.read()
        data_frame = GetFileDataXML(file)

    else:
        raise Exception("Unsuppported")

    return data_frame


def GetFileDataXML(file):
    """
    Read xml file with data
    :param file: string with xml data
    :return: pandas Dataframe
    """

    class XML2DataFrame:
        def __init__(self, xml_data):
            self.root = ET.XML(xml_data)

        def parse_root(self, root):
            return [self.parse_element(child) for child in iter(root)]

        def parse_element(self, element, parsed=None):
            if parsed is None:
                parsed = dict()
            for key in element.keys():
                parsed[key] = element.attrib.get(key)
            if element.text:
                parsed[element.tag] = element.text
            for child in list(element):
                self.parse_element(child, parsed)
            return parsed

        def process_data(self):
            structure_data = self.parse_root(self.root)
            return pd.DataFrame(structure_data)

    # parse text to XML
    xml2df = XML2DataFrame(file)

    # parse XMl to pandas.DataFrame
    df = xml2df.process_data()

    return df


if __name__ == '__main__':

    import time

    print('Read csv by url\n',
          GetDataFrameFromFileData('C:\\Users\\ArtSoft-Srv-1\\OneDrive - hk sar baomin inc\\IXI oo\\AI-WWW\\ReadInputLinesFileUploaded\\tests\\test.csv'),
          '\n')
    time.sleep(3)
    print('Read xls by url\n',
          GetDataFrameFromFileData('C:\\Users\\ArtSoft-Srv-1\\OneDrive - hk sar baomin inc\\IXI oo\\AI-WWW\\ReadInputLinesFileUploaded\\tests\\test.xls'),
          '\n')
    time.sleep(3)
    print('Read xlsx by url\n',
          GetDataFrameFromFileData('C:\\Users\\ArtSoft-Srv-1\\OneDrive - hk sar baomin inc\\IXI oo\\AI-WWW\\ReadInputLinesFileUploaded\\tests\\test.xlsx'),
          '\n')
    time.sleep(3)
    print('Read json by url\n',
          GetDataFrameFromFileData('C:\\Users\\ArtSoft-Srv-1\\OneDrive - hk sar baomin inc\\IXI oo\\AI-WWW\\ReadInputLinesFileUploaded\\tests\\test.json'),
          '\n')
    time.sleep(3)
    print('Read xml by url\n',
          GetDataFrameFromFileData('C:\\Users\\ArtSoft-Srv-1\\OneDrive - hk sar baomin inc\\IXI oo\\AI-WWW\\ReadInputLinesFileUploaded\\tests\\test.xml'),
          '\n')
    time.sleep(3)
    print('Read csv from file\n',
          GetDataFrameFromFileData(open('C:\\Users\\ArtSoft-Srv-1\\OneDrive - hk sar baomin inc\\IXI oo\\AI-WWW\\ReadInputLinesFileUploaded\\tests\\test.csv', 'rb')),
          '\n')
    time.sleep(3)
    print('Read xls from file\n',
          GetDataFrameFromFileData(open('C:\\Users\\ArtSoft-Srv-1\\OneDrive - hk sar baomin inc\\IXI oo\\AI-WWW\\ReadInputLinesFileUploaded\\tests\\test.xls', 'rb')),
          '\n')
    time.sleep(3)
    print('Read xlsx from file\n',
          GetDataFrameFromFileData(open('C:\\Users\\ArtSoft-Srv-1\\OneDrive - hk sar baomin inc\\IXI oo\\AI-WWW\\ReadInputLinesFileUploaded\\tests\\test.xlsx', 'rb')),
          '\n')
    time.sleep(3)
    print('Read json from file\n',
          GetDataFrameFromFileData(open('C:\\Users\\ArtSoft-Srv-1\\OneDrive - hk sar baomin inc\\IXI oo\\AI-WWW\\ReadInputLinesFileUploaded\\tests\\test.json', 'rb')),
          '\n')
    time.sleep(3)
    print('Read xml from file\n',
          GetDataFrameFromFileData(open('C:\\Users\\ArtSoft-Srv-1\\OneDrive - hk sar baomin inc\\IXI oo\\AI-WWW\\ReadInputLinesFileUploaded\\tests\\test.xml', 'rb')),
          '\n')
