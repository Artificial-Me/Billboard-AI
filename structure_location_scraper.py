import requests
import json
import time
import random
import os
from fake_useragent import UserAgent

ua = UserAgent()
BASE_URL = "https://ib.lamar.com/service/api/inventory/"
BASE_HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "x-requested-with": "XMLHttpRequest",
    "referer": "https://ib.lamar.com/app/?webmarket=montana",
    "cookie": "AMCVS_B1CE2D3A63D7D1C10A495FE3%40AdobeOrg=1; SnapABugRef=https%3A%2F%2Flamar.com%2Fmontana%3Ftags%3D%20; SnapABugHistory=1#; kndctr_B1CE2D3A63D7D1C10A495FE3_AdobeOrg_identity=CiY1OTM2NTI5Njc5MTM5NDUxODkxMDY1ODY0OTAzMjQ2MzU5NjczN1IQCO-yzvTdMhgBKgNPUjIwA_AB77LO9N0y; kndctr_B1CE2D3A63D7D1C10A495FE3_AdobeOrg_cluster=or2; AMCV_B1CE2D3A63D7D1C10A495FE3%40AdobeOrg=179643557%7CMCIDTS%7C20176%7CMCMID%7C59365296791394518910658649032463596737%7CMCAAMLH-1743800771%7C9%7CMCAAMB-1743800771%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1743203171s%7CNONE%7CMCSYNCSOP%7C411-20183%7CvVersion%7C5.5.0; OptanonAlertBoxClosed=2025-03-28T21:06:14.479Z; SnapABugNoProactiveChat=no; SnapABugChatWindow=false%7C0%7C; __cf_bm=zk9kimHlm2ma6t40Fx2bTyTkeg_F45.6.ipQdF7CHdY-1743196942-1.0.1.1-FFvkWAGLXlEbTmawIEyC6sA7NH7QsOLwi8_LL2SnMTQVhTAuQRS2EKQNnXmB6m7.hywYSzxQ.Lq8nj3RafKcWXdKfcjxph51rZVhqcewZ4M; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Mar+28+2025+15%3A22%3A43+GMT-0600+(Mountain+Daylight+Time)&version=202403.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=25d563ce-fa75-4ad7-b13f-ccf0ef83db5e&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0003%3A1%2CC0004%3A1%2CC0002%3A1%2CC0001%3A1&geolocation=US%3BMT&AwaitingReconsent=false; SnapABugUserAlias=%23; SnapABugVisit=4#1743195972"
}

def get_random_headers():
    headers = BASE_HEADERS.copy()
    headers["user-agent"] = ua.random
    return headers

def fetch_billboard_details(billboard_id, rate_limit_delay=1, max_retries=3):
    url = f"{BASE_URL}get/{billboard_id}"
    for attempt in range(max_retries):
        try:
            headers = get_random_headers()
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Billboard {billboard_id} - Status: {response.status_code}, Response: {response.text[:100]}...")
            if response.status_code == 200 and response.text.strip():
                data = response.json()
                time.sleep(rate_limit_delay)
                return data
            else:
                print(f"Billboard {billboard_id} - Empty or invalid response")
                return None
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed for billboard {billboard_id}: {e}")
            if attempt < max_retries - 1:
                time.sleep(rate_limit_delay * (2 ** attempt))
            else:
                return None
        except json.JSONDecodeError as e:
            print(f"Billboard {billboard_id} - Invalid JSON: {e}")
            return None

def is_in_montana(lat, lon):
    # Montana bounds: Lat 44.5 to 49, Lon -116 to -104
    return 44.5 <= lat <= 49 and -116 <= lon <= -104

def save_to_file(billboard_data, output_file):
    # Load existing data if file exists, otherwise start fresh
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []
    
    # Append new billboard data
    existing_data.append(billboard_data)
    
    # Write back to file
    with open(output_file, "w") as f:
        json.dump(existing_data, f, indent=4)
    print(f"Saved billboard {billboard_data['panelID']} to {output_file}")

def extract_billboards():
    start_time = time.time()
    output_file = r"C:\Users\david\Desktop\BillboardAI\structures.json"
    
    # Verify directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    print(f"Output file path: {output_file}")

    # Initialize request counters
    total_requests = 0
    max_requests = 10000

    # Load existing entries to avoid duplicates
    existing_entries = set()
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            try:
                existing_data = json.load(f)
                existing_entries = {entry.get('panelID') for entry in existing_data if entry.get('panelID')}
            except json.JSONDecodeError:
                pass

    # Known working IDs
    known_ids = [1065022, 109803]
    # Process known IDs first
    for billboard_id in known_ids:
        if total_requests >= max_requests:
            break
        data = fetch_billboard_details(billboard_id)
        if data and "latitude" in data and "longitude" in data:
            lat, lon = data["latitude"], data["longitude"]
            if is_in_montana(lat, lon) and data.get("panelID") not in existing_entries:
                billboard_entry = {
                    "panelID": data.get("panelID"),
                    "latitude": lat,
                    "longitude": lon,
                    "location": data.get("location"),
                    "weeklyImpressions": data.get("weeklyImpressions"),
                    "mediaTypeStyle": data.get("mediaTypeStyle"),
                    "cost": data.get("cost")
                }
                existing_entries.add(data.get("panelID"))
                save_to_file(billboard_entry, output_file)
            else:
                print(f"Billboard {billboard_id} at {lat}, {lon} is outside Montana or already exists")
        total_requests += 1
        time.sleep(0.2)
    # Start from a reasonable ID and iterate until max_requests is reached
    billboard_id = 1000000

    while total_requests < max_requests:
        data = fetch_billboard_details(billboard_id)
        if data and "latitude" in data and "longitude" in data:
            lat, lon = data["latitude"], data["longitude"]
            if is_in_montana(lat, lon) and data.get("panelID") not in existing_entries:
                billboard_entry = {
                    "panelID": data.get("panelID"),
                    "latitude": lat,
                    "longitude": lon,
                    "location": data.get("location"),
                    "weeklyImpressions": data.get("weeklyImpressions"),
                    "mediaTypeStyle": data.get("mediaTypeStyle"),
                    "cost": data.get("cost")
                }
                existing_entries.add(data.get("panelID"))
                save_to_file(billboard_entry, output_file)
            else:
                print(f"Billboard {billboard_id} at {lat}, {lon} is outside Montana or already exists")
        total_requests += 1
        billboard_id += 1
        time.sleep(0.2)

    elapsed_time = time.time() - start_time
    print(f"Completed extraction in {elapsed_time:.2f} seconds.")

def main():
    print("Starting billboard data extraction with rate limiting and traffic disguise...")
    extract_billboards()
    print("Extraction complete.")

if __name__ == "__main__":
    main()