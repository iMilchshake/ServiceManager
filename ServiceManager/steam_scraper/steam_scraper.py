import json
import sys

import requests
from bs4 import BeautifulSoup

PLAYTIME_EPSILON = 0.1


def scrape_profile(steamid):
    URL_PROFILE = f"https://steamcommunity.com/profiles/{steamid}/"
    profile_soup = BeautifulSoup(requests.get(URL_PROFILE).content, "html.parser")
    headings = ["badges", "games", "inventory", "screenshots", "workshop_items", "reviews", "artwork", "groups",
                "friends"]

    query_counts = profile_soup.find_all(class_="profile_count_link_total")

    profile_stats = dict()
    for html_element, heading in zip(query_counts, headings):
        extract_number = ''.join(filter(lambda x: x.isdigit(), html_element.text))
        profile_stats[heading] = int(extract_number) if len(extract_number) > 0 else 0

    profile_stats["player_level"] = int(profile_soup.find(class_="friendPlayerLevelNum").text)
    profile_stats["recent_activity"] = float(profile_soup.find(class_="recentgame_recentplaytime").text.split(" ")[0]
                                             .replace("\n", ""))
    warning = False
    if len(query_counts) != len(headings):
        warning = True
        print_warning("heading count and html-element count dont match!")

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
