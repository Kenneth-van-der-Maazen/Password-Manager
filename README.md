# Python - Password Manager  
# Author: Kenneth van der Maazen  
# Date: 08-07-2025  
---
Select option:
    (1) Create a new key
    (2) Load existing key
    (q) Quit

    1 - Enter key name: 
    2 - Enter key name: 

    (3) Create new password file
    (4) Load existing password file
    (q) Quit

    3 - Name password file: 
    4 - Password file: 

    (5) Add a new password
    (6) Retrieve a password
    (q) Quit

    5 - Name: 
    5 - Password: 
    6 - Name: 


-- Password Manager --
 
.keys
.list

Key: 
    \ if !key: 
        Key not found!
        Create a new key?
        [YES] / [NO]
        \ [YES] = Enter key name: 
        \ [NO] = Back to -> Key: 

    \ if key:
        Key file: {path}
        Selected list: [NONE] file
        Select an option:
            (1) Create new list
            (2) Load passwords from list
            
            \ 1 Passwords list name: 
            \ 2 Load file name: 

        \ if key && password_list:
            Key file: {path}
            Selected list: {path}
            Select an option:
                (3) Add new password
                (4) Get login credentials
                (5) View all passwords
                (q) Quit

                \ 3 Site: 
                    Username: 
                    Password: 