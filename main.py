import os
import shutil
import datetime
import filecmp
import subprocess

str_Home = os.getenv("HOME")
str_WorkSpace = os.path.join(str_Home, "workspace")
str_gitFolder = os.path.join(str_Home, "temp")
str_list = []


def safeCopyFiles(src, dest):
    #make dir if they dont exist
    if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))
    #copt files over
    shutil.copy2(src, dest)
    print "backing up:" + dest
    str_list.append(dest)


def updateGit():
    os.chdir(str_gitFolder)
    proc = subprocess.Popen(["git", "status"], env=os.environ, stdout=subprocess.PIPE)
    print 'result: ', proc.communicate()
	__commitGit()
	
def __commitGit():
    os.chdir(str_gitFolder)
    for file in m_AddList:
        proc = subprocess.Popen(["git", "add", file],
                            env=os.environ,
                            stdout=subprocess.PIPE)
        print 'result: ', proc.communicate()
    proc = subprocess.Popen(["git", "commit", "-a", "-m", "daily updates"],
                            env=os.environ,
                            stdout=subprocess.PIPE)
    print 'result: ', proc.communicate()
    #git push http://MyLife:1tsux2bu@gitfarm.appspot.com/git/MyLife.git master
	


for dirname, dirnames, filenames in os.walk(str_WorkSpace):
    for filename in filenames:
        if dirname.find('/.') == -1 and filename[0] != '.':
            #work out file paths
            str_BasePath = dirname[len(str_WorkSpace):]
            file_src = os.path.join(dirname, filename)
            file_dest = str_gitFolder + str_BasePath + '/' + filename
            #print datetime.datetime.today() - datetime.timedelta(days=1)
            if os.path.exists(file_dest):
                #if os.path.getmtime(file_dest) < os.path.getmtime(file_src):
                if not filecmp.cmp(file_src, file_dest):
                    safeCopyFiles(file_src, file_dest)
            else:
                safeCopyFiles(file_src, file_dest)
updateGit()
