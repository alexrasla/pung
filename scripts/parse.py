import pandas as pd
import os
import argparse

def parse_output(file_name, num_messages, total_clients, total_servers, rate, contact_rate):
    
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

    new_data = {'num_messages' : [num_messages],
                'total_clients': [total_clients],
                'total_servers': [total_servers], 
                'message_rate' : [rate], 
                'contact_rate' : [contact_rate],
                'avg_send_time': [avg_sent], 
                'avg_retr_time': [avg_retr]}

    pd_frame = pd.DataFrame.from_dict(new_data)
    if not os.path.exists('data.csv'):
        pd_frame.to_csv('data.csv', index=False)
    else:
        curr_data = pd.read_csv('data.csv', index_col=[0])
        new_data = curr_data.append(pd_frame)
        new_data.to_csv('data.csv')
        
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='file', default='', help='file name', type=str)

    results = parser.parse_args()

    file_name = results.file
    parse_output(file_name)