import pandas as pd
import re
import os
import argparse

def process_notion(input_dir, output_file):
    """Process Notion export files and write to text file in Day One format
    
    Args:
        input_dir (str): Directory containing Notion export files
        output_file (str): Path to output text file
    """
    # Dictionary to convert month abbreviations to numbers
    cal_dict = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }

    # Process all files and collect results
    allres = []
    for fs in os.listdir(input_dir):
        # Read and process each file
        file_path = os.path.join(input_dir, fs)
        with open(file_path, 'r') as f2:
            # Read lines and strip whitespace
            data = [i.strip() for i in f2.readlines()]
            
            # Extract relevant content (timestamp and text after line 7)
            res = [data[2]]  # Get timestamp from line 3
            res.extend(data[7:])  # Get content after line 7
            
            # Filter out lines containing image references
            res = [i for i in res if 'png' not in i]
            
            # Format timestamp to Day One format
            date_parts = res[0].split()
            res[0] = (f"Date:{date_parts[3]}年{cal_dict[date_parts[1][:3]]}月"
                     f"{date_parts[2].replace(',', '')}日 GMT+8 上午7:21:00\n\n\n")
            
            allres.extend(res)

    # Write processed content to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for rec in allres:
            f.write(rec + '\n')

def main():
    """Parse command line arguments and run the conversion"""
    parser = argparse.ArgumentParser(description='Convert Notion export to Day One format')
    parser.add_argument('--input-dir', required=True, help='Directory containing Notion export files')
    parser.add_argument('--output', required=True, help='Path to output text file')
    
    args = parser.parse_args()
    
    process_notion(args.input_dir, args.output)

if __name__ == '__main__':
    main()