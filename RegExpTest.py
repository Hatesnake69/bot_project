import re


def isValid(email):
    regex = re.compile(
        r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
        print("Valid email")
    else:
        print("Invalid email")


isValid('g.gulyaev@ylab.io')