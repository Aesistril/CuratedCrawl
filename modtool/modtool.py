#!/bin/env python3

# The GPLv3 License (GPLv3)
# 
# Copyright (c) 2023 Yiğit Ayaz 
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from time import sleep
import wx
import modtoolui
import os
from selenium import webdriver
from webbrowser import open as openurl_ext
from configparser import ConfigParser
import mariadb
from threading import Thread
import os

config = ConfigParser()
config.read("../globsettings.cfg")

# Create rendered pages directory if it doesn't exists
if not os.path.exists("./rendered_pages"):
    os.makedirs("./rendered_pages")

rendered_pages = []

try:
    dbconn = mariadb.connect(password=config["MariaDB"]["passwd"], user=config["MariaDB"]["user"], host=config["MariaDB"]["host"], port=int(config["MariaDB"]["port"]), database=config["MariaDB"]["database"])
    dbconn.autocommit = True
except Exception as err:
    print(f"Database connection error:\n\n{err}")
    exit(1)

cursor = dbconn.cursor()

ask_domains = []
cursor.execute('SELECT domain FROM domains WHERE type = "UNMOD"')
unmod_rows = cursor.fetchall()
for row in unmod_rows:
    ask_domains.append(row[0])

print(ask_domains)

# Create rendered_pages list from files in the rendered_pages directory
for f in os.listdir("./rendered_pages/"): 
    rendered_pages.append(f[:-4])

# Spawn childeren and give data mining jobs to the ones who yearn for the mines (HOLY SHIT IS THAT A MOTHERFUCKING ELON MUSK REFERANCE!11?!1??!)(GOT THATCHERED)(BIG CHUNGUS KEANU REEVES WHOLESOME 100)
def render_thread(thread_id):
    # Setup selenium for screenshotting
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    # options.add_argument("--timeout 30000")
    browser = webdriver.Firefox(options=options)
    browser.set_window_size(config['modtool']['render_x'], config['modtool']['render_y'])
    while True:
        sleep(1)
        msg = globals()['rendermsgpipe_'+str(thread_id)]
        if msg == "Terminate":
            browser.quit()
            break
        elif msg == "Idle":
            pass
        elif msg != None:
            domain = msg
            try:
                browser.get("https://" + domain)
                browser.save_screenshot('./rendered_pages/'+ domain +'.png')
                print(f"[Thread-{str(thread_id)}] " + "Rendered: " + domain)
            except: 
                print(f'Render failed for "{domain}"')
                options = webdriver.FirefoxOptions()
                options.add_argument("--headless")
                # options.add_argument("--timeout 30000")
                browser = webdriver.Firefox(options=options)
                browser.set_window_size(config['modtool']['render_x'], config['modtool']['render_y'])
            globals()['rendermsgpipe_'+str(thread_id)] = "Idle"

def stream_thread(msg):
    for id in range(1, int(config['modtool']['threads'])):
        globals()['rendermsgpipe_'+str(id)] = msg

def check_running():
    for id in range(1, int(config['modtool']['threads'])):
        if globals()['rendermsgpipe_'+str(id)] != "Idle":
            return True
    return False

def assign_to_idle(job):
    outer_break = False
    while True:
        for id in range(1, int(config['modtool']['threads'])):
            if globals()['rendermsgpipe_'+str(id)] == "Idle":
                globals()['rendermsgpipe_'+str(id)] = job
                outer_break = True
                break
        if outer_break: break

stream_thread("Idle")

for id in range(1, int(config['modtool']['threads'])):
    globals()[f'renderthread-{str(id)}'] = Thread(target=render_thread, args=(id,))
    globals()[f'renderthread-{str(id)}'].start()

# Render every page that hasn't been rendered before
rendercount = 0 
willrendercount = len([x for x in ask_domains if x not in rendered_pages])
for domain in ask_domains:
    if domain not in rendered_pages and domain != "":
        assign_to_idle(domain)
        rendercount += 1
        print(f"Renderering pages ({str(rendercount)}/{str(willrendercount)})")

while True:
    sleep(1)
    if not check_running():
        stream_thread("Terminate")
        break


def allow_mblog_domain(url):
    cursor.execute('UPDATE domains SET type = "MBLOG" WHERE domain = %s', (url,))
    print("Approved Modern Blog: " + url)

# Write domain to approved domains file
def allow_uniq_domain(url):
    cursor.execute('UPDATE domains SET type = "UNIQ" WHERE domain = %s', (url,))
    print("Approved Unique: " + url)

def allow_retro_domain(url):
    cursor.execute('UPDATE domains SET type = "RETRO" WHERE domain = %s', (url,))
    print("Approved Retro: " + url)

# Write domain to blacklist domains file
def blacklist_domain(url):
    cursor.execute('DELETE FROM domains WHERE domain = %s', (url,))
    cursor.execute('INSERT INTO blacklist (entry, source, type) VALUES (%s, "MODERATOR", "DOMAIN")', (url,))
    print("Blacklisted: " + url)

# Override UI that has been derived from modtoolui.mainframe
class UiFrame(modtoolui.mainframe): 
    def __init__(self,parent):
        modtoolui.mainframe.__init__(self,parent)
        self.domindex = -1
        # Open the first image
        self.skip_next()
    
    # Skip to the next image if it's not done, otherwise terminate the app
    def skip_next(self):
        self.domindex += 1
        if self.domindex == len(ask_domains):
            cursor.close()
            dbconn.close()
            wx.MessageBox("Every domain has been categorized!", "Info", wx.OK | wx.ICON_INFORMATION)
            self.Close()
        else:
            print(f"Asking the moderator ({str(self.domindex)}/{str(len(ask_domains))})")
            self.entry = ask_domains[self.domindex]
            self.site_screenshot.SetBitmap(wx.Bitmap("./rendered_pages/" + self.entry + ".png"))
            self.domain_text.SetLabelText(self.entry)
    
    def allow_site_uniq(self, _):
        allow_uniq_domain(self.entry)
        self.skip_next()

    def allow_site_mblog(self, _):
        allow_mblog_domain(self.entry)
        self.skip_next()

    def allow_site_retro(self, _):
        allow_retro_domain(self.entry)
        self.skip_next()
    
    def remove_site(self, _):
        blacklist_domain(self.entry)
        self.skip_next()
    
    def ext_browser_open(self, _):
        openurl_ext(self.entry)

    # Key handler for keyboard support
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
            case wx.WXK_CONTROL:
                self.allow_site_mblog(None)
            case _:
                pass


# Start the app
app = wx.App(False)
frame = UiFrame(None) 
frame.Show(True) 
app.MainLoop()
