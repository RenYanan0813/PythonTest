#-*- coding: utf-8 -*-
# libzbar0
#pip install pyzbar
#pip install opencv-python

 import sys
 from pyzbar.pyzbar import decode
 import cv2


 if len(sys.argv) < 2:
 	print ("usage: %s <image file>" % sys.argv[0])
 	sys.exit(1)

 filepath = sys.argv[1]
 image = cv2.imread(filepath)
 result  = decode(image)
 for item in result:
 	print(item.type, item.data)