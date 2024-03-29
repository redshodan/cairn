#!/usr/bin/python
# -* coding: utf-8 -*-
#
# Urwid graphics widgets
#    Copyright (C) 2004-2006  Ian Ward
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Urwid web site: http://excess.org/urwid/

from __future__ import nested_scopes

from util import *
from canvas import *
from widget import *

try: True # old python?
except: False, True = 0, 1


class LineBox(WidgetWrap):
	def __init__(self, w):
		"""Draw a line around w."""
		
		tlcorner=None; tline=None; lline=None
		trcorner=None; blcorner=None; rline=None
		bline=None; brcorner=None
		
		def use_attr( a, t ):
			if a is not None:
				t = urwid.AttrWrap(t, a)
			return t
			
		tline = use_attr( tline, Divider(u"─"))
		bline = use_attr( bline, Divider(u"─"))
		lline = use_attr( rline, SolidFill(u"│"))
		rline = use_attr( rline, SolidFill(u"│"))
		tlcorner = use_attr( tlcorner, Text(u"┌"))
		trcorner = use_attr( trcorner, Text(u"┐"))
		blcorner = use_attr( blcorner, Text(u"└"))
		brcorner = use_attr( brcorner, Text(u"┘"))
		top = Columns([ ('fixed', 1, tlcorner),
			tline, ('fixed', 1, trcorner) ])
		middle = Columns( [('fixed', 1, lline),
			w, ('fixed', 1, rline)], box_columns = [0,2],
			focus_column = 1)
		bottom = Columns([ ('fixed', 1, blcorner),
			bline, ('fixed', 1, brcorner) ])
		pile = Pile([('flow',top),middle,('flow',bottom)],
			focus_item = 1)
		WidgetWrap.__init__(self, pile)


class BarGraphError(Exception):
	pass

