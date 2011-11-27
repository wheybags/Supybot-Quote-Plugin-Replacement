###
# Copyright (c) 2011, lolno
# All rights reserved.
#
#
###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

import supybot.conf as conf
import datetime
import os

class Quote(callbacks.Plugin):
    """This command detailed below is silly and doesn't even work

    Add the help for "@plugin help Quote" here
    This should describe *how* to use this plugin."""
    pass

    def add(self, irc, msg, args, thing):
    	"""[<quote>]
	
	[<quote>] is the quote to be stored.
	Will store the quote to be retrieved with get.
	"""
        if not thing:
		irc.reply("noarg")
	else:
		now = datetime.datetime.now()
		minute = now.minute
		hour = now.hour
		day = now.day
		month = now.month
		year = now.year
		
		if day < 10:
			day = "0%d" % day
		if month < 10:
			month = "0%d" % month
		if minute < 10:
			minute = "0%d" % minute
		if hour < 10:
			hour = "0%d" % hour
		
		toadd = thing + " - Added by %s on %s/%s/%s at %s:%s.\n" % (msg.nick, day, month, year, hour, minute)
		
		filename = conf.supybot.directories.log.dirize(self.name()) + "/%s.txt" % msg.args[0]
		dir = os.path.dirname(filename)
		
		try:
			os.makedirs(dir)
		except OSError:
			pass

		file = open(filename, "a")
		file.write(toadd)
		file.close()
		
		file = open(filename, "r")	
		i = -1
		while True:
			line = file.readline()
			i += 1
			if not line:
				break
		file.close()


		irc.reply("Quote added at index %s." % i)	

	# msg.nick is callers nick
	# msg.args[0] is channel name
	# conf.supybot.directories.log.dirize(self.name()) is logdir/Pluginname with no trailing / 
        # shtuff = wrap(shtuff, [additional('text')])

    add = wrap(add, [additional('text')])

    def get(self, irc, msg, args, index):
    	"""[<index>]
	
	Will return quote stored at index [<index>].
    	"""
    	if not index:
		irc.reply("Usage: get [<index>], will return quote stored at index [<index>].")
	else:
		try:
			intindex = int(index)
		except:
			irc.reply("%s is not a valid index." % index)
			return
		
		if intindex < 1:
			irc.reply("%s is not a valid index." % index)
			return
	

		filename = conf.supybot.directories.log.dirize(self.name()) + "/%s.txt" % msg.args[0]
		
		try:
			file = open(filename, "r")
		except:
			irc.reply("I have no quotes for this channel.")
			return
	
		tosay = ""
			
		for i in range(intindex):
			tosay = file.readline()
			if not tosay:
				irc.reply("I don't have an index that high. The highest index is %d." % i)
				return

		tosay = tosay[0:len(tosay) - 1]
		
		file.close()	
		
		irc.reply(tosay, prefixNick=False)

    get = wrap(get, [additional('text')])	


Class = Quote


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
