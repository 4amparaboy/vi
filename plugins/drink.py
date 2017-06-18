#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    iSida bot VI plugin                                                      #
#    Copyright (C) diSabler <dsy@dsy.name>                                    #
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                             #
# --------------------------------------------------------------------------- #

def cmd_to_drink(raw_in, text):
	drink_dmas = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh',
		'eighth', 'nineth', 'tenth', 'eleventh', 'twelveth', 'thirteenth',
		'fourteenth', 'fivteenth', 'sixteenth', 'seventeenth', 'eighteenth',
		'nineteenth', 'twentieth', 'twenty-first', 'twenty-second', 'twenty-third',
		'twenty-fourth', 'twenty-fifth', 'twenty-sixth', 'twenty-seventh',
		'twenty-eighth', 'twenty-nineth', 'thirtieth', 'thirty-first']
	drink_mmas1 = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
		'august', 'september', 'october', 'november', 'december']
	drink_mmas2 = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
		'August', 'September', 'October', 'November', 'December']
	drink_wday = ['monday', 'tuesday', 'wendesday', 'thirsday', 'friday',
		'saturday', 'sunday']
	drink_lday = ['last', 'last', 'Last', 'last', 'Last', 'Last', 'lAst']
	date_file = DATA_FOLDER % 'date.txt'
	if os.path.isfile(date_file):
		ddate = readfile(date_file).decode('UTF')
		week1 = ''
		week2 = ''
		if not ddate:
			msg = 'Read file error.'
		else:
			if len(text) <= 2:
				ltim = tuple(time.localtime())
				text = '%s %s' % (ltim[2], drink_mmas2[ltim[1]-1])
				week1 = '%s %s %s' % (ltim[2]/7+(ltim[2]%7 > 0), drink_wday[ltim[6]], drink_mmas2[ltim[1]-1])
				if ltim[2]+7 > calendar.monthrange(ltim[0], ltim[1])[1]:
					week2 = '%s %s %s' % (drink_lday[ltim[6]].lower(), drink_wday[ltim[6]], drink_mmas2[ltim[1]-1])
			or_text = text
			if text.count('.') == 1:
				text = text.split('.')
			elif text.count(' ') == 1:
				text = text.split(' ')
			else:
				text = [text]
			msg = ''
			ddate = ddate.split('\n')
			for tmp in ddate:
				if or_text.lower() in tmp.lower():
					msg += '\n🔹'+tmp
				elif week1.lower() in tmp.lower() and week1 != '':
					msg += '\n🔹'+tmp
				elif week2.lower() in tmp.lower() and week2 != '':
					msg += '\n🔹'+tmp
				else:
					try:
						ttmp = tmp.split(' ')[0].split('.')
						tday = [ttmp[0]]
						tday.append(drink_dmas[int(ttmp[0])-1])
						tmonth = [ttmp[1]]
						tmonth.append(drink_mmas1[int(ttmp[1])-1])
						tmonth.append(drink_mmas2[int(ttmp[1])-1])
						tmonth.append(str(int(ttmp[1])))
						t = tday.index(text[0])
						t = tmonth.index(text[1])
						msg += '\n🔹'+tmp
					except:
						pass
			if msg == '':
				msg = 'Holiday: %s not found.' % or_text
			else:
				msg = 'I know holidays: %s' % msg
	else:
		msg = 'Database doesn\'t exist.'
	send_msg(raw_in, msg)

def cmd_calend(raw_in, text):
	msg, url, text = '', '', text.strip()
	if not text:
		url = 'http://www.calend.ru/day/%s-%s/' % tuple(time.localtime())[1:3]
	elif re.match('\d+\.\d+$', text):
		url = 'http://www.calend.ru/day/%s-%s/' % tuple(text.split('.')[::-1])
	elif len(text) > 1:
		url = 'http://www.calend.ru/search/?search_str=' + urllib.quote(text.encode('cp1251'))
	if url:
		data = html_encode(load_page(url))
		t = get_tag(data,'title')
		if t == u'Поиск':
			hl = re.findall('<a  href="(/holidays(?:/\d*?)+?)" title=".+?">(.+?)</a>(?:.|\s)+?/>\s+?(\d+ .+?)\s', data)
			if len(hl) == 1:
				d = re.search('class="img_small" /></a></td>\s+?<td>\s+?(.+?\.)\s+?</td>', data, re.S).group(1)
				d = unescape(re.sub('\s+', ' ', d.strip()))
				msg += '📅 <a href="http://www.calend.ru%s">%s</a> (%s) - %s' % (hl[0][0], hl[0][1], hl[0][2], d)
			elif hl:
				d = '<b>%s</b>' % get_tag(data,'h1')
				for a in hl:
					msg = '%s:\n🔹%s' % (d, '\n🔹'.join(map(lambda x: '<a href="http://www.calend.ru%s">%s</a> (%s)' % x, hl)))
		else:
			d = '<b>%s</b>' % get_tag(data,'h1')
			hl = re.findall('<a  href="(/holidays(?:/\d*?)+?)" title=".+?">(.+?)</a>', data)
			if hl:
				print hl[0]   
				msg = '%s:\n🔹%s' % (d, '\n🔹'.join(map(lambda x: '<a href="http://www.calend.ru%s">%s</a>' % x, hl)))
                
	else:
		msg = 'What?'
	if not msg:
		msg = 'Holiday: %s not found.' % text
	send_msg(raw_in, msg, custom={'disable_web_page_preview': 'true'})

commands = [['drink', cmd_to_drink, False, 'all', 'Find holiday [name_holiday/date]'],
			['calend', cmd_calend, False, 'all', 'Find holiday [name_holiday/date]']]

# The end is near!
