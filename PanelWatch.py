# This thing goes through the log and flags when P+ers approve a question from outside of their field
import praw
import redditcredentials
import mytools
import time
import urllib2
import ast
import re
import os
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
  while True:
    try:
      mods = ast.literal_eval(urllib2.urlopen("http://www.reddit.com/r/"+target_sub+"/about/moderators.json").read())
      break
    except urllib2.HTTPError:
      time.sleep(2)
  # Create list of P+ers
  panel = [mod["name"] for mod in mods["data"]["children"] if "posts" in mod["mod_permissions"] and mod["name"] not in ["AutoModerator","AskScienceModerator"]]
  # Dictionary of allowed flairs. Key is P+er flair. Entries are post flairs
  allowed = {
    "math": ["math","phys","comp"],
    "phys": ["phys","math","astro","eng"],
    "astro":["astro","math","phys"],
    "chem": ["chem","math","geo"],
    "geo":  ["geo","chem"],
    "eng":  ["eng","phys","math"],
    "comp": ["comp","eng","math"],
    "bio":  ["bio","chem","med"],
    "med":  ["med","bio","neuro"],
    "neuro":["neuro","med","psych"],
    "psych":["psych","neuro","soc"],
    "soc":  ["soc","psych"]
    }
  # Retrieve items from the modqueue
  log = mytools.ReadLog(sr=sr,time=now-3600,actiontype="approvelink")
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
    # Get approver flair
    user_flair = sr.get_flair(r.get_redditor(user_name=action.mod))['flair_css_class']
    # Get post and flair
    post = r.get_submission(url="http://www.reddit.com"+action.target_permalink)
    post_flair = post.link_flair_css_class
    # Sanitise input
    if post_flair == None:
      post_flair = "no post"
    if user_flair == None:
      user_flair = "no user"
    if user_flair not in allowed:
      user_flair += " [WARNING: NOT IN ALLOWED DICT]"
    # Begin to build log message
    msg = "/u/" + action.mod + " with **" + user_flair + "** flair approved question [" + re.sub("[^a-zA-Z0-9\s]","", post.title[:24]) + "](" + post.url + ") "
    # If approver flair class isn't the same as the link flair class, complain
    report=False
    # Something cleverer will be
    # if post_flair not in allowed[user_flair]:
    # For now, dumb flair class matching
    if post_flair != user_flair:
      msg += "with **" + post_flair + "** flair "
      report=True
    else:
      msg += "with " + post_flair + " flair "
    # Check that approver has left a comment
    approver_comments = [comment for comment in post.comments if comment.author.name == action.mod]
    if len(approver_comments) > 0:
      msg += "and left a comment."
    else:
      msg += "and **didn't** leave a comment."
      report=True
    # Write to report file
    if report:
      reportfile.write("\n"+str(post.created_utc)+"\t"+msg+"  ")
    print("["+str(count)+"/"+str(nact)+"]\t"+msg+"  ")
  reportfile.close()
  # End PRAW stuff
  print('/r/'+target_sub+' read in '+str(int(time.time()-now))+' seconds')
if __name__ == '__main__':
  main()
