## THIS FILE WILL HAVE THE FUNCTIONS THAT WILL GENERATE STATISTICS
# import necessary libraries
import pandas as pd
from save_read_data import read_data
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from figure_4 import figure_4

def summary_pie_chart(riders_list,save_path=""):
  
    carpooling_i = 0
    foot_i = 0
    transit_i = 0
    no_solution_i = 0
    integrated = 0
    multi_carpooling_i = 0


    for item in riders_list[0]:
        solution = item["solution"]
        if solution == "multi carpooling":
            multi_carpooling_i +=1
        if solution == "carpooling":
            carpooling_i +=1
        if solution == "transit":
            transit_i += 1
        if solution == "walk":
            foot_i += 1
        if solution == "unserved":
            no_solution_i +=1
        if solution == "integrated":
            integrated +=1
        
    
    carpooling_cs = 0
    foot_cs = 0
    transit_cs = 0
    no_solution_cs = 0
    multi_carpooling_cs = 0
    
    for item in riders_list[1]:
        solution = item["solution"]
        if solution == "multi carpooling":
            multi_carpooling_cs +=1
        if solution == "carpooling":
            carpooling_cs +=1
        if solution == "transit":
            transit_cs += 1
        if solution == "walk":
            foot_cs += 1
        if solution == "unserved":
            no_solution_cs +=1
   
    foot_nc = 0
    transit_nc = 0
    no_solution_nc = 0
    

    for item in riders_list[2]:
        solution = item["solution"]
        if solution == "transit":
            transit_nc += 1
        if solution == "walk":
            foot_nc += 1
        if solution == "unserved":
            no_solution_nc +=1

    NUMBER_OF_RIDERS = len(riders_list[0])
    # create DataFrame
    df = pd.DataFrame({'multimodal' : [0,0,0,integrated*100/NUMBER_OF_RIDERS],
                    'foot': [0,foot_nc*100/NUMBER_OF_RIDERS,foot_cs*100/NUMBER_OF_RIDERS,foot_i*100/NUMBER_OF_RIDERS],
                    'transit': [0,transit_nc*100/NUMBER_OF_RIDERS,transit_cs*100/NUMBER_OF_RIDERS,transit_i*100/NUMBER_OF_RIDERS],
                    'carpooling':[0,0,carpooling_cs*100/NUMBER_OF_RIDERS,carpooling_i*100/NUMBER_OF_RIDERS],
                    'multi carpooling':[0,0,multi_carpooling_cs*100/NUMBER_OF_RIDERS,multi_carpooling_i*100/NUMBER_OF_RIDERS],
                    'unserved': [0,no_solution_nc*100/NUMBER_OF_RIDERS,no_solution_cs*100/NUMBER_OF_RIDERS,no_solution_i*100/NUMBER_OF_RIDERS]},
                    index=['','No Carpooling', 'Current','Integrated'])
    
    
    # create stacked bar chart for monthly temperatures
    plt.rcParams.update({'font.size': 25})
    
    plot = df.plot(kind='bar',edgecolor='black',rot=0,figsize=(15,12), stacked=True, color=['1', '0', '0.3','0.5','0.7','0.9'])
    plt.legend(loc=2, prop={'size': 20})

    plt.ylabel('Percentage of riders')#.legend(loc="lower_left")
    
    if save_path != "":
        plt.savefig(save_path+"/served_and_unserved.eps",format='eps')
    plt.show() 

def better_waiting_walking_times(riders_list,save_path=""):
    average_walking_i = 0
    average_waiting_i = 0 

    average_walking_cs = 0
    average_waiting_cs = 0 

    average_walking_nc = 0
    average_waiting_nc = 0 


    relevant_rider_counter_i = 0 
    #don't count not served riders

    relevant_rider_counter_cs = 0
    relevant_rider_counter_nc = 0

    for rider in riders_list[0] :
        if rider['status'] != "unserved":
            if rider['waiting time'] != np.Infinity and rider['walking distance'] != np.Infinity:#and rider.born_time<60:
                average_walking_i += rider['walking distance']
                average_waiting_i += rider['waiting time']
                relevant_rider_counter_i +=1

    for rider in riders_list[1] :
        if rider['status'] != "unserved":
            if rider['waiting time'] != np.Infinity and rider['walking distance'] != np.Infinity:#and rider.born_time<60:
                average_walking_cs += rider['walking distance']
                average_waiting_cs += rider['waiting time']
                relevant_rider_counter_cs +=1

    for rider in riders_list[2] :
        if rider['status'] != "unserved":
            if rider['waiting time'] != np.Infinity and rider['walking distance'] != np.Infinity:#and rider.born_time<60:
                average_walking_nc += rider['walking distance']
                average_waiting_nc += rider['waiting time']
                relevant_rider_counter_nc +=1
    
    average_walking_i =(average_walking_i)/ relevant_rider_counter_i
    average_waiting_i /= relevant_rider_counter_i

    average_walking_cs = average_walking_cs/relevant_rider_counter_cs
    average_waiting_cs /= relevant_rider_counter_cs

    average_walking_nc = average_walking_nc/relevant_rider_counter_nc
    average_waiting_nc /= relevant_rider_counter_nc

    df = pd.DataFrame({"Time/Distance":["Walking Distance","Waiting Time","Walking Distance","Waiting Time","Walking Distance","Waiting Time","Walking Distance","Waiting Time"],
                        "Time (Minutes)/Distance (km)":[average_walking_i,average_waiting_i,average_walking_cs,average_waiting_cs,average_walking_nc,average_waiting_nc,0,0],
                        "System":["Integrated","Integrated","Current","Current","No Carpooling","No Carpooling","",""]})
    plot = sns.barplot(x="System",y="Time (Minutes)/Distance (km)",hue="Time/Distance",data = df)
    
    if save_path != "":
        plt.savefig(save_path+"/waiting and walking times.png",format='png')


    plt.show()
    
    return plot       

