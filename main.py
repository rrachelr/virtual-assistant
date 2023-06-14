"""
Author: Rachel Robins
Updated: 6/14/23
Description: This program runs the virtual assistant "Aida" who will
execute tasks according to the user's input.
"""
from datetime import date
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import time
import requests
import json

load_dotenv()

USER = "Friend"
END_WORDS = ["quit", "stop", "bye"]
SEARCH_WORDS = ["look up", "google"]
JOKES_URL = "https://official-joke-api.appspot.com/jokes/random"
USER_AGENT = os.getenv("USER_AGENT")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
CSE_KEY = os.getenv("CSE_KEY")


def welcome():
    """
    Prints a welcome message for the user upon running the program
    """
    print(f"Welcome back, {USER}!")


def get_date():
    """
    Prints the current date textually using the datetime module
    """
    today = date.today().strftime("%B %d, %Y")
    print(f"Today's date is: {today}")


def get_time():
    """
    Prints the current local time formatted as a string using the time module
    """
    now = time.localtime()
    current_time = time.strftime("%H:%M:%S", now)
    print(f"It is currently {current_time}")


def tell_joke():
    """
    Prints a random joke from the Offical Jokes API with a three second pause in between
    the setup and punchline for comedic effect.
    """
    response = requests.get(JOKES_URL)
    response_dict = json.loads(response.text)
    print(response_dict["setup"])
    for i in range(3):
        print("...")
        time.sleep(1)
    print(response_dict["punchline"])


def check_weather(command: str):
    """
    The user's weather related query is searched in Google, and the relevant
    data is extracted from the result into a dictionary. The weather data is
    then printed. With this method, the weather location can be included in the
    command without the need for a second input.

    Args: command (str) -> the user's input that includes the word "weather"
    """
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    url = f"https://www.google.com/search?lr=lang_en&ie=UTF-8&q={command}"
    html = session.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    results = {}
    results["region"] = soup.find("span", attrs={"class": "BBwThe"}).text
    results["temp"] = soup.find("span", attrs={"id": "wob_tm"}).text
    results["weather"] = soup.find("span", attrs={"id": "wob_dc"}).text
    results["precipitation"] = soup.find("span", attrs={"id": "wob_pp"}).text
    results["humidity"] = soup.find("span", attrs={"id": "wob_hm"}).text
    results["wind"] = soup.find("span", attrs={"id": "wob_ws"}).text
    print("Current weather in:", results["region"])
    print("Temperature:", results["temp"])
    print("Description:", results["weather"])
    print("Precipitation:", results["precipitation"])
    print("Humidity:", results["humidity"])
    print("Wind:", results["wind"])


def google_search():
    """
    Prints the first ten Google search results for the inputted
    query using Google Custom Search Engine API.
    """
    query = input("What would you like to search for?\n")
    url = f"https://www.googleapis.com/customsearch/v1?key={CSE_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start=20"
    response = requests.get(url).json()
    search_results = response.get("items")
    for i, search_results in enumerate(search_results, start=1):
        title = search_results.get("title")
        snippet = search_results.get("snippet")
        link = search_results.get("link")
        print("=" * 10, f"Result #{i}", "=" * 10)
        print("Title:", title)
        print("Description:", snippet)
        print("URL:", link, "\n")


if __name__ == "__main__":
    welcome()

    while True:
        command = input().lower()

        if "date" in command:
            get_date()
        elif "time" in command:
            get_time()
        elif "joke" in command:
            tell_joke()
        elif "weather" in command:
            check_weather(command)
        elif any(word in command for word in SEARCH_WORDS):
            google_search()
        elif any(word in command for word in END_WORDS):
            print(f"Goodbye, {USER}!")
            break
