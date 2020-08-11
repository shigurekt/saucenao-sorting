# saucenao-sorting
Sort your anime images into folders by artist, with additional information


# What the script does

Image sorted into folders
- Folders are named after the artist
Image within folders will be renamed according to what the title on the source is
- In case of duplicate titles, image will have a _(int) appended onto the end
- To prevent duplicates of actual images, use dupeGuru before using this script
Link to artists' pages or the image sources' pages will be created within .txt files in each folder
Links are divided by the domain of the artists' pages/sources' pages (e.g Danbooru, Pixiv, Twitter)
In the case that the result from SauceNAO does not provide an artist page, then the script will use the image 
source's page instead


# IMPORTANT NOTES

This script will only process files in the following formats:
   .png, .jpg, .jpeg, .gif, .jfif
These formats are the ones that have been encountered so far
To add more formats, either edit the section in the script, or contact the creator
There's probably a more efficient way to do this part, but the creator may be too lazy to do research so far
so if there's any way to do it, contact him

You MUST register on SauceNAO for this script to work properly
While you don't need to register to do searches on SauceNAO, this script depends on the API (which requires an account)
If you wish to use this script without an account, edit the sauce variable to remove the API section
It is highly beneficial to register, so I encourage you to do so
  - Higher limits

There are certain variables that you MUST modify for this script to run
They are:
  - api
  - path


# Credits 

This script was created by ShiguRekt with help from BlueTicker117
ShiguRekt can be found on https://github.com/shigurekt
 - Shigurekt can also be contacted @ShiguRekt2 on Twitter
 BlueTicker117 can be found on github at https://github.com/BlueTicker117

 Also huge thanks to Makoto (https://pypi.org/user/MakiPy/) for their module to use SauceNAO API


# Disclaimer

 This script was created by someone relatively new to Python, so there may be inefficient parts of the script.
 However, as much as possible has been done to ensure that the bottleneck to the script is outside 
 the control of the script, meaning that the majority of the script running is waiting for 
 SauceNAO to return a result, or for limits set by SauceNAO to reset

 If there are any errors with the script, feel free to contact the creator of the script for help.
 This also includes any suggestions to improve functionality of the script.
 It is always appreciated to improve this script and help others as well as myself
