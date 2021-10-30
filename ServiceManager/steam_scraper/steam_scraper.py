import json
import re
import sys

import requests
from bs4 import BeautifulSoup

PLAYTIME_EPSILON = 0.2


def scrape_profile(steamid):
    URL_PROFILE = f"https://steamcommunity.com/profiles/{steamid}/"
    profile_soup = BeautifulSoup(requests.get(URL_PROFILE).content, "html.parser")
    warning = False
    profile_stats = dict()

    query = profile_soup.find_all(class_="profile_count_link ellipsis")

    if len(query) == 0:
        warning = True
        print_warning("No 'profile_count' stats have been found on the scraped profile!")

    for stat in query:
        stat_name = str(stat.find("a").find(class_="count_link_label").text).lower()
        numbers = re.findall(r'\d+', stat.find("a").find(class_="profile_count_link_total").text)

        if len(numbers) == 1:
            stat_count = int(numbers[0])
        elif len(numbers) == 0:
            stat_count = 0
        else:
            stat_count = -1
            warning = True
            print_warning(f"RegEx found {len(numbers)} Numbers for '{stat_name}'")

        profile_stats[stat_name] = stat_count

    profile_stats["level"] = int(profile_soup.find(class_="friendPlayerLevelNum").text)
    profile_stats["recent_activity"] = float(profile_soup.find(class_="recentgame_recentplaytime").text.split(" ")[0]
                                             .replace("\n", ""))

    return profile_stats, warning


def get_player_summaries_v2(steam_id, api_key):
    res = requests.get(
        f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_id}")
    if res.status_code == 200:
        return json.loads(res.content.decode('utf-8'))["response"]
    else:
        raise Exception(f"Request was invalid, status-code: {res.status_code} {res.text}")


def get_owned_games_v1(steam_id, api_key):
    res = requests.get(
        f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}"
        f"&format=json&include_played_free_games=true&skip_unvetted_apps=false")
    if res.status_code == 200:
        return json.loads(res.content.decode('utf-8'))["response"]
    else:
        raise Exception(f"Request was invalid, status-code: {res.status_code} {res.text}")


def get_all_user_data(steam_id, api_key):
    scrape, scrape_warning = scrape_profile(steam_id)
    data = {
        "profile_scrape": scrape,
        "get_player_summaries_v2": get_player_summaries_v2(steam_id, api_key),
        "get_owned_games_v1": get_owned_games_v1(steam_id, api_key)
    }

    validate_warning = validate_data(data)
    return data, scrape_warning or validate_warning


def validate_data(data):
    """
    validates fetched data by get_all_user_data()
    :param data: dict returned by get_all_user_data()  # TODO: merge both functions?
    :return:
    """
    # compare recent playtime from scraped profile and from API
    playtime_owned_games = sum(map(lambda game: game['playtime_2weeks'] if 'playtime_2weeks' in game else 0,
                                   data['get_owned_games_v1']['games'])) / 60
    playtime_profile_scrape = float(data['profile_scrape']['recent_activity'])

    if abs(playtime_profile_scrape - playtime_owned_games) > PLAYTIME_EPSILON:
        print_warning(f"scraped and API's recent playtime differ more than {PLAYTIME_EPSILON},"
                      f"({playtime_owned_games}, {playtime_profile_scrape})")
        return True
    return False


def print_warning(message):
    print(f"Warning: {message}", file=sys.stderr)
