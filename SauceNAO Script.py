#!/usr/bin/env python
# coding: utf-8

# In[ ]:


####         ####
#### READ ME ####
####         ####

## This script aims to sort images by artists using the SauceNAO API


#### What the script does

## Image sorted into folders
## - Folders are named after the artist
## Image within folders will be renamed according to what the title on the source is
## - In case of duplicate titles, image will have a _(int) appended onto the end
## - To prevent duplicates of actual images, use dupeGuru before using this script
## Link to artists' pages or the image sources' pages will be created within .txt files in each folder
## - Links are divided by the domain of the artists' pages/sources' pages (e.g Danbooru, Pixiv, Twitter)
## - In the case that the result from SauceNAO does not provide an artist page, then the script will use the image 
##   source's page instead


#### IMPORTANT NOTES

## This script will only process files in the following formats:
##    .png, .jpg, .jpeg, .gif, .jfif
## These formats are the ones that have been encountered so far
## To add more formats, either edit the section in the script, or contact the creator
## There's probably a more efficient way to do this part, but the creator may be too lazy to do research so far
## so if there's any way to do it, contact him

## You MUST register on SauceNAO for this script to work properly
## While you don't need to register to do searches on SauceNAO, this script depends on the API (which requires an account)
## If you wish to use this script without an account, edit the sauce variable to remove the API section
## It is highly beneficial to register, so I encourage you to do so
##    - Higher limits

## There are certain variables that you MUST modify for this script to run
## They are:
##    - api
##    - path


#### Credits 

## This script was created by ShiguRekt with help from BlueTicker117
## ShiguRekt can be found on https://github.com/shigurekt
## - Shigurekt can also be contacted @ShiguRekt2 on Twitter
## BlueTicker117 can be found on github at https://github.com/BlueTicker117

## Also huge thanks to Makoto (https://pypi.org/user/MakiPy/) for their module to use SauceNAO API


#### Disclaimer

## This script was created by someone relatively new to Python, so there may be inefficient parts of the script.
## However, as much as possible has been done to ensure that the bottleneck to the script is outside 
## the control of the script, meaning that the majority of the script running is waiting for 
## SauceNAO to return a result, or for limits set by SauceNAO to reset

## If there are any errors with the script, feel free to contact the creator of the script for help.
## This also includes any suggestions to improve functionality of the script.
## It is always appreciated to improve this script and help others as well as myself

#### Version 2


# In[ ]:


#### importing modules ####

pip install --user pysaucenao
pip install --user tqdm
pip install --user jaconv
pip install --user 

from pysaucenao import SauceNao
import os
import unicodedata as ud
import time
from tqdm import tqdm
import jaconv
import re
import urllib.parse


# In[ ]:


#### this section is for variables that can be modified for different results ##

api = ''  # API key from SauceNAO

sauce = SauceNao(api_key = api,results_limit = 5, min_similarity = 60)  # API, number of results, minimum similarity

path = r''  # working directory where all images
os.chdir(path)                                                # should be placed in before script runs

max_file_size = 30000000  # Maximum size of image (in KB)
                          # Prevents SauceNAO from returning an error
sleep_time = 35  # due to limit of searches made in 30 seconds, script must wait for that 30 seconds to clear


# In[ ]:


#### functions that are used within the script ####

##check if author title is in latin alphabets instead of Japanese
latin_letters= {}
def is_latin(uchr):
    try: return latin_letters[uchr]
    except KeyError:
         return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))
def check_latin(unistr):
    return all(is_latin(uchr)
           for uchr in unistr
           if uchr.isalpha())

## check if author name is a str or a list, takes the first of the list. Returns a str of author name
def check_author_type(raw_author):
    if type(raw_author) == str:
        return raw_author
    elif type(raw_author) == list:
        return(raw_author[0])
    
