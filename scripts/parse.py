import json
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-f', dest='file', default='', help='file name', type=str)

results = parser.parse_args()

file_name = results.file

send_time = []
retr_time = []

with open(file_name, 'r') as out:
    for line in out:
        data = line.split('|')
        if len(data) == 3:
            if data[0][10:14] == 'Sent':
                send_usec_val = data[2].split(' ')[1]
                send_time.append(int(send_usec_val))
                # print('sent', send_usec_val)
            elif data[0][10:14] == 'Retr':
                retr_usec_val = data[2].split(' ')[1]
                retr_time.append(int(retr_usec_val))
                # print('retr', retr_usec_val)

avg_retr = sum(retr_time) / len(retr_time)
avg_sent = sum(send_time) / len(send_time)    
         
print('Average Sent Time:', avg_sent)
print('Average Retr Time:', avg_retr)

new_data = {'avg_send_time': avg_sent, 
            'avg_retr_time':avg_retr}

if not os.path.exists('data.json'):
    data = open('data.json', 'w')
    file_data = dict()
else:
    data = open('data.json', 'r+')
    file_data = json.load(data)

file_data[file_name] = new_data
json.dump(file_data, data, indent = 4)