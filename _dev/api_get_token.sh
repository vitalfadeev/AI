#!/bin/sh

curl -v -X POST -d '{"username":"username@gmail.com","password":"********"}'  -H "Content-Type: application/json" http://ai.ixioo.com/api-token-auth/
