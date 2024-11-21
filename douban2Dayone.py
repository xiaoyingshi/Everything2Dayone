import pandas as pd
import datetime
import re
import argparse

# Process movie data
def process_movies(input_file, output_file):
    """Process movie viewing records from Excel file and write to text file"""
    # Read movie data from Excel
    tb = pd.read_excel(input_file, sheet_name='看过')
    
    # Convert timestamps to Dayone format
    tb.Time = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('Date:%Y年%m月%d日 GMT+8 18:27:56') 
               for x in tb.Time.to_list()]
    tb = tb.dropna()

    # Write formatted movie records to file
    with open(output_file, 'w', encoding='utf-8') as f:
        for _, rec in tb.iterrows():
            if len(rec['content']) > 1:
                f.write(rec['Time'] + '\n\n\n')
                f.write('# ' + rec['Title'] + '\n')
                f.write(rec['content'] + '\n')
                f.write('#评论\n\n\n')

# Process book data                
def process_books(input_file, output_file):
    """Process book reading records from Excel file and write to text file"""
    # Read book data from Excel
    tb = pd.read_excel(input_file, sheet_name='读过')
    
    # Convert timestamps and select relevant columns
    tb.创建时间 = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('Date:%Y年%m月%d日 GMT+8 18:27:56') 
                for x in tb.创建时间.to_list()]
    tb = tb.loc[:,['标题','创建时间','评论']]
    tb = tb.dropna()

    # Write formatted book records to file
    with open(output_file, 'w', encoding='utf-8') as f:
        for _, rec in tb.iterrows():
            if len(rec['评论']) > 1:
                f.write(rec['创建时间'] + '\n\n\n')
                f.write('# ' + rec['标题'] + '\n')
                f.write(rec['评论'] + '\n')
                f.write('#评论\n\n\n')

# Process game data
def process_games(input_file, output_file):
    """Process game playing records from Excel file and write to text file"""
    # Read game data from Excel
    tb = pd.read_excel(input_file, sheet_name='玩过')
    
    # Convert timestamps and select relevant columns
    tb.创建时间 = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('Date:%Y年%m月%d日 GMT+8 18:27:56') 
                for x in tb.创建时间.to_list()]
    tb = tb.loc[:,['标题','创建时间','评论']]
    tb = tb.dropna()

    # Write formatted game records to file
    with open(output_file, 'w', encoding='utf-8') as f:
        for _, rec in tb.iterrows():
            if len(rec['评论']) > 1:
                f.write(rec['创建时间'] + '\n\n\n')
                f.write('# ' + rec['标题'] + '\n')
                f.write(rec['评论'] + '\n')
                f.write('#评论\n\n\n')

# Process broadcast data
def process_broadcasts(input_file, output_file):
    """Process broadcast records from CSV file and write to text file"""
    # Read broadcast data
    tb = pd.read_csv(input_file)
    tb = tb.loc[:,['时间','广播带前缀']]
    tb = tb.dropna()

    # Remove unwanted records
    filters = [
        'https://img9.doubanio.com/view/status/l/public/5d976384b7b5926.jpg',
        'Shortcuts'
    ]
    for filter_text in filters:
        boolist = [filter_text in i for i in tb.时间.to_list()]
        rows = tb.index[[i for i, x in enumerate(boolist) if x]]
        tb.drop(rows, inplace=True)

    # Convert timestamps
    tb.时间 = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('Date:%Y年%m月%d日 GMT+8 %H:%M:%S') 
              for x in tb.时间.to_list()]

    # Remove records with specific keywords
    keywords = ['读过', '看过', '想读', '想看', '在看', '上传1张照片']
    for keyword in keywords:
        boolist = [keyword in i for i in tb.广播带前缀.to_list()]
        rows = tb.index[[i for i, x in enumerate(boolist) if x]]
        tb.drop(rows, inplace=True)

    # Clean up content
    tb.广播带前缀 = [i.replace('海鲜你个小土豆 说:\n','') for i in tb.广播带前缀.tolist()]
    tb.广播带前缀 = [re.sub('\n\n.*','',i) for i in tb.广播带前缀.tolist()]

    # Write formatted broadcast records to file
    with open(output_file, 'w', encoding='utf-8') as f:
        for _, rec in tb.iterrows():
            if len(rec['广播带前缀']) > 1:
                f.write(rec['时间'] + '\n\n\n')
                f.write(rec['广播带前缀'] + '\n\n\n')

def main():
    parser = argparse.ArgumentParser(description='Convert Douban export data to Day One format')
    parser.add_argument('--excel', required=True, help='Path to the Douban export Excel file (e.g., 豆伴.xlsx)')
    parser.add_argument('--broadcast', required=True, help='Path to the broadcast CSV file (e.g., broadcastBackUp.csv)')
    parser.add_argument('--output-dir', default='.', help='Directory to save output files (default: current directory)')
    
    args = parser.parse_args()
    
    # Create output paths
    movie_output = f"{args.output_dir}/movie.txt"
    book_output = f"{args.output_dir}/book.txt"
    game_output = f"{args.output_dir}/game.txt"
    broadcast_output = f"{args.output_dir}/podcasts.txt"
    
    # Process all data types
    process_movies(args.excel, movie_output)
    process_books(args.excel, book_output)
    process_games(args.excel, game_output)
    process_broadcasts(args.broadcast, broadcast_output)

if __name__ == '__main__':
    main()
