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
#       database: [{"name": "root", "uid": 0 },{"name": "dwoodlins", "uid": 1001}, {"name": "dwoodlins", "uid": 1002}]
#       queries: [{"name": "dwoodlins"}, {"uid": 1002}]
#    output: 
#       [{'name': 'dwoodlins', 'uid': 1002}]
# returns empty list if no matches found.
def filterResults(database, queries = []):

    # if no query parameters passed in, return the input database. 
    if queries == []:
        return database

    unfiltered_list = database

    for query in queries:
        # successively filter the input list by each query parameter,
        # until we have a list of items matching all the queries. 
        filtered_list = []
        query_key = list(query)[0]
        query_value = query[query_key]

        for entry in unfiltered_list:
            # the member query is a special case that gets handled here, since the query key
            # doesn't map to a data key name.
            if query_key == "member":
                if query_value in entry["members"]:
                    filtered_list.append(entry)
            else:
                # this takes advantage of the fact that the database and the queries
                # use the same key names. 
                if entry[query_key] == query_value:
                    filtered_list.append(entry)

        unfiltered_list = filtered_list
        
        # quit early if no items matched this query parameter. 
        if filtered_list == []:
            break
            
    return filtered_list


# parseFileToDict
# input:  file path to a /etc/group or /etc/passwd file (or similar colon-separated file)
# output: multi dictionary (list of dictionaries) of key:value pairs corresponding to the lines in the files. 
#         also removes the "password" column, as it is not needed.
def parseFileToDict(default_path, override_path, field_names):
   
    if override_path is not None:
        # we can also check if this path exists, and fall back on the default. 
        file_path = override_path
    else:
        file_path = default_path

    # can perform additional checking of file here

    # csv reader creates an ordered dict. we just want a regular dict.
    entries_ordered_dict = []
    with open(file_path, mode='r', newline='' ) as f:
        reader = csv.DictReader(f, delimiter=':', quoting=csv.QUOTE_NONE, fieldnames = field_names)
        entries_ordered_dict = list(reader)

    # convert ordered dicts to regular dicts. 
    entries_multidict = []
    for entry in entries_ordered_dict:
        del entry["password"]
        entries_multidict.append(dict(entry))
    
    return entries_multidict


# getUsersDict()
# input: optional env variable PASSWDFILE_PATH, the path to the passwd file. if not present, defaults to /etc/passwd 
# output: returns a multidict (list of dictionaries) corresponding to the entries in the passwd file. 
# Will read from a file. 
def getUsersDict():
    default_passwd_path = "/etc/passwd"
    optional_configured_path = os.environ.get('PASSWDFILE_PATH')

    passwd_fieldnames = ["user",
                         "password",
                         "uid",
                         "gid",
                         "comment",
                         "home",
                         "shell"]

    users_multidict = parseFileToDict(default_passwd_path, optional_configured_path, passwd_fieldnames)



    return users_multidict 

# getGroupsDict()
# input: optional env variable GROUPFILE_PATH, the path to the group file. 
#        defaults to /etc/group if not present. 
# output: returns a multidict (list of dictionaries) corresponding to the entries in the group file. 
# GROUPFILE_PATH
def getGroupsDict():
    default_group_path = "/etc/group"
    optional_configured_path = os.environ.get('GROUPFILE_PATH')

    group_fieldnames = ["name",
                        "password",
                        "gid",
                        "members"]

    groups_multidict = parseFileToDict(default_group_path, optional_configured_path, group_fieldnames)

    # parse the members string into a list, because the parsing doesn't handle these.
    for entry in groups_multidict:
        if "," in entry["members"]:
            entry["members"] = entry["members"].split(",")
        else:
            if entry["members"]=="":
                entry["members"] = []
            else:
                entry["members"] = [entry["members"]]

    return groups_multidict


# temporary test for filterResults
@app.route('/filterResultTest')
def runFilterResultTest():
    users = [{"name": "root", "uid": 0 },{"name": "dwoodlins", "uid": 1001}, {"name": "dwoodlins", "uid": 1002}]
    queries = [{"name": "dwoodlins"}, {"uid": 1002}]
    # expect {"name": "dwoodlins", "uid": 1002}
    return str(filterResults(users,queries))

# /users
# returns all users in the passwd file. 
@app.route('/users')
def getUsers():
    users = getUsersDict()
    return str(users)

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

@app.route('/users/<uid>')
def getUserById(uid):
    """ /users/<uid> returns the user with the given <uid> or 404 if the <uid> was not found. """
    users = getUsersDict()

    # handle errors with getting users dict

    # query for the user matching the uid passed in
    query = [{'uid': uid}]
    result = filterResults(users, query)

    if result == []:
        abort(404)
        return

    return str(result)

@app.route('/groups')
def getGroups():
    """ /groups returns all groups in the group file """ 
    groups = getGroupsDict()
    return str(groups)

@app.route('/groups/query')
def getQueriedGroups():
    groups = getGroupsDict()

    query = []

    allowed_queries = set(["name",
                        "gid",
                        "member"])

    for item in request.args:
        # check the query parameters to make sure the requested fields exist
        if item in allowed_queries:
            if item == "member":
                for member in request.args.getlist(item):
                    query.append({item: member})
            else:
                query.append({item: request.args.get(item)})

    return str(filterResults(groups,query))

