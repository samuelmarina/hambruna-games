from defines import getCreds, fetchData

myPageID = ""

def getUserPages(params):
	"""Get user's FB pages
	API Endpoint:
		https://graph.facebook.com/v7.0/me/accounts?access_token={access-token}
	Returns:
		object: data from the endpoint
	"""

	endpointParams = dict() #parameters to send to the endpoint
	endpointParams['access_token'] = params['access_token'] #access token

	url = params['endpoint_base'] + '/me/accounts' #endpoint url

	return fetchData(url, endpointParams, params['debug']) #API call


def getFBPageID(response):
	"""Get FB page id
	Returns:
		string: FB page id
	"""
	pagePosition = 0 #the position of the page to get

    return response['json_data']['data'][pagePosition]['id'] #API call


def getInstagramPage(params, fbPageID):
	"""Get Instagram page
	API Endpoint:
		https://graph.facebook.com/v7.0/134895793791914?fields=instagram_business_account&access_token={access-token}
	Args:
		params: dictionary of endpoint parameters
		fbPageId: string of FB page id
	Returns:
		object: data from the endpoint
	"""
    endpointParams = dict() #parameters to send to the endpoint
    endpointParams['access_token'] = params['access_token'] #access token
    endpointParams['fields'] = 'instagram_business_account'

    url = params['endpoint_base'] + fbPageID #endpoint url

    return fetchData(url, endpointParams, params['debug']) #API call

def getIGPageID(response):
	"""Get Instagram page id
	Returns:
		string of Instagram page id
	"""

    return response['json_data']['instagram_business_account']['id']


def getInstagramPosts(params, igPageID):
	"""Get all Instagram media objects
	API Endpoint:
		https://graph.facebook.com/v7.0/17841405822304914/media?access_token={access-token}
	Args:
		params: dictionary of endpoint parameters
		igPageId: string of Ig page id
	Returns:
		object: data from the endpoint
	"""

    endpointParams = dict() #parameters to send to the endpoint
    endpointParams['access_token'] = params['access_token'] #access token

    url = params['endpoint_base'] + igPageID + '/media' #endpoint url

    return fetchData(url, endpointParams, params['debug']) #API call

def getLastPostID(response):
	"""Get id of last ig post
	Args:
		response: object response of api call
	Returns:
		string of post id
	"""
    return response['json_data']['data'][0]['id'] # 0 to get the very last post

def getComments(params, postID):
	"""Get comments of an ig media content
	Args:
		params: dictionary of endpoint parameters
		postID: string of the ig post id
	Returns:
		object: data from the endpoint
	"""
    endpointParams = dict() #parameters to send to the endpoint
    endpointParams['access_token'] = params['access_token'] #access token
    endpointParams['limit'] = "400" #limit of comments to return

    url = params['endpoint_base'] + postID + '/comments' #endpoint url

    return fetchData(url, endpointParams, params['debug']) #API call

def getAllComments():
	"""All in one function to get all the getComments
	of the last ig post
	Returns:
		object: data from the endpoint
	"""
    params = getCreds() #dictionary of credentials
    fbPages = getUserPages(params) #fb pages
    fbID = getFBPageID(fbPages) #fb page id
    igPage = getInstagramPage(params, fbID) #ig page
    igPageID = getIGPageID(igPage) #ig page id
    myPageID = igPageID
    igPosts = getInstagramPosts(params, igPageID) #ig media content
    postID = getLastPostID(igPosts) #ig last post

    return getComments(params, postID)

def getUserProfilePic(user):
	"""Get user's instagram profile picture
	API Endpoint:
		https://graph.facebook.com/{instagram_page_id}?fields=business_discovery.username(bluebottle){fields}
	Args:
		user: string of the user (ex: @shakira)
	Returns:
		object: data from the endpoint
	"""

    params = getCreds() #dictionary of credentials
    endpointParams = dict() #dictionary of parameters
    endpointParams['access_token'] = params['access_token'] #acces token
    endpointParams['fields'] = 'business_discovery.username(' + user + '){profile_picture_url}' #fields

    url = params['endpoint_base'] + obtainIgPageID() + "?" #endpoint url

    return fetchData(url, endpointParams, params['debug']) #API call

def obtainIgPageID():
	"""All in one function to get ig page id
	Returns:
		string of the ig page id
	"""
    params = getCreds()
    fbPages = getUserPages(params)
    fbID = getFBPageID(fbPages)
    igPage = getInstagramPage(params, fbID)
    igPageID = getIGPageID(igPage)
    return igPageID
