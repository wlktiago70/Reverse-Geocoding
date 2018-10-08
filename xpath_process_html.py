import argparse
import requests
from lxml import html
# Setup script arguments
parser = argparse.ArgumentParser()
parser.add_argument('-o','--fout', nargs=1)
parser.add_argument('-l','--limit', nargs=1, default="0")
# Assign values from arguments to variables
fileOut = (parser.parse_args().fout)[0]
limit = int((parser.parse_args().limit)[0])
url = "https://www.tripadvisor.com.br/Search?geo=294280&latitude=&longitude=&searchNearby=&pid=3826&redirect=&startTime=1526738521542&uiOrigin=MASTHEAD&q=hamburgueria+brasil&supportedSearchTypes=find_near_stand_alone_query%2Cname_stop_query&enableNearPage=true&returnTo=https%253A__2F____2F__www__2E__tripadvisor__2E__com__2E__br__2F__Tourism__2D__g294280__2D__Brazil__2D__Vacations__2E__html&searchSessionId=AD300D9F7DB07A7E3C07733D1AFCE5B41526738081614ssid#&ssrc=e&o="
baseXpath = "string((//*[@id=\"search_result\"]//div[@class=\"all-results\"]//div[@class=\"result EATERY\"]//div[@class=\"info poi-info  \"]/div[@class=\""
titlXpath = "string((//*[@id=\"search_result\"]//div[@class=\"all-results\"]//div[@class=\"result EATERY\"]//div[@class=\"info poi-info  \"]/div[@class=\"title\"])["
addrXpath = "string((//*[@id=\"search_result\"]//div[@class=\"all-results\"]//div[@class=\"result EATERY\"]//div[@class=\"info poi-info  \"]/div[@class=\"address\"])["
count = 0
setCount = 0
resultsPerPage = 30

# Starting processing web content
output = open("./"+fileOut+".csv","w")
output.write("sep=,\n\"Establishment\",\"Address\"\n")
while count < limit:
	try:
		index = 1
		count = setCount*resultsPerPage
		print("Opening: "+url+str(count))
		pageContent=requests.get(url+str(count))
		tree = html.fromstring(pageContent.content)
		title = tree.xpath(titlXpath+str(index)+"])")
		address = tree.xpath(addrXpath+str(index)+"])")
		while title!="":
			print("Establishment..: "+title)
			print("Address........: "+address)
			print("WRITING..................................................................................")
			output.write("\""+title+"\",\""+address+"\"\n")
			title = tree.xpath(titlXpath+str(index)+"])")
			address = tree.xpath(addrXpath+str(index)+"])")
			index+=1
		setCount+=1
	except:
		break
output.close()
