# Doc
    
    graph/
        templates/
            page.html
            
    static/
        react/
            *.js


    REST
        GET /machine/<id>/graph
        GET /machine/<id>/graph/<id>

    
    DB:
        Graph


    PROTOCOL:
        request: 
            GET { params }
        response: 
            200 { result: div }
            400 {}
            404 {}
        

    React -> REST -> Django
    
    