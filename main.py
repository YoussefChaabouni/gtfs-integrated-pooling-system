# MAIN SCRIPT TO BE EXECUTED AFTER RUNNING THE OTP SERVER WITH RELEVANT GTFS

from environmental_impact_handling import environmental_request_handling
from requests_handling import request_handling
from riders_generation import generate_riders
from save_read_data import read_data, save_data
import time

#number_of_riders = 100
#departure_times_window = [1100,1105] # 17:40 -> 18:00
start = time.time()

print("__________________generating riders data______________________________")
riders_data = read_data("riders_data_actual.pkl")

'''
print("______________________request handling for integrated__________________________________")
integrated_riders_simulation_data, integrated_drivers_simulation_data = environmental_request_handling(riders_data,"integrated")
save_data(integrated_riders_simulation_data,"costs_integrated_system_riders.pkl")
save_data(integrated_drivers_simulation_data,"costs_integrated_system_drivers.pkl")
#print(integrated_drivers_simulation_data)
'''
print("______________________request handling for current__________________________________")
current_riders_simulation_data, current_drivers_simulation_data = environmental_request_handling(riders_data,"current")
save_data(current_riders_simulation_data,"current_system_riders.pkl")
save_data(current_drivers_simulation_data,"current_system_drivers.pkl")

'''
print("______________________request handling for no carpooling__________________________________")
no_carpooling_riders_simulation_data,no_carpooling_drivers_simulation_data = environmental_request_handling(riders_data,"no carpooling")

save_data(no_carpooling_riders_simulation_data,"no_carpooling_system_riders")
save_data(no_carpooling_drivers_simulation_data,"no_carpooling_system_drivers")
'''


print("the program lasted = ",(time.time() - start)/60)

#print(riders_data[0])
#print(simulation_data)
