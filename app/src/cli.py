import argparse
import sys
from .converter import convert_all_csv_in_directory
from .indexer import create_index
from .search_api import search as api_search
from .config import DATA_DIR, logger

if __name__ == "__main__":
    print("CLI Tool Placeholder")

def main():
    parser = argparse.ArgumentParser(description='nfacct converter and search tool')
    subparsers = parser.add_subparsers(dest='command')

    convert_parser = subparsers.add_parser('convert', help='Convert CSV files to Parquet')
    convert_parser.add_argument('--data-dir', default=DATA_DIR, help='Data directory')

    index_parser = subparsers.add_parser('index', help='Create indexes for Parquet files')
    index_parser.add_argument('--data-dir', default=DATA_DIR, help='Data directory')

    search_parser = subparsers.add_parser('search', help='Search for records by SRC_IP')
    search_parser.add_argument('src_ip', help='SRC_IP to search for')

    args = parser.parse_args()

    if args.command == 'convert':
        convert_all_csv_in_directory(args.data_dir)
    elif args.command == 'index':
        create_index(args.data_dir)
    elif args.command == 'search':
        import asyncio
        loop = asyncio.get_event_loop()
        try:
            results = loop.run_until_complete(api_search(args.src_ip))
            print(results)
        except Exception as e:
            logger.error(e)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
