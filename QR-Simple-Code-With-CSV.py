#Code is similar to before but note the Adding Time section and the CSV Write control

#most importantly for this code to run is to import OpenCV
import cv2
import csv

#adding time and date stuff and rearranging it
from datetime import date, datetime

today = date.today()
date = today.strftime("%d-%b-%Y")

now = datetime.now()
timeRN = now.strftime("%H:%M:%S")
old=''

# set up camera object called Cap which we will use to find OpenCV
cap = cv2.VideoCapture(0)

# QR code detection Method
detector = cv2.QRCodeDetector()

#This creates an Infinite loop to keep your camera searching for data at all times
while True:
    
    # Below is the method to get a image of the QR code
    _, img = cap.read()
    
    # Below is the method to read the QR code by detetecting the bounding box coords and decoding the hidden QR data 
    data, bbox, _ = detector.detectAndDecode(img)
    
    # This is how we get that Blue Box around our Data. This will draw one, and then Write the Data along with the top
    if(bbox is not None):
        bb_pts = bbox.astype(int).reshape(-1, 2)
        num_bb_pts = len(bb_pts)
        for i in range(num_bb_pts):
            cv2.line(img,
                     tuple(bb_pts[i]),
                     tuple(bb_pts[(i+1) % num_bb_pts]),
                     color=(255, 0, 255), thickness=2)
        cv2.putText(img, data,
                    (bb_pts[0][0], bb_pts[0][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
        
        #Below prints the found data to the below terminal (This we can easily expand on to capture the data to an Excel Sheet)
        #You can also add content to before the pass. Say the system reads red it'll activate a Red LED and the same for Green.
        if data:
            if old == data:
                break
            print("data found: ", data)
            
            
       #**** This location is where we are adding the ability for the code to capture the Data and write it to a Text file
       #For this here we are writing the Information to Database.csv File located in the same directory (the desktop) as this code.     
            with open('Wifi_info.txt', mode='a') as txtfile:
                txtfile.truncate(0)
                old=data
                txtfile.write(data)    
                pas = ''
                ssid = ''
                s = data.split(';')
                print(s)
                for i in s:
                    if len(i)>0:
                        if i[0]=='P':
                            pas = i[2:]
                        if i[0]=='S':
                            ssid= i[2:]
                    if pas!='' and ssid!='':
                        #Create connection file wor wpa
                        text = "network={\n"
                        text+="""ssid="{}"
                    psk="{}"
                    proto=RSN
                    key_mgmt=WPA-PSK
                    pairwise=CCMP
                    auth_alg=OPEN""".format(ssid,pas)
                        text+="\n}"
                        text_file = open("wpa_supplicant.conf", "w")
                        n = text_file.write(text)
                
            if data == 'red':
                pass
            if data == 'green':
                pass
        
            
    # Below will display the live camera feed to the Desktop on Raspberry Pi OS preview
    cv2.imshow("code detector", img)
    
    #At any point if you want to stop the Code all you need to do is press 'q' on your keyboard
    if(cv2.waitKey(1) == ord("q")):
        break



# When the code is stopped the below closes all the applications/windows that the above has created
cap.release()
cv2.destroyAllWindows()
