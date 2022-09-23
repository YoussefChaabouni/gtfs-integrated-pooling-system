import numpy as np
import pickle
from tqdm import tqdm
import geojson
import random


from save_read_data import save_data
import json




# rider creation function
## input : number_of_riders : int , departure_times_window = [first_time,last_time] (times are in minutes)
## output : list of dictionnaries containing id, origin, dest, departure_time, url_request
def generate_riders(departure_times_window):
    
    path_to_file = "map (2).geojson"
    with open(path_to_file) as f:
        gj = geojson.load(f)

    full_area = 0
    list_of_rectangle_boundaries = []
    for i in range(len(gj['features'])):
        # print("rectangle "+str(i)+" : ",gj['features'][i]['geometry']['coordinates']) 
        #print(" first point  : ",gj['features'][i]['geometry']['coordinates'][0][0])
        list_of_rectangle_boundaries.append([(gj['features'][i]['geometry']['coordinates'][0][0][0],gj['features'][i]['geometry']['coordinates'][0][0][1]),(gj['features'][i]['geometry']['coordinates'][0][2][0],gj['features'][i]['geometry']['coordinates'][0][2][1])])
        print(list_of_rectangle_boundaries[i])
        print(gj['features'][i]['properties']['area'])
        full_area += float(gj['features'][i]['properties']['area'])
  

    riders_list = []
    number_of_riders = int(full_area*8.3)
    print(number_of_riders)
    for i in tqdm(range(number_of_riders)):
        
        id = "Rider_"+str(i+1)
        rectangle_to_choose = random.randint(0,len(list_of_rectangle_boundaries)-1)
        rectangle = list_of_rectangle_boundaries[rectangle_to_choose]
        origin = (np.random.uniform(rectangle[0][1],rectangle[1][1]),np.random.uniform(rectangle[0][0],rectangle[1][0]))
        rectangle_to_choose = random.randint(0,len(list_of_rectangle_boundaries)-1)
        rectangle = list_of_rectangle_boundaries[rectangle_to_choose]
        destination = (np.random.uniform(rectangle[0][1],rectangle[1][1]),np.random.uniform(rectangle[0][0],rectangle[1][0]))
        departure_time = np.random.randint(departure_times_window[0],departure_times_window[1])

        if departure_time < 780 :
            am_or_pm = "am"
            hours = str(int(departure_time / 60)%12)
            minutes = str(int(departure_time % 60))
        else:
            am_or_pm = "pm"
            hours = str(int(departure_time / 60) % 12)
            minutes = str(int(departure_time % 60))
            #print(str(hours)+"_____"+str(minutes))
        
        #url_request = "http://localhost:8803/otp/routers/current/plan?&fromPlace="+str(origin[0])+"%2C"+str(origin[1])+"&toPlace="+str(destination[0])+"%2C"+str(destination[1])+"&time="+str(hours)+"%3A"+str(minutes)+str(am_or_pm)+"&date=07-20-2022&mode=TRANSIT%2CWALK&maxWalkDistance=4828.032&arriveBy=false&wheelchair=false&showIntermediateStops=true&debugItineraryFilter=false&numItineraries=7&additionalParameters=numItineraries&locale=en"
        url_request = "http://localhost:8803/otp/routers/current/plan?&fromPlace="+str(origin[0])+"%2C"+str(origin[1])+"&toPlace="+str(destination[0])+"%2C"+str(destination[1])+"&time="+str(hours)+"%3A"+str(minutes)+str(am_or_pm)+"&date=07-20-2022&mode=TRANSIT%2CWALK&maxWalkDistance=2500.032&arriveBy=false&wheelchair=false&showIntermediateStops=true&debugItineraryFilter=false&additionalParameters=numItineraries&numItineraries=10&locale=en"
        riders_list.append({"id" : id,
                            "origin":origin,
                            "destination":destination,
                            "departure_time":departure_time,
                            "otp_request":url_request})

        
    save_data(riders_list,"riders_data_actual")                        
    return riders_list


departure_times_window = [10*60+30,11*60+30] # 17:30 -> 18:30

#print("__________________generating riders data______________________________")
#riders_data = generate_riders(departure_times_window)
#save_data(riders_data,"riders_data_500")

#simulation_data = request_handling(riders_data,"integrated")
#save_data(simulation_data,"integrated_simulation_data")