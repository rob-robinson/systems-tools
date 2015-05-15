#!/usr/bin/python
import httplib
import urllib2
import smtplib
import datetime

import config


class checkLinks:

    # i'd like to refactor this program significantly...
    # I don't want the 

    listOfLinks = []
    pageBuffer = ""
    now = datetime.datetime.now()

    def __init__(self):
        self.listOfLinks = []
        del self.listOfLinks[:]

    def mailPageBuffer(self):

        messageBody =  "MIME-Version: 1.0\nContent-type: text/html\n"
        messageBody += "From: " + config.mail['From'] + "\n"
        messageBody += "To: " + ', '.join(config.mail['to']) + "\n"
        messageBody += "Subject: """ + config.mail['subject'] + self.now.strftime("%Y-%m-%d") + "\n"
        messageBody +=  self.pageBuffer

        server = smtplib.SMTP(config.mail['host'])
        server.sendmail(config.mail['From'], config.mail['to'], messageBody)
        server.quit()

    def checkPage(self, pageurl):

        del self.listOfLinks[:]

        self.pageBuffer +=  "<h2>looking at: " + pageurl + "</h2>"

        page = urllib2.urlopen(pageurl)
        pagedata = page.read()
        page.close()

        self.print_all_links(pagedata)

        self.pageBuffer +=  "<table width=\"90%\" border=\"1\">"
        self.pageBuffer += "<tr><th width=\"45%\" >Link in Page</th><th>Details</th></tr>\n"

        for i in range(len(self.listOfLinks)):
            if self.listOfLinks[i].find("http://" + config.url_info['baseurl']) != -1:
                resp = self.getHead(self.listOfLinks[i][26:])
                if resp.find("200 OK") == -1:
                    self.pageBuffer +=  "<tr><td valign=\"top\">" + self.listOfLinks[i][26:] + "</td><td valign=\"top\">" + resp + "</td></tr>\n"
        self.pageBuffer +=   "</table>\n"

    def getHead(self, inUrl):
        conn = httplib.HTTPConnection(config.url_info['baseurl'])
        conn.request("HEAD",inUrl)
        res = conn.getresponse()
        if res.status == 301:
            fwd = res.getheader('location')
            # at this point in this program, we are only looking for full path url
            if fwd.find("http://" + config.url_info['baseurl']) != -1:
                conn = httplib.HTTPConnection(config.url_info['baseurl'])
                conn.request("HEAD",fwd[26:])
                res = conn.getresponse()
                return "<ul><li>" + str(res.status) + " " + res.reason + "</li><li>301, redirected to " + fwd + "</li></ul>"
        return "<ul><li>" + str(res.status) + " " + res.reason + "</li></ul>"

    def print_all_links(self, page):
        while self.get_next_target(page):
            url, endpos = self.get_next_target(page)
            if url:
                self.listOfLinks.append(url)
                page = page[endpos:]
            else:
                return None

    def get_next_target(self, s):
        start_link = s.find('<a href=')
        if start_link == -1:
            return None,0
        else:
            start_quote = s.find('"',start_link)
            end_quote = s.find('"',start_quote+1)
            url = s[start_quote+1:end_quote]
            return url,end_quote


