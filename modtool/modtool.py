#!/bin/env python3

import wx
import modtoolui
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webbrowser import open as openurl_ext

# Create rendered pages directory if it doesn't exists
if not os.path.exists("./rendered_pages"):
    os.makedirs("./rendered_pages")

domains = open("./found_domains.csv").read().split("\n") # Input csv generated by scraper
rendered_pages = []
ask_domains = [] # Domains to ask
uniq_outfile = open("approved_uniq.csv", "a+")
retro_outfile = open("approved_retro.csv", "a+")
blacklist_outfile = open("blacklist_mod.csv", "a+")
approved_uniq_domains = uniq_outfile.read().split("\n")
approved_retro_domains = retro_outfile.read().split("\n")
blacklisted_domains = blacklist_outfile.read().split("\n")

# Add to ask_domains list if domain wasn't seen by a mod before
for dom in domains:
    if dom not in approved_uniq_domains and dom not in blacklisted_domains and dom not in approved_retro_domains:
        ask_domains.append(dom)

# Create rendered_pages list from files in the rendered_pages directory
for f in os.listdir("./rendered_pages/"): 
    rendered_pages.append(f[:-4])

def render_pages():
    # Setup selenium for screenshotting
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.set_window_size(1000,700)

    # Render every page that hasn't been rendered before
    for domain in domains:
        if domain not in rendered_pages and domain != "":
            try:
                browser.get("https://" + domain)
                browser.save_screenshot('./rendered_pages/'+ domain +'.png')
                print("Rendered: " + domain)
            except: 
                print(f'Render failed for "{domain}"')
                options = Options()
                options.headless = True
                browser = webdriver.Firefox(options=options)
                browser.set_window_size(1000,700)

    browser.close()

render_pages()

# Write domain to approved domains file
def allow_uniq_domain(url):
    uniq_outfile.write(url + "\n")
    print("Approved Unique: " + url)

def allow_retro_domain(url):
    retro_outfile.write(url + "\n")
    print("Approved Retro: " + url)

# Write domain to blacklist domains file
def blacklist_domain(url):
    blacklist_outfile.write(url + "\n")
    print("Blacklisted: " + url)

# A last item in the list to see if it's done
domains.append("INTERRUPT")

# Override UI that has been derived from modtoolui.mainframe
class UiFrame(modtoolui.mainframe): 
    def __init__(self,parent):
        modtoolui.mainframe.__init__(self,parent)
        # Open the first image
        self.entry = domains[0]
        self.site_screenshot.SetBitmap(wx.Bitmap("./rendered_pages/" + self.entry + ".png"))
    
    # Skip to the next image if it's not done, otherwise terminate the app
    def skip_next(self):
        domains.remove(self.entry)
        self.entry = domains[0]
        if self.entry == "INTERRUPT":
            wx.MessageBox("Every domain has been categorized!", "Info", wx.OK | wx.ICON_INFORMATION)
            self.Close()
        else:
            self.site_screenshot.SetBitmap(wx.Bitmap("./rendered_pages/" + self.entry + ".png"))
    
    def allow_site_uniq(self, _):
        allow_uniq_domain(self.entry)
        self.skip_next()

    def allow_site_retro(self, _):
        allow_retro_domain(self.entry)
        self.skip_next()
    
    def remove_site(self, _):
        blacklist_domain(self.entry)
        self.skip_next()
    
    def ext_browser_open(self, _):
        openurl_ext(self.entry)

    # Key handler for keyboard support
    def keyhandler(self, event):
        match event.GetKeyCode():
            case wx.WXK_LEFT:
                self.allow_site_uniq(None)
            case wx.WXK_RIGHT:
                self.allow_site_retro(None)
            case wx.WXK_DOWN:
                self.remove_site(None)
            case wx.WXK_UP:
                self.ext_browser_open(None)
            case _:
                pass


# Start the app
app = wx.App(False)
frame = UiFrame(None) 
frame.Show(True) 
app.MainLoop()