import yaml,requests,argparse

parser = argparse.ArgumentParser(description="Sends a pushover alert on a new beacon")
parser.add_argument('--host')
parser.add_argument('--ip')
parser.add_argument('--os')
parser.add_argument('--version')

args = parser.parse_args()

try:
	conf = yaml.safe_load(open('config.yaml'))
except IOError as e:
	print(dir(e))
	quit("Error opening config file. Does it exist?")

for usertoken in conf['usertokens'].keys():
	headers = {'Content-Type' : 'application/x-www-form-urlencoded'}
	payload = {'token' : conf['apptoken']}
	payload.update({'user' : usertoken})
	payload.update({'title' : 'New beacon reporting in!'})
	payload.update({'sound' : 'cashregister'})
	payload.update({'priority' : '1'})
	payload.update({'message' : 'Hostname %s | Internal IP: %s | OS: %s %s ' % (args.host, args.ip, args.os, args.version)})
	r = requests.post('https://api.pushover.net/1/messages', headers=headers, data=payload)
