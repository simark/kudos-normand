import mechanicalsoup
import configparser
import sys

cfg = configparser.ConfigParser()
cfg.read('config.ini')

email = cfg['login']['email']
password = cfg['login']['password']
normand_id = cfg['data']['normand_id']

# For debugging with mitmproxy.  Use with:
#
#	proxies=proxies, verify=False
#
# in requests.
# 
# proxies = {
#   'http': 'http://127.0.0.1:1234',
#   'https': 'http://127.0.0.1:1234',
# }

browser = mechanicalsoup.Browser()

login_page = browser.get("https://www.strava.com/login")

login_form = login_page.soup.select("#login_form")[0]
login_page.soup.select("#email")[0]['value'] = email
login_page.soup.select("#password")[0]['value'] = password

page2 = browser.submit(login_form, "https://www.strava.com/session")

csrf_token = None
for meta in page2.soup.select('meta'):
	if 'name' in meta.attrs and meta['name'] == 'csrf-token':
		csrf_token = meta['content']
assert csrf_token is not None

activities = page2.soup.select('.entity-details')

for activity in activities:
	avatars = activity.select('a.avatar-athlete')
	if len(avatars) > 0:
		avatar = avatars[0]
		profile_link = avatar['href']
		
		if profile_link == '/athletes/{}'.format(normand_id):
			kudo_btn = activity.select('button.btn-kudo')[0]
			
			kudo_img = kudo_btn.select('span.icon-kudo')[0]
			
			if 'icon-dark' in kudo_img['class']:
				activity_id = activity['id'].split('-')[1]
				url = 'https://www.strava.com/feed/activity/{}/kudo'.format(activity_id)
				print('Kudoing {}'.format(url))
				headers = {
					'X-CSRF-Token': csrf_token,
				}
				result = browser.post(url, headers=headers)
				assert result.status_code == 200
