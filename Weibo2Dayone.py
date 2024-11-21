import pandas as pd
import os
import calendar
import argparse

def get_all_weibo_files(input_dir):
    """Get all Weibo HTML files from input directory
    
    Args:
        input_dir (str): Directory containing Weibo HTML files
        
    Returns:
        list: List of Weibo HTML filenames
    """
    weibo_files = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.html'):
                weibo_files.append(os.path.join(root, file))
    return weibo_files

def clean_weibo_content(weibo_files):
    """Clean and process Weibo HTML content
    
    Args:
        weibo_files (list): List of Weibo HTML file paths
        
    Returns:
        list: Cleaned Weibo content
    """
    all_weibo = []
    # HTML elements and text to remove
    remove_elements = ['div', 'meta', 'head', 'html', 'link', '<i', 'href', 
                      'content', 'style', 'title', 'article', '/a', '<ul',
                      'body', '<h3', 'm-auto-box']
    remove_text = ['Sakuraxxy2333', '<span>', '</span>', '分享图片', '来自']
    
    for file in weibo_files:
        with open(file, 'r') as f:
            weibo = [line.strip() for line in f.readlines()]
            # Remove lines containing HTML elements
            for element in remove_elements:
                weibo = [line for line in weibo if element not in line]
            # Remove specific text
            weibo = [line for line in weibo if line not in remove_text]
            all_weibo.extend(weibo)
            
    return all_weibo

def process_timestamps(weibo_content):
    """Process and format timestamps in Weibo content
    
    Args:
        weibo_content (list): List of Weibo content lines
        
    Returns:
        list: Content with formatted timestamps
    """
    # Create month name to number mapping
    month_dict = {month: index for index, month in enumerate(calendar.month_abbr) if month}
    
    for i in range(len(weibo_content)):
        if '<span class="time">' in weibo_content[i]:
            # Extract timestamp components
            tmp = weibo_content[i].replace('<span class="time">', '').replace('</span>', '').split()
            clock = tmp[3].split(':')
            
            # Convert to 12-hour format
            if int(clock[0]) > 12:
                clock[0] = str(int(clock[0]) - 12)
                period = '下午'
            else:
                period = '上午'
                
            # Format timestamp
            weibo_content[i] = f"Date:{tmp[5]}年{month_dict[tmp[1]]}月{tmp[2]}日 GMT+8 {period}{clock[0]}:{clock[1]}:{clock[2]}"
            
    return weibo_content

def write_weibo_to_file(weibo_df, output_file):
    """Write processed Weibo content to output file
    
    Args:
        weibo_df (DataFrame): DataFrame containing Weibo content
        output_file (str): Path to output file
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for _, rec in weibo_df.iterrows():
            content = rec['content'].strip()
            if len(content) > 1 and not content.isspace():
                f.write(f"{rec['Time']}\n\n\n")
                cleaned_content = (content.replace('<span>', '')
                                        .replace('</span>', '')
                                        .replace('<span class="m-line-gradient">', ''))
                f.write(f"{cleaned_content}\n\n\n")

def process_weibo(input_dir, output_file):
    """Main function to process Weibo HTML files to Day One format
    
    Args:
        input_dir (str): Directory containing Weibo HTML files
        output_file (str): Path to output text file
    """
    # Get all Weibo files
    weibo_files = get_all_weibo_files(input_dir)
    
    # Clean and process content
    weibo_content = clean_weibo_content(weibo_files)
    
    # Process timestamps
    weibo_content = process_timestamps(weibo_content)
    
    # Create DataFrame
    weibo_df = pd.DataFrame(list(zip(weibo_content[0::2], weibo_content[1::2])),
                           columns=['Time', 'content'])
    
    # Write to output file
    write_weibo_to_file(weibo_df, output_file)

def main():
    parser = argparse.ArgumentParser(description='Convert Weibo HTML exports to Day One format')
    parser.add_argument('--input-dir', required=True, help='Directory containing Weibo HTML files')
    parser.add_argument('--output', required=True, help='Path to output text file')
    
    args = parser.parse_args()
    
    process_weibo(args.input_dir, args.output)

if __name__ == '__main__':
    main()