## splitting names to remove event titles, etc
## In case of any new events not covered by this function, add to event_splits variable
def split(string):
    split_string = string
    if split_string.count('@') == 1:
        if len(split_string.split('@')[0]) > 1:
            split_string = split_string.split('@')[0]
    split_string = re.split(r'[\\//]',split_string)[0]
    events = re.compile(r'..+'
                        r'(([0-9一二三四五六七八九十]日目)'+'|'
                        r'[月火水木金土日]曜' + '|'
                        r'C[0-9]{2,4}'+'|'
                        r'夏mote' + '|'
                        r'冬mote' + '|'
                        r'お仕事|o仕事|仕事'+'|'
                        r'komi[0-9]' + '|'
                        r'次回' + '|'
                        'AFA'+'|'
                        r'[a-zA-Z][0-9]{2,3}[a-zA-Z]{1,2}'+'|'
                        r'夏komi|冬komi'+'|'
                        r'[0-9]月)')
#     events_split = re.compile(r'..+' + events)
#     events_split = (r'..+' + events)
    split_string = re.split(events,split_string)[0]
    return split_string

## removing troublesome characters from title (AFTER SPLIT)
def remove_chars(source):
    removed = source
    removed = removed.replace('￦', 'W')
    removed = re.sub(r'\&amp',r' and ', removed)
    brackets = r'({[<>]})'
    for i in brackets:
        removed = removed.strip(i)
    removed = re.sub(r'\(.+\)|\[.+\]|\{.+\}|\<.+\>','',removed)
    removed = removed.replace(' ', '_')
    removed = re.sub('\W','',removed)
    removed = removed.strip()
    removed = removed.strip('_')
    return removed
        
## processing of source
def process(source):
    author_name = source_index_anime(source,0)
    index = source_index(source, 0)
    author_url = source[0].author_url
    source_url = source[0].source_url
    title_process = source[0].title
    if empty_string(author_name):
        results_count = 0
        for results_count in range(1,len(source)):
            author_name = source_index_anime(source,results_count)
            index = source_index(source,results_count)
            if (empty_string(author_name)) == False:
                author_name = convertion_alphabets(author_name)
                author_name = split(author_name)
                author_name = remove_chars(author_name)
                break
        author_url = source[results_count].author_url
        source_url = source[results_count].source_url
        title_process = source[results_count].title
        if (empty_string(author_name)):
            author_name = source_index_anime(source,0)
    elif (empty_string(author_name)) == False:
        author_name = convertion_alphabets(author_name)
        author_name = split(author_name)
        author_name = remove_chars(author_name)
    else:
        author_name = source_index_anime(source,0)
    if empty_string(title_process):
        title_process = 'No Title'
    else:
        title_process = remove_chars(title_process)
    return(author_name, title_process, author_url, index, source_url)

## converting author name to alphabets instead of katakana/hiragana
def convertion_alphabets(source):
    return jaconv.z2h(jaconv.z2h(jaconv.kana2alphabet(jaconv.kata2hira(source)), digit = True))

## check if source is an anime
def source_index_anime(source, count):
    if source[count].index == 'Anime':
        return 'Anime'
    else:
        return check_author_type(source[count].author_name)
    
## returns purely the index of source
def source_index(source, count):
    return source[count].index

## creates a folder of author's name, and moves image to that folder
def folder_moving(image, author_name, title_func):
    if os.path.isdir(author_name):
        title_modified = return_new_filename(title_func, author_name)
        os.rename(image , author_name + '\\' + title_modified)
    else:
        os.mkdir(author_name)
        title_modified = return_new_filename(title_func, author_name)
        os.rename(image , author_name + '\\' + title_modified)

## check if filename exists for same title
def check_existence_file(pre,ext,author_name,number):
    tf = os.path.isfile(author_name + '\\' + pre + '_' + str(number) + ext)
    return(tf)
    
## return new filename for repeat titles
def return_new_filename(filename, author_name):
    pre = os.path.splitext(filename)[0]
    ext = os.path.splitext(filename)[1]
    new_filename = filename
    path = author_name + '\\%s%s' % (pre,ext)
    count = 1
    while os.path.isfile(path):
        new_filename = '\\%s_%d%s' % (pre,count,ext)
        path = author_name + new_filename
        count += 1
    return(new_filename)

