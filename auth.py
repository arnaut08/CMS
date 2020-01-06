# Verification will be done in the HRMS login API only
def verify(username, password):
    pass


def identity(payload):
# Response object needs to be updated yet
    return {"userId": payload["userId"]}