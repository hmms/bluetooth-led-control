import appuifw
import btsocket as socket
import e32

class BTReader:
	def connect(self):
		global sock
		arduino_addr='00:19:a4:02:44:2a'   #add your arduino BT adress here
		sock=socket.socket(socket.AF_BT, socket.SOCK_STREAM)
		target=(arduino_addr,1) # serial connection to arduino BT
		sock.connect(target)
		
	def readline(self):
		line=[]
		while 1:
			ch=self.sock.recv(1)
			if(ch=="A"):
				break
			line.append(ch)
		return ''.join(line)
	def writechar(ch):
		# ch="1";
		self.sock.send(ch);
	def close(self):
		self.sock.close();

bt=BTReader()
bt.connect()

mode = appuifw.query(u"MODE","number")
red_val = appuifw.query(u"RED","number")
green_val = appuifw.query(u"GREEN","number")
blue_val = appuifw.query(u"BLUE","number")
delay_val = appuifw.query(u"Delay","number")

m_str = "m" + str(mode)
sock.send(m_str)

r_str = "r" + chr(int(red_val))
sock.send(r_str)

g_str = "g" + chr(int(green_val))
sock.send(g_str)

b_str = "b" + chr(int(blue_val))
sock.send(b_str)

d_str = "d" + chr(int(delay_val))
sock.send(d_str)