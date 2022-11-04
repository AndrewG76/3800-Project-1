import client_recep as cr
from cryptography.hazmat.primitives import serialization

def receive(message):
    time, a, params1, params2, user = cr.unpack(message)
    takeAction(time,a,params1, params2, user)

def takeAction(time,a,params1,params2, user):
    field = ["registerSuccess","joinSuccess","loginSuccess"]
    if a in field:
        cacheSessionKey(params1)
    elif a == "receive":
        displayComment(time, params1)
    elif a =="signup":
        signup

def cacheSessionKey(params):
    pass


