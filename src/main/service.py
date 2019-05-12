from flask import Flask
from flask import request
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
    
    # alternatively use string.split on each line of the passwd file. 
    # with open(passwd_path, "r", newline ="\n") as f:
    #     passwd_text = f.read().splitlines()

    # output = []
    # for line in passwd_text:
    #     output.append(line.split(':'))

    # output_dictlist = [{}]*len(output)

    # for line in range(0,len(output)):
    #     for item in range(0,len(passwd_fieldnames)):
    #         # create a dictionary that maps the field names to their values, per line
    #         output_dictlist[line][passwd_fieldnames[item]] = output[line][item]

    # return output

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

@app.route('/users')
def getUsers():
    users = getUsersDict()
    #return str([request.args.to_dict()])
    return str(getAllUsers(users))

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