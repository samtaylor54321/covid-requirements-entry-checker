import requests
import json
import pandas as pd
import geopandas as gpd
from flask import Flask
import folium
import re

COUNTRY_NAME_LOOKUP = {
    "Côte d'Ivoire": "Ivory Coast",
    "Tanzania": "United Republic of Tanzania",
    "USA": "United States of America",
    "Serbia": "Republic of Serbia",
    "North Macedonia": "Macedonia",
    "Myanmar (Burma)": "Myanmar",
    "The Gambia": "Gambia",
    "Guinea-Bissau": "Guinea Bissau",
    "Democratic Republic of the Congo": "Democratic Republic of the Congo",
}


app = Flask(__name__)


def extract_covid_requirements(string: str) -> str:
    """
    Extracts entry requirements to a country from string

    Args:
        String (str): HTML formatted as a str
    Returns:
        str: Extracted entry requirements for a given country
    """
    try:
        covid_entry_requirements = (
            '<h3 id="entry-to-'
            + re.findall(
                r'h3 id="entry-to-(.+?)</p>\n\n<h3',
                string,
                re.DOTALL,
            )[0]
            + "</p>"
        )
    except IndexError:
        covid_entry_requirements = (
            "No entry rules in response to coronavirus are listed"
        )
    return covid_entry_requirements


def build_foreign_travel_advice_dataset(country_urls: dict) -> pd.DataFrame:
    """
    Builds pd.DataFrame containing foreign travel advice for each country

    Args:
        urls (dict): Dictionary containing the name of the country and the url
            containing the travel advice
    Returns:
        pd.DataFrame: pd.DataFrame where each country is a row and each column
            represents travel advice about a specific topic eg. Terrorism
    Notes:
        NaNs will be filled with an empty string
    """
    # Extract data for each category for each country
    dataset = pd.DataFrame()
    country_list = []

    for link in country_urls.values():
        try:
            html = requests.get(link)
            res = json.loads(html.content.decode())

            country_list.append(res["details"]["country"]["name"])

            country_content = {}

            for part in res["details"]["parts"]:
                country_content[part["slug"]] = part["body"]

            country_data = pd.DataFrame(country_content, index=[0])

            dataset = pd.concat([dataset, country_data], ignore_index=True)
        except requests.exceptions.MissingSchema:
            continue

    # Update country lists to remove naming inconsistancies between countries
    country_list = [COUNTRY_NAME_LOOKUP.get(item, item) for item in country_list]
    dataset["name"] = country_list

    # Fill missing values in dataset
    dataset = dataset.fillna("")

    return dataset


# Call data from API
html = requests.get("https://www.gov.uk/api/content/foreign-travel-advice")
res = json.loads(html.content)

# Parse through JSON to find country links
countries = {}

for doc in res["links"]["children"]:
    print(doc["api_url"])
    countries[doc["details"]["country"]["name"]] = doc["api_url"]

# Build dataset of foreign travel advice
dataset = build_foreign_travel_advice_dataset(countries)
print("dataset built")

# Extract COVID entry requirements from html
dataset["entry-requirements"] = dataset["entry-requirements"].apply(
    lambda x: extract_covid_requirements(x)
)

# Extract basic values to visualise on map
dataset["value"] = dataset["entry-requirements"].apply(
    lambda x: 0 if x == "No entry rules in response to coronavirus are listed" else 100
)


@app.route("/")
def index():
    # Get map data
    url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data"
    country_shapes = f"{url}/world-countries.json"

    print("map data loaded")
    # Parse geodata and combine with foreign office travel advice data
    geoJSON_df = gpd.read_file(country_shapes)
    final_df = geoJSON_df.merge(
        dataset[["name", "value", "entry-requirements"]], on="name"
    )

    print("map data combined")
    # Instantiate map
    the_map = folium.Map(tiles="cartodbpositron", location=[40, 34], zoom_start=2)

    # Add choropleth layer
    choropleth = folium.Choropleth(
        geo_data=final_df,
        name="choropleth",
        data=final_df,
        columns=["name", "value"],
        key_on="feature.properties.name",
        fill_color="YlOrBr",
        nan_fill_color="black",
        fill_opacity=0.7,
        line_opacity=0.2,
    ).add_to(the_map)

    # Add layer control for tooltip
    folium.LayerControl().add_to(the_map)

    # Add tool tip HTML
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(
            ["name", "entry-requirements"],
            labels=False,
            style=(
                "overflow-wrap: break-word; background-color: white; color: black; margin: auto;"
            ),
            localize=True,
        )
    )
    print("map_built")
    return the_map._repr_html_()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=888)
