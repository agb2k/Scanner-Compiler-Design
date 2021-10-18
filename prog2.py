import statistics
import tweepy
import re
import enchant
import os

# Twitter API keys
APIKey = os.environ.get("TWITTER_API_KEY")
APISecretKey = os.environ.get("TWITTER_API_KEY_SECRET")

accessToken = os.environ.get("TWITTER_ACCESS_TOKEN")
accessTokenSecret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

# Tweepy Authentication
auth = tweepy.OAuthHandler(APIKey, APISecretKey)
auth.set_access_token(accessToken, accessTokenSecret)

api = tweepy.API(auth)

# Initializing lists, dictionaries and strings
words = []
final_words = []
final_words_cleaned = []
unique_words = []
word_count = {}
sorted_dict = {}
suggestions = {}
spellCheck_clean = []
s = ""

# Gets user input for type of analysis required
option = input(
    "Choose from the following options: \na. Search Twitter for a key term and perform analysis on the corresponding "
    "data received\nb. Grab Tweets from \"tweets.txt\" and perform analysis\n>> ")


# Search for tweets and adds it to the text file
def twitter_search(search):
    f_write = open('tweets.txt', 'w', encoding='utf-8')
    public_tweets = api.search(q=search + " -filter:retweets", lang="en")
    for tweet_twitter in public_tweets:
        f_write.write(str(tweet_twitter.text) + "\n")
    f_write.close()


# Gets input on whether the user would like to implement the autocorrect feature
spellCheck = input("Would you like to use autocorrect? (Y/N)\n>> ")

# Takes place if user selects option a, grabbing tweets from the API
if option == "a":
    num_terms = int(input("How many search terms (including alternatives) would you like to include?\n>> "))
    for n in range(num_terms):
        if n == 0:
            s = (input("Enter (alternative) search term to be included:\n>> "))
        else:
            s = s + " OR " + (input("Enter (alternative) search term to be included:\n>> "))
    num_non_terms = int(input("How many search terms would you like to exclude?\n>> "))
    for j in range(num_non_terms):
        s = s + " -" + (input("Enter search term to be excluded:\n>> "))
    twitter_search(s)
    print(f"Your search term: {s}")

# Opens text files
input_f = open('tweets.txt', 'r', encoding='utf-8')
unique_f = open("uniqueWords.txt", 'w', encoding='utf-8')
median_f = open("median.txt", "w", encoding='utf-8')
custom_f = open("customDictAddOn.txt", 'r', encoding='utf-8')

# Reads, converts to lowercase and stores contents of the text file to the text variable
# It's converted to lowercase to avoid case-sensitive issues
text_file = input_f.read().lower()

# Separates the text by certain delimiters and stores in tweets list
tweets = re.split('[; |, |/ |\n |""]', text_file)

# For loop that splits each tweets variable into its own lists and adds it to the words list
for tweet in tweets:
    words.append(tweet.split())

# For loop that splits up each smaller list within the words list into words and adds it to the words list
for lists in words:
    final_words = final_words + lists


# Gets rid of emojis
def strip_emoji(text):
    re_emoji = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    return re_emoji.sub(r'', text)


# Cleans data using regex
def regex_cleaner(w1):
    regx = '[!:“#_$.?)(”~`‘^}{><+=;…\]\[\"]'
    word_new = re.sub(regx, '', w1)
    final_words_cleaned.append(word_new)


# Cleans data
for word in final_words:
    word = strip_emoji(word)
    if word == "rt" or word == '' or word == "-" or word == "—":
        continue
    elif word.startswith("@") or word.startswith("http") or word.startswith("t.co"):
        continue
    elif word.startswith("\'"):
        new_word = re.sub('[\']', '', word, 1)
        regex_cleaner(new_word)
    elif word.startswith("&"):
        new_word = re.sub('[&]', '', word, 1)
        regex_cleaner(new_word)
    elif word.startswith("#"):
        new_word = re.sub('[#]', '', word, 1)
        regex_cleaner(new_word)
    elif word.find("…rt"):
        new_word = word.replace('…rt', '')
        regex_cleaner(new_word)
    elif bool(re.search('[!:“#_$.?)(”~`‘^}{><+=;…\]\[\"]', word)):
        regex_cleaner(new_word)
    else:
        final_words_cleaned.append(word)

# Takes place if user uses autocorrect feature
if spellCheck.lower() == "y":
    # Initializing dictionary
    us_dict = enchant.DictWithPWL("en_US", "customDictAddOn.txt")
    uk_dict = enchant.DictWithPWL("en_GB", "customDictAddOn.txt")

    # Checks if word exists in dictionary to add to list. If not, it finds the closest word and adds that instead.
    for word in final_words_cleaned:
        if len(word) > 0:
            if us_dict.check(word) or uk_dict.check(word):
                spellCheck_clean.append(word)
            else:
                if bool(uk_dict.suggest(word)) and bool(uk_dict.suggest(word)):
                    new_word_uk = str(uk_dict.suggest(word)[0]).lower()
                    suggestions[word] = new_word_uk
                    spellCheck_clean.append(new_word_uk)
                else:
                    continue

    # For loop that checks how many times a word appears in the list and adds the corresponding info to a dictionary
    for word_clean in spellCheck_clean:
        num = spellCheck_clean.count(word_clean)
        word_count[word_clean] = num
        num_count = list(word_count.values())
        if num == 1:
            unique_words.append(word_clean)

# Takes place if user doesn't want to use the autocorrect feature
if spellCheck.lower() == "n":
    for word_clean in final_words_cleaned:
        num = final_words_cleaned.count(word_clean)
        word_count[word_clean] = num
        num_count = list(word_count.values())
        if num == 1:
            unique_words.append(word_clean)

# Sort keys
sorted_keys = sorted(word_count, key=word_count.get)

# Sort dictionary
for w in sorted_keys:
    sorted_dict[w] = word_count[w]

# Sorts the num_count and unique_words list
num_count.sort()
unique_words.sort()

print(f"Suggestion List:{suggestions}")
print(f"Word Count Dict:{sorted_dict}")
print(f"Word Count List: {num_count}")

# Finds the median, mean & mode using statistics library
median = statistics.median(num_count)
mean = statistics.mean(num_count)
mode = statistics.mode(num_count)

# Writes unique words to text file
unique_f.write("Unique Words: ")
for word in unique_words:
    unique_f.write(word + ", ")

# Writes median to text file
median_f.write(
    f"Word Count Dict:{sorted_dict}\nWord Count List: {num_count}\nMedian: {str(median)}\nMean: {str(mean)}\nMode: {str(mode)}")

# Closes all open file readers
input_f.close()
unique_f.close()
median_f.close()
