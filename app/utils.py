from passlib.context import CryptContext

#password context
ctx = CryptContext(schemes=['bcrypt'],deprecated='auto')

def hash(pwd):
    return ctx.hash(pwd)