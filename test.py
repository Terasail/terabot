import pywikibot

lang = "test"
site = pywikibot.Site(lang, "wikipedia")
site.login()
pages = []
categories = ["Candidates for speedy deletion"]#, "Wikipedia files requiring renaming", "Wikipedia files that shadow a file on Wikimedia Commons", "IMDb ID not in Wikidata"
for catName in categories:
	cat = pywikibot.Category(site, catName)
	pages += list(cat.articles())
	print(len(list(cat.articles())), "|", catName)
print("-----")
wikitext = "There are currently no files waiting to be renamed."
if len(pages) > 0:
	wikitext = "There are currently " + str(len(pages)) + " files waiting to be renamed:\n"
	if len(pages) == 1:
		wikitext = wikitext.replace("files", "file")
	for page in pages:
		wikitext += "* [[:" + page.title() + "]]\n"
print(wikitext)