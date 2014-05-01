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
from xml.sax.saxutils import escape

##allow imports from evernote
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))+'/evernote/lib')

import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types

from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec


kobo_db_loc = "/Volumes/KOBOeReader/.kobo/KoboReader.sqlite"
evernote_dev_token = "get_your_developer_token_from_evernote"
evernote_notestore = "get_your_evernote_notestore_from_evernote"

def sendtoevernote(row):
	print 'sendrowtoevernote'
	client = EvernoteClient(token=evernote_dev_token)
	userStore = client.get_user_store()
	noteStore = client.get_note_store()
	user = userStore.getUser()

	#user logged in now let's see if the note exists?
	print 'Check if note: '+row[1]+' exists'
	filter = NoteFilter()
	filter.words = "kobosync-link="+row[1]

	spec=NotesMetadataResultSpec(includeTitle=True)

	ourNoteList = noteStore.findNotesMetadata(evernote_dev_token,filter,0,1,spec)			#we only want to return 1
	if len(ourNoteList.notes) > 0:
		print 'note exists'
	else:
		print 'note desn\'t exist create'
		note = Types.Note()
		note.title = row[0]
		note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
		note.content += '<en-note>'
		note.content += '<p><b>TEXT</b></p><p>'+escape(row[2].encode('ascii','ignore'))+'</p>'
		if (row[3] is not None):
			print row[3].encode('ascii','ignore')
			note.content += '<p><b>ANNOTATION</b></p><p>'+escape(row[3].encode('ascii','ignore'))+'</p>'
		note.content += '<p>kobosync-link='+row[1]+'</p>'
		note.content += '</en-note>'
		note = noteStore.createNote(note)
		print 'note created'


def main():
	print 'hello from kobosync - I will be importing bookmarks from '+kobo_db_loc
	print 'I will be using evernote dev token '+evernote_dev_token
	print 'I will be using evernote note store '+evernote_notestore
	print 'I am using the sourceurl: in the filter to match existing records'

	conn = sqlite3.connect(kobo_db_loc)
	c=conn.cursor()
	for row in c.execute("select content.BookTitle,Bookmark.BookmarkID,Bookmark.Text,Bookmark.Annotation from Bookmark join content on content.ContentID = Bookmark.ContentID"):
		sendtoevernote(row)



if __name__ == "__main__":
	main()