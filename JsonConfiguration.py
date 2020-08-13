import sys, os
import json

conf_file = 'twitter_api.conf'

def _import_conf():
	global CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET
	with open(conf_file) as json_file:
		data = json.load(json_file)
		for p in data['API_KEY']:
			print('CONSUMER_KEY: ' + p['CONSUMER_KEY'])
			CONSUMER_KEY = p['CONSUMER_KEY']
			ACCESS_KEY = p['ACCESS_KEY']
			print('')
		for p in data['API_SECRET']:
			CONSUMER_SECRET = p['CONSUMER_SECRET']
			ACCESS_SECRET = p['ACCESS_SECRET']

		print('')

def _export_conf():
	print('Get a real API consumer key & secret from https://dev.twitter.com/apps/new')
	print('')
	CONSUMER_KEY =  input('Paste your CONSUMER_KEY: ')
	CONSUMER_SECRET = input('Paste your CONSUMER_SECRET: ')
	ACCESS_KEY = input('Paste your ACCESS_KEY: ')
	ACCESS_SECRET = input('Paste your ACCESS_SECRET: ')
	data = {}
	data['API_SECRET'] = []
	data['API_KEY'] = []
	data['API_SECRET'].append({ 'CONSUMER_SECRET': CONSUMER_SECRET, 'ACCESS_SECRET': ACCESS_SECRET })
	data['API_KEY'].append({ 'CONSUMER_KEY': CONSUMER_KEY, 'ACCESS_KEY': ACCESS_KEY })
	with open(conf_file, 'w') as outfile:
		json.dump(data, outfile, indent=4)

def _export_global_conf():
	if os.path.exists(conf_file):
		print('Configuration file available.', conf_file)
		_import_conf()
	else:
		_export_conf()
		print('Conf file created.')
		sys.exit()

_export_global_conf()
