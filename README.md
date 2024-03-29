## Installation 
Full description in [INSTALL.md](INSTALL.md)

Script:

    ./1-install-<platform>.sh


## Docs:

- [Django workflow](docs/django-workflow.png)
- [Showing Tensorboard](docs/TensorBoard.png)
- [Creating machine (REST API)](docs/AI-creating-machine.png)  
- [Access-to-server-by-SSH-Key](docs/Access-to-server-by-SSH-Key.md)

    
## Deploy

For deploy without password, need add SSH RSA public key to dev-server.
See [Access-to-server-by-SSH-Key](docs/Access-to-server-by-SSH-Key.md)


Then can to run ./deploy.sh  

    ./deploy.sh


## Send logic
- phase 1 (uploading)
    - upload file xls / csv
    - read
      - detect column names 
      - detect column types
    - create SQL table
    - insert data into SQL


- phase 2 (PreAnalyser)
    - run PreAnalyser
    - if OK:
        - go to phase 3 
    - if FAIL: 
        - show errors

 
- phase 3 (NN parameters)