class BarGraph(BoxWidget):
	eighths = u" ▁▂▃▄▅▆▇"
	hlines =  u"_⎺⎻─⎼⎽"
	
	def __init__(self, attlist, hatt=None, satt=None):
		"""
		Create a bar graph with the passed display characteristics.
		see set_segment_attributes for a description of the parameters.
		"""
		
		self.set_segment_attributes( attlist, hatt, satt )
		self.set_data([], 1, None)
		self.set_bar_width(None)
		
	def set_segment_attributes(self, attlist, hatt=None, satt=None ):
		"""
		attlist -- list containing attribute or (attribute, character)
			tuple for background, first segment, and optionally
			following segments. ie. len(attlist) == num segments+1
			character defaults to ' ' if not specified.
		hatt -- list containing attributes for horizontal lines. First 
			lement is for lines on background, second is for lines
		       	on first segment, third is for lines on second segment
			etc..
		satt -- dictionary containing attributes for smoothed 
			transitions of bars in UTF-8 display mode. The values
			are in the form:
				(fg,bg) : attr
			fg and bg are integers where 0 is the graph background,
			1 is the first segment, 2 is the second, ...  
			fg > bg in all values.  attr is an attribute with a 
			foreground corresponding to fg and a background 
			corresponding to bg.
			
		If satt is not None and the bar graph is being displayed in
		a terminal using the UTF-8 encoding then the character cell
		that is shared between the segments specified will be smoothed
		with using the UTF-8 vertical eighth characters.
		
		eg: set_segment_attributes( ['no', ('unsure',"?"), 'yes'] )
		will use the attribute 'no' for the background (the area from
		the top of the graph to the top of the bar), question marks 
		with the attribute 'unsure' will be used for the topmost 
		segment of the bar, and the attribute 'yes' will be used for
		the bottom segment of the bar.
		"""
		self.attr = []
		self.char = []
		if len(attlist) < 2:
			raise BarGraphError, "attlist must include at least background and seg1: %s" % `attlist`
		assert len(attlist) >= 2, 'must at least specify bg and fg!'
		for a in attlist:
			if type(a)!=type(()):
				self.attr.append(a)
				self.char.append(' ')
			else:
				attr, ch = a
				self.attr.append(attr)
				self.char.append(ch)

		self.hatt = []
		if hatt is None:
			hatt = [self.attr[0]]
		elif type(hatt)!=type([]):
			hatt = [hatt]
		self.hatt = hatt
		
		if satt is None:
			satt = {}
		for i in satt.items():
			try:
				(fg,bg), attr = i
			except:
				raise BarGraphError, "satt not in (fg,bg:attr) form: %s"%`i`
			if type(fg) != type(0) or fg >= len(attlist):
				raise BarGraphError, "fg not valid integer: %s"%`fg`
			if type(bg) != type(0) or bg >= len(attlist):
				raise BarGraphError, "bg not valid integer: %s"%`fg`
			if fg<=bg:
				raise BarGraphError, "fg (%s) not > bg (%s)" %(fg,bg)
		self.satt = satt
			
			
		
	
	def set_data(self, bardata, top, hlines=None):
		"""
		Store bar data, bargraph top and horizontal line positions.
		
		bardata -- a list of bar values.
		top -- maximum value for segments within bardata
		hlines -- None or a bar value marking horizontal line positions

		bar values are [ segment1, segment2, ... ] lists where top is 
		the maximal value corresponding to the top of the bar graph and
		segment1, segment2, ... are the values for the top of each 
		segment of this bar.  Simple bar graphs will only have one
		segment in each bar value.

		Eg: if top is 100 and there is a bar value of [ 80, 30 ] then
		the top of this bar will be at 80% of full height of the graph
		and it will have a second segment that starts at 30%.
		"""
		if hlines is not None:
			hlines = hlines[:] # shallow copy
			hlines.sort()
		self.data = bardata, top, hlines
	
	def get_data(self, (maxcol, maxrow)):
		"""
		Return (bardata, top, hlines)
		
		This function is called by render to retrieve the data for
		the graph. It may be overloaded to create a dynamic bar graph.
		
		This implementation will truncate the bardata list returned 
		if not all bars will fit within maxcol.
		"""
		bardata, top, hlines = self.data
		widths = self.calculate_bar_widths((maxcol,maxrow),bardata)
		
		if len(bardata) > len(widths):
			return bardata[:len(widths)], top, hlines

		return bardata, top, hlines
	
	def set_bar_width(self, width):
		"""
		Set a preferred bar width for calculate_bar_widths to use.

		width -- width of bar or None for automatic width adjustment
		"""
		assert width is None or width > 0
		self.bar_width = width
	
	def calculate_bar_widths(self, (maxcol, maxrow), bardata ):
		"""
		Return a list of bar widths, one for each bar in data.
		
		If self.bar_width is None this implementation will stretch 
		the bars across the available space specified by maxcol.
		"""
		
		if self.bar_width is not None:
			return [self.bar_width] * min(
				len(bardata), maxcol/self.bar_width )
		
		if len(bardata) >= maxcol:
			return [1] * maxcol
		
		widths = []
		grow = maxcol
		remain = len(bardata)
		for row in bardata:
			w = int(float(grow) / remain + 0.5)
			widths.append(w)
			grow -= w
			remain -= 1
		return widths
		

	def selectable(self):
		"""
		Return False.
		"""
		return False
	
	def use_smoothed(self):
		return self.satt and get_encoding_mode()=="utf8"
		
	def calculate_display(self, (maxcol, maxrow) ):
		"""
		Calculate display data.
		"""
		bardata, top, hlines = self.get_data( (maxcol, maxrow) )
		widths = self.calculate_bar_widths( (maxcol, maxrow), bardata )

		if self.use_smoothed():
			disp = calculate_bargraph_display(bardata, top, widths,
				maxrow * 8 )
			disp = self.smooth_display( disp )
	
		else:
			disp = calculate_bargraph_display(bardata, top, widths,
				maxrow )

		if hlines:
			disp = self.hlines_display( disp, top, hlines, maxrow )
		
		return disp

	def hlines_display(self, disp, top, hlines, maxrow ):
		"""
		Add hlines to display structure represented as bar_type tuple
		values:
		(bg, 0-5)
		bg is the segment that has the hline on it
		0-5 is the hline graphic to use where 0 is a regular underscore
		and 1-5 are the UTF-8 horizontal scan line characters.
		"""
		if self.use_smoothed():
			shiftr = 0
			r = [	(0.2, 1),
				(0.4, 2),
				(0.6, 3),
				(0.8, 4),
				(1.0, 5),]
		else:
			shiftr = 0.5
			r = [	(1.0, 0), ]

		# reverse the hlines to match screen ordering
		rhl = []
		for h in hlines:
			rh = float(top-h) * maxrow / top - shiftr
			if rh < 0:
				continue
			rhl.append(rh)
	
		# build a list of rows that will have hlines
		hrows = []
		last_i = -1
		for rh in rhl:
			i = int(rh)
			if i == last_i:
				continue
			f = rh-i
			for spl, chnum in r:
				if f < spl:
					hrows.append( (i, chnum) )
					break
			last_i = i

		# fill hlines into disp data
		def fill_row( row, chnum ):
			rout = []
			for bar_type, width in row:
				if (type(bar_type) == type(0) and 
						len(self.hatt) > bar_type ):
					rout.append( ((bar_type, chnum), width))
					continue
				rout.append( (bar_type, width))
			return rout
			
		o = []
		k = 0
		rnum = 0
		for y_count, row in disp:
			if k >= len(hrows):
				o.append( (y_count, row) )
				continue
			end_block = rnum + y_count
			while k < len(hrows) and hrows[k][0] < end_block:
				i, chnum = hrows[k]
				if i-rnum > 0:
					o.append( (i-rnum, row) )
				o.append( (1, fill_row( row, chnum ) ) )
				rnum = i+1
				k += 1
			if rnum < end_block:
				o.append( (end_block-rnum, row) )
				rnum = end_block
		
		#assert 0, o
		return o

		
	def smooth_display(self, disp):
		"""
		smooth (col, row*8) display into (col, row) display using
		UTF vertical eighth characters represented as bar_type
		tuple values:
		( fg, bg, 1-7 )
		where fg is the lower segment, bg is the upper segment and
		1-7 is the vertical eighth character to use.
		"""
		o = []
		r = 0 # row remainder
		def seg_combine( (bt1,w1), (bt2,w2) ):
			if (bt1,w1) == (bt2,w2):
				return (bt1,w1), None, None
			wmin = min(w1,w2)
			l1 = l2 = None
			if w1>w2:
				l1 = (bt1, w1-w2)
			elif w2>w1:
				l2 = (bt2, w2-w1)
			if type(bt1)==type(()):
				return (bt1,wmin), l1, l2
			if not self.satt.has_key( (bt2, bt1) ):
				if r<4:
					return (bt2,wmin), l1, l2
				return (bt1,wmin), l1, l2
			return ((bt2, bt1, 8-r), wmin), l1, l2
					
		def row_combine_last( count, row ):
			o_count, o_row = o[-1]
			row = row[:] # shallow copy, so we don't destroy orig.
			o_row = o_row[:]
			l = []
			while row:
				(bt, w), l1, l2 = seg_combine(
					o_row.pop(0), row.pop(0) )
				if l and l[-1][0] == bt:
					l[-1] = (bt, l[-1][1]+w)
				else:
					l.append((bt, w))
				if l1:
					o_row = [l1]+o_row
				if l2:
					row = [l2]+row
			
			assert not o_row
			o[-1] = ( o_count + count, l )
			
		
		# regroup into actual rows (8 disp rows == 1 actual row)
		for y_count, row in disp:
			if r:
				count = min( 8-r, y_count )
				row_combine_last( count, row )
				y_count -= count
				r += count
				r = r % 8
				if not y_count:
					continue
			assert r == 0
			# copy whole blocks
			if y_count > 7:
				o.append( (y_count/8*8 , row) )
				y_count = y_count %8
				if not y_count:
					continue
			o.append( (y_count, row) )
			r = y_count
		return [(y/8, row) for (y,row) in o]
			
			
	def render(self, (maxcol, maxrow), focus=False):
		"""
		Render BarGraph.
		"""
		disp = self.calculate_display( (maxcol,maxrow) )
		#assert 0, disp
		
		r = []
		for y_count, row in disp:
			l = []
			for bar_type, width in row:
				if type(bar_type) == type(()):
					if len(bar_type) == 3:
						# vertical eighths
						fg,bg,k = bar_type
						a = self.satt[(fg,bg)]
						t = self.eighths[k] * width
					else:
						# horizontal lines
						bg,k = bar_type
						a = self.hatt[bg]
						t = self.hlines[k] * width
				else:
					a = self.attr[bar_type]
					t = self.char[bar_type] * width
				l.append( (a, t) )
			c = Text(l).render( (maxcol,) )
			assert c.rows() == 1, "Invalid characters in BarGraph!"
			r += [c] * y_count
			
		return CanvasCombine(r)



