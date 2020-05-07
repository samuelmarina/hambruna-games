import requests
import json

#
def getCreds() :
	""" Get credentials for use in applications
	Returns:
			dictionary: credentials needes globally
	"""
	creds = dict()	#dictionary to hold credentials
	creds['access_token'] = 'YOUR-ACCES-TOKEN' 	#token for API calls
	creds['client_id'] = 'YOUR-FB-CLIENT-ID'	#client id from Instagram Graph API
	creds['client_secret'] = 'YOUR-FB-CLIENT-SECRET'	#client secret from Facebook app
	creds['graph_domain'] = 'https://graph.facebook.com/'	#base domain for API calls
	creds['graph_version'] = 'v6.0'	#current version (change if necessary)
	creds['endpoint_base'] = creds['graph_domain'] + creds['graph_version'] + '/'	#base endpoint
	creds['debug'] = 'no'	#debug mode for API calls

	return creds

def fetchData( url, endpointParams, debug = 'no' ):
	""" Request data from endpoint with its params
	Args:
			url: string of the url to make the request from
			endpointParams: dictionary keyed with the name of the url parameters
	Returns:
			object: data retrieved from the endpoint
	"""
	data = requests.get( url, endpointParams )	#get request

	response = dict() #dictionary of the response
	response['url'] = url #url we're hitting
	response['endpoint_params'] = endpointParams #parameters for the endpoint
	response['endpoint_params_pretty'] = json.dumps(endpointParams, indent = 4, ensure_ascii=False)	#pretty print
	response['json_data'] = json.loads(data.content)	#API response
	response['json_data_pretty'] = json.dumps(response['json_data'], indent = 4, ensure_ascii=False) #pretty print

	if ( 'yes' == debug ): #display response
		displayData(response)

	return response


def displayData( response ):
	""" Print the response in the console
	Args:
		response: object response of API call
	"""
	print ("\nURL: ")
	print (response['url'])
	print ("\nEndpoint Params: ")
	print (response['endpoint_params_pretty'])
	print ("\nResponse: ")
	print (response['json_data_pretty'])
