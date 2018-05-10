from TwitterAPI import TwitterAPI
import json
import sys

def get_twitter():

    consumer_key = ''
    access_token = ''
    consumer_secret = ''
    access_token_secret = ''
    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)

def robust_request(twitter, resource, params, max_tries=5):

    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print('Got error %s \nsleeping for 15 minutes.' % request.text)
            #sys.stderr.flush()
            #time.sleep(61 * 15)

def read_screen_names(filename):

    with open(filename) as f:
        lines = f.read().splitlines()
    return lines

def get_users(twitter, screen_names):

    return robust_request(twitter, 'users/lookup', {'screen_name':screen_names}, max_tries=5)

def get_friends(twitter, screen_name):

    return sorted(robust_request(twitter, 'friends/ids', {'screen_name':screen_name}, max_tries=5))

def add_all_friends(twitter, users):

    for u in users:
        u['friends'] = get_friends(twitter, u['screen_name'])

def print_num_friends(users):

    for u in users:
        print(u['screen_name'], len(u['friends']))

def get_followers(twitter, screen_name):

    return sorted(robust_request(twitter, 'followers/ids', {'screen_name': screen_name}, max_tries=5))

def add_all_followers(twitter, users):

    for u in users:
        u['followers'] = get_followers(twitter, u['screen_name'])

def print_num_followers(users):

    for u in users:
        print(u['screen_name'], len(u['followers']))

def friend_overlap(users):

    l = []
    for i in range(len(users)):
        for j in range(i+1,len(users)):
            s = len(set(users[i]['friends']) & set(users[j]['friends']))
            l.append(tuple([users[i]['screen_name'], users[j]['screen_name'],s]))
    return sorted(l, key=lambda tup: (-tup[2],tup[0],tup[1]))

def followed_by_all(users, twitter):

    common = []
    user_id = set(users[0]['friends']) & set(users[1]['friends']) & set(users[2]['friends'])
    for i in user_id:
        request = robust_request(twitter, 'users/lookup', {'user_id': i}, max_tries=5)
        for r in request:
            common.append(r['screen_name'])
    return sorted(common)

def get_tweets(twitter, common):

    tweets = []
    for c in common:
        timeline = robust_request(twitter, 'statuses/user_timeline', {'screen_name': c, 'include_rts': False, 'count': 200})
        for i in timeline:
            tweets.append(i)
    return tweets

def friends_of_common(twitter, common):

    fc = open('c_f.txt', 'a')
    fc.truncate(0)
    c = {str(i): get_friends(twitter, i) for i in common}
    json.dump(c, fc)

def save_tweets(tweets):

    json.dump(tweets, open('tweets.txt', 'w'))

def save_commons(common):

    f = open("common.txt","a")
    f.truncate(0)
    for c in common:
        f.write(c + "\n")
    f.close

def main():

    twitter = get_twitter()
    screen_names = read_screen_names('name.txt')
    print('Established Twitter connection.')
    print('Read screen names: %s' % screen_names)
    users = sorted(get_users(twitter, screen_names), key=lambda x: x['screen_name'])
    print('found %d users with screen_names %s' %
          (len(users), str([u['screen_name'] for u in users])))
    add_all_friends(twitter, users)
    print('Friends per candidate:')
    print_num_friends(users)
    add_all_followers(twitter, users)
    print('Followers per candidate:')
    print_num_followers(users)
    print('Friend Overlap:\n%s' % str(friend_overlap(users)))
    common = followed_by_all(users, twitter)
    friends_of_common(twitter, common)
    tweets = get_tweets(twitter, common)
    save_tweets(tweets)
    save_commons(common)

if __name__ == '__main__':
    main()
