# -*- coding: utf-8 -*-
# This thing goes through the modqueue and identifies links over a certain age that need a flair
# Log in, get subreddit
import praw
import redditcredentials
import mytools
import time
def main():
  dangerphrases = ["would","speed of light","ftl","how can I"]
  now = time.time()
  user = redditcredentials.username
  passw = redditcredentials.password
  target_sub = "askscience"
  ua = "/u/"+user+" for /r/"+target_sub
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
      if ageh>8:
        # Read flair
        flair = item.link_flair_text
        if flair == None:
          flair = "None"
        # Flaired
        if flair != "None":
          reason = "this flaired post "
          if item.author_flair_text != None:
            decision = "Approve"
            reason += "was posted by a flaired user"
          elif ageh > 24:
            decision = "Remove"
            reason += "is over 24h old"
          elif item.score <= 0:
            decision = "Defer"
            reason += "has been downvoted"
          else:
            danger = False
            for phrase in dangerphrases:
              danger = phrase in str(item).lower()
              if danger:
                break
            if danger:
              decision = "Defer"
              reason += "contains the following dangerous word/phrase: **'" + phrase + "'**"
            else:
              decision = "Approve"
              reason += "seems ok"
        # Unflaired
        else:
          reason = "this unflaired post "
          if item.author_flair_text != None:
            decision = "Defer"
            reason += "was posted by a flaired user"
          elif ageh > 12:
            decision = "Remove"
            reason += "is over 12h old"
          else:
            decision = "Defer"
            reason += "is under 12h old"
        print(decision+": ["+flair.__str__()[:3]+"] '"+item.__str__()[:16]+"' because "+reason+".  ")
  # End PRAW stuff
  print("/r/"+target_sub+" read in "+str(int(time.time()-now))+" seconds")
if __name__ == "__main__":
  main()
