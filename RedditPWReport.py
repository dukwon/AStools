# Publish reports on /r/AskScienceReports
import praw
import redditcredentials
import time
import os
import re
def main():
  # Log in, get subreddits
  user = redditcredentials.username
  passw = redditcredentials.password
  target_sub = 'AskScienceReports'
  ua = "/u/"+user+" for /r/"+target_sub
  print(ua)
  r = praw.Reddit(user_agent=ua)
  r.login(user, passw)
  target = r.get_subreddit(target_sub)
  reportdir="./reports/"
  reportfile="PanelWatch.report"
  if not os.path.exists(reportdir):
    print "No such directory:", reportdir
  if not os.path.exists(reportdir+reportfile):
    print "No such file:", reportfile
  else:
    reportfile = open(reportdir+reportfile, "r")
    now = time.time()
    report = "#PanelWatch Report\n\n---\n"
    title = "PanelWatch Report - " + time.strftime("%a %d %b %Y", time.localtime(now))
    footer = "\n---\n\n Some actions not included. [See full log](http://188.166.55.237/cgi-bin/fetchreport.py)"
    counter = 0
    for line in reversed(reportfile.readlines()):
      timestamp = line[:line.find(".0")]
      try:
        if (now-int(timestamp)) < 24*60*60:
          if len(report+line+footer)<15000:
            body = line[line.find(".0")+3:]
            body1 = re.sub("https?://www\.reddit\.com","",body)
            body2 = re.sub("/[_a-zA-Z0-9]*/\)","/)",body1)
            report += time.strftime("%H:%M", time.localtime(int(timestamp))) + " " + body2
            if line.find("\n")==-1:
              report += "\n"
          else:
            counter+=1
      except ValueError:
        pass
    if counter > 0:
      report += re.sub("Some",str(counter),footer)
    print title
    print report
    print len(report)
#    target.submit(title=title,text=report)
  print target_sub, " updated"
if __name__ == '__main__':
  main()