## create a textfile containing the URL of the artist's page
def create_textfile(author_name, index, url):
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url[1] == 'twitter.com':
        index = 'Twitter'
        user = parsed_url[2].split(r'/')[1]
        url = urllib.parse.urlunparse(parsed_url._replace(path = (r'/' + user)))
    elif parsed_url[1] == 'www.pixiv.net':
        index = 'Pixiv'
    if os.path.isfile(author_name + '\\' + index + '.txt'):
        if textfile_url_duplicate(author_name, index, url) == False:
            text_file = open(author_name + '\\' + index + '.txt', 'a+')
            text_file.write('\n' + str(url))
    else:
        text_file = open(author_name + '\\' + index + '.txt', 'w+')
        text_file.write(str(url))

## check textfiles to prevent duplicate URLs
def textfile_url_duplicate(author_name, index, url):
    text_file = open(author_name + '\\' + index + '.txt', 'r')
    if empty_string(text_file.read()):
        return(True)
    elif (url in text_file.read()):
        return(True)
    else:
        return(False)

## change URL to source URL if author URL is None
def change_url(url, source_url):
    if empty_string(url):
        return(source_url)
    else:
        return url
    
## check if string is empty
def empty_string(string):
    return(string == None or string == '' or string == 'Unknown' or string == 'nameless')
    


# In[ ]:


#### the actual script ####

current_iteration = 0
limit_reached = False
long_remaining = -1

if os.path.isdir(r'~problems') == False:
    os.mkdir(r'~problems')
if os.path.isdir(r'~no results') == False:
    os.mkdir(r'~no results')
if os.path.isdir(r'~too large') == False:
    os.mkdir(r'~too large')
if os.path.isdir(r'~anime') == False:
    os.mkdir(r'~anime')

    
for image in tqdm(os.listdir()):
    if os.stat(image).st_size > max_file_size:
        folder_moving(image, '~too large', image)
    elif image.endswith('.png') or image.endswith('.jpeg') or image.endswith('.jpg') or image.endswith('.gif') or image.endswith('.jfif'):
        current_iteration += 1
        source = await sauce.from_file(image)
        long_remaining = source.long_remaining
        if len(source) > 0:
            processed_source = process(source)
            author_name = processed_source[0]
            title = processed_source[1]
            url = change_url(processed_source[2], processed_source[4])
            index = processed_source[3]
            if empty_string(author_name):
                folder_moving(image, '~problems', image)
            elif author_name == 'Anime':
                folder_moving(image, '~anime', image)
            else:
                folder_moving(image, author_name, title + os.path.splitext(image)[1])
                create_textfile(author_name, index, url)
        elif len(source) == 0:
            folder_moving(image, '~no results', image)
        if source.short_remaining == 0:
            time.sleep(sleep_time)
        if source.long_remaining == 0:
            limit_reached = True
            break
    long_remaining = long_remaining

if limit_reached == True:
    print('Daily limit hit, done for today.')
elif limit_reached == False:
    print('All images processed!')

print('Number of no results: ' + str(len(os.listdir(r'~no results'))))
print('Number of other problems: ' + str(len(os.listdir(r'~problems'))))
print('Number of too large: ' + str(len(os.listdir(r'~too large'))))

if long_remaining == -1:
    print('Remaining number of searches (24hr): ' + 'ERROR')
else:
    print('Remaining number of searches (24hr): ' + str(long_remaining))


# In[ ]:


#### How many images left to be sorted

files_in_folder = os.listdir()
folders_created = 0
images_remaining = 0
total = len(files_in_folder)

for i in range(0, len(files_in_folder)):
    if os.path.isdir(files_in_folder[i]):
        folders_created += 1
    if os.path.isdir(files_in_folder[i]) == False:
        images_remaining += 1

print('Number of folders created: ' + str(folders_created))
print('Number of images remaining: ' + str(images_remaining))
print('Error?' + str((total == images_remaining + folders_created) == False))


# In[ ]:


#### For trouble-shooting

# image = r'E:\Pictures\Online stuff\Sorting\Python Processing\~problems\はい提督あん.jpg'

# source = await sauce.from_file(image)
# long_remaining = source.long_remaining
# if len(source) > 0:
#     processed_source = process(source)
#     author_name = processed_source[0]
#     title = processed_source[1]
#     url = change_url(processed_source[2], processed_source[4])
#     index = processed_source[3]

# print('Sources from SauceNAO:')
# for i in range(0,len(source)):
#     print(source[i])
# print('----------------------------')
# print('Processed source:')
# print(processed_source)

