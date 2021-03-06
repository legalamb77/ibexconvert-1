#PLAN: take two input files, and an output name(3 args). The first input is the original experiment file, the second is
#the experiment results.
import sys
import re
import json

originalExperiment=sys.argv[1]
trialDataFile=sys.argv[2]
outputFileName=sys.argv[3]

f=open(originalExperiment)

experimentData=re.split(r"(?:\r\n)|(?:\n)|(?:\r)",f.read())

f.close()

f2=open(trialDataFile)
trialDataList=re.split(r"(?:\r\n)|(?:\n)|(?:\r)",f2.read())

f2.close()
#nonHeadersString=''.join(experimentData[1:len(experimentData)])#old code, possibly useful later
#attempting to grab the trial headers
trialDataHeadersA=[]
pattern=re.compile(r"(?:^#\s*Col\.\s*)(\d?\d?)(?::)(.*)")
for trialHeadA in trialDataList:
    match=pattern.match(trialHeadA)
    if match:
        if ("\t"+match.group(2)) not in trialDataHeadersA and int(match.group(1)) >len(trialDataHeadersA):
            trialDataHeadersA.append("\t"+match.group(2))
        elif int(match.group(1)) < len(trialDataHeadersA) and (match.group(2) not in trialDataHeadersA[int(match.group(1))-1]) and ("\t"+match.group(2)) not in trialDataHeadersA:
            trialDataHeadersA[int(match.group(1))-1]+="/"+match.group(2)

#trialDataHeadersA=re.split(r"(?:^#\s*Col\.\s*\d?\d?:)(.*)",f2.read())
trialString=''.join(trialDataHeadersA)

#get worker ID
workerid='ID not Found'
for workerLines in trialDataList:
    if len(workerLines)>0 and workerLines[0]!="#":
            workerLinesList=workerLines.split(',')
            workerid=workerLinesList[8]
            break
#retrieve headers from original files
headersString=experimentData[0]+trialString+"\tWorker ID Number"

#open output
newoutput=open(outputFileName,'w')
#write headers to newoutput
newoutput.write(headersString+'\n')
#check item number(4th in each row from trial data) with row number of originalExperiment
for trialLine in trialDataList:
    if len(trialLine)>0 and trialLine[0]!="#":
        itemNum=int(trialLine.split(',')[3])-2
        if itemNum and itemNum>0:
            #take row number item num from experimentData
            newoutput.write(experimentData[itemNum]+"\t"+trialLine.replace(",", "\t")+"\t"+workerid+"\n")
newoutput.close()
