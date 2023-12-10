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
if len(pages) == 1:
	wikitext = "There is currently 1 file waiting to be renamed:\n"
	wikitext += "* [[:" + pages[0].title() + "]]\n"
if len(pages) > 1:
	wikitext = "There are currently " + str(len(pages)) + " files waiting to be renamed:\n"
	for page in pages:
		wikitext += "* [[:" + page.title() + "]]\n"

wikitext = "{{Bots|deny=luckyrename}}\n" + wikitext.strip()
targetPage = pywikibot.Page(site, "User:TeraBot/FileRequests")
if targetPage.text != wikitext:
	print(time.strftime("%y/%m/%d %X", time.localtime()) + " | " + "Change")
	targetPage.text = wikitext
	targetPage.save(summary="Update: " + str(len(pages)) + " file rename requests", minor=False)
