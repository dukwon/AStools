# -*- coding: utf-8 -*-
# Gives ReadQueue and ReadLog functions
import sys
import praw
import urllib2
import time
import ast
def ReadQueue(sr,only="",time=0,lim=1000):
  # Retrieve items from the modqueue
  last_item=None
  last_last_item = last_item
  q=[]
  count=0
  qlim=100
  done=False
  print "Fetching first page of modqueue  "
  while not done:
    qgen = sr.get_mod_queue(limit=qlim, params={"after": last_item,"only": only})
    if last_item != None:
      print "Fetching page after", last_item,"  "
    loopcount=0
    for item in qgen:
      if time != 0:
        if item.created_utc < time:
          print "Reached requested timestamp  "
          done=True
          break
      # Counters
      count+=1
      loopcount+=1
      if item not in q:
        # Add item to array
        q.append(item)
      else:
        print "Trying to add duplicate item to array  "
      last_item = item.fullname
      if count == lim:
        done=True
        print "Reached requested number of items  "
        break
    if loopcount<qlim:
      done=True
      print "Reached end of queue  "
    if last_last_item == last_item:
      done=True
      print "Duplicate page  "
    last_last_item = last_item
  if only==None:
    print "Retrieved", count, "items  "
  else:
    print "Retrieved", count, only,"  "
  return q
def ReadLog(sr,time=0,lim=1000,actiontype=""):
   # Retrieve items from the modlog
  last_item=None
  last_last_item = last_item
  l=[]
  count=0
  done=False
  llim=100
  print "Fetching first page of modlog  "
  while not done:
    qgen = sr.get_mod_log(limit=llim, params={"after": last_item,"type": actiontype})
    if last_item != None:
      print "Fetching page after", last_item,"  "
    loopcount=0
    for item in qgen:
      if time != 0:
        if item.created_utc < time:
          print "Reached requested timestamp  "
          done=True
          break
      # Counters
      count+=1
      loopcount+=1
      if item not in l:
        # Add item to array
        l.append(item)
      else:
        print "Trying to add duplicate item to array  "
      last_item = item.id
      if count == lim:
        done=True
        print "Reached requested number of items  "
        break
    if loopcount<llim:
      done=True
      print "Reached end of log  "
    if last_last_item == last_item:
      done=True
      print "Duplicate page  "
    last_last_item = last_item
  if actiontype == None:
    print "Retrieved", count, "actions  "
  else:
    print "Retrieved", count, actiontype, "actions  "  
  return l
def Panel(target_sub="askscience"):
  while True:
    try:
      mods = ast.literal_eval(urllib2.urlopen("http://www.reddit.com/r/"+target_sub+"/about/moderators.json").read())
      break
    except urllib2.HTTPError:
      time.sleep(2)
  # Create list of P+ers
  panel = [mod["name"] for mod in mods["data"]["children"] if "posts" in mod["mod_permissions"] and mod["name"] not in ["AutoModerator","AskScienceModerator"]]
  return panel
def FullMods(target_sub="askscience"):
  while True:
    try:
      mods = ast.literal_eval(urllib2.urlopen("http://www.reddit.com/r/"+target_sub+"/about/moderators.json").read())
      break
    except urllib2.HTTPError:
      time.sleep(2)
  # Create list of P+ers
  panel = [mod["name"] for mod in mods["data"]["children"] if "all" in mod["mod_permissions"]]
  return panel
  
def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    else:
        return 'invalid time'
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return 'sometime in the future'

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff / 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 14:
        return "last week"
    if day_diff < 31:
        return str(day_diff / 7) + " weeks ago"
    if day_diff < 62:
        return "a month ago"
    if day_diff < 365:
        return str(day_diff / 30) + " months ago"
    if day_diff < 2*365:
        return "a year ago"
    return str(day_diff / 365) + " years ago"
