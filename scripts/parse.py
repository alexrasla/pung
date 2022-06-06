import pandas as pd
import os
import argparse

def parse_output(file_name, num_messages, total_clients, total_servers, rate, contact_rate):
    
    send_time, retr_time, download_bytes, upload_bytes = [], [], 0, 0

    with open(file_name, 'r') as out:
        for line in out:
            data = line.split('|')
            if len(data) == 3:
                if (data[0][7:8] == '0' or data[0][7:8] == '5'):
                    if data[0][10:14] == 'Sent':
                        send_usec_val = data[2].split(' ')[1]
                        send_time.append(int(send_usec_val)/10**6)
                    elif data[0][10:14] == 'Retr': 
                        retr_usec_val = data[2].split(' ')[1]
                        retr_time.append(int(retr_usec_val)/10**6)
                    elif data[0][10:13] == 'PIR' and data[1] == " Download ":
                        download_pir_bytes = data[2].split(' ')[1]
                        download_bytes += int(download_pir_bytes)
                        # print('down', download_bytes)
                    elif data[0][10:13] == 'PIR' and data[1] == "   Upload ":
                        upload_pir_bytes = data[2].split(' ')[1]
                        upload_bytes += int(upload_pir_bytes)
                        # print('up', upload_bytes)

    avg_retr = sum(retr_time) / len(retr_time)
    avg_sent = sum(send_time) / len(send_time)    
            
    print('Average Sent Time:', avg_sent)
    print('Average Retr Time:', avg_retr)
    print('Download Bytes:', download_bytes)
    print('Upload Bytes:', upload_bytes)

    new_data = {'num_messages'  : [num_messages],
                'total_clients' : [total_clients],
                'total_servers' : [total_servers], 
                'message_rate'  : [rate], 
                'contact_rate'  : [contact_rate],
                'avg_send_time' : [avg_sent], 
                'avg_retr_time' : [avg_retr], 
                'upload_bytes'  : [upload_bytes],
                'download_bytes': [download_bytes]
                }

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
    parser.add_argument('-n', dest='num_messages', default='', help='file name', type=int)
    parser.add_argument('-c', dest='total_clients', default='', help='file name', type=int)
    parser.add_argument('-s', dest='total_servers', default='', help='file name', type=int)
    parser.add_argument('-k', dest='message_rate', default='', help='file name', type=int)
    parser.add_argument('-v', dest='contact_rate', default='', help='file name', type=int)

    results = parser.parse_args()

    file_name = results.file
    num_messages = results.num_messages
    total_clients = results.total_clients
    total_servers = results.total_servers
    rate = results.message_rate
    contact_rate = results.contact_rate
    
    parse_output(file_name, num_messages, total_clients, total_servers, rate, contact_rate)