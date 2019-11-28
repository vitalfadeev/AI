import os

if __name__ == "__main__":
    import requests

    with open('machine/tests/test-2.xls','rb') as f:
        files = {'input_file': f}
        values = {
            'name': "Test 1",
            'desc': "Desc 11"
        }

        r = requests.post( 'http://localhost:8000/api/machine/', files=files, data=values )

        print( r.status_code )
        # 201 - Created
        print( r.text )
