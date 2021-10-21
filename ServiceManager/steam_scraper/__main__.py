import argparse
from datetime import datetime

from .steam_scraper import get_all_user_data

if __name__ == "__main__":
    # initialize parser
    parser = argparse.ArgumentParser(description="A simple steam scraper", prefix_chars="/-",
                                     prog="python -m test_service.py")

    # add arguments
    parser.add_argument("steam_id", type=str, help="a steamid to scrape (steamID64)")
    parser.add_argument("api_key", type=str, help="steam web api key")
    parser.add_argument("--tofile", action="store_true", help="save result to a new file in cwd")
    parser.add_argument("--noprint", action="store_true", help="dont print result on terminal")

    # parse arguments
    args = vars(parser.parse_args())

    # fetch user data
    user_data = get_all_user_data(args["steam_id"], args["api_key"])

    if args["tofile"]:
        file_name = datetime.now().strftime("steamscraper_%d_%m_%Y_%H_%M_%S")
        with open(file_name, "w") as file:
            file.write(str(user_data))

    if not args["noprint"]:
        print(user_data)