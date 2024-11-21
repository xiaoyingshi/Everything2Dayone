import pandas as pd
import os
import time
from datetime import datetime
import fileinput
import re
import argparse

def add_date_headers(directory):
    """Add Date header to files based on modification time"""
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        
        # Get file modification time and convert to list of strings
        res = time.gmtime(os.path.getmtime(file_path))
        res = [str(i) for i in list(res)]
        
        # Convert 24-hour time to 12-hour format with AM/PM
        if int(res[3]) > 11:
            res[3] = int(res[3]) - 12
            res[3] = str(res[3])
            res1 = "Date:\t" + res[0] + "年" + res[1] + "月" + res[2] + "日" + " GMT+8 下午" + res[3] + ":" + res[4] + ":" + res[5]
        else:
            res1 = "Date:\t" + res[0] + "年" + res[1] + "月" + res[2] + "日" + " GMT+8 上午" + res[3] + ":" + res[4] + ":" + res[5]
        
        # Prepend date header to file
        with open(file_path, 'r') as f:
            content = f.read()
        with open(file_path, 'w') as f:
            f.write(res1 + '\n' + content)

def add_empty_lines(directory):
    """Add empty lines after Date headers in files"""
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                content = file.read()
            
            # Replace Date line with itself plus newlines
            modified_content = re.sub(r'(Date:.*?)(\n|$)', r'\1\n\n\n\n', content)
            
            with open(filepath, 'w') as file:
                file.write(modified_content)

def remove_hash_lines(input_file):
    """Remove lines starting with # from file"""
    with open(input_file, 'r') as file:
        lines = file.readlines()

    with open(input_file, 'w') as file:
        for line in lines:
            if not line.startswith('#'):
                file.write(line)

def main():
    parser = argparse.ArgumentParser(description='Process Bear notes for Day One import')
    parser.add_argument('--input-dir', required=True, 
                      help='Directory containing Bear notes to process')
    parser.add_argument('--clean-file',
                      help='File to remove # lines from (optional)')
    
    args = parser.parse_args()
    
    # Add date headers and empty lines to all files in directory
    add_date_headers(args.input_dir)
    add_empty_lines(args.input_dir)
    
    # Optionally clean # lines from specified file
    if args.clean_file:
        remove_hash_lines(args.clean_file)

if __name__ == '__main__':
    main()