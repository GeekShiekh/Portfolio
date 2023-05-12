import sys, os, argparse, subprocess
from datetime import datetime

def generate_steam_script(src, dst, version, no_changes, setlive):
    with open(src) as src_file:
        contents = src_file.read()

    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # print("date and time =", dt_string)
    contents = contents.replace('%DESC%', "IA Nightly Build - " + version + " built at " + dt_string)
    contents = contents.replace('%SETLIVE%', setlive)
    if no_changes:
        contents = contents.replace('%PREVIEW%', '1')
    else:
        contents = contents.replace('%PREVIEW%', '0')
    with open(dst,'w') as scriptfile:
        scriptfile.write(contents)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Publish a build to Steam')
    parser.add_argument("--steamcmd", help="absolute path to steamcmd.exe.")
    parser.add_argument('--version', help='specify the version to remap.')
    parser.add_argument('--branch', help='specify the branch to direct this upload to on steam')
    parser.add_argument('--no-changes', '-n', help="don't make any changes, just show what you would do")
    parser.add_argument('--account', help="account to log into steam with")
    parser.add_argument('--password',help="password for account")
    args = parser.parse_args()

    if args.steamcmd != None and args.version != None and args.branch != None and args.account != None and args.password != None:
        print(args)
        generatedFileName = "BuildScripts\\generated_app_build_1796720.vdf"
        generate_steam_script("BuildScripts\\app_build_1796720.vdf", generatedFileName, args.version, args.no_changes, args.branch)
        fullPathFileName = os.getcwd() + "\\" + generatedFileName
        print(fullPathFileName)
        subprocess.call([args.steamcmd, "+login", args.account, args.password, "+run_app_build", fullPathFileName, "+quit"])
    else:
        print("Error: Usage is upload_IA_to_steam.py --version XXX --branch YYYY ---no_changes Z --account AAA --password BBBB\nWhere XXX is the version (e.g. 1.0.0.1)\nYYY is the name of the upload branch on steam\nZ is optional - if you miss this value, then the script uploads, for upload or not\nAAA is the steam account to be used\nand BBB is the password for that account")
