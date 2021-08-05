#!/usr/bin/python3.6
import urllib3 
import html
import json
http = urllib3.PoolManager() 
def lambda_handler(event, context): 
#url = "https://outlook.office.com/webhook/a6953594-6e06-4334-925e-467ee7b8c9ec@8535436a-46bb-4cc6-a9c9-9ec392e449ee/IncomingWebhook/1ee5ded02ac94043848b9fcf36955a9c/fdb38b18-4786-4bea-bc7b-93983d7c1df1"    
    cloudWatchAlarms = json.loads(event['Records'][0]['Sns']['Message'])
    alarmName = cloudWatchAlarms['AlarmName']
    alarmName = alarmName.replace("_",("&#95;"))
    alarmSplitReplaceValue = str(alarmName).replace("[","").split("]")
    region = cloudWatchAlarms['Region']
    newStateValue = cloudWatchAlarms['NewStateValue']
    oldStateValue = cloudWatchAlarms['OldStateValue']
    url = cloudWatchAlarms['AlarmDescription']
    url = url.split("[")[-1]
    url = url.replace("]","")
    #print(url)
    msg = {
        "text": 
        '<h1 style="color:black; font-size:15px; font-style:normal; font-weight:bold;">' +   alarmName + '</h1>' + 
        '<br>' +
		'<p><strong>' + 'Service name: ' +  '</strong>' +  alarmSplitReplaceValue[2] + '</p>' +
		'<p><strong>' + 'Metric name: '  +  '</strong>' +  alarmSplitReplaceValue[4].lstrip()+ '</p>' +
		'<p><strong>' + 'Region: ' + '</strong>' + region + '</p>'+
		'<p><strong>'  + 'Alarm State: ' +  '</strong>' + newStateValue + '</p>'
        '<p><strong>' + 'Service Ownership: ' +  '</strong>' +  alarmSplitReplaceValue[0] + '</p>' +
        '<p><strong>' + 'Service level: '  +  '</strong>' +  alarmSplitReplaceValue[1] + '</p>' +
        '<p><strong>' + 'Severity: '     +  '</strong>' +  alarmSplitReplaceValue[3] + '</p>' +
        '<br>'
        '<p style="color:black;">' + 'Please check alert information below:' + '</p>' + 
        '<br>' + '<code>' +  str(cloudWatchAlarms).replace(",",",<br>") + '</code>'
    }
   
    encoded_msg = json.dumps(msg).encode('utf-8')
    resp = http.request('POST',url, body=encoded_msg, headers={'Content-Type': 'application/json', })
    print({
        "message": msg, 
        "status_code": resp.status, 
        "response": resp.data
    })