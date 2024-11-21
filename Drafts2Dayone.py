import pandas as pd
import re
import argparse

def process_drafts(input_file, output_file):
    """Process Drafts export data and write to text file in Day One format
    
    Args:
        input_file (str): Path to Drafts export CSV file
        output_file (str): Path to output text file
    """
    # Read Drafts export CSV file
    draftcsv = pd.read_csv(input_file, sep=',')

    # Extract and format creation timestamps
    create_time = draftcsv.created_at.to_list()
    # Split timestamp strings into components
    create_time = [re.split('-|:|T|Z',i) for i in create_time]
    # Format timestamps into Day One format
    create_time = ['Date:'+res[0]+'年'+res[1]+'月'+res[2]+'日 GMT+8 下午9:21:00\n\n\n' for res in create_time]

    # Create DataFrame with formatted timestamps and content
    draft = pd.DataFrame(zip(create_time, draftcsv.content.tolist()), 
                        columns=['Time','content'])

    # Write formatted records to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for _, rec in draft.iterrows():
            f.write(rec['Time'])
            f.write(rec['content']+'\n')

def main():
    parser = argparse.ArgumentParser(description='Convert Drafts export to Day One format')
    parser.add_argument('--input', required=True, help='Path to the Drafts export CSV file')
    parser.add_argument('--output', required=True, help='Path to output text file')
    
    args = parser.parse_args()
    
    process_drafts(args.input, args.output)

if __name__ == '__main__':
    main()