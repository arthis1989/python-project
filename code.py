import json
import re
import os
import datetime
from pprint import pprint

today_day = datetime.datetime.now()
day_of_the_week = today_day.strftime("%A")
final_feature = {}
trigger_list = []
verify_list = []

def read_input(filename,day_of_the_week):
    try:
        with open(filename, 'r') as data_file:
            data = json.load(data_file)
            global userverify
            global usertrigger
            global features
            global node
            global triggers
            global path
            global job_path
            path = data["path"]
            job_path = data["job_path"]

            for key, value in data.iteritems():
                if key == day_of_the_week:
                    dict_data = data[day_of_the_week]
                    userverify = dict_data[0].get('user_verify')
                    node = dict_data[0].get('node')
                    usertrigger = dict_data[0].get('user_trigger')
                    features = dict_data[0].get('features')
                    triggers = dict_data[0].get('triggers')
    except:
        print 'COULD NOT LOAD:', filename

def parse_file(path):
    global trigger_list
    global verify_list
    pattern = re.compile(r'{psat_trigger\S*\s{')
    pattern1 = re.compile(r'{verify\S*\s{')
    try:
        for subdir, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".tcl"):
                    x = path+'/'+file
                    with open(x) as f:
                        for line in f:
                            if pattern.search(line):
                                list_new = re.sub(r'\s|{|{', r'', line)
                                trigger_list.append(list_new.strip())
                            if pattern1.search(line):
                                list_new1 = re.sub(r'\s|{|{', r'', line)
                                verify_list.append(list_new1.strip())
    except ValueError:
        print 'No TCL file found in the given path:', path


def create_final_feature_list(features):
    for i in features:
        final_feature[i] = {}
        final_feature[i]['verification'] = []
        final_feature[i]['trigger'] = []
        for item in trigger_list:
            if i in item:
                final_feature[i]['trigger'].append(item)
        for item in verify_list:
            if i in item:
                final_feature[i]['verification'].append(item)
        final_feature[i]['trigger'].extend(usertrigger)
        final_feature[i]['verification'].extend(userverify)



if __name__ == "__main__":
    filename = "input.json"
    read_input(filename,day_of_the_week)
    parse_file(path)
    create_final_feature_list(features)

pprint(final_feature)
