# 2023-05-09 - shuffle-steam-builds-down.py
#
# A program that moves builds one slot down from their previous slot on Steam.
#
# Written by Yousif Mohamad

import json, urllib.request, subprocess, argparse

# Create a function titled 'shuffle_steam_builds_down'
def shuffle_steam_builds_down(key, appid, count):
    # Store the URL of the web service in the variable name 'url'
    url = 'https://partner.steam-api.com/ISteamApps/GetAppBuilds/v1/?key={}&appid={}&count={}'.format(key,appid,count)

    # Call the web service
    response = urllib.request.urlopen(url)

    # Load the JSON response into a Python data structure
    result = json.loads(response.read())

    # Store the BuildID value in the variable name 'buildID'
    buildIDList = result['response']['builds']

    # Store the integer '1' in the variable name 'branchNumber'
    branchNumber = 0

    # Store the Build ID value in the variable name 'buildID' to be used as a counter
    # Use a 'for' loop to cycle through a dictionary of objects and extract the 'buildID' from the aforementioned dictionary.
    for buildID in buildIDList:
        # subprocess.run() is a method in the subprocess module that runs a command in a new process and captures its output.
        # The string calls the 'steamctl' CLI utility and uses a HTTP POST query named 'SetAppBuildLive' from the ISteamApps
        # interface to specify which build goes into which branch.
        # This repeats a total of 6 times as that is how many branches there are in the depot.
        subprocess.run('steamctl webapi call --method POST ISteamApps.SetAppBuildLive appid={} buildid={} betakey=nightly_build_{}'.format(appid,buildID,branchNumber), shell=True)
        # Increment the value stored in the variable name 'branchNumber' by 1.
        branchNumber+=1

# This conditional checks whether a python module is being run directly or imported.
# If it is being run directly, the condition will be True and execute the code underneath.
# If it is being imported from another python file, it will not run.
if __name__ == '__main__':
    # Parse a series of arguments into this script using the appropriate shell (e.g. MS-DOS, Terminal, etc.)
    parser = argparse.ArgumentParser(description='Program that shuffles steam builds on Steamworks down by one slot')
    parser.add_argument('--key', type=str, metavar='', help='Steamworks Web API publisher authentication key.')
    parser.add_argument('--appid', type=str, metavar='', help='App ID to get the build history of.')
    parser.add_argument('--count', default='5', type=str, metavar='', help='Number of builds to retrieve, the default is 5.')
    args = parser.parse_args()

    # If conditions are met, output the result of the string after it has been replaced.
    if args.key != None and args.appid != None and args.count != None:
        print(shuffle_steam_builds_down(args.key, args.appid, args.count))
    # Instruct the user how to use this program
    else:
        print('Error: Usage is shuffle-steam-builds-down.py --key XXX --appid YYY --count ZZZ,where\nXXX is the Steamworks Web API publisher authentication key\nYYY is the App ID of the Steam product and\nZZZ is the number of builds to retrieve.')
