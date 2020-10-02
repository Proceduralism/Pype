import hou
import webbrowser

n = hou.selectedNodes()

items = n[0].type().name().split("::")

if len(items) == 1:
	name = n[0].type().name().split("::")[0]
else:
	name = n[0].type().name().split("::")[1]


#hou.ui.displayMessage(name)

db = {"Globals":"http://www.google.com"
		,"Geomtry":"http://www.google.com"
		,"File":"http://www.google.com"
		}


def load(search_item, db):
	if search_item in db.keys():
		url = db[search_item]
		webbrowser.open(url)
	else:
		hou.ui.displayMessage("No video yet. If you want to add, contact admin")


load(name, db)