def calculate_bargraph_display( bardata, top, bar_widths, maxrow ):
	"""
	Calculate a rendering of the bar graph described by data, bar_widths
	and height.
	
	bardata -- bar information with same structure as BarGraph.data
	top -- maximal value for bardata segments
	bar_widths -- list of integer column widths for each bar
	maxrow -- rows for display of bargraph
	
	Returns a structure as follows:
	  [ ( y_count, [ ( bar_type, width), ... ] ), ... ]

	The outer tuples represent a set of identical rows. y_count is
	the number of rows in this set, the list contains the data to be
	displayed in the row repeated through the set.

	The inner tuple describes a run of width characters of bar_type.
	bar_type is an integer starting from 0 for the background, 1 for
	the 1st segment, 2 for the 2nd segment etc..

	This function should complete in approximately O(n+m) time, where
	n is the number of bars displayed and m is the number of rows.
	"""

	assert len(bardata) == len(bar_widths)

	maxcol = sum(bar_widths)

	# build intermediate data structure
	bars = len(bardata)
	rows = [None]*maxrow
	def add_segment( seg_num, col, row, width, rows=rows ):
		if rows[row]:
			last_seg, last_col, last_end = rows[row][-1]
			if last_end > col:
				if last_col >= col:
					del rows[row][-1]
				else:
					rows[row][-1] = ( last_seg, 
						last_col, col)
			elif last_seg == seg_num and last_end == col:
				rows[row][-1] = ( last_seg, last_col, 
					last_end+width)
				return
		elif rows[row] is None:
			rows[row] = []
		rows[row].append( (seg_num, col, col+width) )
	
	col = 0
	barnum = 0
	for bar in bardata:
		width = bar_widths[barnum]
		if width < 1:
			continue
		# loop through in reverse order
		tallest = maxrow
		segments = scale_bar_values( bar, top, maxrow )
		for k in range(len(bar)-1,-1,-1): 
			s = segments[k]
			
			if s >= maxrow: 
				continue
			if s < 0:
				s = 0
			if s < tallest:
				# add only properly-overlapped bars
				tallest = s
				add_segment( k+1, col, s, width )
		col += width
		barnum += 1
	
	#print `rows`
	# build rowsets data structure
	rowsets = []
	y_count = 0
	last = [(0,maxcol)]
	
	for r in rows:
		if r is None:
			y_count = y_count + 1
			continue
		if y_count:
			rowsets.append((y_count, last))
			y_count = 0
		
		i = 0 # index into "last"
		la, ln = last[i] # last attribute, last run length
		c = 0 # current column
		o = [] # output list to be added to rowsets
		for seg_num, start, end in r:
			while start > c+ln:
				o.append( (la, ln) )
				i += 1
				c += ln
				la, ln = last[i]
				
			if la == seg_num:
				# same attribute, can combine
				o.append( (la, end-c) )
			else:
				if start-c > 0:
					o.append( (la, start-c) )
				o.append( (seg_num, end-start) )
			
			if end == maxcol:
				i = len(last)
				break
			
			# skip past old segments covered by new one
			while end >= c+ln:
				i += 1
				c += ln
				la, ln = last[i]

			if la != seg_num:
				ln = c+ln-end
				c = end
				continue
			
			# same attribute, can extend
			oa, on = o[-1]
			on += c+ln-end
			o[-1] = oa, on

			i += 1
			c += ln
			if c == maxcol:
				break
			assert i<len(last), `on, maxcol`
			la, ln = last[i]
	
		if i < len(last): 
			o += [(la,ln)]+last[i+1:]	
		last = o
		y_count += 1
	
	if y_count:
		rowsets.append((y_count, last))

	
	return rowsets
			

