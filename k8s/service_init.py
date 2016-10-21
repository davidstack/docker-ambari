import sys
import json
import requests
import time

headers = {'X-Requested-By': 'ambari-server'}
auth = ('admin', 'admin')
# ip:port
ambari_server_address = '172.17.17.4:8080'


def get(url):
    response = requests.get(url, headers=headers, auth=auth)

    try:
        if response.status_code == 200:
            return response.json()
        return False
    except Exception as e:
        print 'Exception ', type(e), e


def post(url, data):
    response = requests.post(url, headers=headers, auth=auth, data=data)
    # print response.status_code
    try:
        if response.status_code == 200 or response.status_code == 201:
            return True
        return json.loads(response.content)

    except Exception as e:
        print 'Exception ', type(e), e


def put(url, data):
    response = requests.put(url, headers=headers, auth=auth, data=data)
    # print response.status_code
    try:
        if response.status_code == 200 or response.status_code == 201:
            return True
        return json.loads(response.content)

    except Exception as e:
        print 'Exception ', type(e), e


def delete(url):
    response = requests.delete(url, headers=headers, auth=auth)
    if response.status_code == 200:
        return True
    return False


def get_method_url(suffix):
    # print 'http://{}{}'.format(ambari_server_address, suffix)
    return 'http://{0}{1}'.format(ambari_server_address, suffix)


def get_hosts():
    suffix = '/api/v1/hosts'
    method_url = get_method_url(suffix)
    data = get(method_url)
    if data is not None:
        return data['items']
    else:
        return None


def wait_server_ready():
        count = 240
        for i in range(0, count):
            try:
                response = requests.get('http://'+ambari_server_address)
                if response.status_code == 200:
                    break
                time.sleep(1)
            except Exception as e:
                print 'Exception ', type(e), e
                time.sleep(1)
                continue
        return i < count - 1


def wait_agents_ready(hosts_num):
    # wait for count second until all hosts get ready
    count = 300
    is_ready = False
    # for i in range(0, count):
    while True:
        hosts = get_hosts()
		
        if len(hosts) == int(hosts_num):
            print "all hosts is ok"
            is_ready = True
            break
	print "hosts is not ready "
	print hosts
        time.sleep(1)
    return is_ready


def create_blueprint(blue_print_name):
    base_path = sys.path[0]
    json_file = file('./'+blue_print_name+".json")
    # json_file = file(base_path+'/../template/'+blue_print_name+'.ftl')
    blue_print = json.load(json_file)
    cmd = "curl --user admin:admin -H 'X-Requested-By:ambari' -X " \
          "POST http://"+ambari_server_address+"/api/v1/blueprints/"+blue_print_name+" -d '" \
          + json.dumps(blue_print) + "'"
    # os.system(cmd)

    suffix = '/api/v1/blueprints/' + blue_print_name
    create_blueprint_url = get_method_url(suffix)
    data = post(create_blueprint_url, json.dumps(blue_print))
    return data


#
def set_repo():
    base_path = sys.path[0]
    json_file = file('./repo.json')
    repo = json.load(json_file)
    
    HD_suffix = '/api/v1/stacks/HDP/versions/2.3/operating_systems/redhat6/repositories/HD-2.3'
    HD_UTILS_suffix = '/api/v1/stacks/HDP/versions/2.3/operating_systems/redhat6/repositories/HD-UTILS-2.3'
    HD_repo_url = get_method_url(HD_suffix)
    HD_UTILS_repo_url = get_method_url(HD_UTILS_suffix)
    print "before set repo put"
    print put(HD_repo_url, json.dumps(repo["HD"]))
    print put(HD_UTILS_repo_url,  json.dumps(repo["HD-UTILS"]))
    print "after set repo put"


def add_hosts(blue_print_name):
    base_path = sys.path[0]
    json_file = file('./'+blue_print_name+'_hosts.json')
    # json_file = file(base_path+'/../template/'+blue_print_name+'_hosts_test')
    hosts = json.load(json_file)
    suffix = '/api/v1/clusters/'+blue_print_name
    cmd = "curl --user admin:admin -H 'X-Requested-By:ambari' -X POST " \
          "http://"+ambari_server_address+"/api/v1/clusters/"+blue_print_name+" -d '" \
          + json.dumps(hosts) + "'"
    add_hosts_url = get_method_url(suffix)
    # must change the host name to lower, the ambari server can't recognize upper host name
    data = post(add_hosts_url, json.dumps(hosts).lower())
    print "add_hosts"
    print data
    # os.system(cmd)


if __name__ == '__main__':
    blueprint_name = "emr_blueprint"
    agent_server_num = 5
    is_server_ready = wait_server_ready()
    if is_server_ready is False:
        print "error, ambari-server can't start up"
        exit(1)
    print "server is ready"
    result=create_blueprint(blueprint_name)
    print "create_blueprint result"
    print result
    set_repo()
    if wait_agents_ready(agent_server_num):
        add_hosts(blueprint_name)

