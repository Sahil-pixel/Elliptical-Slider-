from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import*
from kivy.graphics import*
from math import  atan,tan,pi
from kivy.uix.gridlayout import*
from  kivy.uix.button import*
from kivy.metrics import dp
from kivy.uix.slider import Slider

class CWidget(Widget):
	def __init__(self,_colour=[0.0,1,0,1],**k):
		super().__init__(**k)
		with self.canvas.before:
			Color(rgba=_colour)
			self._elpse=Ellipse(pos=self.pos,size=self.pos)
	
		self.bind(pos=self.update_rect, size=self.update_rect)
	

	def update_rect(self,instance, value):
		instance._elpse.pos = instance.pos
		instance._elpse.size = instance.size

class CircularSlider(Widget):
	max=NumericProperty(100.0)
	min=NumericProperty(0.0)
	value=NumericProperty(50.0)
	broder_colour=ListProperty([1,1,1,1])
	disk_colour=ListProperty([0,1,0,1])

	def __init__(self,broder=15,**k):
		super().__init__(**k)
		self.broder=dp(broder)
		with self.canvas:
			Color(rgba=self.broder_colour)

			self._c=Ellipse(pos=self.pos,size=self.pos)
			self._c.angle_end=90
			self._c.angle_start=90
		self._cwidget=CWidget(_colour=self.disk_colour,pos=(self.pos[0]+self.broder,self.pos[1]+self.broder),
			size=(self.size[0]-2*self.broder,self.size[1]-2*self.broder))
		self.add_widget(self._cwidget)
		
		self.bind(pos=self._update_rect, size=self._update_rect)
		self.bind(value=self._callback)
	#	self.bind(value=self.callback2)
	#def callback2(self,*l):
		#print(l)

	def _callback(self,ins,value):
		#print(ins,value)
		angle=((360-0)/(self.max-self.min))*(value-self.min)
		print('angle',angle)
		self._c.angle_end=angle+90

	


	def _update_rect(self,instance, value):
		instance._c.pos = instance.pos
		instance._c.size = instance.size
		instance._cwidget.pos=(instance.pos[0]+self.broder,instance.pos[1]+self.broder)
		instance._cwidget.size=(instance.size[0]-2*self.broder,instance.size[1]-2*self.broder)

	def _scale(self,ia,fa,ca):
		self.value=(ca-ia)*((self.max-self.min)/(fa-ia))
		#print('Value=',self.value)

	def on_touch_down(self,touch):
		if self.collide_point(*touch.pos):
			
			touch.grab(self)
			x=touch.pos[0]-self.center[0]
			y=touch.pos[1]-self.center[1]
			self._detect_coordinate(x, y)
	def _detect_coordinate(self,x,y):
		if x >0 and y>0:
			print('++')
			angle=(180/pi)*abs(atan(y/x))
			self._c.angle_end=360-(angle-90)
			self._scale(0, 360, 360-angle)
			print(angle)
		if x<0 and y>0:
			print('-+')
			angle=180-(180/pi)*abs(atan(y/x))
			self._c.angle_end=360-(angle-90)
			print(angle)
			self._scale(0, 360, 360-angle)

		if x>0 and y<0:
			print('+-')
			angle=360-(180/pi)*abs(atan(y/x))
			self._c.angle_end=360-(angle-90)
			print(angle)
			self._scale(0, 360, 360-angle)

		if x<0 and y<0:
			print('--')
			angle=180+(180/pi)*abs(atan(y/x))
			self._c.angle_end=360-(angle-90)
			print(angle)
			self._scale(0, 360, 360-angle)


	def on_touch_move(self, touch):
		if touch.grab_current == self:
			
			x=touch.pos[0]-self.center[0]
			y=touch.pos[1]-self.center[1]
			self._detect_coordinate(x, y)

			#print(x)
			#print(self.center)
			return True








class MyApp(App):
	def build(self):
		self.gid=GridLayout(cols=3)
		self.sdr=Slider(max=100,min=0,value=50)
		self.csldr=CircularSlider(broder=100,disk_colour=[1,1,1,1],broder_colour=[0,0,1,1],max=100,min=0,value=5)
		#self.gid.add_widget(self.sdr)

		#self.gid.add_widget(self.csldr)
		for i in range(0,10):
			self.gid.add_widget(CircularSlider(broder=10,disk_colour=[1,1,1,1],broder_colour=[0,0,1,1],max=100,min=0,value=5))
		#self.sdr.bind(value=self.call)

		return self.gid
	def call(self,ins,value):
		self.csldr.value=value

if __name__=='__main__':
	MyApp().run()

