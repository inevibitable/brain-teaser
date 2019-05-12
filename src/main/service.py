from flask import Flask
from flask import request
from flask import abort
import os
import csv

app = Flask(__name__)

# input: list of dictionaries, list of key:value pair queries as dictionaries
# output: the input list, filtered by the queries.
# example: 
#    input:
#       users: [{"name": "root", "uid": 0 },{"name": "dwoodlins", "uid": 1001}, {"name": "dwoodlins", "uid": 1002}]
#       queries: [{"name": "dwoodlins"}, {"uid": 1002}]
#    output: 
#       [{'name': 'dwoodlins', 'uid': 1002}]
# returns empty list if no matches found.
def filterResults(users, queries = []):

    # if no query parameters passed in, return the input users. 
    if queries == []:
        return users

    unfiltered_list = users

    for query in queries:
        # successively filter the input dictionary by each query parameter,
        # until we have a list of items matching all the queries. 
        filtered_list = []
        query_key = list(query)[0]
        query_value = query[query_key]

        for user in unfiltered_list:
            if user[query_key] == query_value:
                filtered_list.append(user)

        unfiltered_list = filtered_list
        
        # quit early if no items matched this query parameter. 
        if filtered_list == []:
            break
            
    return filtered_list


# parseFileToDict
# input:  file path to a 
# output: dictionary of key:value pairs corresponding to the lines in the files. 
#def parseFileToDict(file_path, column_names):
#    pass

# input: optional env variable PASSWDFILE_PATH, the path to the passwd file. if not present, defaults to /etc/passwd 
# output: dictionary of key:value pairs, corresponding to the entries in the passwd file. 
def getUsersDict():
    default_passwd_path = "/etc/passwd"
    optional_configured_path = os.environ.get('PASSWDFILE_PATH')
    passwd_path = ""

    if optional_configured_path is not None:
        # we can also check if this path exists, and fall back on the default. 
        passwd_path = optional_configured_path
    else:
        passwd_path = default_passwd_path
    passwd_fieldnames = ["user",
                         "password",
                         "uid",
                         "gid",
                         "comment",
                         "home",
                         "shell"]

    # csv reader creates an ordered dict. we just want a regular dict.
    ordered_dict_users = []
    with open(passwd_path, mode='r', newline='' ) as f:
        reader = csv.DictReader(f, delimiter=':', quoting=csv.QUOTE_NONE, fieldnames = passwd_fieldnames)
        ordered_dict_users = list(reader)

    # convert ordered dicts to regular dicts. 
    dict_users = []
    for item in ordered_dict_users:
        dict_users.append(dict(item))

    return dict_users

# GROUPFILE_PATH
def getGroupsDict():

    # if entry["users"] is not None and "," in entry["users"]
    #   entry["users"] = entry["users"].split()
    pass



# temporary test for filterResults
@app.route('/filterResultTest')
def runFilterResultTest():
    users = [{"name": "root", "uid": 0 },{"name": "dwoodlins", "uid": 1001}, {"name": "dwoodlins", "uid": 1002}]
    queries = [{"name": "dwoodlins"}, {"uid": 1002}]
    # expect {"name": "dwoodlins", "uid": 1002}
    return str(filterResults(users,queries))

@app.route('/passwdParseTest')
def runPasswdParseTest():
    return str(getUsersDict())


def getAllUsers(users):
    return filterResults(users)

# /users
# returns all users in the passwd file. 
@app.route('/users')
def getUsers():
    users = getUsersDict()
    return str(getAllUsers(users))

# /users/query
# examines the URL parameters and returns users matching the query parameters. 
# allowable URL params: [?name=<nq>][&uid=<uq>][&gid=<gq>][&comment=<cq>][&home=<hq>][&shell=<sq>]
@app.route('/users/query')
def getQueriedUsers():
    users = getUsersDict()

    if users is None:
        #404 or other error: could not find passwd file or passwd file blank.
        pass

    query = []
    for item in request.args:
        # check the query parameters to make sure the requested fields exist
        if item in users[0].keys():
            query.append({item: request.args.get(item)})

    return str(filterResults(users,query))

# /users/<uid>
# returns the user with the given <uid> or 404 if the <uid> was not found. 
@app.route('/users/<uid>')
def getUserById(uid):
    users = getUsersDict()

    # handle errors with getting users dict

    # query for the user matching the uid passed in
    query = [{'uid': uid}]
    result = filterResults(users, query)

    if result == []:
        abort(404)
        return

    return str(result)