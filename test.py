from typing import Optional

import typer
from rich import print_json, print
import requests
from requests.exceptions import HTTPError


app = typer.Typer()


@app.command()
def feed(start_date: str, end_date: Optional[str] = typer.Argument(None), api_key: str = typer.Option("", envvar="NASA_API_KEY", help="API key to the NASA API")):
    uri_path = "https://api.nasa.gov/neo/rest/v1/feed?"
    uri_args = [
        f"start_date={start_date}",
        f"api_key={api_key}"
        ]
    
    if end_date is not None:
        uri_args.append(f"end_date={end_date}")
        
    uri = uri_path + '&'.join(uri_args)
    
    try:
        response = requests.get(uri)
        response.raise_for_status()
    except HTTPError as http_error:
        print(f"HTTP error occurred: {http_error}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    else:
        print_json(response.text)


@app.command()
def lookup(asteroid_id: str, api_key: str = typer.Option("", envvar="NASA_API_KEY", help="API key to the NASA API")):
    uri = f"https://api.nasa.gov/neo/rest/v1/neo/{asteroid_id}?api_key={api_key}"
    
    try:
        response = requests.get(uri)
        response.raise_for_status()
    except HTTPError as http_error:
        print(f"HTTP error occurred: {http_error}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    else:
        print_json(response.text)
    


if __name__ == "__main__":
    app()