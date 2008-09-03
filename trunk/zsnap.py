#!/usr/bin/python
#filename:zsnap.py
#description:another screenshot tools,make screenshot more attractive
#author: hyliker@gmail.com lvscar@gmail.com jessinio@gmail.com
#version 0.01
#usage: python zsnap [options] arguments

#  TO-DO:1. save image in user home dir (eg: ~/zsnap/ )default
#        2. create user configure file (eg: ~/.zsnap)
#        3. provide  multiple  snapshot vision effect

import sys
import os
import errno
import time
import os.path



def scrotScreen():
    """call scrot by shell to snap a screenshot"""
    try:
	os.mkdir("./zsnapFolder")
    except OSError,err:
	if err.errno != errno.EEXIST:
	    raise
    #cmd="""scrot -s '%Y-%m-%d_$wx$h.png' -e 'mv $f ./zsnapFolder/'"""
    zsnapTempImg="zsnap.tmp.png"
    zsnapSaveFoler="./zsnapFolder/"
    zsnapSavePath=zsnapSaveFoler+zsnapTempImg
    cmd="scrot -s "+zsnapSavePath
    screen = os.popen(cmd)
    return zsnapSavePath

def merge_layer(inputFile):
    """merge inputFile with the ScreenFrame Image Given"""
    screenFrame = Image.open('zsnap1280x800.png')    
    screenFrameBackup=screenFrame.copy()
    targetImage=Image.open(inputFile)
    tw,th = targetImage.size
    screenFrameBackupResized=screenFrameBackup.resize((tw,th),Image.ANTIALIAS)
    newScreenFrame=Image.new("RGBA",(tw,th))
    newScreenFrame.paste(targetImage,(0,0))
    newScreenFrame.paste(screenFrameBackupResized,(0,0),screenFrameBackupResized)
    return newScreenFrame

def main():
    print "Notice: beginning snap screenshot,please move your mouse to select a region to be snapped :-)"
    scrotScreenPath = scrotScreen()
    img=merge_layer(scrotScreenPath)
    ISOTIMEFORMAT ='%Y-%m-%d-'
    timeStamp = time.strftime(ISOTIMEFORMAT, time.localtime())+str(int(time.time()))
    savePath="./zsnapFolder/"+timeStamp+".png"
    img.save(savePath)
    print "Wow,great,you snap screenshot is be saved to here"+savePath+"\n Thank you for enjoying this tools,any question will be welcome"
    cmd="eog "+savePath
    os.popen(cmd)

def check_depend_env():
    """
    check zsnap depend environment satisfy
       Now Check:
          PIL
          scrot
    """
    def check_scrot_install():
        OSPATH =  os.environ.get("PATH");
        checkTarget = [x+"/scrot" for x in OSPATH.split(":")]
        scrotInstall = False
        for path in checkTarget:
            if os.path.exists(path):
                scrotInstall = True
        print scrotInstall
        return scrotInstall

    def check_pil_install():
        try:
            import Image
        except ImportError:
            return False
        else:
            return True
    if not check_pil_install():
        print """
you should install pil first
in deb based system try:
$sudo apt-get install python-imaging
"""
        import sys
        sys.exit(2)
    if not check_scrot_install():
        print """
you should install scrot first
in deb based system try:
$sudo apt-get install scrot"""
        import sys
        sys.exit(2)
        
    
if __name__=="__main__":
    check_depend_env()
    import Image
    main()
