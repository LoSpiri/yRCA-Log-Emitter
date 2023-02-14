import subprocess, sys, time, threading, json
from datetime import datetime, timedelta


def ZeroOrNull(num):
    if num and num > 0:
        return False
    else:
        return True

def run_cmd(outputFile):
    cmd = "stern -n {} . > {}"
    if(len(sys.argv) < 2 ):
        cmd = cmd.format("default", outputFile)
    else:
        cmd = cmd.format(sys.argv[1], outputFile)
    subprocess.run(cmd, shell=True)


# Function to generate the logs according to yrca's specific
def produce_yrca_logs(requestJson, responseJson):
    responseCode = requestJson["response_code"]
    requestID = requestJson["x-request-id"]
    requestServiceName = requestJson["pod_name"]
    requestStartTime = requestJson["start_time"]
    responseServiceName = ""
    responseStartTime = 0
    if(responseJson != None):
        responseServiceName = responseJson["pod_name"]
        responseStartTime = responseJson["start_time"]
    else:
        responseServiceName = requestJson["authority"]

    # Single failing to contact
    if(responseJson == None):
        print(requestStartTime + " - " + "INFO" + " - " + requestServiceName + " - " + "Sending request to " + responseServiceName + " (request_id: " + requestID + ")")
        requestDateTime = datetime.strptime(requestStartTime, '%Y-%m-%dT%H:%M:%S.%fZ')
        delta2 = timedelta(milliseconds=requestJson["duration"])
        requestEndTime = datetime.strftime(requestDateTime + delta2,'%Y-%m-%dT%H:%M:%S.%fZ')[:-4] + "Z"
        print(requestEndTime + " - " + "INFO" + " - " + requestServiceName + " - " + "Failing to contact " + requestJson["authority"] + " (request_id: " + requestID + ")")
    # Request / response OK
    elif(responseCode == 200):
        print(requestStartTime + " - " + "INFO" + " - " + requestServiceName + " - " + "Sending request to " + responseServiceName + " (request_id: " + requestID + ")")
        print(responseStartTime + " - " + "INFO" + " - " + responseServiceName + " - " + "Reading request from " + requestServiceName + " (request_id: " + requestID + ")")
        responseDateTime = datetime.strptime(responseStartTime, '%Y-%m-%dT%H:%M:%S.%fZ')
        delta1 = timedelta(milliseconds=responseJson["duration"])
        responseEndTime = datetime.strftime(responseDateTime + delta1,'%Y-%m-%dT%H:%M:%S.%fZ')[:-4] + "Z"
        print(responseEndTime + " - " + "INFO" + " - " + responseServiceName + " - " + "Answering response to " + requestServiceName + " (request_id: " + requestID + ")")
        requestDateTime = datetime.strptime(requestStartTime, '%Y-%m-%dT%H:%M:%S.%fZ')
        delta2 = timedelta(milliseconds=requestJson["duration"])
        requestEndTime = datetime.strftime(requestDateTime + delta2,'%Y-%m-%dT%H:%M:%S.%fZ')[:-4] + "Z"
        print(requestEndTime + " - " + "INFO" + " - " + requestServiceName + " - " + "Received response OK from " + responseServiceName + " (request_id: " + requestID + ")")
    # Request / response internal error
    #### To change with else
    elif(responseCode == 500):
        print(requestStartTime + " - " + "INFO" + " - " + requestServiceName + " - " + "Sending request to " + responseServiceName + " (request_id: " + requestID + ")")
        print(responseStartTime + " - " + "INFO" + " - " + responseServiceName + " - " + "Reading request from " + requestServiceName + " (request_id: " + requestID + ")")
        responseDateTime = datetime.strptime(responseStartTime, '%Y-%m-%dT%H:%M:%S.%fZ')
        delta1 = timedelta(milliseconds=responseJson["duration"])
        responseEndTime = datetime.strftime(responseDateTime + delta1,'%Y-%m-%dT%H:%M:%S.%fZ')[:-4] + "Z"
        print(responseEndTime + " - " + "INFO" + " - " + responseServiceName + " - " + "Answering response to " + requestServiceName + " (request_id: " + requestID + ")")
        requestDateTime = datetime.strptime(requestStartTime, '%Y-%m-%dT%H:%M:%S.%fZ')
        delta2 = timedelta(milliseconds=requestJson["duration"])
        requestEndTime = datetime.strftime(requestDateTime + delta2,'%Y-%m-%dT%H:%M:%S.%fZ')[:-4] + "Z"
        print(requestEndTime + " - " + "INFO" + " - " + requestServiceName + " - " + "Received response ERROR from " + responseServiceName + " (request_id: " + requestID + ")")


# key: request-id /// value: corresponding log
# To add the authority check, this must be rewritten, adding it to the key
ToBeProcessed = {}

# take from args
logFile = "log.log"
t = threading.Thread(target=run_cmd, args=[logFile])
t.start()
time.sleep(4)
with open(logFile,"r") as f:
    while 1:
        where = f.tell()
        string = f.readline()
        if not string:
            time.sleep(1)
            f.seek(where)
        else:
            # Processor
            if string[-2] == "}":
                stack = []
                for i in range(len(string) - 2, -1, -1):
                    if string[i] == "}":
                        stack.append(string[i])
                    elif string[i] == "{":
                        if len(stack) > 1:
                            stack.pop()
                        else:
                            start = i
                            if len(string[start:-2]) >= 20:
                                jsonLog = json.loads(string[start:-1])
                                # Added key pod_name and value name of the pod emitting the log to the json
                                podName = string.split(" ")[0]
                                jsonLog["pod_name"] = podName
                                requestID = jsonLog["x-request-id"]
                                authority = jsonLog["authority"]
                                # Determining if it's a single fail
                                # Add 1 to func check
                                if(jsonLog["response_code"] == 408 or jsonLog["response_code"] == 504 or (jsonLog["response_code"] == 503 and not(ZeroOrNull(jsonLog["duration"])) and ZeroOrNull(jsonLog["request_tx_duration"]) and ZeroOrNull(jsonLog["response_duration"]) and ZeroOrNull(jsonLog["response_tx_duration"]))):
                                    produce_yrca_logs(jsonLog, None)
                                    break
                                added = False
                                for key, value in ToBeProcessed.items():
                                    if(key == (requestID, authority) and value["pod_name"] != podName):
                                        oldJsonLog = ToBeProcessed.pop((key))
                                        timestamp1 = jsonLog["start_time"]
                                        timestamp2 = oldJsonLog["start_time"]
                                        date1 = datetime.strptime(timestamp1, '%Y-%m-%dT%H:%M:%S.%fZ')
                                        date2 = datetime.strptime(timestamp2, '%Y-%m-%dT%H:%M:%S.%fZ')
                                        if(date1 < date2):
                                            produce_yrca_logs(jsonLog, oldJsonLog)
                                        else:
                                            produce_yrca_logs(oldJsonLog, jsonLog)
                                        added = True
                                        break   
                                if(not(added)):
                                    ToBeProcessed[(requestID,authority)] = jsonLog
                            break