class GraphVScale(BoxWidget):
	def __init__(self, labels, top):
		"""
		GraphVScale( [(label1 position, label1 markup),...], top )
		label position -- 0 < position < top for the y position
		label markup -- text markup for this label
		top -- top y position

		This widget is a vertical scale for the BarGraph widget that
		can correspond to the BarGraph's horizontal lines
		"""
		self.set_scale( labels, top )
	
	def set_scale(self, labels, top):
		"""
		set_scale( [(label1 position, label1 markup),...], top )
		label position -- 0 < position < top for the y position
		label markup -- text markup for this label
		top -- top y position
		"""
		
		labels = labels[:] # shallow copy
		labels.sort()
		labels.reverse()
		self.pos = []
		self.txt = []
		for y, markup in labels:
			self.pos.append(y)
			self.txt.append( Text(markup) )
		self.top = top
		
	def selectable(self):
		"""
		Return False.
		"""
		return False
	
	def render(self, (maxcol, maxrow), focus=False):
		"""
		Render GraphVScale.
		"""
		pl = scale_bar_values( self.pos, self.top, maxrow )

		r = []
		rows = 0
		blank = Canvas([""])
		for p, t in zip(pl, self.txt):
			p -= 1
			if p >= maxrow: break
			if p < rows: continue
			if p > rows:
				run = p-rows
				r += [blank]*run
				rows += run
			c = t.render((maxcol,))
			rows += c.rows()
			r.append(c)
		if rows < maxrow:
			r += [blank]* (maxrow-rows)
		c = CanvasCombine(r)
		if c.rows()>maxrow:
			c.trim(0,maxrow)
		return c
			
			
	
