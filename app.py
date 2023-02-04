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

# Build desktop file path for current user
desktopPath = userHome + "/" + ".local/share/applications/"

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

class profileManager(Gtk.Window):
    def __init__(self):
        super().__init__(title="Profilium")
        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.set_homogeneous(False)

        detailBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        detailBox.set_homogeneous(False)
        detailBox.set_margin_top(20)

        profileList = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str, str)

        # for each profile in profilePaths, add to profileDic dictionary

        for profileName in profileNames:
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

            profileButtonLabel=' '+profileName+" - "+user_name

            # Set the icon from the profile image
            icon = GdkPixbuf.Pixbuf.new_from_file_at_size(picPath, 30, 30)

            # Append row to the listStore
            profileList.append([icon, user_name, profileName, profileNameString])
            

        treeview = Gtk.TreeView()
        treeview.set_model(profileList)
    
        vbox.add(treeview)
        vbox.add(detailBox)

        self.add(vbox)

        profilePixbuf = Gtk.CellRendererPixbuf()

        profileImageCol = Gtk.TreeViewColumn("")
        treeview.append_column(profileImageCol)
        profileImageCol.pack_start(profilePixbuf, False)
        profileImageCol.add_attribute(profilePixbuf, "pixbuf", 0)

        accountUserName = Gtk.CellRendererText()

        accountCol = Gtk.TreeViewColumn("Google Account")
        treeview.append_column(accountCol)
        accountCol.pack_start(accountUserName, True)
        accountCol.add_attribute(accountUserName, "text", 1)
        accountCol.set_sort_column_id(1)

        profileDirName = Gtk.CellRendererText()

        profileDirCol = Gtk.TreeViewColumn("Profile")
        treeview.append_column(profileDirCol)
        profileDirCol.pack_start(profileDirName, True)
        profileDirCol.add_attribute(profileDirName, "text", 2)
        profileDirCol.set_sort_column_id(2)

        wmClassText = Gtk.CellRendererText()
        wmClassCol = Gtk.TreeViewColumn("wmClass")
        treeview.append_column(wmClassCol)
        wmClassCol.pack_start(wmClassText, True)
        wmClassCol.add_attribute(wmClassText, "text", 3)

        self.profileDetail = Gtk.Label()
        self.profileDetail.set_text("")
        self.profileDetail.set_halign(Gtk.Align.START)
        detailBox.add(self.profileDetail)        
        treeview_selection = treeview.get_selection()
        treeview_selection.connect('changed', self.on_tree_selection_changed)


    # Callback to handle getting/using list selection
    def on_tree_selection_changed(self, profileSelection):
        model, treeiter = profileSelection.get_selected()
        if treeiter is not None:
            # Read the selected user_name into selUser
            selUser = (model[treeiter][1])

            # Read the user's local application dir into localAppDir
            localAppDir = desktopPath

            selNameString = (model[treeiter][3])
            # Check if the selected profile has a desktop entry
            desktopFile = localAppDir + selNameString + ".desktop"
            if(os.path.exists(desktopFile)):
                dfExists = True
            else:
                dfExists = False

            # Build a multiline label to show all the info
            selString = (
                "Desktop Entry Path:\n" + localAppDir + "\n" + "\n" +
                "Selected Profile:\n" + selUser +" \n" + "\n" +
                "Desktop File:\n" + str(desktopFile) + "\n" + "\n" +
                "File Exists:\n" + str(dfExists) + "\n"
            )

            self.profileDetail.set_text(selString)

    # Build the desktop file in for each profile
    def buildDesktopFile(currentProfile):
        desktopFilePath = profileManager.desktopPath+profileManager.wmClass+"-profilium.desktop"
        with open(desktopFilePath, "a") as f:
            desktopFile = [
            "Comment=Access the Internet\n",
            profileManager.execLine+'\n',
            "StartupNotify=true\n",
            "Terminal=false\n",
            "Icon='"+profileManager.picPath+"'\n",
            "Type=Application",
            "Categories=Network;WebBrowser;\n",
            "MimeType=application/pdf;application/rdf+xml;application/rss+xml;application/xhtml+xml;application/xhtml_xml;application/xml;image/gif;image/jpeg;image/png;image/webp;text/html;text/xml;x-scheme-handler/http;x-scheme-handler/https;\n",
            "Actions=new-window;new-private-window;\n",
            "StartupWMClass="+profileManager.wmClass+"\n",
            "\n",
            "[Desktop Action new-window]\n",
            "Name=New Window\n",
            profileManager.execLine+'\n',
            "\n",
            "[Desktop Action new-private-window]\n",
            "Name=New Incognito Window\n",
            "Exec=/usr/bin/google-chrome-stable --incognito\n"
            ]
        f.writelines(desktopFile)
        f.close()        

window = profileManager()

window.show_all()

Gtk.main()