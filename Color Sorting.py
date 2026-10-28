#!/usr/bin/env python
# coding: utf-8

# In[17]:


#!/usr/bin/env python
# coding: utf-8
import Arm_Lib
import cv2 as cv
import threading
from time import sleep
import ipywidgets as widgets
from IPython.display import display
from color_sorting import color_sorting
import json
import pickle
from dofbot_config import *


# In[18]:


import Arm_Lib
Arm = Arm_Lib.Arm_Device()
joints_0 = [90, 135, 0, 10, 90, 0]
Arm.Arm_serial_servo_write6_array(joints_0, 1000)


# In[19]:


sorting = color_sorting()
model = 'General'


# In[20]:


HSV_path="HSV_config.txt"

# color_hsv  = {"red"   : ((0, 59, 46), (89, 255, 255)),
#               "green" : ((60, 143, 145), (68, 255, 255)),
#               "blue"  : ((100, 143, 145), (119, 255, 255)),
#               "yellow": ((26, 143, 145), (28, 255, 255))}
# with open('HSV_Config.pkl', 'wb') as f:
#     pickle.dump(color_hsv, f)

with open('HSV_Config.pkl', 'rb') as f:
    color_hsv = pickle.load(f)

try: read_HSV(HSV_path,color_hsv)
except Exception as e: print("Read HSV_config Error!!!", e)


# In[21]:


model = "General"
button_layout = widgets.Layout(width='320px', height='60px', align_self='center')
output = widgets.Output()

exit_button = widgets.Button(description='Exit', button_style='danger', layout=button_layout)
imgbox = widgets.Image(format='jpg', height=480, width=640, layout=widgets.Layout(align_self='center'))
controls_box = widgets.VBox([imgbox, exit_button], layout=widgets.Layout(align_self='center'))


# In[22]:


def exit_button_Callback(value):
    global model
    model = 'Exit'
    with output: print(model)
exit_button.on_click(exit_button_Callback)


# In[23]:


import numpy as np
def change_brightness(img, alpha, beta):
   return cv.addWeighted(img, alpha, np.zeros(img.shape, img.dtype),0, beta)

def camera():
    # Open camera
    capture = cv.VideoCapture(0)
    while capture.isOpened():
        try:
            _, img = capture.read()
            img = cv.resize(img, (640, 480))
            img = cv.flip(img, 1)
            show_img = img.copy()
            #r=(147,320,239,160)
            #img= img[int(r[1]):int(r[1]+r[3]),int(r[0]):int(r[0]+r[2])]
            img = change_brightness(img, 1, 0)
            if sorting.status == 'waiting':
                sorting.Sorting_grap(img, color_hsv)
                #sorting.sorting_run(color_hsv)
            if model == 'Exit':
                cv.destroyAllWindows()
                capture.release()
                break
            imgbox.value = cv.imencode('.jpg', show_img)[1].tobytes()
        except KeyboardInterrupt:capture.release()


# In[24]:


display(controls_box,output)
threading.Thread(target=camera, ).start()


# In[ ]:





# In[9]:






##### 

