from login import login
from navigate import navigate_to_page
from filler import select_dates, fill_info
import json

defaults = {"is_last_month" : 'False',
            "presence" : "0",
            "start_time" : "09:30",
            "min_hours" : "9",
            "project_code" : "",
            "is_random" : "True",
            "start_time_distribution" : "[0.2,0.6,0.2]",
            "hours_distribution" : "[0.8, 0.1, 0.1]",
            }

# setting configurations
def load_config(filename="conf.json"):
    try:
        with open(filename, "r") as file:
            config = json.load(file)
        conf = {key: item["value"] for key, item in config.items()}
        for key in ['website', 'username', 'password']:
            if key not in conf.keys():
                raise Exception(key + ' key is required and is not specified in conf.json')
    except:
        raise Exception('Failed to read ' + filename)

    for key in defaults.keys():
        if key not in conf.keys():
            conf[key] = defaults[key]
    return conf

def main():
    filename = 'conf.json'
    conf = load_config(filename)
    driver = login(conf)
    navigate_to_page(driver)
    select_dates(driver, conf)
    fill_info(driver, conf)

if __name__ == "__main__":
    main()