# 2023-03-24 - commit-CE-dir-to-P4.py
#
# Program to commit a directory into P4. Optionally features versioning, xcopy and revert.
#
# Written by Yousif Mohamad.

# Import necessary modules
from P4 import P4,P4Exception
import os,shutil,argparse,subprocess

# Create an instance of the P4() class.
p4=P4()
# Method to connect to the P4 server.
p4.connect()

# Perform versioning on source file using the "Major.Minor.Build.P4_Changelist" format.
def versioning(verFile,ogVerStr,rplcVerStr):
    with open(verFile) as srcfile:
        contents=srcfile.read()
    with open(verFile,"r+") as scriptfile:
        contents=contents.replace(ogVerStr,rplcVerStr)
        scriptfile.write(contents)
    return rplcVerStr

def p4Revert(ccDepotPath):
    p4.run("revert",ccDepotPath)

# Perform P4 checkout on a file in the depot.
def ccP4Checkout(ccDepotPath):
    p4.run("edit",ccDepotPath)
    return

# Function to build a solution file.
def msbuild(msbuildPath,msbuildConfig,slnPath):
    command = [msbuildPath,msbuildConfig,slnPath]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(stdout.decode('utf-8'))
    print(stderr.decode('utf-8'))
    return

# Copy all the files from one directory to another.
def xcopy(srcDir,destDir):
    files=os.listdir(srcDir)
    try:
        for file in files:
            srcFile=os.path.join(srcDir,file)
            destFile=os.path.join(destDir,file)
            shutil.copy2(srcFile,destFile)
        print("All files copied successfully\n")
    except shutil.Error as e:
        print("Error copying directory: {}".format(e))
    except OSError as e:
        print("Error accessing directory: {}".format(e))
    return

def ceP4Checkout(ceDepotPath):
    file_list = p4.run("files", ceDepotPath)
    for file in file_list:
        p4.run("edit", file["depotFile"])

# Check in the directory into P4.
def p4CheckIn(destDir):
    for root, dirs, files in os.walk(destDir):
        for file in files:
            filePath=os.path.join(root,file)
            try:
                with open(filePath,"rb") as f:
                    p4.run_add("-t","binary",filePath)
                    p4.run_submit("-d","Initial import of files")
            except P4Exception as e:
                print(e)

def main():
    # Argument Parser
    parser=argparse.ArgumentParser(description="Program that commits a directory to P4.\nOptionally provides versioning, xcopy and reverting.")
    parser.add_argument("--p4Port",type=str,metavar="",help="P4 server to connect to.")
    parser.add_argument("--p4Client",type=str,metavar="",help="Client workspace to connect to.")
    parser.add_argument("--p4User",type=str,metavar="",help="Password to connect to destination P4 server.")
    parser.add_argument("--p4Password",type=str,metavar="",help="Username to connect to destination P4 server.")
    parser.add_argument("--srcDir",default=None,type=str,metavar="",help="Source directory to copy contents to destination directory.")
    parser.add_argument("--destDir",default=None,type=str,metavar="",help="Destination directory to overwrite contents from source directory.")
    parser.add_argument("--verFile",default=None,type=str,metavar="",help="Absolute path of file to perform versioning.")
    parser.add_argument("--ogVerStr",default=None,type=str,metavar="",help="Version string to be replaced.")
    parser.add_argument("--rplcVerStr",default=None,type=str,metavar="",help="Version string to overwrite original string.")
    parser.add_argument("--ccDepotPath",type=str,metavar="",help="P4 depot location for CardCreator.cs")
    parser.add_argument("--ceDepotPath",type=str,metavar="",help="P4 depot location for Current Executables directory.")
    parser.add_argument("--msbuildPath",type=str,metavar="",help="Absolute path to msbuild.exe.")
    parser.add_argument("--msbuildConfig",type=str,metavar="",help="Configuration to build .sln file.")
    parser.add_argument("--slnPath",type=str,metavar="",help="Absolute path to .sln file.")
    args=parser.parse_args()

    # Test to determine P4 can be logged into.
    p4=P4()
    try:
        p4.port=args.p4Port
        p4.client=args.p4Client
        p4.user=args.p4User
        p4.password=args.p4Password
        p4.connect()
        p4.run_login()
    except P4Exception:
        for e in p4.errors:
            print(e)
        exit(1)

    # main()
    ccP4Checkout(args.ccDepotPath)
    versioning(args.verFile,args.ogVerStr,args.rplcVerStr)
    msbuild(args.msbuildPath,args.msbuildConfig,args.slnPath)
    ceP4Checkout(args.ceDepotPath)
    xcopy(args.srcDir,args.destDir)
    p4Revert(args.ccDepotPath)
    p4CheckIn(args.destDir)

    # Method to disconnect from the P4 server.
    p4.disconnect()
    exit(0)

if __name__ == "__main__":
    main()