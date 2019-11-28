import os

if __name__ == "__main__":
    import requests

    values = {
        'Project_Description': "Desc 11"
    }

    r = requests.put( 'http://api.local-ixioo.com//api/machine/3/',data=values )

    print( r.status_code )
    # 201 - Created
    print( r.text )
