#!/usr/bin/python
import sys, httplib, urllib2, smtplib, string, datetime, time, config

class ServerPingdown:

    now = datetime.datetime.now()

    def __init__(self):
        self.checkPages()

    def mailPageBuffer(self,message):

        messageBody =  "MIME-Version: 1.0\nContent-type: text/html\n"
        messageBody += "From: " + config.mail['From'] + "\n"
        messageBody += "To: " + ', '.join(config.mail['to']) + "\n"
        messageBody += "Subject: """ + config.mail['subject'] + self.now.strftime("%Y-%m-%d") + "\n"
        messageBody +=  message

        server = smtplib.SMTP(config.mail['host'])
        server.sendmail(config.mail['From'], config.mail['to'], messageBody)
        server.quit()

    def checkPages(self):
        
        for server in config.serverList: 
            startTime = time.time()
            
            try:
                conn = httplib.HTTPConnection(server['base'],server['port'])
                conn.request("HEAD",server['file'])
                res = conn.getresponse()
                
                endTime = time.time()
                
                print "{\"time\":\"" + str(self.now) + "\", \"server\":\"" + server['base'] + "\", \"status\":\"" + str(res.status) + "\", \"responseTime\":\"" + str( endTime - startTime ) + "\"},"
                
                if str(res.status) != "200":
                    self.mailPageBuffer(str(server['base']) + " " + str(res.status) + " ")
            except Exception:
               self.mailPageBuffer(str(server['base']) + "<br />" + str(sys.exc_info()[0]) + "<br />" +  str(sys.exc_info()[1]) + "<br />" + str(sys.exc_info()[2]) )
               pass
