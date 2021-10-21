import json

import requests
from bs4 import BeautifulSoup


def scrape_profile(steamid):
    URL_PROFILE = f"https://steamcommunity.com/profiles/{steamid}/"
    profile_page = requests.get(URL_PROFILE)
    profile_soup = BeautifulSoup(profile_page.content, "html.parser")

    headings = ["badges", "games", "inventory", "screenshots", "workshop_items", "reviews", "artwork", "groups",
                "friends"]
    query_counts = profile_soup.find_all(class_="profile_count_link_total")

    profile_stats = dict()
    for html_element, heading in zip(query_counts, headings):
        extract_number = ''.join(filter(lambda x: x.isdigit(), html_element.text))
        if len(extract_number) > 0:
            profile_stats[heading] = int(extract_number)
        else:
            profile_stats[heading] = 0

    profile_stats["player_level"] = int(profile_soup.find(class_="friendPlayerLevelNum").text)
    return profile_stats


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
        f"&format=json&include_played_free_games=true")
    if res.status_code == 200:
        return json.loads(res.content.decode('utf-8'))["response"]
    else:
        raise Exception(f"Request was invalid, status-code: {res.status_code} {res.text}")


def get_all_user_data(steam_id, api_key):
    data = {
        "profile_scrape": scrape_profile(steam_id),
        "get_player_summaries_v2": get_player_summaries_v2(steam_id, api_key),
        "get_owned_games_v1": get_owned_games_v1(steam_id, api_key)
    }
    return str(data)