#!/usr/bin/env python
# coding: utf-8

# In[3]:


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


# In[ ]:


#### importing modules ####

pip install pysaucenao
pip install jaconv
pip install tqdm

from pysaucenao import SauceNao
import os
import unicodedata as ud
import time
from tqdm import tqdm
import jaconv


# In[ ]:


#### this section is for variables that can be modified for different results ##

api = 'FILLUP'  # API key from SauceNAO
                # THIS SECTION MUST BE FILLED

sauce = SauceNao(api_key = api,results_limit = 4, min_similarity = 80)  # change API, number of results, minimum similarity

path = r'FILLUP'  # working directory where all images should be placed in before script runs
os.chdir(path)    # THIS SECTION MUST BE FILLED

max_file_size = 30000000  # if image is too large, SauceNAO will reject it and script will return an error
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
    
## splitting names to take everything before @
def split_at(processed):
    if processed.count('@') == 1:
        if len(processed.split('@')[0]) > 1:
            processed = processed.split('@')[0]
    return processed

## removing troublesome characters from title
def remove_chars(source):
    char_removed = '<>?,.\/;\':\"[]\\{}|+_)(*&^%$#!=-'
    title_remove = source
    for i in char_removed:
        title_remove = title_remove.replace(i,' ')
    return title_remove
        
## processing of source
def process(source):
    processed = source_index_anime(source,0)
    index = source_index(source, 0)
    author_url = source[0].author_url
    source_url = source[0].source_url
    title_process = remove_chars(source[0].title)
    if (processed == None) or (processed == ''):
        for results_count in range(0,len(source)):
            processed = convertion_alphabets(source_index_anime(source,results_count))
            index = source_index(source,results_count)
            if (processed == None) == False or (processed == '') == False:
                break
        author_url = source[results_count].author_url
        source_url = source[results_count].source_url
        title_process = remove_chars(source[results_count].title)
    processed = split_at(processed)
    processed = convertion_alphabets(processed)
    return(processed, title_process, author_url, index, source_url)

## converting author name to alphabets instead of katakana/hiragana
def convertion_alphabets(source):
    return jaconv.z2h(jaconv.kana2alphabet(jaconv.kata2hira(source)), ascii = True)

## check if source is an anime
def source_index_anime(source, count):
    if source[count].index == 'Anime':
        return 'Anime'
    else:
        return convertion_alphabets(check_author_type(source[count].author_name))
    
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
    if check_existence_file(pre,ext,author_name,1):
        new_filename = pre + '_2' + ext
    elif check_existence_file(pre,ext,author_name,2):
        new_filename = pre + '_3' + ext
    elif check_existence_file(pre,ext,author_name,3):
        new_filename = pre + '_4' + ext
    elif check_existence_file(pre,ext,author_name,4):
        new_filename = pre + '_5' + ext
    elif check_existence_file(pre,ext,author_name,5):
        new_filename = pre + '_6' + ext
    elif os.path.isfile(author_name + '\\' + pre + ext):
        new_filename = pre + '_1' + ext
    return(new_filename)

## create a textfile containing the URL of the artist's page
def create_textfile(author_name, index, url):
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
    if url in text_file.read():
        return(True)
    else:
        return(False)

## change URL to source URL if author URL is None
def change_url(url, source_url):
    if url == None:
        return(source_url)
    else:
        return url


# In[2]:


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
    current_iteration += 1
    if os.stat(image).st_size > max_file_size:
        folder_moving(image, '~too large', image)
    elif image.endswith('.png') or image.endswith('.jpeg') or image.endswith('.jpg') or image.endswith('.gif') or image.endswith('.jfif'):
        source = await sauce.from_file(image)
        if len(source) > 0:
            processed_source = process(source)
            author_name = processed_source[0]
            title = processed_source[1]
            url = change_url(processed_source[2], processed_source[4])
            index = processed_source[3]
            if author_name == None or author_name == '' or author_name == 'Unknown':
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
        elif source.long_remaining == 0:
            limit_reached = True
            break
        else:
             continue
        long_remaining = source.long_remaining
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




