# Scraping test

Scapping portalinmobiliario web for search appartments in 'providencia-metropolitana' with '1 room' and '1 bath' (CONSTANTS VARS) with three criterias:

- square_meters_value: ordered from cheapest square meteres value to most expensive
- square_meters: ordered from lowest square meteres to highest
- price: ordered from cheapest price to most expensive

Please, write the criteria when the script starts

Then, two files .json will be create with the names: criteria_posts (first 15 posts with the criteria) and last_posts (50 posts) (CONSTANTS VARS)

# Execution

Create virtualenv (optional and depend the OS)

- Windows commands:
  python -m pip install virtualenv

- Create virtualenv:
  python -m venv name_virtualenv

- Actiavate virtualenv:
  name_virtualenv\Scripts\activate

- Install requeriments (libraries):
  python -m pip install -r requeriments.txt

- Execute script:
  python scrapping.py
