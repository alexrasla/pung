import pandas as pd
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

new_data = {'test_type'    : [file_name],
            'avg_send_time': [avg_sent], 
            'avg_retr_time': [avg_retr]}

if not os.path.exists('data.csv'):
    pd_frame = pd.DataFrame.from_dict(new_data)
    pd_frame.to_csv('data.csv')
else:
    data = pd.read_csv('data.csv')
    # file_data = json.load(data)

# file_data[file_name] = new_data
# json.dump(file_data, data, indent = 4)