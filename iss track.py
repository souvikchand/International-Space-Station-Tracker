#iss tracker
import requests
import smtplib
from tkinter import *
from datetime import datetime
from PIL import ImageTk,Image

#constants
My_Lat=0.0      # add your own
My_Long=0.0     # add your own
Null_Lat=495
Null_Long=470
iss_prev=None

#definations
def resize_image(e):
   global image, resized, image2
   # open image to resize it
   image = Image.open("world-map.png")
   # resize the image with width and height of root
   resized = image.resize((e.width, e.height), Image.Resampling.LANCZOS)
   image2 = ImageTk.PhotoImage(resized)
   canvas.create_image(0, 0, image=image2, anchor='nw')

def track_iss():
   global iss_lat, iss_long, iss_prev
   
   canvas.delete(iss_prev)
   response= requests.get(url="http://api.open-notify.org/iss-now.json")
   data= response.json()
   iss_lat= float(data['iss_position']['latitude'])
   iss_long= float(data['iss_position']['longitude'])
   canvas.itemconfig(pos,text=f'{iss_lat}, {iss_long}')
   if iss_lat>0 and iss_long>0:
      n_x= int(470+(iss_long*2.9446))
      n_y= int(495-(iss_lat*5.5))
      
   elif iss_lat>0 and iss_long<0:
      n_x= int(470+(iss_long*2.61))
      n_y= int(495-(iss_lat*5.5))
   elif iss_lat<0 and iss_long<0:
      n_x= int(470+(iss_long*2.61))
      n_y= int(495-(iss_lat*2.77))
   elif iss_lat<0 and iss_long>0:
      n_x= int(470+(iss_long*2.9446))
      n_y= int(495-(iss_lat*2.77))
   
   iss_now=canvas.create_image(n_x,n_y,i=iss_img)
   iss_prev= iss_now
   
   
   print(n_x,n_y)
   
    

def click_img():
    pass
#====================1.get iss position=============


#===============2. locate & track live iss on a map=====================
window = Tk()
window.title("ISS Tracker")
window.config(padx=15,pady=15,bg='black')

canvas= Canvas(window,height=700,width=1000)
map_img= ImageTk.PhotoImage(file='world-map.png')
iss_img= ImageTk.PhotoImage(file="ISS_spacecraft_model 2.png")

pos=canvas.create_text(500,680,text="Lat, Long",fill='white')

canvas.config(bg='black',highlightthickness=0)
canvas.grid(row=0,column=0,columnspan=3)

track=Button(text='Track',bg='blue',fg='white',command= track_iss)
track.grid(row=1,column=0)

click= Button(text="Click",bg='blue',fg='white',command= click_img)
click.grid(row=1,column=2)

#pos= Label(text="Lat, Long",bg='black',fg='white')
#pos.grid(row=1,column=1)

window.bind("<Configure>",resize_image)
window.mainloop()
#================3.know today sunrise &sunset================
parameters={
    'lat':23.250630, 
    'lng':87.060439,
    'formatted':0
}

'''response2=requests.get(url="https://api.sunrise-sunset.org/json",params=parameters)
response2.raise_for_status()
data2=response2.json()
#print(data2['results']['sunrise'])
#print(data2['results']['sunset'])'''

#=============4. if current time is dark and iss is nearest send a mail=======
#time= datetime.now()
#print(time)
print(iss_lat)
print(iss_long)
