import requests

URL='http://ai.ixioo.com/api/machine/16/InputLines?format=xls'
API_KEY="b5726b6b3c50644d52921acc3a52c09864a18143"
outfile = "/tmp/1.xls"

with requests.session() as client:
    response = client.get( URL, headers={"Authorization": f"Token {API_KEY}"} )
    print( "response.status_code: ", response.status_code )
    print( "response.content length:", len(response.content), "bytes" )

    with open( outfile, 'wb' ) as f:
        f.write( response.content )
