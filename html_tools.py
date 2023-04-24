# importing beautifulsoup4
from bs4 import BeautifulSoup
import json
import demjson
import requests
import os


def download_html_as_text(id):
    """Downloads a HTML page and returns it as a string"""
    if os.path.isfile(f"htmls/expose_{id}.html"):
        with open(f"htmls/expose_{id}.html", "r") as f:
            html_source = f.read()
    else:
        raise Exception("HTML file not found")
    return html_source


def generate_html_summary(exp_id):
    """Generates a summary of the HTML page"""
    html_source = download_html_as_text(exp_id)
    html_data_dict = scrape_is_html(html_source)
    html_details_text = ""
    for key, value in html_data_dict.items():
        if value is not None:
            html_details_text += f"---{key}: {value}\n\t"
    return html_details_text


def scrape_is_html(html_source):
    """Scraping the html source and returning a dictionary with the scraped data"""
    # creating empty data dictionary
    html_data = {}

    # Using beautifulsoup4 to parse the html source
    soup = BeautifulSoup(html_source, "html.parser")

    try:
        # Find the class <div class=""is24qa-kaltmiete-main is24-value font-semibold is24-preis-value"> and get the text
        coldrent = soup.find("div", class_="is24qa-kaltmiete-main").text.strip().split(" €")[0]
        # printing the rent
        print(coldrent)
        html_data["coldrent"] = coldrent
    except:
        print("No rent found")
        html_data["coldrent"] = None

    try:
        warmrent = soup.find("div", class_="is24qa-warmmiete-main").text.strip().split(" €")[0]
        # printing the warm rent
        print(warmrent)
        html_data["warmrent"] = warmrent
    except:
        print("No warm rent found")
        html_data["warmrent"] = None

    try:
        num_rooms = soup.find("div", class_="is24qa-zi-main").text.strip()
        # printing the number of rooms
        print(num_rooms)
        html_data["num_rooms"] = num_rooms
    except:
        print("No number of rooms found")
        html_data["num_rooms"] = None

    try:
        flat_size = soup.find("div", class_="is24qa-flaeche-main").text.strip().split(" m")[0].replace(",", ".")
        # printing the flat size
        print(flat_size)
        html_data["flat_size"] = flat_size
    except:
        print("No flat size found")
        html_data["flat_size"] = None

    try:
        level = soup.find("dd", class_="is24qa-etage").text.strip()
        # printing the level
        print(level)
        html_data["level"] = level
    except:
        print("No level found")
        html_data["level"] = None

    try:
        with_balcony = soup.find("span", class_="is24qa-balkon-terrasse-label").text.strip()
        # printing if there is a balcony
        print(with_balcony)
        html_data["with_balcony"] = with_balcony
    except:
        print("No balcony found")
        html_data["with_balcony"] = None

    try:
        caution = soup.find("div", class_="is24qa-kaution-o-genossenschaftsanteile").text.strip().split(" €")[
            0].replace(".", "").replace(",", ".")
        # printing the caution
        print(caution)
        html_data["caution"] = caution
    except:
        print("No caution found")
        html_data["caution"] = None

    try:
        built_in = soup.find("dd", class_="is24qa-baujahr").text.strip()
        # printing the built in year
        print(built_in)
        html_data["built_in"] = built_in
    except:
        print("No built in year found")
        html_data["built_in"] = None

    try:
        heating_type = soup.find("dd", class_="is24qa-heizungsart").text.strip()
        # printing the heating type
        print(heating_type)
        html_data["heating_type"] = heating_type
    except:
        print("No heating type found")
        html_data["heating_type"] = None

    try:
        energy_efficiency_class = soup.find("dd", class_="is24qa-energieeffizienzklasse").text.strip()
        # printing the energy efficiency class
        print(energy_efficiency_class)
        html_data["energy_efficiency_class"] = energy_efficiency_class
    except:
        print("No energy efficiency class found")
        html_data["energy_efficiency_class"] = None

    try:
        object_decsription = soup.find("pre", class_="is24qa-objektbeschreibung").text.strip()
        # printing the object description
        print(object_decsription)
        html_data["object_decsription"] = object_decsription
    except:
        print("No object description found")
        html_data["object_decsription"] = None

    try:
        technical_details = soup.find("pre", class_="is24qa-ausstattung").text.strip().replace("\n", "")
        # printing the technical details
        print(technical_details)
        html_data["technical_details"] = technical_details
    except:
        print("No technical details found")
        html_data["technical_details"] = None

    try:
        place = soup.find("pre", class_="is24qa-lage").text.strip().replace("\n", "")
        # printing the place
        print(place)
        html_data["place"] = place
    except:
        print("No place found")
        html_data["place"] = None

    try:
        other_details = soup.find("pre", class_="is24qa-sonstiges").text.strip().replace("\n", "")
        # printing the other details
        print(other_details)
        html_data["other_details"] = other_details
    except:
        print("No other details found")
        html_data["other_details"] = None

    metadata_dict = scrape_is_json(html_source)

    contact_person_dict = metadata_dict.get("contactData", {}).get("contactPerson", None)
    print(contact_person_dict)
    if contact_person_dict is not None:
        html_data["contact_person"] = contact_person_dict.get("salutationAndTitle", "") + " " + contact_person_dict.get(
            "firstName", "") + " " + contact_person_dict.get("lastName", "")
    else:
        html_data["contact_person"] = None

    contact_realtor_dict = metadata_dict.get("contactData", {}).get("realtorInformation", None)
    if contact_realtor_dict is not None:
        html_data["contact_realtor"] = contact_realtor_dict.get("companyName", None)

    html_data["expose_id"] = metadata_dict.get("id", None)
    if html_data["expose_id"] is None:
        try:
            expose_id = soup.find("div", class_="is24-scoutid__content").text.split("Scout-ID:")[1].strip().replace(
                "\n", "")
            # printing the other details
            print(expose_id)
            html_data["expose_id"] = other_details
        except:
            print("No expose id found in HTML soup")

    return html_data


# scraping dictionaries from script tag
def scrape_is_json(html_source):
    """Scraping the html source and returning a dictionary with the scraped data"""
    # creating empty data dictionary
    try:
        raw_text = html_source.split("IS24.reporting")[0].split("IS24.expose = ")[1].strip()[
                   :-1]  # .replace("true", "\"True\"").replace("false", "\"False\"")
        expose_dict = demjson.decode(raw_text)
    except:
        expose_dict = {}
    return expose_dict

