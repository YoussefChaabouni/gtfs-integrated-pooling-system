import copy
import requests as req
import json
import numpy as np
from tqdm import tqdm
import datetime
from save_read_data import read_data, save_data


def requests_generation(riders_list):
    
    requests_list = []
    drivers_data = []

    for i in tqdm(range(len(riders_list))):
        response = req.get(riders_list[i]["otp_request"])
        response.raise_for_status()  # raises exception when not a 2xx response
        if response.status_code != 204:
            response = response.json()
            requests_list.append(response)
    
    save_data(requests_list,"_requests.pkl")
    return requests_list
riders_data = read_data("environment_stat_riders.pickle")
requests_generation(riders_data)
            