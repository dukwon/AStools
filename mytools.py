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
