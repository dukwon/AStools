import praw
import redditcredentials
user = redditcredentials.username
passw = redditcredentials.password


def main():

    approved = []
    flaired = []

    target_sub = 'asksciencepanel'  # migrating to this sub
    current_sub = 'askscience'
    ua = "/u/"+user+" for /r/"+target_sub
    print(ua)
    r = praw.Reddit(user_agent=ua)
    r.login(user, passw)

    target = r.get_subreddit(target_sub)
    current = r.get_subreddit(current_sub)

    target_approved = target.get_contributors(limit=None)
    current_flaired = current.get_flair_list(limit=None)

    for i in target_approved:
        approved.append(i.name)

    for i in current_flaired:
        flaired.append(i['user'])

    to_approve = [i for i in flaired if i not in approved]
    print(len(to_approve), "to approve")

    for i in to_approve:
        try:
            target.add_contributor(i)
            print("Added", i)
        except praw.errors.InvalidUser:
            pass

if __name__ == '__main__':
    main()
