#!/usr/bin/python
import urllib2, re, string, time, datetime, config, smtplib
from os.path import basename
from urlparse import urlsplit
from xml.dom.minidom import parseString

class FindLargeImages:
    # save current date for later...
    now = datetime.datetime.now()
    
    # set up buffers for later distribution
    mailMessage = ""
    jsonMessage = "["
    
    def __init__(self):
        # call initializer
        self.init()
        
        # create json file
        self.writeJSONFile(self.jsonMessage)
        # sen
        self.mailPageBuffer(self.mailMessage)

    def init(self):
        pages = self.getListOfPages()
        
        print "getting ready to loop over " + str(len(pages)) + " pages"
        
        for page in pages: 

            try:
                # read page contents
                urlContent = urllib2.urlopen(page).read()
                
                # create list of all image URLs
                imgUrls = re.findall('img .*?src="(.*?)"', urlContent)
                
                # for each image URL:
                for imgUrl in imgUrls:
                    
                    # do come clean up...  
                    imageURL = self.makeImageUrl(imgUrl,page)

                    try:
                        # get image from server
                        f = urllib2.urlopen(imageURL)
                        
                        # if file size is greater than half a meg...
                        if(int(f.headers['Content-Length']) > .5*(1024*1024)):
                            # add to mail buffer
                            self.mailMessage += "Page:" + page + "\r\nImage:" + imageURL + "\r\nSize:" + str(round(float(f.headers['Content-Length']) / (1024*1024),2)) + " MB\r\n\r\n"
                            
                            # add to json buffer
                            self.jsonMessage += "{\"Page\":\"" + page + "\",\"Image\":\"" + imageURL + "\",\"Size\":\"" + str(round(float(f.headers['Content-Length']) / (1024*1024),2)) + " MB\"},"
                    except:
                        pass
                # sleep for a quarter of a second... to be nice...
                time.sleep(.25)
            except:
                pass
            
        # remove trailing , added from previous loop     
        self.jsonMessage = self.jsonMessage[:-1] 
        
        # end json array
        self.jsonMessage += "]"  

    def writeJSONFile(self,message):
        f = open(config.app['jsonFile'],'w')
        f.write(message)
        f.close

    
    def mailPageBuffer(self,message):
        messageBody =  "MIME-Version: 1.0\nContent-type: text/plain\n"
        messageBody += "From: " + config.mail['From'] + "\n"
        messageBody += "To: " + ', '.join(config.mail['to']) + "\n"
        messageBody += "Subject: """ + config.mail['subject'] + self.now.strftime("%Y-%m-%d") + "\n\n"
        messageBody +=  message

        try:
            server = smtplib.SMTP(config.mail['host'])
            server.sendmail(config.mail['From'], config.mail['to'], messageBody)
            server.quit()
        except Exception:
            #print Exception.message
            pass
        
    def makeImageUrl(self,orig_image_url,orig_page_url):
        # set clear base from settings
        realBase = config.app['realBase']
        
        # remove base from image and page...
        orig_image_url = orig_image_url.replace(realBase,'')
        orig_page_url = orig_page_url.replace(realBase,'')
        
        #explode into array based on /
        dirs = string.split(orig_page_url,'/')
        #print dirs
        
        #count number of ../ in orig_image_url
        dds = orig_image_url.count('../')
        
        #build and return url
        if dds > 0:
        
            orig_image_url = orig_image_url.replace('../','')
            
            #back up that many number of tokens
            proper = len(dirs) - (dds+1)
            
            buffer = ""
            for i in range(0, proper):
                buffer += dirs[i] + "/"
        
            return realBase + buffer + orig_image_url
        else:
            return realBase + orig_image_url
        
    def getListOfPages(self):
        cleanListOfUrls = []
        page = urllib2.urlopen(config.app['sitemap'])
        pagedata = page.read()
        page.close()
        
        print "got the xml correctly"
        
        dom = parseString(pagedata)
        
        listOfUrls = dom.getElementsByTagName('url')
        
        for line in listOfUrls:
            # strip xml tags from string
            cleanLine = line.toxml().replace('<url>','').replace('</url>','').replace('<loc>','').replace('</loc>','')
            cleanListOfUrls.append(cleanLine)
        
        return cleanListOfUrls 
