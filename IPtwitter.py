import time
import twitter #python-twitter
import re
import httplib
import sys
import os

#OAuth Credentials
api = twitter.Api("98FCOXIIoHp2IB8aPDSlcg",
"ckTVLL6W5yTBw6LSASCD2HQC3poDOrGcWq7dBliMfIA",
"266344567-tN51PHf94d4NOwlJoLmmX1YUqeV3oMJ0zICFzVzT",
"bZLL747Hcbr2K4T54XCtWOJ3zOgxDK4jZ6Oqw4U8QQ")

if len(sys.argv) != 2:
  print "usage: program <IP Check Frequency in Seconds>"
  sys.exit()

sleepTime = int(sys.argv[1])
if sleepTime < 60:
  sleepTime = 60

lastIP = "0.0.0.0"

while(True):
  try: 
    
    #use dyndns to check external IP
    dynDNS = httplib.HTTPConnection("checkip.dyndns.org")
    dynDNS.request("GET", "/index.html")
    dynRES = dynDNS.getresponse()
    html = dynRES.read()

    IP = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", html)
    currentIP = IP[0]
    #if currentIP == lastIP:
      #print "no change"
    #else:
    if currentIP != lastIP:
      #print "new ip", currentIP
      lastIP = currentIP
      obscured = lastIP.split('.')
      obscured[0] = str(int(obscured[0]) + 1)
      obscured[1] = str(int(obscured[1]) + 2)
      obscured[2] = str(int(obscured[2]) + 3)
      obscured[3] = str(int(obscured[3]) + 4)
      obscured =  '.'.join(obscured)
      #print "twitter", obscured
      tweet = "PID: " + str(os.getpid()) + ". Obscured IP: " + obscured
      api.PostUpdate(tweet)
  
  except Exception as ex:
    print "Error occured: ", ex 
  
  time.sleep(sleepTime)
