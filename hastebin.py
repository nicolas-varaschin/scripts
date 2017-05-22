import requests
import json
import sys
import fileinput
import signal


url = "https://hastebin.com/documents"
data = []
if len(sys.argv) == 1:
    while 1:
        try:
            line = sys.stdin.readline()
        except KeyboardInterrupt:
            break
        if not line:
            break
        data.append(line)
else:
    for line in fileinput.input():
        data.append(line)
r = requests.post(url, data=''.join(data))
print "https://hastebin.com/" + json.loads(r.text)['key']
