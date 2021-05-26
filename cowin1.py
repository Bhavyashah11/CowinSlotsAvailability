import requests
from datetime import datetime, timedelta
import time
import json

age = int(input("Enter the age : "))
print("Note:Enter the next pincode with a space in between")
pinCodes=list(map(int,input("Enter the pincodes: ").rstrip().split()))

num_days = 2    #slot checking next upcoming two days 
print_flag = 'y'

print("Starting search for Covid vaccine slots!")

actual = datetime.today()
list_format = [actual + timedelta(days=i) for i in range(num_days)]    #time delta adds days to the actual today's date

actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]        #formats the data in the given dmy format
#print(actual_dates)

while True:
    counter = 0   
    
    for pinCode in pinCodes:   
        for given_date in actual_dates:

            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pinCode, given_date)
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 
            
            result = requests.get( URL, headers=header )
            if result.ok:
                response_json = result.json()
                
                
                if response_json["centers"]:            
                    if(print_flag.lower() =='y'):

                        for center in response_json["centers"]:
                    
                            for session in center["sessions"]:
                                if (session["min_age_limit"] <= age and session["available_capacity"] > 0 ) :
                                    print("Pincode: " + str(pinCode))
                                    print("Available on: {}".format(given_date))
                                    print("\t", center["name"])
                                    print("\t", center["block_name"])
                                    print("\t Price: ", center["fee_type"])
                                    print("\t Availablity : ", session["available_capacity"])

                                    if(session["vaccine"] != ''):
                                        print("\t Vaccine type: ", session["vaccine"])
                                    print("\n")

                                    counter = counter + 1
                                else:
                                    pass                                    
                else:
                    pass        
                          
            else:
                print("No Response!")

                
    if(counter == 0):
        print("No Vaccination slot avaliable!")
    else:
        print("Search Completed!")


    dt = datetime.now() + timedelta(seconds=60)

    while datetime.now() < dt:
        time.sleep(1)
