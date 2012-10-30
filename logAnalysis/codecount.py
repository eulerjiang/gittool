# -*- coding: utf-8 -*

#
# Parse git diff output
#
# Require: Python 2.7 or high version, not support Python 2.6
#

import sys
import os
import re
import codecs

enableDebug = False

languageTypeList = ['Java', 'C++', 'Shell', 'Xml', 'Dup', 'Others']

def getFileNameByString(line):
    # Format like:
    #     diff --git a/mpe/mpe-tool-maint/pom.xml b/mpe/mpe-tool-maint/pom.xml

    fileNamePair = line.split()[2:4]
    fileName = fileNamePair[0].replace('a/','')
    
    return  fileName

#===============================================================================
# def checkFileTypeInRepo(fullFilename):
#    tempFile = open(fullFilename)
#    
#    headLine = tempFile.readline()
#    if not headLine:
#        break
#    
#    if headLine.startswith('#!/bin/') or headLine.startswith('#!/usr/'):
#        return "Script"
#    
#    tempFile.close()
#===============================================================================
    

def getFileType(filename):
    fileType = "Others"
    
    if filename.endswith(".java"):
        fileType = "Java"
    elif filename.endswith(".cc") or filename.endswith(".hh"):
        fileType = "C++"
    elif filename.endswith(".sh") or filename.endswith(".tcsh"):
        fileType = "Shell"
    elif filename.endswith(".xml"):
        fileType = "Xml"
    elif filename.endswith(".pc") or filename.endswith(".ipc"):
        fileType = "Dup"    
    if enableDebug:
        print(fileType + " files")
    
    return fileType

def initFileStatusDB():
    codeCountDB = {}
    
    languageList = languageTypeList
    
    for oneLanguage in languageList:
        if enableDebug:
            print(oneLanguage)
        codeCountDB[oneLanguage] = {'Add': 0 , 'Remove' : 0 }
    
    return codeCountDB  

def printFileStatusDB(statusDB):
    print("")
    print("")
    print("Code line change status:")
    
    for oneLang in languageTypeList:
        print(oneLang + " Files: ")
        print("    add line: " + str(statusDB[oneLang]['Add']) )
        print("    remove line: " + str(statusDB[oneLang]['Remove']) )
       
def parseDiffFile(diffLogFile):
    ''' parse the diff.log file: git diff tag1 tag2 > diff.log
    '''
    
    logfile = codecs.open(diffLogFile, 'r', 'iso-8859-1')
    #logfile = open(diffLogFile)
    
    filetype = "NOT_SET"
    filename = "NOT_SET"
    
    fileDiffSection = []
    
    codeCountDB = {}
    
    languageList = languageTypeList
    
    for oneLanguage in languageList:
        #print(oneLanguage)
        codeCountDB[oneLanguage] = {'Add': 0 , 'Remove' : 0 }
    
    #printFileStatusDB(codeCountDB)
    
    while True:
        line = logfile.readline()
        
        if not line:
            break
        
        line = line.rstrip('\n')
        
        if line.startswith("diff --git"):
            if filetype != "NOT_SET":
                result = parseFile(filetype,fileDiffSection)
                if result != None:
                    codeCountDB[filetype]['Add'] += result[0]
                    codeCountDB[filetype]['Remove'] += result[1]
                filetype = "NOT_SET"
                fileDiffSection = []
            
            filename = getFileNameByString(line)
            filetype = getFileType(filename)
        
        if line.startswith("+++") or line.startswith("---"):
            line = ""
        elif line.startswith("+") or line.startswith("-"):
            fileDiffSection.append(line)
            
    logfile.close()

    printFileStatusDB(codeCountDB)

def parseFile(filetype,lines):
    if filetype == "Java":
        return parseJavaFile(filetype, lines)
    elif filetype == "Cxx":
        return parseCxxFile(filetype, lines)
    elif filetype == "Shell":
        return parseShellFile(filetype, lines)
    elif filetype == "Xml":
        return parseXmlFile(filetype, lines)
    elif filetype == "Dup":
        return parseDupFile(filetype, lines)
    else:
        return parseOthersFile(filetype, lines)

def isIgnoreLine(filetype, line):
    javaPatternString = '^[\+\-]$|^[\+\-][\s]*\*.*$|^[\+\-][\s]*\/\*.*$|^[\+\-]\/\/.*$'
    cxxPatternString = '^[\+\-]$'
    ingorePattern = re.compile(javaPatternString + '|' + cxxPatternString )
    result = ingorePattern.match(line)
    if result is None:
        return False
    else:
        return True
    
