On local machine

    ssh-keygen

output:
    
    Generating public/private rsa key pair.
    Enter file in which to save the key (/home/username/.ssh/id_rsa):
    ...

then

    ssh-copy-id root@94.23.192.197

output

    Password: 
    
    Number of key(s) added: 1
    
    Now try logging into the machine, with:   "ssh 'root@94.23.192.197'"
    and check to make sure that only the key(s) you wanted were added.


Done.
