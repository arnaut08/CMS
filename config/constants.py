statusCode = {
    'success': 200,
    'created': 201,
    'error': {
        'internalServer': 500,
        'badRequest': 400,
        'unauthorized': 401,
        'notFound': 404,
    }
}

fieldTypes = ['username', 'password', 'file', 'key', 'software']

# Event Comments Skeleton
addCredential = " added credential "
updateCredential = " updated credential "
giveAccess = " gave access to "
updateAccess = " updated access of "
forCredential = " for credential "
forProject = " for project "
inProject = " in project "
