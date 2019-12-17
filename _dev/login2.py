import requests
URL1='http://ai.local-ixioo.com/admin/'
URL2='http://ai.local-ixioo.com/admin/login/?next=/admin/'
UN='admin@localhost'
PWD='777'
client = requests.session()

# Retrieve the CSRF token first
client.get(URL1)  # sets the cookie
csrftoken = client.cookies['csrftoken']

login_data = dict(username=UN, password=PWD, csrfmiddlewaretoken=csrftoken)
r = client.post(URL2, data=login_data, headers={"Referer": "foo"})

print( r.text )