def parseJavaFile(filetype, lines):
    removeLineNum = 0
    addLineNum = 0
    for line in lines:
        if isIgnoreLine(filetype, line) == True:
            continue
        
        if line.startswith("+"):
            addLineNum += 1
        elif line.startswith("-"):
            removeLineNum += 1
        
        if enableDebug:
            print(line)
    
    if enableDebug:
        print("add line: " + str(addLineNum) + " remove line: " + str(removeLineNum) )
    
    return [addLineNum, removeLineNum]


def parseCxxFile(filetype, lines):
    removeLineNum = 0
    addLineNum = 0
    for line in lines:
        if isIgnoreLine(filetype, line) == True:
            continue
        
        if line.startswith("+"):
            addLineNum += 1
        elif line.startswith("-"):
            removeLineNum += 1
        
        if enableDebug:
            print(line)
    
    if enableDebug:
        print("add line: " + str(addLineNum) + " remove line: " + str(removeLineNum) )
    
    return [addLineNum, removeLineNum]

def parseXmlFile(filetype, lines):
    removeLineNum = 0
    addLineNum = 0
    for line in lines:
        if isIgnoreLine(filetype, line) == True:
            continue
        
        if line.startswith("+"):
            addLineNum += 1
        elif line.startswith("-"):
            removeLineNum += 1
        
        if enableDebug:
            print(line)
    
    if enableDebug:
        print("add line: " + str(addLineNum) + " remove line: " + str(removeLineNum) )
    
    return [addLineNum, removeLineNum]

def parseDupFile(filetype, lines):
    removeLineNum = 0
    addLineNum = 0
    for line in lines:
        if isIgnoreLine(filetype, line) == True:
            continue
        
        if line.startswith("+"):
            addLineNum += 1
        elif line.startswith("-"):
            removeLineNum += 1
        
        if enableDebug:
            print(line)
    
    if enableDebug:
        print("add line: " + str(addLineNum) + " remove line: " + str(removeLineNum) )
    
    return [addLineNum, removeLineNum]

def parseShellFile(filetype, lines):
    removeLineNum = 0
    addLineNum = 0
    for line in lines:
        if isIgnoreLine(filetype, line) == True:
            continue
        
        if line.startswith("+"):
            addLineNum += 1
        elif line.startswith("-"):
            removeLineNum += 1
        
        if enableDebug:
            print(line)
    if enableDebug:
        print("add line: " + str(addLineNum) + " remove line: " + str(removeLineNum) )
    
    return [addLineNum, removeLineNum]

def parseOthersFile(filetype, lines):
    removeLineNum = 0
    addLineNum = 0
    for line in lines:
        if isIgnoreLine(filetype, line) == True:
            continue
        
        if line.startswith("+"):
            addLineNum += 1
        elif line.startswith("-"):
            removeLineNum += 1
        
        if enableDebug:
            print(line)
    
    if enableDebug:
        print("add line: " + str(addLineNum) + " remove line: " + str(removeLineNum) )
    
    return [addLineNum, removeLineNum]

def generateGitDiffLog(repoRoot, sha1, sha2, diffLogFilePath):
    os.system("cd " + repoRoot + "; git diff " + sha1 + " " + sha2 + " > " + diffLogFilePath)
    
    
def usage():
    print '''
Usage: 
    codecount.py --repo <git_repo_root> --version <sha1> <sha2>
    '''

def executeTest():
    logFile='/tmp/gitdiff.log'
    
    generateGitDiffLog('/var/tmp/repo/emacm/ma', 'c5c3bdadfe82e4da2a1d06353e4d276d2b3046a8', 'HEAD', logFile)
    initFileStatusDB()
    parseDiffFile(logFile)    
    
def countLineChange(repoRoot, versionA, versionB):
    logFile='/tmp/gitdiff.log'
    
    generateGitDiffLog(repoRoot, versionA, versionB, logFile)
    
    initFileStatusDB()
    parseDiffFile(logFile)    
         
if __name__ == '__main__':  
    num = 1
    while num < len(sys.argv):
        if sys.argv[num] == '--repo':
            repoRoot = sys.argv[num+1]
            num = num + 1
        elif sys.argv[num] == '--version':
            versionA = sys.argv[num+1]
            versionB = sys.argv[num+2]
            num = num + 2
        elif sys.argv[num] == '--log-file':
            logFile = sys.argv[num+1]
            num = num + 1
        else:
            usage()
            sys.exit(1)
        
        num = num + 1
        
    countLineChange(repoRoot, versionA, versionB)