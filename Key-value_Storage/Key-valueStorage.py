import argparse
import json
import os
import tempfile


def update_file(args, storage_path):
    '''changes the data in the file according 
    to the conditions of the problem'''

    # check file presence in the directory
    if os.path.exists(storage_path):
        
        # read what is already in the file
        with open(storage_path, 'r') as file_data:
            data_in_file = json.loads(file_data.read())

        # update file contents
        if args.key in data_in_file:
            data_in_file[args.key].append(args.val)
        else:
            data_in_file[args.key] = [args.val]

        # write update the contents of the file
        with open(storage_path, 'w') as file_data:
            json.dump(data_in_file, file_data)
    else:
        # create a new file
        with open(storage_path, 'w') as file_data:
            json.dump({args.key: [args.val]}, file_data)


def print_value(args, storage_path):
    '''displays to the console the data in the 
    file according to the conditions of the task'''

    # check file presence in the directory
    if os.path.exists(storage_path):

        # read what is in the file
        with open(storage_path, 'r') as file_data:
            data_in_file = json.loads(file_data.read())
        
        if args.key in data_in_file:
            print(*data_in_file[args.key], sep=', ')
        else:
            print(None)
    else:
        print(None)


if __name__ == '__main__':

    # work with console and file directory
    parser = argparse.ArgumentParser()
    parser.add_argument('--key')
    parser.add_argument('--val')
    arg = parser.parse_args()
    storage_file = os.path.join(tempfile.gettempdir(), 'storage.json')

    # program
    if arg.key and arg.val:
        update_file(arg, storage_file) 
    else:
        print_value(arg, storage_file)
