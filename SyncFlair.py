# Modified version of migrate_flair.py from gavin19 https://gist.github.com/gavin19/7874646
import praw
import redditcredentials
# PRAW ident
user = redditcredentials.username
passw = redditcredentials.password
OurSubredditList = ['AskScienceDiscussion', 'AskSciencePanel']
uaList = ['/u/'+user+' for /r/'+OurSubredditList[0], '/u/'+user+' for /r/'+OurSubredditList[1]]
for i in range(0,2):
  ua = uaList[i]
  print ua
  r = praw.Reddit(user_agent=ua)
  r.login(user, passw)
  source_sub = 'AskScience'
  target_sub = OurSubredditList[i]
  # Grab flairs from source subreddit
  flair = r.get_subreddit(source_sub).get_flair_list(limit=None)
  # Dump flair entries into a list
  flair_map = []
  for item in flair:
    if item['flair_text'] == None:
      item['flair_text'] = ''
    if item['flair_css_class'] == None:
      item['flair_css_class'] = ''
    flair_map.append(item)
  # Migrate flairs to target subreddit
  r.get_subreddit(target_sub).set_flair_csv(flair_map)
  print(OurSubredditList[i], " updated")
