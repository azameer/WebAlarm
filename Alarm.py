### Use as 'from Alarms import Alarms' ##########
import requests,json
import re
from datetime import datetime
from log import *

class Alarms:
    def RaiseClearAlarm(self,AlarmCode,Severity,AlarmMessage):
        self.AlarmCode = AlarmCode
        self.AlarmSeverity = Severity
        status = commands.getoutput('/bin/sh /DG/activeRelease/Tools/RaiseClearAlarm.sh -A '+str(self.AlarmCode)+' -S '+str(self.AlarmSeverity)+'').split('\n')

        matchObj = re.match( r'.*Alarm\s*post\s*is\s*Success.*', str(status), re.M)
        if matchObj:
            return 0
        else:
            return 1

    def RaiseWebAlarm(self,url,json_payload,headers):
        """
        Json payload format as mentioned in 3rd Party PegAlarm ICD
        {
            "alarmList": [{
            "alarmCode": "21332",
            "alarmSeverity": "1",
            "serviceName": "test",
            "message": "msg"
                        }],
            "pttServerId": "010071"
        }

        headers = {'content-type': 'application/json'}

        Response = {u'message': u'SUCCESS', u'statusCode': u'0000'}
        """
        try:
            session_obj = requests.Session()
            r = session_obj.post(url, data=json.dumps(json_payload), headers=headers)
            json_obj = r.json()
            if json_obj['message'] == 'SUCCESS':
                return 0

        except requests.exceptions.HTTPError:
            return 1
        except requests.exceptions.InvalidURL:
            return 1
        except requests.exceptions.ConnectionError:
            return 1
        except requests.exceptions.Timeout:
            return 1
