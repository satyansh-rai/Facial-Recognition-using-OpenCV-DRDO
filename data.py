import pymysql
import serial
import time
import datetime


ser = serial.Serial('/dev/ttyACM0',500000)
conn1=pymysql.connect(host='localhost',user='root',password='password123',db='firstapp')
    
with conn1:
    
    while(True):
        data = ser.readline()[:-2] #the last bit gets rid of the new-line chars
        data = str(data.decode('ascii'))
        if data: 
            print(data.split())
            line = data.split()

            if line[0] == "entry" or line[0] == "exit":
                if len(line)==2:
                    a=conn1.cursor()
                    if line[0] == "entry":
                        k=1
                    else:
                        k=0
                    emp = 1
                    a.execute("insert into entryExit (employee, entryExit) values (%s,%s)",(emp,k))
                    conn1.commit()
                    a.close()

                else:    
                    print("partial data observed!")
            elif line[0] == "V":
                if len(line)==6:
                    a=conn1.cursor()
                    a.execute("insert into sensorData (temp,smoke,vibration) values (%s,%s,%s)",(line[3],line[5],line[1]))
                    conn1.commit()
                    a.close()
                else:
                    print("partial data observed!")

            else:
                print("Garbage data!")