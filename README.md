# Profilium
### *A Chrome/Chromium Profile Shortcut Manager for Linux*

---

This little app was created to fix a problem that a *lot* of people seem to have: Ubuntu does not seem to correctly handle the way that the Google Chrome/Chromium browsers create user profiles. 

For example, perhaps you have one Chrome profile for work and another for home. 
- On Windows, you can simply create each profile in Chrome, go into the profile settings, and click "Create Desktop Shortcut", and then drag that onto your taskbar.
- On Linux, this doesn't work. 
  - There's no option to create the desktop shortcut (a .desktop file) in Chrome on linux, and there isn't an easily discoverable way to do it included in Gnome (the Ubuntu desktop manager).
  - Even if you DO create a generic .desktop file for your chrome profile, it will just open in the same generic Chrome icon, so there is no easy way to tell which browser window is which.
  - There are many forum posts on the web about how to solve this problem manually, but no easily installable app that Just Works<sup>tm</sup>.
  
This is why I created Profilium.

*Note: This app has only been tested in Ubuntu 22.10 with Google Chrome (Stable) 109.0.5414.74 (Official Build). It may work just fine in Chromium and/or other versions of Chrome, but YMMV.*

---

### Installation:
1. Clone the repo

```git clone https://github.com/jwoyak/profilium.git```

2. Install Profilium

```[commands here]```

---

### Usage:

*[syntax here]*

---

### To Do:

- [ ] Add support for setting Chrome App settings
- [ ] Build automated testing (and test for more browsers/platforms)
