# Python program to Google Chrome Local State
# and create Gnome desktop entries for user profiles

import os
import json
import flatten_json as fj
import pandas as pd
import requests as rq
import string

# Get user home path
userHome = (os.environ['HOME'])
#print("User HOME is: " + userHome)

# Build user's Chrome dir path
chromeDir = (userHome + '/.config/google-chrome')

# Build path of localState
localState = chromeDir + "/Local State"
 
# Check for profile folders in chromeDir
dirEnt = []
profileNames = []
ppString = "/Google Profile Picture.png"
for e in os.listdir(chromeDir):
    if e == 'Safe Browsing':
        exit

    dirEnt = os.path.join(chromeDir, e)
    if os.path.isdir(dirEnt):
        # Build user's Chrome Local State file path
        ppPath = dirEnt + ppString
        if os.path.exists(ppPath):
            # if localState exists, add localState path to profilePaths
            profileNames.append(e)


# Open localState for reading
with open(localState) as file:
    data = file.read()

# load json data from localState
js = json.loads(data)

# for each profile in profilePaths, add to profileDic dictionary
for profileName in profileNames:
    profileDict = pd.json_normalize(js['profile']['info_cache'][profileName]).to_dict()

    # Get Chrome profile name
    CPname = profileDict['name'][0]

    # Get user_name
    user_name = profileDict['user_name'][0]

    # Build chrome profile folder path
    pfPath = chromeDir + '/' + profileName

    # Get user account picture URL
    picURL = profileDict['last_downloaded_gaia_picture_url_with_size'][0]

    # Print values
    #print(CPname + ':' + profileName + ':' + user_name + ':' + pfPath + ':' + picURL)

    # Build wmClass name for desktop entry
    # 1. start with 'chrome'
    wmClassPrefix = 'chrome'
    # 2. remove spaces from profile name
    profileNameString = ''.join(profileName.split())
    # 3, combine into wmClass entry
    wmClass = wmClassPrefix + profileNameString

    # Build exec line for desktop entry
    execLine = 'Exec=/usr/bin/google-chrome-stable %U --class=' + wmClass + ' --user-data-dir=' + pfPath

    # Print execLine
    print(execLine)