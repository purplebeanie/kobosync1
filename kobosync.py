#!/usr/bin/env python

"""kobosync.py: Script for syncing kobo Bookmarks to Evernote."""

__author__ = "Eric Fernance"
__copyright__ = "Copyright 2014. Eric Fernance"
__credits__ = ["Eric Fernance"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Eric Fernance"
__email__ = "eric@purplebeanie.com"
__status__ = "Development"

import sqlite3
import sys
import os
import config
from xml.sax.saxutils import escape
from time import sleep

##allow imports from evernote
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))+'/evernote/lib')

import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import config

from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
import evernote.edam.error.ttypes as Errors



client = None
noteStore = None
userStore = None
user = None

def connect_to_evernote():
	"""Connects to evernote and sets up the globals"""
	global client
	global noteStore
	global userStore
	global user
	try:
		client = EvernoteClient(token=config.evernote_dev_token,sandbox=False)
		userStore = client.get_user_store()
		noteStore = client.get_note_store()
		user = userStore.getUser()
		print 'Connected to Evernote'
	except Errors.EDAMSystemException, e:
		if e.errorCode == Errors.EDAMErrorCode.RATE_LIMIT_REACHED:
			print "Rate limit reached"
			print "Retry yout request in %d seconds" % e.rateLimitDuration
			sleep(e.rateLimitDuration)


def sendtoevernote(row):
	"""This function is used to send to evernote. It's just a testing implementation
	TODO: It needs to properly handle time outs rather than the ugly method it is using currently"""
	print 'sendrowtoevernote'

	#user logged in now let's see if the note exists?
	print 'Check if note: '+row[1]+' exists'
	filter = NoteFilter()
	filter.words = "kobosync-link="+row[1]

	spec=NotesMetadataResultSpec(includeTitle=True)

	ourNoteList = noteStore.findNotesMetadata(config.evernote_dev_token,filter,0,1,spec)			#we only want to return 1
	if len(ourNoteList.notes) > 0:
		print 'note exists'
	else:
		print 'note desn\'t exist create'
		note = Types.Note()
		note.title = row[0]
		note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
		note.content += '<en-note>'
		if (row[2] is not None):
			note.content += '<p><b>TEXT</b></p><p>'+escape(row[2].encode('ascii','ignore'))+'</p>'
		if (row[3] is not None):
			print row[3].encode('ascii','ignore')
			note.content += '<p><b>ANNOTATION</b></p><p>'+escape(row[3].encode('ascii','ignore'))+'</p>'
		note.content += '<p>kobosync-link='+row[1]+'</p>'
		note.content += '</en-note>'
		try:
			note = noteStore.createNote(note)
		except Errors.EDAMSystemException, e:
			if e.errorCode == Errors.EDAMErrorCode.RATE_LIMIT_REACHED:
				print "Rate limit Reached"
				print "Retry your request in %d seconds" % e.rateLimitDuration
				sleep(e.rateLimitDuration)


def main():
	print 'hello from kobosync - I will be importing bookmarks from '+config.kobo_db_loc
	print 'I will be using evernote dev token '+config.evernote_dev_token
	print 'I will be using evernote note store '+config.evernote_notestore
	print 'I am using the sourceurl: in the filter to match existing records'

	while noteStore == None:
		connect_to_evernote()

	conn = sqlite3.connect(config.kobo_db_loc)
	c=conn.cursor()
	for row in c.execute("select content.BookTitle,Bookmark.BookmarkID,Bookmark.Text,Bookmark.Annotation from Bookmark join content on content.ContentID = Bookmark.ContentID"):
		sendtoevernote(row)



if __name__ == "__main__":
	main()