import praw
import datetime
from sys import *
import os
import mmap
import time



#This function works as a diagnostic log. Activity, whether or not anything is found, is written here.
def Log_Activity(result):
    log_check = os.path.isfile('Sanitized - file path goes here')
    runtime = datetime.datetime.now()
    hour = str(runtime.hour-12)
    minute = str(runtime.minute)
    year = str(runtime.year)
    day = str(runtime.day)
    month = str(runtime.month)
    date_string = month + "-" + day + "-" + year + ": " + hour + ":" + minute
    if log_check == False:
        file = open('Sanitized - file path goes here')
        file.write('Sanitized - file path goes here')
        file.close()
        file = open('Sanitized - file path goes here')
        file.write("\nScript ran at " + date_string + "----" + "Items found: " + result)
    else:
        file = open('Sanitized - file path goes here')
        file.write("\nScript ran at " + date_string + "----" + "Items found: " + result)

#This function searches the log file to see if the post was already found.
        
def Check_Log_File(url):
    file = open('Sanitized - file path goes here')
    try:
        s = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
    except:
        print "Error?"
    print "Finding " + url
    finder = s.find(url)
    print finder
    if finder != -1:
        print "Duplicate!"
        return 0
    else:
        print "Writing to log..."
        file.write(url)
        file.write("\n")
        file.close()
        return -1

    
        
#This actually does the scanning.
def ScanSubreddit(reddit, file):
    
    
    subreddit = reddit.get_subreddit('forhire')

    submissions = subreddit.get_new(limit=200)
    post_list = []

    #This class is what post information is parsed into.
    class SM:
        def __init__(self, title, author, url, link, s):
            self.title = title
            self.author = author
            self.url = url
            self.link = link
            self.submission_obj = s #Submission object for checking if commented already.

    #This part goes through the found posts to scan for keywords that I am looking for.
    for submission in submissions:
        title = submission.title.lower()
        if 'powershell' in title:
            #print title
            if '[hiring]' in title:
                c = Check_Log_File(submission.url)
                if c == -1:
                    print "New link!"
                    entry = SM(submission.title, submission.author, submission.url, submission.short_link, submission)
                    post_list.append(entry)
        if 'python' in title:
            #print title
            if '[hiring]' in title:
                c = Check_Log_File(submission.url)
                if c == -1:
                    print "New link!"
                    entry = SM(submission.title, submission.author, submission.url, submission.short_link, submission)
                    post_list.append(entry)
        if 'scripting' in title:
            #print title
            if '[hiring]' in title:
                c = Check_Log_File(submission.url)
                if c == -1:
                    entry = SM(submission.title, submission.author, submission.url, submission.short_link, submission)
                    post_list.append(entry)
           
        if 'windows server' in title:
            #print title
            if 'hiring' in title:
                c = Check_Log_File(submission.url)
                if c == 0:
                    entry = SM(submission.title, submission.author, submission.url, submission.short_link, submission)
                    post_list.append(entry)

    return post_list

def Main():
    #Creates the main reddit object for PRAW. Pretty much everything in the module is based off that.
    reddit = praw.Reddit(client_id='Sanitized. Login information',
                     client_secret='Sanitized. Login information',
                     password='Sanitized. Login information',
                     user_agent='Sanitized. Login information',
                     username='Sanitized. Login information')
    #initialize log file
    #Look for the log file at a specific path.
    log_check = os.path.isfile('Sanitized - file path goes here')
    #If it isn't found, create said log file.
    if log_check == False:
        runtime = datetime.datetime.now()
        hour = str(runtime.hour-12)
        minute = str(runtime.minute)
        year = str(runtime.year)
        day = str(runtime.day)
        month = str(runtime.month)
        date_string = month + "-" + day + "-" + year + ": " + hour + ":" + minute
        print "File not found... creating."
        file = open('Sanitized - file path goes here')
        file.write("Log file for reddit /r/forhire scraper: Created " + date_string + "\n")
        file.close()
    else:
        print "Log file found. Scanning..."
    
    message_string = ""
    #Actually scan the /r/forhire subreddit
    posts = ScanSubreddit(reddit, file)
    result = str(len(posts))
    Log_Activity(result)
    runtime = datetime.datetime.now()
    hour = str(runtime.hour-12)
    minute = str(runtime.minute)
    year = str(runtime.year)
    day = str(runtime.day)
    month = str(runtime.month)
    date_string = month + "-" + day + "-" + year + ": " + hour + ":" + minute
    #If it doesn't find any new posts, it goes to sleep for an hour.
    if result == "0":
        next_hour = str((runtime.hour-12)+1)
        date_string_2 = month + "-" + day + "-" + year + ": " + next_hour + ":" + minute
        print "No new results: Sleeping. Will run again at " + date_string_2
        exit()
    #For each found post, it sends you a private message via reddit.
    for item in posts:
        #This formats the private message. It's an array, so, each relevant posting is put here.
        message_string += "\nTitle: " + item.title + " - Link: " + item.url + "\n"
    #You have to explicitly login via praw to send a PM.
    reddit.login('Sanitized. Login information')
    
    subj =  "Scan of /r/forhire on " +  date_string
    reddit.send_message('Sanitized. Login information', subj, message_string)
    next_hour = str((runtime.hour-12)+1)
    date_string_2 = month + "-" + day + "-" + year + ": " + next_hour + ":" + minute
    print "Executed successfully. Will run again at " + date_string_2
    time.sleep(3600)
    Main()


Main()
    

            
