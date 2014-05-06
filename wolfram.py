import xml.etree.ElementTree as ET
import requests

def wolfram(query):
	appid='xxxxx'
	results = requests.get("http://api.wolframalpha.com/v2/query", params={'input':query,'appid': appid}, headers={'User-Agent': "Mozilla"})
	results = results.text
	results=results.encode('utf-8')
	root=ET.fromstring(results)
	reply=None
	print "querying wolfram for "+query
	for pod in root.findall('pod'):
		if (pod.attrib['id']=="Result"):
			reply=pod[0][0].text
			print reply
	if not reply:
		reply="noidea"
	return reply
