import pygtk
import gtk
import serial
import time
import sys

pygtk.require('2.0')
mode = 0

COLOUR_CHANGER = 0
BREATHE = 1
COLOR_SELECT = 2
#########################################
#
#  This program was written by John Meichle on 2/25/2010
#  as a GTK GUI Front end to an Arduino Sketch that was written
#  to control an RGB LED. This could be a single LED, or a 
#  multiple LED Array. This program interfaces with the Arduino
#  via a serial connection, and uses simple byte commands to 
#  set the color values in the Arduino.
#
#  The Python code is not commented well, as it is old code I had that 
#  uses the UIManager to build the GTK GUI. If anyone has any questions
#  I can provide a commented copy to use. 
#
#  The HSV Loop function is built into the Arduino Sketch, and
#  has a simple serial command called to start the loop. The Sketch
#  activly monitors the serial connection during the loop to check for 
#  new RGB values.
#
#  Serial Command set for the Arduino Sketch:
#
#  (Ascii m)(mode)                  	- Sets the mode value
#  (Ascii r)(Red Value)                 - Sets the Red RGB value
#  (Ascii g)(Green Value)               - Sets the Green RGB value
#  (Ascii b)(Blue Value)                - Sets the Blue RGB value
#  (Ascii d)(ms Delay)                  - Update Delay,defines the update rate of the led color changer loop
#
# 	Modified for use as a PC GUI interface for the Bluetooth Controlled RGB LED Strip By Muralidhar M. Shenoy 
#	Thanks John!
#	http://murlidharshenoy.wordpress.com
#   
#########################################
class ArduinoRGB:
	global ser
	ser = serial.Serial()
	serialPort = "COM47" #secify the comport for used by the bluetooth module on your PC here.
	serialBaud = 9600 #specify the baudrate used by the bluetooth serial Comm. channel
	ui = '''<ui>
	<menubar name="MenuBar">
	<menu action="mnuFile">
		<menuitem action="funConnect"/>
		<menuitem action="funQuit"/>
	</menu>
	</menubar>
	<toolbar name="Toolbar">
	<toolitem action="funConnect"/>
	<toolitem action="funQuit"/>
	</toolbar>
	</ui>'''
	serialConnect = False
	#mode = 0;
		
	def aboutButton(self,widget):
		about = gtk.AboutDialog()
		about.set_name("Bluetooth RGB Controller")
		about.set_version("0.1")
		about.run()
		about.destroy() 
	
	# This is a callback function
	def callback(self,widget,data = None):
		print "%s was toggled %s" % (data,("OFF","ON")[widget.get_active()])
		if data == "Color Changer":
			mode = 0
			self.setSliderZero()
			self.disableSliders();
			self.ser.write('m' + '0')
			# self.serial_write(0,0,0,0,10);
			print 'm0';
		if data == "Breathe":
			mode = 1
			self.setSliderZero()
			self.disableSliders();
			self.ser.write('m' + '1')
			# self.serial_write(1,rval,0,0,10);
			print 'm1';
		if data == "Color Select":
			mode = 2
			self.setSliderZero()
			self.enableSliders();
			self.ser.write('m' + '2')
			# self.serial_write(2,0,0,0,10);
			print 'm2';
		# print " mode ", '0'
		#print "m" + mode
		
	def __init__(self):

		self.window = gtk.Window()
		self.colorsel = gtk.ColorSelection()
		self.window.connect('destroy', lambda w: gtk.main_quit())
		self.window.set_size_request(400, 300)
		self.window.set_title("Bluetooth RGB Controller")
		icon = self.window.render_icon(gtk.STOCK_CONVERT, gtk.ICON_SIZE_BUTTON)
		self.window.set_icon(icon)
		self.vbox = gtk.VBox()
		self.window.add(self.vbox)
		# self.window.add(self.colorsel)
		self.uimanager = gtk.UIManager()
		accelgroup = self.uimanager.get_accel_group()
		self.window.add_accel_group(accelgroup)


		genericactions = gtk.ActionGroup('GenericActions')
		self.genericactions = genericactions
		self.uimanager.insert_action_group(genericactions, 0)
		
		serialactions = gtk.ActionGroup('SerialActions')
		self.serialactions = serialactions
		serialactions.add_actions([
								('mnuHelp', None, '_Help'),                             
								# ('funAbout', gtk.STOCK_ABOUT, '_About', None, 'About', self.aboutButton),
								('funQuit', gtk.STOCK_QUIT, '_Quit', None, 'Quit the Program', self.quit),
								('mnuFile', None, '_File'),
								('funConnect', gtk.STOCK_REFRESH, 'Serial _Connect', None, 'Serial Connect', self.setup_serial)
								])
		self.uimanager.insert_action_group(serialactions, 0)
		
		
		
		self.uimanager.add_ui_from_string(self.ui)
		self.menubar = self.uimanager.get_widget('/MenuBar')
		self.vbox.pack_start(self.menubar, False)
		self.toolbar = self.uimanager.get_widget('/Toolbar')
		self.vbox.pack_start(self.toolbar, False)

		self.content = gtk.VBox()

		headerVbox = gtk.VBox(True,0)
		headerLabel1 = gtk.Label("Select RGB Color")
		headerVbox.pack_start(headerLabel1)
		mainHbox = gtk.HBox(True, 0)	
		
		loopVbox = gtk.VBox(True, 0)
		fadeLabel = gtk.Label("Fade Delay (variable on arduino (ms): ")  
		self.fadeScale = gtk.HScale()
		self.fadeScale.set_name("fade")
		self.fadeScale.set_range(5, 60)
		self.fadeScale.set_digits(0)
		self.fadeScale.set_size_request(160, 35)
		self.fadeScale.set_value(35)
		
		loopVbox = gtk.VBox(False, 0)
		
		# the radio buttons
		global button																														
		button = gtk.RadioButton(None,"Color Changer")
		button.connect("toggled",self.callback,"Color Changer")
		loopVbox.pack_start(button, gtk.TRUE,gtk.TRUE, 10)																
		button.show()
		
		global button1
		button1 = gtk.RadioButton(button,"Breathe")															
		button1.connect("toggled",self.callback,"Breathe")
		loopVbox.pack_start(button1, gtk.TRUE,gtk.TRUE, 10)																							
		button1.show()
		
		global button2
		button2 = gtk.RadioButton(button,"Color Select");
		button2.set_active(False)	
		button2.connect("toggled",self.callback,"Color Select")
		loopVbox.pack_start(button2, gtk.TRUE,gtk.TRUE, 10)
		button2.show()

		rHbox = gtk.HBox(True,0)
		rLabel = gtk.Label("Red: ")
		rHbox.pack_start(rLabel, expand=False, fill=False)   
			
		self.rScale = gtk.HScale()
		self.rScale.set_name("red")
		self.rScale.set_range(0, 255)
		self.rScale.set_increments(1, 10)
		self.rScale.set_digits(0)
		self.rScale.set_size_request(160, 35)
		self.rScale.connect("value-changed", self.slider_changed)
		rHbox.pack_end(self.rScale)
		
		gHbox = gtk.HBox(True,0)
		gLabel = gtk.Label("Green: ")
		gHbox.pack_start(gLabel, expand=False, fill=False)   
		
		self.gScale = gtk.HScale()
		self.gScale.set_name("green")
		self.gScale.set_range(0, 255)
		self.gScale.set_increments(1, 10)
		self.gScale.set_digits(0)
		self.gScale.set_size_request(160, 35)
		self.gScale.connect("value-changed", self.slider_changed)
		gHbox.pack_end(self.gScale)
		
		bHbox = gtk.HBox(True,0)       
		bLabel = gtk.Label("Blue: ")
		bHbox.pack_start(bLabel, expand=False, fill=False)   
		
		self.bScale = gtk.HScale()
		self.bScale.set_name("blue")
		self.bScale.set_range(0, 255)
		self.bScale.set_increments(1, 10)
		self.bScale.set_digits(0)
		self.bScale.set_size_request(160, 35)
		self.bScale.connect("value-changed", self.slider_changed)
		bHbox.pack_end(self.bScale)
		
		#make a new hbox
		delayHbox = gtk.HBox(True,0)
		delayLabel = gtk.Label("Delay :")

		#pack the delay slider into the hbox
		delayHbox.pack_start(delayLabel, expand=True, fill=False)
		
		#define the various stuff for the slider itself
		self.delayScale = gtk.HScale()		
		self.delayScale.set_name("delay")
		self.delayScale.set_range(0, 100)
		self.delayScale.set_increments(1, 10)
		self.delayScale.set_digits(0)
		# self.delayScale.set_size_request(160, 35)
		self.delayScale.connect("value-changed", self.slider_changed)
		delayHbox.pack_end(self.delayScale)
		
		
		cHbox = gtk.HBox(True,0)
		cLabel = gtk.Label("RGB")
		cHbox.pack_start(cLabel, expand=False, fill=False)
		cHbox.pack_end(self.colorsel)
		
		rgbVbox = gtk.VBox(True,0)

		rgbVbox.pack_start(headerVbox)
		rgbVbox.pack_start(rHbox)
		rgbVbox.pack_start(gHbox)
		rgbVbox.pack_end(bHbox)
		# rgbVbox.pack_end(dHbox)
		
		
		self.colorsel.connect('color-changed', self.color_picker_callback)
		self.window.connect('destroy', sys.exit)
		
		# mainHbox.pack_start(radio_vbox)
		mainHbox.pack_start(loopVbox)
		mainHbox.pack_end(rgbVbox)
		# mainHbox.pack_end(delayHbox)
		
		self.content.pack_start(mainHbox)
		self.content.pack_end(delayHbox)
		if(mode == 2):
			self.enableAll()	
		else:
			self.disableAll()
			# button.set_sensitive(False);
			# button1.set_sensitive(False);
			# button2.set_sensitive(False);
		self.vbox.pack_start(self.content)
		self.window.show_all()
		return
			
	def disableSliders(self):
		self.rScale.set_sensitive(False)
		self.gScale.set_sensitive(False)
		self.bScale.set_sensitive(False)
		self.genericactions.set_sensitive(False)
		
	def enableSliders(self):
		self.rScale.set_sensitive(True)
		self.gScale.set_sensitive(True)
		self.bScale.set_sensitive(True)
		self.genericactions.set_sensitive(True)
	
	def enableDelaySlider(self):
		self.delayScale.set_sensitive(True)
		
	def disableDelaySlider(self):
		self.delayScale.set_sensitive(False)
	
	def disableAll(self):
		self.disableSliders()
		self.disableDelaySlider()
		self.disbale_radio_buttons()
	
	def enableAll(self):
		self.disableSliders()
		self.enableDelaySlider()
		self.disbale_radio_buttons()
	
	def disbale_radio_buttons(self):
		button.set_sensitive(False);
		button1.set_sensitive(False);
		button2.set_sensitive(False);
	
	def enable_radio_buttons(self):
		button.set_sensitive(True);
		button1.set_sensitive(True);
		button2.set_sensitive(True);
	
	def setSliderZero(self):
		self.rScale.set_value(0)
		self.gScale.set_value(0)
		self.bScale.set_value(0)
		self.delayScale.set_value(5)
		
	def slider_changed(self, widget):
		val = widget.get_value()
		name = widget.get_name()
		if name == "red":
			self.ser.write("r" + chr(int(val)))
		elif name == "green":
			self.ser.write("g" + chr(int(val)))
		elif name == "blue":
			self.ser.write("b" + chr(int(val)))
		elif name == "delay":
			self.ser.write("d" + chr(int(val)))	
		else: 
			print "ERROR: Invalid widget name, in on_changed function"
	
	def serial_write(self, m , rval, gval, bval,dval):
		self.ser.write("m" + chr(m))
		self.ser.write("r" + chr(int(rval)))
		self.ser.write("g" + chr(int(gval)))
		self.ser.write("b" + chr(int(bval)))
		self.ser.write("d" + chr(int(dval)))
	
	# def hsvLoop(self, b): 
		# delay = self.fadeScale.get_value()
		# self.ser.write("d" + chr(int(delay)))
		# time.sleep(.015)
		# self.ser.write("d" + chr(int(delay)))
	
	def setup_serial(self, widget):
		if (self.serialConnect == False):
			self.ser = serial.Serial()
			self.ser.setPort(self.serialPort)
			self.ser.baudrate = self.serialBaud
			self.ser.open()
			if (self.ser.isOpen()):
				self.serialConnect = True
				button.set_sensitive(True);
				button1.set_sensitive(True);
				button2.set_sensitive(True);
				self.enableDelaySlider();
				if(mode == 2 ):	
					self.enableSliders()
			else:
				self.disableSliders()
				self.disableDelaySlider();
				# button.set_sensitive(False);
				# button1.set_sensitive(False);
				# button2.set_sensitive(False);
				# self.disableAll()
				self.serialConnect = False
			#print "ERROR: Serial Unable to connect on " + ser.portstr
	
	def color_picker_callback(*args):
		color=c.get_current_color()
		ser.write("r" + chr(int(color.red/257)))
		ser.write("g" + chr(int(color.green/257)))
		ser.write("b" + chr(int(color.blue/257)))
	
	def quit(self, b):
		print 'Closing Serial Connection...'
		ser.close()
		print 'Quitting program'
		gtk.main_quit()

if __name__ == '__main__':
	main = ArduinoRGB()
	gtk.main()