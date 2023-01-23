
import cv2
import csv
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

from datetime import date, datetime

today = date.today()
date = today.strftime("%d-%b-%Y")

now = datetime.now()
timeRN = now.strftime("%H:%M:%S")

button = 23
LED = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED,GPIO.OUT)



def searchforwifi():
    cap = cv2.VideoCapture(0) #setting up capture
    detector = cv2.QRCodeDetector() #setting up detector
    old=''
    while True:
        
        # gets QR image
        _, img = cap.read()
        
        # how tor ead QR code 
        data, bbox, _ = detector.detectAndDecode(img)
        
        # Makes Camera feed look nice
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
            if data:
                if old == data: #on second scan of QR code it'll break loop
                    cap.release()
                    cv2.destroyAllWindows()
                    break
                print("data found: ", data)
                
                
           #write data to file and format     
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
            
                
        #will show what camera sees
        cv2.imshow("code detector", img)
        
        #pressing Q will also break program
        if(cv2.waitKey(1) == ord("q")):
            break

while True:
    button_push=GPIO.input(button)
    if button_push == 0:
        GPIO.output(LED,GPIO.HIGH) #lights button up while searching
        searchforwifi()
    else:
        GPIO.output(LED,GPIO.LOW)
