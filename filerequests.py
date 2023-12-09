import pywikibot
import time

site = pywikibot.Site("en", "wikipedia")
site.login()
pages = []
categories = ["Wikipedia files requiring renaming", "Wikipedia files that shadow a file on Wikimedia Commons"]
for catName in categories:
	cat = pywikibot.Category(site, catName)
	pages += list(cat.articles())
wikitext = "There are currently no files waiting to be renamed."
if len(pages) > 0:
	wikitext = "There are currently " + str(len(pages)) + " files waiting to be renamed:\n"
	if len(pages) == 1:
		wikitext = wikitext.replace("files", "file")
	for page in pages:
		wikitext += "* [[:" + page.title() + "]]\n"

wikitext = "{{Bots|deny=luckyrename}}\n" + wikitext.strip()
targetPage = pywikibot.Page(site, "User:TeraBot/FileRequests")
outMsg = time.strftime("%y/%m/%d %X", time.localtime()) + " | File requests: "
if targetPage.text != wikitext:
	outMsg += "Change"
	targetPage.text = wikitext
	targetPage.save("Update: " + str(len(pages)) + " file rename requests")
else:
	outMsg += "No change"
print(outMsg)
