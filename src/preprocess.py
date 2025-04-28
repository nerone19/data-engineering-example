import csv
import re

data_dict = {}


def clean_raw_message(raw_message: str) -> str:
    """
    Cleans the raw message from not allowed characters (not alphanumeric or dot) 

    Args:
        raw_message (str): the raw message to clean

    Returns:
        str: The clean message, formatted as follow (value1,value2,...)
    """
    
    formatted_message = []
    for el in raw_message.split(","):
        cleaned = re.sub("[^A-Za-z0-9.]", "", el)
        filtered = re.match("[a-zA-Z0-9]+$|(\d+)(?:\.)?(\d+)?", cleaned)
        if filtered:
            formatted_message.append(filtered[0])
    
    return ",".join(formatted_message)

def  is_raw_message_noised(raw_message: str) -> bool:
    """
    States whether a message is noised or not (containing not allowed messages or not)

    Args:
        raw_message (str): the raw message to be checked.

    Returns:
        bool: if the message is noised.
    """

    isNoised = re.search("[^A-Za-z0-9., ]", raw_message)
    if isNoised: 
        return True
    return False

def preprocess_dataset() -> None:
    """
    Preprocess the dataset, cleaning any records containing not allowed characters. A new dataset will then be created with the 
    preprocessed dataset.
    
    
    """
    with open('./data/raw_messages.csv', newline='') as csvfile:
        # We split based on the comma operator but we keep it when encountering the raw message inside ""
        reader = csv.reader(csvfile, delimiter=',', doublequote=True, quotechar='"')
        for i,row in enumerate(reader):
            device_id, date_time, address_ip, address_port, original_message_id, raw_message = row
            if i > 0: 
                key = f"{device_id}-{date_time}"
                if (key in data_dict and data_dict[key][-1] is True):
                    if not is_raw_message_noised(raw_message):
                        data_dict[key][-2],data_dict[key][-1] = raw_message, False
                else:
                    data_dict[key] = [
                        device_id, 
                        date_time, 
                        address_ip, 
                        address_port, 
                        original_message_id, 
                        raw_message, 
                        is_raw_message_noised(raw_message)]
    
    for key, value in data_dict.items():
        device_message, is_message_noised =  value[-2:]
        if is_message_noised is True:
            data_dict[key][-2] = clean_raw_message(device_message)

    
    
    with open('./data/preprocessed_messages.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', doublequote=True, quotechar='"')
        for key, value in data_dict.items():
            writer.writerow(value[:-1])
            
preprocess_dataset()