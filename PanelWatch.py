# This thing goes through the log and flags when P+ers approve a question from outside of their field
import praw
import redditcredentials
import mytools
import time
import re
import os
import sys
def main():
  now = time.time()
  # Log in, get subreddit
  user = redditcredentials.username
  passw = redditcredentials.password
  target_sub = 'askscience'
  ua = '/u/'+user+' for /r/'+target_sub
  print ua,"  "
  r = praw.Reddit(user_agent=ua)
  r.login(user, passw)
  sr = praw.objects.Subreddit(r,subreddit_name=target_sub)
  # Subreddit actions
  # Get the list of moderators by a shitty shitty method
  panel = mytools.Panel()
  # Dictionary of allowed flairs. Key is P+er flair. Entries are post flairs
  allowed = {
    "maths":     ["maths","physics","computing"],
    "physics":   ["physics","maths","astro","eng"],
    "astro":     ["astro","maths","physics"],
    "chem":      ["chem","maths","geo","physics"],
    "geo":       ["geo","chem"],
    "eng":       ["eng","physics","maths"],
    "computing": ["computing","eng","maths"],
    "bio":       ["bio","chem","med","neuro"],
    "med":       ["med","bio","neuro","chem"],
    "neuro":     ["neuro","med","psych","bio"],
    "psych":     ["psych","neuro","soc"],
    "soc":       ["soc","psych"]
    }
  # Retrieve items from the modqueue
  log = mytools.ReadLog(sr=sr,time=now-24*3600,actiontype="")
  # Find actions by P+ers
  panelactions = [action for action in log if action.mod in panel]
  nact=len(panelactions)
  print "Stripped log to",nact,"P+ actions  "
  # Open file for logging
  if not os.path.exists("reports"):
    os.makedirs("reports")
  if not os.path.exists("reports/PanelWatch.report"):
    reportfile = open("reports/PanelWatch.report", "w")
  else:
    reportfile = open("reports/PanelWatch.report", "a")
  # Loop through actions
  count=0
  for action in panelactions:
    count+=1
    report = False
    msg=""
    # Get P+er flair
    user_flair = sr.get_flair(r.get_redditor(user_name=action.mod))['flair_css_class']
    try:
      if action.action=="approvelink":
        # Get post and flair
        post = r.get_submission(url="http://www.reddit.com"+action.target_permalink)
        post_flair = post.link_flair_css_class
        # Sanitise input
        if post_flair == None:
          post_flair = "no post flair"
        if user_flair == None:
          user_flair = "no user flair"
        if user_flair not in allowed:
          user_flair += " [WARNING: NOT IN ALLOWED DICT]"
        # Begin to build log message
        msg = "/u/" + action.mod + " [" + user_flair + "] approved question [" + re.sub("[^a-zA-Z0-9\s]","", post.title[:24]) + "](" + post.url + ") "
        # If approver flair class isn't the same as the link flair class, complain
        # Something cleverer will be
        if post_flair not in allowed[user_flair]:
          msg += " **[" + post_flair + "]** "
          report=True
        else:
          msg += " [" + post_flair + "] "
        # Check that approver has left a comment
        comments = [comment for comment in post.comments if isinstance(comment, praw.objects.Comment)]
        approver_comments = [comment for comment in comments if comment.author.name == action.mod]
        if len(approver_comments) > 0:
          msg += "and left a comment."
        else:
          msg += "and **didn't** leave a comment."
          report=True
      elif action.action not in ["approvecomment","removecomment","approvelink","editflair"]:
        msg = "/u/" + action.mod + " [" + user_flair + "] did a **non-P+ action:** " + action.action + " on [**this**]("+action.target_permalink+") post." 
        report=True
      else:
        msg = "/u/" + action.mod + " [" + user_flair + "] did a P+ action: " + action.action + " on [**this**]("+action.target_permalink+") post."
      # Write to report file
      if report:
        reportfile.write("\n"+str(action.created_utc)+"\t"+msg+"  ")
      print("["+str(count)+"/"+str(nact)+"]\t"+msg+"  ")
    except:
      print("["+str(count)+"/"+str(nact)+"]\tSomething went wrong: "+sys.exc_info()[0]+"  ")
  reportfile.close()
  # End PRAW stuff
  print('/r/'+target_sub+' read in '+str(int(time.time()-now))+' seconds')
if __name__ == '__main__':
  main()
