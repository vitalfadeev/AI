import requests


URL='http://ai.local-ixioo.com/api/machine/1/InputLines'
API_KEY="b5726b6b3c50644d52921acc3a52c09864a18143"

with requests.session() as client:
    files = { 'file': open( '../machine/tests/1.csv', 'rb' ) }

    response = client.post(
        URL,
        headers={"Authorization": f"Token {API_KEY}"},
        files=files
    )

    if response.status_code == 200:
        print( "OK" )
