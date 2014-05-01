kobosync
========

This syncs kobo e-reader bookmark and annotations to Evernote


Usage
=====

You need a developer token and shard details from Evernote to run this.  

1. Rename the config.dist.py to config.py.  This file stores your configuration settings.
2. Login to your main production evernote account.
3. Jump over to [https://www.evernote.com/api/DeveloperToken.action](https://www.evernote.com/api/DeveloperToken.action) and login.  This will provide you with your developer token and notestore shard information.
4. Update the config.py with these settings.
5. Connect your Kobo by USB
6. Update the config.py with the path to the KoboReader.sqlite file.  On my device this was ```/Volumes/KOBOeReader/.kobo/KoboReader.sqlite```
7. run ```python kobosync.py``` 


Warning
=======

Presently this is just a script that I am using for protoyping a full client app.  So it's console based without a UI at the moment.  That will be coming once I have everything working the way I want it to.

Make sure you check out the issues [https://github.com/purplebeanie/kobosync1/issues](https://github.com/purplebeanie/kobosync1/issues).  Most notably the rate limiting is not yet implemented so if you have large bookmarks / annotations it's not going to transfer all of them presently.


My Dev Environment
==================

I am building and testing this on a Mac using Python 2.7.  The OAuth2 module has been installed using pip and the Evernote SDK is included as a submodule to this project.

I am connecting to a Kobo Glo at last check running 3.2.0 of the Kobo software.