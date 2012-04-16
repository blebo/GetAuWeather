# GetAuWeather 1.0
# Copyright (c) 2006, 2007, Luke Maurits <luke@maurits.id.au>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# * The name of Luke Maurits may not be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from urllib import urlopen

def getauweather(weatherurl="http://www.bom.gov.au/cgi-bin/wrap_fwo.pl?IDY03021.txt"):

	# We'll store the weather data in this dictionary

	output={}

	# Grab the weather and split it into lines

	datafile=urlopen(weatherurl)
	lines=datafile.readlines()

	# "lines" contains the lines of a HTML document.
	# The actual weather data is contained within <pre> tags.
	# Let's get rid of everything but the data.

	start=lines.index("""<pre style="font: Courier;">\n""")
	end=lines.index("""</pre>\n""")
	data=lines[start+1:end]

	# Now we have just the data.
	# First things first - have the BoM changed their data format?

	for line in data:
		if "Format last changed" in line:
			if "Format last changed: 15 Jul 1999" not in line:
				raise Exception("Data format has changed!")

	# If the data format is still good, let's parse data

	for line in data:

		# Some lines are just decoration, etc.  We skip these.
	
		if True in [line.startswith(x) for x in ["+","|","IDY"]]:
			pass
		else:
			stationdict={}
			split=line.split()

			# Store the first few variables in the dictionary

			for variable  in  ["Tx","Tn","Weather","Rain"]:
				stationdict[variable]=split.pop()

			# The next variable in the list is pressure, "Bar".
			# Occasionally, this value has whitespace in it:
			# It can take the form "Q xxx.yy".
			# We then need to join the two elements of "split".

			if "Q" in split:
				pressure=" ".join([split.pop(),split.pop()])
				stationdict["Bar"]=pressure
			else:
				stationdict["Bar"]=split.pop()
			
			# The remaining variables can be read without incident

			for variable  in  ["RH","Temp","Wind","Cld","Vis",
			"Hour","Day","Long","Lat"]:
				stationdict[variable]=split.pop()

			# The remainder of "split" makes up the station name

			stationname=" ".join(split)
			output[stationname]=stationdict

	return output
