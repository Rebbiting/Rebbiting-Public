import praw
from praw.models import Comment
import time
import numpy as np
import random
import traceback

while True:
    try:
        def make_pairs(words):
            for i in range(len(words)-1):
                yield words[i], words[i + 1]

        def markov(troll,c_min,c_max,endw):
            print('{}, {}, {}, {}'.format(troll,c_min,c_max,endw))
            text = troll
            words = text.split()
            pairs = make_pairs(words)
            word_dict = {}
            cwc = 0
            #print('My')
            for word_1, word_2 in pairs:
                if word_1 in word_dict.keys():
                    word_dict[word_1].append(word_2)
                else:
                    word_dict[word_1] = [word_2]
            #print('Words')
            first_word = np.random.choice(words)
            #print("First word")
            while first_word.islower() and cwc < c_max * 1.5:
                first_word = np.random.choice(words)
                #print(first_word)
                cwc = cwc + 1
            chain = [first_word]
            cwc = 0
            #print("Chain start")
            word_c = random.randint(c_min,c_max)
            #print('m_start')
            try:
                try:
                    for i in range(word_c):
                        ran_word = np.random.choice(word_dict[chain[-1]])
                        chain.append(ran_word)
                except:
                    for i in range(0):
                        ran_word = np.random.choice(word_dict[chain[-1]])
                        chain.append(ran_word)
            except:
                traceback.print_exc()
            if endw != ' ':
                print('Yes')
                while ' '.join(chain).endswith(endw) == False and cwc < c_max * 1.5:
                    chain.append(np.random.choice(word_dict[chain[-1]]))
                    cwc = cwc + 1
                    #print(cwc)
            else:
                print('Nope')
            return ' '.join(chain)

        reddit = praw.Reddit(client_id = '-ey9ezFGs-EQcA',
                             client_secret = '5uBNmWHnMmZK2ky9gVKlRo0KH0A',
                             user_agent = 'This bot is you. Author: /u/DefaultAccount0',
                             username = 'this_bot_is_you',
                             password = 'this_bot_is_you')

        j = 0
        l_thread = reddit.live('1544x9tvyy6sz')
        while True:
            for comment in reddit.inbox.unread(limit=25):
                try:
                    subject = comment.subject.lower()
                    if (subject == 'username mention' or 'comment reply' or 'post reply') and isinstance(comment,praw.models.Comment) and comment.author.name != 'this_bot_is_you':
                        t_body = ''
                        li = 0
                        k = 0
                        c_reply = ''
                        rebbitor = None
                        try:
                            rebbitor = comment.body.split()[1]
                            print('1')
                            print(rebbitor)
                        except:
                            if comment.body == 'u/this_bot_is_you':
                                rebbitor = 'this_bot_is_you'
                                print(rebbitor)
                            elif comment.body.lower() == 'me' or comment.body.lower() == 'u/this_bot_is_you me':
                                rebbitor = comment.author.name
                                print(rebbitor)
                            else:
                                rebbitor = comment.body
                                print(rebbitor)
                        try:
                            for commenta in reddit.redditor(rebbitor).comments.new(limit=500):
                                t_body = t_body + commenta.body + '\n\n'
                                li = li + len(commenta.body.split())
                                k = k + 1
                            if True:
                                print('True')
                                c_reply = markov(t_body, int(li/(2*k)), int(li/(0.5*k)), ('.', '?', '!'))
                                print(c_reply)
                                comment.reply(c_reply)
                                try:
                                    l_thread.contrib.add(c_reply)
                                except Exception as e:
                                    print(repr(e))
                        except Exception as e:
                            print(repr(e))
                            if 'u/this_bot_is_you' in comment.body:
                                comment.reply('Error: {}\n\n^(I\'m shit.)'.format(repr(e)))
                            comment.mark_read()
                        print("Finished le fer")
                        j = 0
                        comment.mark_read()
                    else:
                        print('Read')
                        comment.mark_read()
                except Exception as e:
                    if j >= 10:
                        comment.mark_read()
                        print('Failed 10 times, read')
                    j = j + 1
                    print(repr(e))
                    time.sleep(1)
    except:
        traceback.print_exc()
        time.sleep(10)
