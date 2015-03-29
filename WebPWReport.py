#! /bin/python
# Publish reports somewhere visible
import time
import os
import snudown
import mytools
print "Content-type: text/html"
print
print """
<html>
<head>
<title>AskScience PanelWatch report</title>
<link rel="stylesheet" type="text/css" href="//www.redditstatic.com/old-markdown.Lcx8i-O12_8.css" media="all">
<link rel="stylesheet" type="text/css" href="//www.redditstatic.com/reddit.SqZ51CYvVKk.css" media="all">
<script type="text/javascript" language="JavaScript">
<!--
function livetimes() {
  var timeboxes = document.getElementsByClassName("live-timestamp");
  var i;
  for(i = 0; i < timeboxes.length; i++) {
    var datetime = timeboxes[i].getAttribute("datetime");
    var date = new Date();
    date.setTime(parseInt(datetime)*1000)
    timeboxes[i].title=date.toString();
  }
}
//-->
</script>
</head>
<body onload="livetimes();">
<div id="header" role="banner">
<div id="header-bottom-left"><a href="//www.reddit.com/" id="header-img" class="default-header" title="">reddit.com</a>&nbsp;<span class="hover pagename redditname"><a href="//www.reddit.com/r/askscience/">AskScience</a>: PanelWatch Report</span></div>
</div>
<div class="content" role="main">
"""
reportdir="/home/bot/AskSci/AStools/reports/"
reportfile="PanelWatch.report"
if not os.path.exists(reportdir):
  print "No such directory:", reportdir
if not os.path.exists(reportdir+reportfile):
  print "No such file:", reportfile
else:
  print """<div id="siteTable" class="sitetable modactionlisting">
<table class="generic-table">
<tbody>
  """
  reportfile = open(reportdir+reportfile, "r")
  now = time.time()
  counter = True
  for line in reversed(reportfile.readlines()):
    timestamp = line[:line.find(".0")]
    try:
      then=time.localtime(int(timestamp))
      counter = not counter
      if counter:
        colour="#FFF"
      else:
        colour="#ECECEC"
      print '<tr class="modactions" style="background-color:', colour,'">'
      print ('<td class="timestamp"><time class="live-timestamp" datetime="'+timestamp+'" title="'+time.strftime("%a %d %b %Y %H:%M %Z", then)+'">'+mytools.pretty_date(int(timestamp))+'</time></td>')
      print '<td class="description">', snudown.markdown(line[line.find(".0")+3:]), "</td>"
      print "</tr>"
    except ValueError:
      pass
  print """</tbody>
</table>
</div>
  """
print """</div>
</body>
</html>
"""
