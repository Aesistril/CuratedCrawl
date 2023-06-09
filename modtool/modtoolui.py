# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class mainframe
###########################################################################

class mainframe ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"CuratedCrawl Moderator Tools", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.domain_text = wx.StaticText( self, wx.ID_ANY, u"domain", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.domain_text.Wrap( -1 )

		bSizer1.Add( self.domain_text, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.site_screenshot = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.site_screenshot.SetBackgroundColour( wx.Colour( 0, 0, 0 ) )

		bSizer2.Add( self.site_screenshot, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.allow_mblog_button = wx.Button( self, wx.ID_ANY, u"Modern Blog", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.allow_mblog_button, 2, wx.ALL, 5 )

		self.allow_uniq_button = wx.Button( self, wx.ID_ANY, u"Unique", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.allow_uniq_button, 2, wx.ALL|wx.EXPAND, 5 )

		self.blacklist_button = wx.Button( self, wx.ID_ANY, u"Blacklist", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.blacklist_button, 2, wx.ALL|wx.EXPAND, 5 )

		self.allow_retro_button = wx.Button( self, wx.ID_ANY, u"Retro", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.allow_retro_button, 2, wx.ALL, 5 )


		bSizer6.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.ext_browser = wx.Button( self, wx.ID_ANY, u"Open In Browser", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.ext_browser, 2, wx.ALL|wx.EXPAND, 5 )


		bSizer1.Add( bSizer6, 0, wx.EXPAND, 5 )

		self.keybinds = wx.StaticText( self, wx.ID_ANY, u"Up Arrow: Open In browser  Down Arrow: Blacklist  Left Arrow: Unique  Right Arrow: Retro  CTRL: Modern Blog", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.keybinds.Wrap( -1 )

		bSizer1.Add( self.keybinds, 0, wx.ALL, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CHAR_HOOK, self.keyhandler )
		self.allow_mblog_button.Bind( wx.EVT_BUTTON, self.allow_site_mblog )
		self.allow_uniq_button.Bind( wx.EVT_BUTTON, self.allow_site_uniq )
		self.blacklist_button.Bind( wx.EVT_BUTTON, self.remove_site )
		self.allow_retro_button.Bind( wx.EVT_BUTTON, self.allow_site_retro )
		self.ext_browser.Bind( wx.EVT_BUTTON, self.ext_browser_open )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def keyhandler( self, event ):
		event.Skip()

	def allow_site_mblog( self, event ):
		event.Skip()

	def allow_site_uniq( self, event ):
		event.Skip()

	def remove_site( self, event ):
		event.Skip()

	def allow_site_retro( self, event ):
		event.Skip()

	def ext_browser_open( self, event ):
		event.Skip()


###########################################################################
## Class renderloading
###########################################################################

class renderloading ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Web Renderer", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )


		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


