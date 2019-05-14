import service
import pytest 

users = [{
    'user': 'root',
    'uid': '0',
    'gid': '0',
    'comment': 'root',
    'home': '/root',
    'shell': '/bin/ash'
}, {
    'user': 'bin',
    'uid': '1',
    'gid': '1',
    'comment': 'bin',
    'home': '/bin',
    'shell': '/sbin/nologin'
}, {
    'user': 'daemon',
    'uid': '2',
    'gid': '2',
    'comment': 'daemon',
    'home': '/sbin',
    'shell': '/sbin/nologin'
}, {
    'user': 'adm',
    'uid': '3',
    'gid': '4',
    'comment': 'adm',
    'home': '/var/adm',
    'shell': '/sbin/nologin'
}]

groups = [{'name': 'root', 'gid': '0', 'members': ['root']}, 
        {'name': 'bin', 'gid': '1', 'members': ['root', 'bin', 'daemon']}, 
        {'name': 'daemon', 'gid': '2', 'members': ['root', 'bin', 'daemon']}, 
        {'name': 'sys', 'gid': '3', 'members': ['root', 'bin', 'adm']}, 
        {'name': 'adm', 'gid': '4', 'members': ['root', 'adm', 'daemon']}, 
        {'name': 'tty', 'gid': '5', 'members': []}, 
        {'name': 'disk', 'gid': '6', 'members': ['root', 'adm']}, 
        {'name': 'lp', 'gid': '7', 'members': ['lp']}, 
        {'name': 'mem', 'gid': '8', 'members': []}, 
        {'name': 'kmem', 'gid': '9', 'members': []}, 
        {'name': 'wheel', 'gid': '10', 'members': ['root']}, 
        {'name': 'floppy', 'gid': '11', 'members': ['root']}, 
        {'name': 'mail', 'gid': '12', 'members': ['mail']}]


def test_filterResults_noQuery():
    # checks that a filterResults request with an empty query returns the input.
    assert service.filterResults(users) == users


def test_filterResults_singleQuery():
    #checks that a filterResults request with a single query returns the expected value.
    query = [{'user': 'daemon'}]
    queried_user = [{
        'user': 'daemon',
        'uid': '2',
        'gid': '2',
        'comment': 'daemon',
        'home': '/sbin',
        'shell': '/sbin/nologin'
    }]

    assert service.filterResults(users, query) == queried_user

def test_filterResults_memberQuery():
    # test checks that the special "member" query works.
    query = [{'member': 'root'}]
    queried_groups = [{'name': 'root', 'gid': '0', 'members': ['root']}, 
                    {'name': 'bin', 'gid': '1', 'members': ['root', 'bin', 'daemon']}, 
                    {'name': 'daemon', 'gid': '2', 'members': ['root', 'bin', 'daemon']}, 
                    {'name': 'sys', 'gid': '3', 'members': ['root', 'bin', 'adm']}, 
                    {'name': 'adm', 'gid': '4', 'members': ['root', 'adm', 'daemon']}, 
                    {'name': 'disk', 'gid': '6', 'members': ['root', 'adm']}, 
                    {'name': 'wheel', 'gid': '10', 'members': ['root']}, 
                    {'name': 'floppy', 'gid': '11', 'members': ['root']}]

    assert service.filterResults(groups, query) == queried_groups

def test_filterResults_multiMemberQuery():
    # test checks that multiple special "member" queries work.
    query = [{'member': 'root'}, {'member': 'daemon'}]
    queried_groups = [{'name': 'bin', 'gid': '1', 'members': ['root', 'bin', 'daemon']}, 
                    {'name': 'daemon', 'gid': '2', 'members': ['root', 'bin', 'daemon']}, 
                    {'name': 'adm', 'gid': '4', 'members': ['root', 'adm', 'daemon']}]
    
    assert service.filterResults(groups, query) == queried_groups 

def test_filterResults_multiQuery():
    # test to make sure successive filter works
    query = [{'shell': '/sbin/nologin'}, {'user': 'daemon'}]
    queried_user =  [{
        'user': 'daemon',
        'uid': '2',
        'gid': '2',
        'comment': 'daemon',
        'home': '/sbin',
        'shell': '/sbin/nologin'}]

    assert service.filterResults(users, query) == queried_user

def test_filterResults_multiQueryWithMember():
    # test using the special "member" query and a normal query
    query = [{'name': 'adm'}, {'member': 'daemon'}]
    queried_groups = [{'name': 'adm', 'gid': '4', 'members': ['root', 'adm', 'daemon']}]

    assert service.filterResults(groups, query) == queried_groups 

def test_filterResults_noMatchQuery():
    # filterResults should return an empty list when the result of a query does not match anything.
    query = [{'name': 'foobar'}]
    queried_groups = []

    assert service.filterResults(groups,query) == queried_groups


def test_filterResults_nonsenseQuery():
    # filterResults does not handle queries when the key doesn't exist.
    # this query should raise a KeyError. 
    query = [{'foobar': 'foobar'}]
    
    with pytest.raises(KeyError): service.filterResults(groups,query)

