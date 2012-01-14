import requests
from BeautifulSoup import BeautifulSoup

def image_extracter(url):
    assert url, 'missing args'
    #twitpic, instagr.am, flic.kr, yfrog.com
    if 'twitpic' in url:
	tag = 'img'
	attrs_dict = {'class' : 'photo'}
    elif 'instagr.am' in url:
	tag = 'img'
	attrs_dict = {'class' : 'photo'}
    elif 'flic.kr' in url:
	if 'lightbox' not in url:
	    url = '%s/%s' %(url, 'lightbox')
	tag = 'img'
	attrs_dict = {'alt' : 'photo'}
    elif 'yfrog.com' in url:
	tag = 'img'
	attrs_dict = {'id' : 'main_image'}
    else:
	return None
    r = requests.get(url = url)
    if r.status_code == 200:
	soup = BeautifulSoup(r.content)
	try:
	    return soup.find(tag, attrs = attrs_dict)['src']
	except:
	    return None
    return None