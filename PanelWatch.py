# This thing goes through the log and flags when P+ers approve a question from outside of their field
import praw
import redditcredentials
import mytools
import time
import urllib2
import ast
import re
import os
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
panel = [mod["name"] for mod in mods["data"]["children"] if "posts" in mod["mod_permissions"] and mod["name"] != "AutoModerator"]
# Retrieve items from the modqueue
log = mytools.ReadLog(sr=sr,time=now-3600,actiontype="approvelink")
# Find actions by P+ers
panelactions = [action for action in log if action.mod in panel]
nact=len(panelactions)
print "Stripped log to",nact,"P+ actions  "
# Are they doing at least a third of approvals?
if nact*3 < len(log):
  print nact,"out of",str(len(log))+"?!","The lazy bastards!  "
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
  # Get approver and flair
  username = action.mod
  user_flair = sr.get_flair(r.get_redditor(user_name=username))['flair_css_class']
  # Get post and flair
  post = r.get_submission(url="http://www.reddit.com"+action.target_permalink)
  post_flair = post.get_flair_choices()['current']['flair_css_class']
  # Sanitise input
  if post_flair == None:
    post_flair = "no post"
  if user_flair == None:
    user_flair = "no user"
  # If approver flair class isn't the same as the link flair class, complain
  msg=""
  if post_flair != user_flair:
    msg = "/u/" + username + " with **" + user_flair + "** flair approved question [" + re.sub("[^a-zA-Z0-9\s]","", post.title[:24]) + "](" + post.url + ") with **" + post_flair + "** flair.  "
    reportfile.write("\n"+str(post.created_utc)+"\t"+msg+"  ")
  else:
    msg = user_flair+"="+post_flair
  print("["+str(count)+"/"+str(nact)+"]\t"+msg+"  ")
reportfile.close()
# End PRAW stuff
print('/r/'+target_sub+' read in '+str(int(time.time()-now))+' seconds')
