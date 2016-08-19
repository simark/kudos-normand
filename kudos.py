import argparse
import mechanicalsoup
import yaml
import generate_comment

# proxies = {
#  'http': 'http://127.0.0.1:1234',
#  'https': 'http://127.0.0.1:1234',
# }


def load_config():
    with open('config.yml') as ymlfile:
        cfg = yaml.load(ymlfile)

    email = cfg['login']['email']
    password = cfg['login']['password']
    athlete_ids = cfg['athlete_ids']

    return email, password, athlete_ids


def login_strava(email, password):
    browser = mechanicalsoup.Browser()
    login_page = browser.get("https://www.strava.com/login")
    login_form = login_page.soup.select("#login_form")[0]
    login_page.soup.select("#email")[0]['value'] = email
    login_page.soup.select("#password")[0]['value'] = password

    feed_page = browser.submit(login_form, "https://www.strava.com/session")

    csrf_token = None
    for meta in feed_page.soup.select('meta'):
        if 'name' in meta.attrs and meta['name'] == 'csrf-token':
            csrf_token = meta['content']
    assert csrf_token is not None

    return browser, csrf_token, feed_page


def do_kudo(browser, csrf_token, activity_id):
    kudo_url = 'https://www.strava.com/feed/activity/{}/kudo'.format(
        activity_id)
    headers = {
        'X-CSRF-Token': csrf_token,
    }
    result = browser.post(kudo_url, headers=headers)
    assert result.status_code == 200


def find_activities_from_feed_page(feed_page):
    return feed_page.soup.select('.entity-details')


def do_comment(browser, csrf_token, activity_id, comment):
    comment_url = 'https://www.strava.com/feed/activity/{}/comment'.format(
        activity_id)
    headers = {
        'X-CSRF-Token': csrf_token,
    }
    comment_data = {
        'comment': comment,
        'mentions': {}
    }
    result = browser.post(comment_url, headers=headers, json=comment_data)
    assert result.status_code == 200

if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument('-d', '--dry-run',
                           action='store_true',
                           help=('Don\'t do any changes (kudos, comments), '
                                 'just print what would be done.'))
    args = argparser.parse_args()

    email, password, athlete_ids = load_config()

    browser, csrf_token, feed_page = login_strava(email, password)

    activities = find_activities_from_feed_page(feed_page)

    for activity in activities:
        avatars = activity.select('a.avatar-athlete')
        if len(avatars) > 0:
            avatar = avatars[0]
            profile_link = avatar['href']

            # Get the athlete from the url i.e '/athletes/1234567
            # The YAML parser parsed the user ids as ints, so we cast the
            # string to an int
            athlete_id = int(profile_link[len('/athletes/'):])

            if athlete_id in athlete_ids:
                kudo_btn = activity.select('button.btn-kudo')[0]
                kudo_img = kudo_btn.select('span.icon-kudo')[0]

                activity_url = activity.select('.entry-title > a')[0]['href']
                activity_url = 'http://www.strava.com{}'.format(activity_url)
                activity_id = activity['id'].split('-')[1]

                if 'icon-dark' in kudo_img['class']:
                    print('Kudoing {}'.format(activity_url))
                    if not args.dry_run:
                        do_kudo(browser, csrf_token, activity_id)

                    comment = generate_comment.get_random_comment()
                    print('Commenting {}'.format(comment))
                    if not args.dry_run:
                        do_comment(browser, csrf_token, activity_id, comment)
