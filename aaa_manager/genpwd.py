from random import choice
 
ALLOWED = ['abcdefghijklmnopqrstuvwxyz',
           '0123456789',
           'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
           '@^!$?'
            ]
 
 
def genpwd(l=20):
    """
    Generate a password.
    """
    pwd = []
    while len(pwd) < l:
        k = choice(range(4))
        pwd.append(choice(ALLOWED[k]))
    return ''.join(pwd)
