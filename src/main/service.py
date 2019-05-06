from flask import Flask

app = Flask(__name__)

# input: list of dictionaries, list of key:value pair queries as dictionaries
# output: the input list, filtered by the queries.
# example: 
#    input:
#       users: [{"name": "root", "uid": 0 },{"name": "dwoodlins", "uid": 1001}, {"name": "dwoodlins", "uid": 1002}]
#       queries: [{"name": "dwoodlins"}, {"uid": 1002}]
#    output: 
#       [{'name': 'dwoodlins', 'uid': 1002}]
def filterResults(users, queries):

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

# temporary test for filterResults
@app.route('/filterResultTest')
def runFilterResultTest():
    users = [{"name": "root", "uid": 0 },{"name": "dwoodlins", "uid": 1001}, {"name": "dwoodlins", "uid": 1002}]
    queries = [{"name": "dwoodlins"}, {"uid": 1002}]
    # expect {"name": "dwoodlins", "uid": 1002}
    return str(filterResults(users,queries))
