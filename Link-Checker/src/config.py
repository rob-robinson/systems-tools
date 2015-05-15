# config items for the linkchecker program
# config items called as config.mail["host"]

mail = dict(
	host = "localhost",
	subject = "Link Check - ",
	to = ["to@theirserver.org"],
	From = "from@ourserver.org"
)

url_info = dict(
	# currently this program only checks a single domain's worth of links...
	baseurl = "www.yourbasedomain.com"
)