def scale_bar_values( bar, top, maxrow ):
	"""
	Return a list of bar values aliased to integer values of maxrow.
	"""
	return [maxrow - int(float(v) * maxrow / top + 0.5) for v in bar]


class ProgressBar( FlowWidget ):
	eighths = u" ▏▎▍▌▋▊▉"
	def __init__(self, normal, complete, current=0, done=100, satt=None):
		"""
		normal -- attribute for uncomplete part of progress bar
		complete -- attribute for complete part of progress bar
		current -- current progress
		done -- progress amount at 100%
		satt -- attribute for smoothed part of bar where the foreground
			of satt corresponds to the normal part and the
			background corresponds to the complete part.  If satt
			is None then no smoothing will be done.
		"""
		self.normal = normal
		self.complete = complete
		self.current = current
		self.done = done
		self.satt = satt
	
	def set_completion(self, current ):
		"""
		current -- current progress
		"""
		self.current = current
	
	def rows(self, (maxcol,), focus=False):
		"""
		Return 1.
		"""
		return 1

	def render(self, (maxcol,), focus=False):
		"""
		Render the progress bar.
		"""
		percent = int( self.current*100/self.done )
		if percent < 0: percent = 0
		if percent > 100: percent = 100
			
		txt=Text( str(percent)+" %", 'center', 'clip' )
		c = txt.render((maxcol,))

		cf = float( self.current ) * maxcol / self.done
		ccol = int( cf )
		cs = 0
		if self.satt is not None:
			cs = int((cf - ccol) * 8)
		if ccol < 0 or (ccol == 0 and cs == 0):
			c.attr = [[(self.normal,maxcol)]]
		elif ccol >= maxcol:
			c.attr = [[(self.complete,maxcol)]]
		elif cs and c.text[0][ccol] == " ":
			t = c.text[0]
			cenc = self.eighths[cs].encode("utf-8")
			c.text[0] = t[:ccol]+cenc+t[ccol+1:]
			a = []
			if ccol > 0:
				a.append( (self.complete, ccol) )
			a.append((self.satt,len(cenc)))
			if maxcol-ccol-1 > 0:
				a.append( (self.normal, maxcol-ccol-1) )
			c.attr = [a]
		else:
			c.attr = [[(self.complete,ccol),
				(self.normal,maxcol-ccol)]]
		return c
	
