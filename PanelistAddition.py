import praw
import redditcredentials
import time
def main():
  # Log in, get subreddits
  user = redditcredentials.username
  passw = redditcredentials.password
  target_sub = 'asksciencepanel'  # migrating to this sub
  current_sub = 'askscience'
  ua = "/u/"+user+" for /r/"+target_sub
  print(ua)
  r = praw.Reddit(user_agent=ua)
  r.login(user, passw)
  target = r.get_subreddit(target_sub)
  current = r.get_subreddit(current_sub)
  # Open file for logging
  if not os.path.exists("reports"):
    os.makedirs("reports")
  if not os.path.exists("reports/PanelAdd.report"):
    reportfile = open("reports/PanelAdd.report", "w")
  else:
    reportfile = open("reports/PanelAdd.report", "a")
  # Fetch list of flaired users and ASP submitters
  target_approved = target.get_contributors(limit=None)
  current_flaired = current.get_flair_list(limit=None)
  # Fill arrays with above
  approved = []
  for i in target_approved:
    approved.append(i.name)
  flaired = []
  for i in current_flaired:
    flaired.append(i['user'])
  # Find new panel members
  to_approve = [i for i in flaired if i not in approved]
  print len(to_approve), "to approve"
  reportfile.write("\nAdding "+str(len(to_approve))+" users")
  # Add new members to ASP
  for i in to_approve:
    try:
      target.add_contributor(i)
      print "Added", i
      reportfile.write("\n"+i)
    except praw.errors.InvalidUser:
      print "No such user", i
      pass
if __name__ == '__main__':
    main()
