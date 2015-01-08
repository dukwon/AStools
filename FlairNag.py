# This thing goes through the modqueue and identifies links over a certain age that need a flair
# Log in, get subreddit
import praw
import redditcredentials
import mytools
import time
now = time.time()
user = redditcredentials.username
passw = redditcredentials.password
target_sub = 'askscience'
ua = '/u/'+user+' for /r/'+target_sub
print ua,"  "
r = praw.Reddit(user_agent=ua)
r.login(user, passw)
sr = praw.objects.Subreddit(r,subreddit_name=target_sub)
# Subreddit actions
# Retrieve items from the modqueue
q = mytools.ReadQueue(sr,"links")
for item in q:
  # Check the item is a submission in the spam filter (not reported)
  if isinstance(item,praw.objects.Submission) and len(item.report_reasons) == 0 and item.approved_by == None:
    # Calculate the age of the post (rounding down minutes and hours)
    timestamp = item.created_utc
    ages = int(now-timestamp)
    agem = ages/60
    ageh = agem/60
    # Ignore the new stuff
    if ageh>0:
      # Read flair
      flair = item.get_flair_choices()['current']['flair_text']
      # Print queue
      print(str(ageh).zfill(2)+':'+str(agem%60).zfill(2)+' ago: ['+flair.__str__()[:3]+'] '+item.__str__()+"  ")
      if flair.__str__() == 'None':
        cs = item.comments
        # More than a few comments means something's going on
        if len(cs) < 5:
          shouldremind = True
          if len(cs) > 0:
            # If there's a few comments, go through them
            for comment in cs:
              # If a mod has already made a comment, leave the submission alone
              if comment.author.is_mod:
                shouldremind = False
          if shouldremind:
            print('Needs a flair  ')
          else:
            print('Mod has commented  ')
        else:
          print('5 or more comments  ')
      else:
        print('Flair is set  ')
# End PRAW stuff
print('/r/'+target_sub+' read in '+str(int(time.time()-now))+' seconds')
