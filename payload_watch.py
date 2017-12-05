import time,requests,subprocess,select,re,yaml

TARGET_FILE='/var/log/apache2/access.log'
ip_re = re.compile("(\d{1,3}\.){3}\d{1,3}")
payload_re = re.compile("^.+\.hta.+$")
headers = {'Content-Type' : 'application/x-www-form-urlencoded'}

# Format expected for config:
# usertokens:
#	'uthisisapushovertoken' : 'Bob User'
#	'uthisisanothertokenok'	: 'Joe Hackerman'
# apptoken:
#	'aathisismyapptokenlol'
try:
	conf = yaml.safe_load(open('config.yaml'))
except IOError as e:
	print(dir(e))
	quit("Error opening config file. Does it exist?")

try:
	file = subprocess.Popen(['tail', '-f', '-n', '0', TARGET_FILE], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	p = select.poll()
	p.register(file.stdout)
	source_ips = []
	while True:
		if p.poll(1):
			line = file.stdout.readline().strip()
			parts = line.split()
			ip_result = ip_re.search(line)
			payload_result = payload_re.search(line)
			if ip_result and payload_result:
				for usertoken in conf['usertokens'].keys():
					ip_info = requests.get("https://ipinfo.io/%s" % ip_result.group().strip()).json()
					payload = {'token' : conf['apptoken']}
					payload.update({'user' : usertoken})
					payload.update({'title' : 'New Payload Notification'})
					payload.update({'sound' : 'cashregister'})
					payload.update({'priority' : '1'})
					payload.update({'message' : 'The payload has been accessed!\nIP: %s | Location: %s, %s | Org: %s' % (ip_info['ip'], ip_info['city'], ip_info['region'], ip_info['org'])})
					r = requests.post('https://api.pushover.net/1/messages', headers=headers, data=payload)

			elif ip_result and not payload_result:
				for usertoken in conf['usertokens'].keys():
					if ip_result.group() not in source_ips:
						source_ips.append(ip_result.group())
						ip_info = requests.get("https://ipinfo.io/%s" % ip_result.group().strip()).json()
						payload = {'token' : conf['apptoken']}
						payload.update({'user' : usertoken})
						payload.update({'title' : 'New IP Notification'})
						payload.update({'sound' : 'cashregister'})
						payload.update({'message' : 'IP: %s | Location: %s, %s | Org: %s' % (ip_info['ip'], ip_info['city'], ip_info['region'], ip_info['org'])})
						r = requests.post('https://api.pushover.net/1/messages', headers=headers, data=payload)
		time.sleep(1)
except IOError as e:
	quit("Quitting due to IOError: %s." % e.strerror)
except KeyboardInterrupt:
	exit("Cleaning up...")
