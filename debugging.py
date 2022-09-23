

from save_read_data import read_data
from tqdm import tqdm

data = [read_data("integrated_system_riders"),read_data("current_system_riders"),read_data("no_carpooling_system_riders")]
for i in range(len(data[0])):

    if (data[1][i]["solution"] == "unserved") and (data[2][i]["solution"] != "unserved"):
        print("discrepancy in rider number ",i)
        print("______rider ",i,"____________")
        print(" integrated : ",data[0][i]["solution"]," his journey lasted : ",data[0][i]["total duration"]," he walked : ",data[0][i]["walking distance"]," he waited : ",data[0][i]["waiting time"])
        print(" current : ",data[1][i]["solution"]," his journey lasted : ",data[1][i]["total duration"]," he walked : ",data[1][i]["walking distance"]," he waited : ",data[1][i]["waiting time"])
        print(" no carpooling : ",data[2][i]["solution"]," his journey lasted : ",data[2][i]["total duration"]," he walked : ",data[2][i]["walking distance"]," he waited : ",data[2][i]["waiting time"])
    
    if data[0][i]["total distance"] <= 2.5 and data[0][i]["solution"] == "unserved":
        print("__________rider ",i," should've walked________________________")
        print(" integrated : ",data[0][i]["solution"]," his journey lasted : ",data[0][i]["total duration"]," he walked : ",data[0][i]["walking distance"]," he waited : ",data[0][i]["waiting time"])
        print(" current : ",data[1][i]["solution"]," his journey lasted : ",data[1][i]["total duration"]," he walked : ",data[1][i]["walking distance"]," he waited : ",data[1][i]["waiting time"])
        print(" no carpooling : ",data[2][i]["solution"]," his journey lasted : ",data[2][i]["total duration"]," he walked : ",data[2][i]["walking distance"]," he waited : ",data[2][i]["waiting time"])
  