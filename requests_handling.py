# THIS SCRIPT IS INTENDED TO DEFINE FUNCTIONS THAT WILL
# SAVE RELEVANT DATA FOR EACH RIDER REQUEST
import copy
import requests as req
import json
import numpy as np
from tqdm import tqdm
import datetime
from save_read_data import save_data,read_data

number_of_drivers = 2848

def request_handling(riders_list,system):
    
    riders_data_list = []
    drivers_data = []
    requests = read_data("requests")
    for i in range(number_of_drivers):
        drivers_data.append({"id" : i, "boarding_alighting_list":[]})

    for i in tqdm(range(len(riders_list))):

        itinerary = -1


        response = requests[i]
        id = riders_list[i]['id']
        

        if 'plan' in response.keys() and len(response['plan']['itineraries']) >= 1:
            # solve itineraries by making the rider choose the shortest one
            '''
            shortest_duration = np.Infinity
            for i in range(len(response['plan']['itineraries'])): # number of tested itineraries
                if response['plan']['itineraries'][i]["duration"] < shortest_duration :
                    shortest_duration = response['plan']['itineraries'][0]["duration"]
                    itinerary = i
            '''
            fastest_itinerary = itinerary
            
            if system == "integrated":
                status, solution, itinerary = get_status_for_integrated(response,itinerary)
            if system == "current":
                status, solution, itinerary = get_status_for_current(response,itinerary)
                #print(status)
            if system == "no carpooling":
                status, solution, itinerary = get_status_for_no_carpooling(response,itinerary)
            waiting_time = get_waiting_time(response,itinerary)
            walking_distance = get_walking_distance(response,itinerary)
            total_duration = get_total_duration(response,itinerary)
            total_distance = get_total_distance(response)
        
        else :
            waiting_time = np.inf
            walking_distance = np.inf
            status = "unserved"
            solution = "unserved"
            total_duration = np.inf
            total_distance = get_total_distance(response)
            
        
        riders_data_list.append({"id" : id,
                        "waiting time":waiting_time,
                        "walking distance":walking_distance,
                        "status":status,
                        "solution":solution,
                        "total duration":total_duration,
                        "total distance":total_distance})        

        # filling drivers data with {"driver_id" : "id",
        #                           "boarding_alighting_list" : [(boarding_time,alighting,time)]}
        #                           "" :  
        #print("itinerary = ",itinerary)
        if itinerary != -1 and system != "no carpooling":
            drivers_data = single_driver_data(response,itinerary,drivers_data)
            #print(drivers_data[:50])
    save_data(riders_data_list,'riders_simulation_data')

    return riders_data_list,drivers_data

def single_driver_data(response,itinerary,drivers_data):
   # for i in range(number_of_drivers):
    copy_of_drivers_data = copy.deepcopy(drivers_data)
    for item in response['plan']['itineraries'][itinerary]['legs']:
        if "route of carpooler number" in str(item["route"]):
            id = int(str.split(str(item["route"])," ")[-1])
            departure = datetime.datetime.fromtimestamp(int(item["startTime"])/1e3).time()
            arrival = datetime.datetime.fromtimestamp(int(item["endTime"])/1e3).time()
            
            copy_of_drivers_data[id-1]["boarding_alighting_list"].append([departure,arrival])
            #print(copy_of_drivers_data[id])
    return copy_of_drivers_data


def get_waiting_time(response,itinerary):

    return int(response['plan']['itineraries'][itinerary]["waitingTime"]/60)

def get_walking_distance(response,itinerary):

    return response['plan']['itineraries'][itinerary]["walkDistance"]/1000

def get_total_duration(response,itinerary):

    return int(response['plan']['itineraries'][itinerary]["duration"]/60)

def get_status_for_integrated(response,itinerary):

    solution = "unserved"
    status = "unserved"
    transit = False
    carpooling = False
    multi_carpooling = False
    carpooling_counter = 0
    
    duration_sorted_itin_list = [(response['plan']['itineraries'][x]['duration'],x) for x in range(len(response['plan']['itineraries']))]
    list.sort(duration_sorted_itin_list,key = lambda x : x[0])

    for k in range(len(duration_sorted_itin_list)):
        itinerary = duration_sorted_itin_list[k][1]
        carpooling = False
        transit = False
        multi_carpooling = False
        multi_carpooling_counter = 0
        walking_distance = get_walking_distance(response,itinerary)
        waiting_time = get_waiting_time(response,itinerary)

        if walking_distance > 2.5 or waiting_time > 10 :
            itinerary = -1
            status = "unserved"
            solution = "unserved"

        else :   
            
            if response['plan']['itineraries'][itinerary]["transitTime"] == 0:
                solution = "walk"
                status = "served"
                break

            else :
                carpooling_counter = 0

                for item in response['plan']['itineraries'][itinerary]['legs']:
                    
                    #print("_____________route name = ",item['route'],"____________________")
                    if "route of carpooler number" in str(item["route"]):
                        carpooling = True
                        carpooling_counter += 1
                    if str(item["route"]) != "" and "route of carpooler number" not in str(item["route"]) :
                        transit = True

                if carpooling_counter>1:
                    multi_carpooling = True

                if transit and carpooling :
                    solution = "integrated"
                    status = "served"
                    return status, solution, itinerary
                else:
                    if transit :
                        solution = "transit"
                        status = "served"
                        return status, solution, itinerary
                    if carpooling :
                        solution = "carpooling"
                        status = "served"        
                        if multi_carpooling:
                            solution = "multi carpooling" 
                            status = "served" 
                        return status, solution, itinerary         
    #print("transit is : ",transit,"/ carpooling is : ",carpooling," / multi carpooling is : ",multi_carpooling)                
    return status, solution, itinerary


