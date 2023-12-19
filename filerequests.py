import pywikibot
import time
import re

site = pywikibot.Site("en", "wikipedia")
site.login()
pages = []
categories = ["Wikipedia files requiring renaming", "Wikipedia files that shadow a file on Wikimedia Commons"]
for catName in categories:
	cat = pywikibot.Category(site, catName)
	pages += list(cat.articles())

editSummary = "Update: "
wikitext = '\n{|class="wikitable" style="width:100%;text-align:center;"\n!File!!Target!!Reason'
if len(pages) == 0:
	editSummary += "No file rename requests"
	wikitext = "There are currently no files waiting to be renamed." + wikitext + "\n|-\n|colspan=3|—"
if len(pages) > 0:
	if len(pages) == 1:
		editSummary += "1 file rename request"
		wikitext = "There is currently 1 file waiting to be renamed:\n" + wikitext
	else:
		editSummary += str(len(pages)) + " file rename request"
		wikitext = "There are currently " + str(len(pages)) + " files waiting to be renamed:\n" + wikitext
	for page in pages:
		wikitext += "\n|-\n|[[:" + page.title() + "]]"
		pageTemplates = page.templatesWithParams()
		search = True
		for template in pageTemplates:
			if (search):
				if template[0].title() == "Template:ShadowsCommons":
					search = False
					wikitext += "||—||[[WP:FNC#9]]: File with the same name on Wikimedia Commons"
				if template[0].title() == "Template:Rename media":
					search = False
					if len(template[1]) > 0:
						wikitext += "||[[:File:" + template[1][0] + "]]"
					else:
						wikitext += "||—"
					if len(template[1]) > 1:
						wikitext += "||" + template[1][1]
					else:
						wikitext += "||—"
wikitext = "{{bots|allow=TeraBot}}\n" + wikitext.replace("File:File:", "File:") + "\n|}"
targetPage = pywikibot.Page(site, "User:TeraBot/FileRequests")
if re.sub("\n<sup>[^<]+</sup>", "", targetPage.text) != wikitext:
	print(time.strftime("%y/%m/%d %X", time.localtime()) + " | " + editSummary)
	targetPage.text = wikitext + "\n<sup>Last updated: " + time.ctime() + " (UTC)</sup>"
	targetPage.save(summary=editSummary, minor=False)