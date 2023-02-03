# Python program to Google Chrome Local State
# and create Gnome desktop entries for user profiles

import os
import json
import flatten_json as fj
import pandas as pd
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GdkPixbuf

# Get user home path
userHome = (os.environ['HOME'])

# Build user's Chrome dir path
chromeDir = (userHome + '/.config/google-chrome')

# Build path of localState
localState = chromeDir + "/Local State"
 
### Check for profile folders in chromeDir

# Declare a bunch of variables we'll need later
# so they are global instead of local inside the loop
dirEnt = []
profileNames = []
ppString = "/Google Profile Picture.png"
user_name = ''
profileName = ''
ppPath = ''
execLine = ''

image=Gtk.Image()

for e in os.listdir(chromeDir):
    dirEnt = os.path.join(chromeDir, e)
    if os.path.isdir(dirEnt):
        # Build user's Chrome Local State file path
        ppPath = dirEnt + ppString
        if os.path.exists(ppPath):
            # if localState exists, add localState path to profilePaths
            profileNames.append(e)


# Open localState for reading
with open(localState) as file:
    data = file.read()

# load json data from localState
js = json.loads(data)

# Build the GUI
listIndex=0


def profileListAction(*args):
    print("Current Profile - ",listIndex)

def hello_button_clicked(self, *args):
    pass

def on_tree_selection_changed(selection):
    model, treeiter = selection.get_selected()
    if treeiter is not None:
        print("You selected", model[treeiter][0])
        
class profileList(Gtk.Window):
    def __init__(self):
        super().__init__(title="Profilium")
        store = self.liststore = Gtk.ListStore(str,str)
        treeview = Gtk.TreeView(store)
        self.set_default_size(200, 200)
        profileCol = Gtk.TreeViewColumn("Chrome Profile")
        profileImage = Gtk.CellRendererPixbuf()
        profileText = Gtk.CellRendererText()
        profileCol.pack_start(profileImage, False)
        profileCol.pack_start(profileText, True)
        profileCol.add_attribute(profileText, "text", 0)
        profileCol.add_attribute(profileImage, "pixbuf", 1)
        
        treeview.append_column(profileCol)    

        listIndex=0
        # for each profile in profilePaths, add to profileDic dictionary

        #headerLabel = Gtk.Label(label=' Click on the button for the Chrome profile you want to manage. ')
        #self.pack_start(headerLabel, True, True, 0)

        for profileName in profileNames:
            listIndex = listIndex + 1

            print("Processing profile " + profileName)
            profileDict = pd.json_normalize(js['profile']['info_cache'][profileName]).to_dict()

            # Get user_name
            user_name = profileDict['user_name'][0]

            # Build chrome profile folder path
            pfPath = chromeDir + '/' + profileName

            # Build profile picture path
            picPath = pfPath + ppString

            # Build wmClass name for desktop entry
            # 1. start with 'chrome'
            wmClassPrefix = 'chrome'
            # 2. remove spaces from profile name
            profileNameString = ''.join(profileName.split())
            # 3, combine into wmClass entry
            wmClass = wmClassPrefix + profileNameString
 
            # Build exec line for desktop entry
            execLine = "Exec='/usr/bin/google-chrome-stable %U --class=" + wmClass + " --user-data-dir='" + pfPath + "'"

            # Build desktop file path for current user
            desktopPath = userHome + "/" + ".local/share/applications/"

            # Add rows in GUI
            profImagePB = GdkPixbuf.Pixbuf
            profImagePB.new_from_file(picPath)
            #profImagePB = profImagePB.scale_simple(40, 40, 2) # 2 := BILINEAR
            #profImage = image.new_from_pixbuf(profImagePB)
            #image = GdkPixbuf.Pixbuf.new_from_file("images/icon.png")
            profileButtonLabel=' '+profileName+" - "+user_name

            ### cell renderer

            self.liststore.append([profImagePB, profileButtonLabel])

            #detailLabel_name = Gtk.Label(label=execLine)
            #self.pack_start(detailLabel_name, True, True, 0)

            
        self.add(treeview)
        select = treeview.get_selection()
        select.connect("changed", on_tree_selection_changed)



win = profileList()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

'''
    # Build the desktop file in for each profile
    with open(desktopPath+wmClass+"-profilium.desktop", "a") as f:
        desktopFile = [
            "Comment=Access the Internet\n",
            execLine+'\n',
            "StartupNotify=true\n",
            "Terminal=false\n",
            "Icon='"+picPath+"'\n",
            "Type=Application",
            "Categories=Network;WebBrowser;\n",
            "MimeType=application/pdf;application/rdf+xml;application/rss+xml;application/xhtml+xml;application/xhtml_xml;application/xml;image/gif;image/jpeg;image/png;image/webp;text/html;text/xml;x-scheme-handler/http;x-scheme-handler/https;\n",
            "Actions=new-window;new-private-window;\n",
            "StartupWMClass="+wmClass+"\n",
            "\n",
            "[Desktop Action new-window]\n",
            "Name=New Window\n",
            execLine+'\n',
            "\n",
            "[Desktop Action new-private-window]\n",
            "Name=New Incognito Window\n",
            "Exec=/usr/bin/google-chrome-stable --incognito\n"
            ]
        f.writelines(desktopFile)
        f.close()
'''