def get_status_for_current(response,itinerary):

    solution = "unserved"
    status = "unserved"
    carpooling = False
    transit = False
    multi_carpooling = False
    multi_carpooling_counter = 0  

    duration_sorted_itin_list = [(response['plan']['itineraries'][x]['duration'],x) for x in range(len(response['plan']['itineraries']))]
    list.sort(duration_sorted_itin_list,key = lambda x : x[0])

    for k in range(len(duration_sorted_itin_list)):
        solution = "unserved"
        status = "unserved"
        carpooling = False
        transit = False
        multi_carpooling = False
        multi_carpooling_counter = 0

        itinerary = duration_sorted_itin_list[k][1]
        walking_distance = get_walking_distance(response,itinerary)
        waiting_time = get_waiting_time(response,itinerary)

        # if the current path is unusable
        if walking_distance > 2.5 or waiting_time > 10 :
            status = "unserved"
            solution = "unserved"
            itinerary = -1

        # else check if on foot or other
        else: 
            itinerary = duration_sorted_itin_list[k][1]
            if response['plan']['itineraries'][itinerary]["transitTime"] == 0:
                status = "served"
                solution = "walk"
                break

            else :
                for item in response['plan']['itineraries'][itinerary]['legs']:
                    if "route of carpooler number" in str(item["route"]):

                        carpooling = True
                        multi_carpooling_counter +=1 
                    if str(item["route"]) != "" and "route of carpooler number" not in str(item["route"]) :
                        transit = True 
        
                if transit and carpooling :
                    status = "unserved"
                    solution = "unserved"
                    itinerary = -1
                else:
                    itinerary = duration_sorted_itin_list[k][1]
                    if transit :
                        status = "served"
                        solution = "transit"
                        break
                    if carpooling :                        
                        if multi_carpooling_counter>1:
                            status = "served"
                            solution = "multi carpooling"
                            break
                        else:
                            status = "served"
                            solution = "carpooling"
                            break

              
    return status, solution, itinerary

def get_status_for_no_carpooling(response,itinerary):

    solution = "unserved"
    status = "unserved"
    transit = False
    walk = False

    
    duration_sorted_itin_list = [(response['plan']['itineraries'][x]['duration'],x) for x in range(len(response['plan']['itineraries']))]
    list.sort(duration_sorted_itin_list,key = lambda x : x[0])

    for k in range(len(duration_sorted_itin_list)):
        solution = "unserved"
        status = "unserved"

        itinerary = duration_sorted_itin_list[k][1]
        transit = False
        carpooling = False
        walking_distance = get_walking_distance(response,itinerary)
        waiting_time = get_waiting_time(response,itinerary)

        if walking_distance > 2.5 or waiting_time > 10 :
            status = "unserved"
            solution = "unserved"
            itinerary = -1

        else :    
            # voir si il y va à pied
            if response['plan']['itineraries'][itinerary]["transitTime"] == 0:
                walk = True
                solution = "walk"
                status = "served"
                break

            else :
                for item in response['plan']['itineraries'][itinerary]['legs']:
                    if str(item["route"]) != "" and "route of carpooler number" not in str(item["route"]):
                        transit = True
                    if "route of carpooler number" in str(item["route"]):
                        carpooling = True
                        
                if transit == True and carpooling == False:
                    solution = "transit"
                    status = "served"
                    break   
    #print(solution)          
    return status, solution, itinerary

def get_total_distance(response):
    origin = str.split(response['requestParameters']['fromPlace'],sep=",")
    origin = (float(origin[0]),float(origin[1]))
    destination = str.split(response['requestParameters']['toPlace'],sep=",")
    destination = (float(destination[0]),float(destination[1]))
    return compute_distance(origin,destination)

def compute_distance(origin,destination):
    import math

    circuity = 1
    distance = 0

    lat1 = origin[0]
    lat2 = destination[0]
    lon1 = origin[1]
    lon2 = destination[1]

    φ1 = lat1 * math.pi/180; # φ, λ in radians
    φ2 = lat2 * math.pi/180;
    Δφ = (lat2-lat1) * math.pi/180;
    Δλ = (lon2-lon1) * math.pi/180;

    p = 0.017453292519943295;    # Math.PI / 180
    c = math.cos;
    a = 0.5 - c((lat2 - lat1) * p)/2 + c(lat1 * p) * c(lat2 * p) * (1 - c((lon2 - lon1) * p))/2;
    distance += 12742 * math.asin(math.sqrt(a)) # 2 * R; R = 6371 km

    return circuity * distance; 