def maximum_capacity(system,save_path="results/28 aout 2022"):
    drivers_list = read_data(system+"_system_drivers")
    capacity_list = [0,0,0]
    number_of_drivers = len(drivers_list)
    for item in drivers_list:
        capacity = 0
        times_list = item["boarding_alighting_list"]
        if len(times_list) == 1:
            capacity = 1
        if len(times_list) >1:
            intersections = []
            
            for i in range(len(times_list)):
                intersection_value = 0
                for j in range(i+1,len(times_list)):
                    if (times_list[i][0] <times_list[j][0] and times_list[i][1]>times_list[j][0]) | (times_list[i][0]<times_list[j][1] and times_list[i][1]>times_list[j][1]):
                        intersection_value += 1
                intersections.append(intersection_value)
            capacity = max(intersections)
        
        if capacity>4 :
            print(capacity)
            number_of_drivers -=1 # faire comme si ce driver n'a jamais existé
        else :
            if capacity>1:
                capacity_list[2] +=1
            else :
                capacity_list[capacity] +=1

    # plot
    labels = ['0 rider', '1 rider',
        '>1 riders']

    data = [item * 100/len(drivers_list) for item in capacity_list]


    explode = (0, 0, 0) 
    colors = plt.cm.gray(np.linspace(0.5,1,5))
    fig1, ax1 = plt.subplots(figsize=(10, 8))

    hatches = ['+','/','.']

    pie =ax1.pie(data, colors=colors,explode=explode, autopct='%1.1f%%',pctdistance=1.3,
            shadow=False,textprops={'fontsize': 35}, startangle=0)

    for patch, hatch in zip(pie[0],hatches):
        patch.set_hatch(hatch)

  
    plt.legend(labels,loc="upper right", fontsize=35)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.tight_layout()
    #plt.show()
    if save_path != "" :
        plt.savefig(save_path+"/maximum_occupancy_"+system+".eps")    
    plt.show()        
    return 0

data = [read_data("integrated_system_riders"),read_data("current_system_riders"),read_data("no_carpooling_system_riders")]
new_data = [[],[],[]]
riders_data = read_data("riders_data_actual")
for i in range(len(data[0])):
    if (data[0][i]["total distance"] <= 2.5)  and (data[0][i]["status"] == "unserved"):
        pass # account for errors in OTP
    else :
        if riders_data[i]["departure_time"]>645 and riders_data[i]["departure_time"]<675: 
            if data[0][i]["total distance"] != np.Infinity:         
                new_data[0].append(data[0][i])
                new_data[1].append(data[1][i])
                new_data[2].append(data[2][i])

data = new_data



# parameters for plot function "figure_4"
T_t = []
T_d = []

C_t = []
C_d = []

I_t = []
I_d = []

T_d_inf = []
C_d_inf = []
I_d_inf = []

for i in tqdm(range(len(data[0]))):

    

        rider_T = data[0][i]
        rider_C = data[1][i]
        rider_I = data[2][i]

        distance_T = rider_T["total distance"]#ALL_GRAPHS[0].get_distance(ALL_GRAPHS[0].get_node(rider_T.get_pos_depart()),ALL_GRAPHS[0].get_node(rider_T.get_pos_arrivee()))
        distance_C = rider_C["total distance"]#ALL_GRAPHS[1].get_distance(ALL_GRAPHS[1].get_node(rider_C.get_pos_depart()),ALL_GRAPHS[1].get_node(rider_C.get_pos_arrivee()))
        distance_I = rider_I["total distance"]#ALL_GRAPHS[2].get_distance(ALL_GRAPHS[2].get_node(rider_I.get_pos_depart()),ALL_GRAPHS[2].get_node(rider_I.get_pos_arrivee()))

        time_T = rider_T["total duration"]
        time_C = rider_C["total duration"]
        time_I = rider_I["total duration"]

        faster_than_foot = 0
        slower_than_foot = 0
        if time_T != np.inf and time_T<=distance_T*60/4.5:# accounting for circuity
            T_t.append(time_T)
            T_d.append(distance_T)
        else:
            T_d_inf.append(distance_T)

        if time_C != np.inf and time_C<=distance_C*60/4.5:
            C_t.append(time_C)
            C_d.append(distance_C)
        else:
            C_d_inf.append(distance_C)

        if time_I != np.inf and time_I<=distance_I*60/4.5:
            I_t.append(time_I)
            I_d.append(distance_I)
        else:
            I_d_inf.append(distance_I)

# THE "pattes de mouches"
#figure_4(T_t,T_d, C_t,C_d, I_t,I_d, T_d_inf,C_d_inf,I_d_inf,save_path = "results/28 aout 2022")


#data = [read_data("integrated_system"),read_data("current_system"),read_data("no_carpooling_system")]
#print(data)
#maximum_capacity("integrated")
#maximum_capacity("current")
summary_pie_chart(data,save_path="results/28 aout 2022")
#better_waiting_walking_times(data)
