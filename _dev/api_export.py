import requests

URL='http://ai.local-ixioo.com/api/machine/16/InputLines?format=csv'
API_KEY="b5726b6b3c50644d52921acc3a52c09864a18143"

with requests.session() as client:
    response = client.get( URL, headers={"Authorization": f"Token {API_KEY}"} )
    print( "response.status_code: ", response.status_code )
    print( "response.text:" )
    print( response.text )

