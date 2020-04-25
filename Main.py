import praw
import csv
import time
from datetime import datetime
from pathlib import Path

reddit = praw.Reddit(client_id="NHDbHQms44VAcw",
                     client_secret="SqyyUq4Hpv47GCNXc8CfQ8dXWiw",
                     username="ARMScrawler",
                     password="CrawlerARMS",
                     user_agent="ARMScrawler")


def create_directory(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def generate_file_name(subreddit, category):
    path = "Data/" + category + "/" + datetime.now().strftime("%d%B")
    create_directory(path)
    file_name = path + "/" + subreddit + ".csv"
    return file_name


def split_list(lista, size):
    new_list = []
    position = 0
    if size > len(lista):
        new_list.append(lista)
    else:
        while position + size < len(lista):
            new_list.append(lista[position: position + size])
            position += size
        else:
            new_list.append(lista[position:])
    return new_list


def get_top_posts(subreddit, time_period='day'):
    try:
        lastday_subreddit = list(reddit.subreddit(subreddit).top(time_period))
        print(lastday_subreddit[-1].id)
        with open(generate_file_name(subreddit, "Top"), "w", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file, delimiter='/')
            writer.writerow(["Subreddit", "Title", "ID", "Score", "Upvote Ratio"])
            for lista in split_list(lastday_subreddit, 10):
                start_time = time.time()
                for submission in lista:
                    line = list()
                    line.append(submission.subreddit.display_name)
                    line.append(submission.title)
                    line.append(submission.id)
                    line.append(submission.score)
                    line.append(submission.upvote_ratio)
                    writer.writerow(line)
                end_time = time.time()
                print(end_time - start_time)
                time.sleep(60 - (end_time - start_time))
    except Exception as e:
        print(e)


def populate_today_top(list_of_subreddits):
    for subreddit in list_of_subreddits:
        try:
            print(50 * "*")
            print(subreddit.title)
            get_top_posts(subreddit.display_name)
        except Exception as e:
            print(e)

def start_data_extraction():
    popular_subreddits = list(reddit.subreddits.popular())
    populate_today_top(popular_subreddits)


start_data_extraction()
# get_top_posts("The Witcher")
# print(reddit.subreddit("The Witcher").display_name)
# print(list(reddit.subreddit("witcher").top(limit = 10)))
# list(reddit.subreddit(subreddit).top(time_period))
# popular_subreddits = list(reddit.subreddits.popular())
# print(popular_subreddits)

# popular_subreddits = list(reddit.subreddits.popular())
# for i in popular_subreddits:
#     print(i.title)

# import pandas
# # pandas.set_option('display.max_columns', None)
# csvfile = pandas.read_csv('Data.csv', encoding='utf-8', delimiter='/')
# print(csvfile)




# subreddit = reddit.subreddit('python')
# print(subreddit.description)
# print(subreddit.public_description)
# hot_python = subreddit.hot(limit=5)
# for submission in hot_python:
#     if submission.stickied is False:
#         print(submission.title)
#         print(submission.id)
#
# for count in range(0, 10):
#     print(popular_subreddits[count])
#
# print(len(popular_subreddits))







