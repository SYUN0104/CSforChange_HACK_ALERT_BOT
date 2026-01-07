import requests
import re
import time

def clean_html_tags(text):
    """
    Removes HTML tags (<...>) included in a string.
    Example: "<span>$100</span>" -> "$100"
    """
    if not text:
        return "0"
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text).strip()

def get_hackathons_via_api(num_pages=1):
    base_url = "https://devpost.com/api/hackathons"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    all_hackathons = []
    
    print(f"🔄 Starting API Request: Fetching a total of {num_pages} page(s).\n")

    for page in range(1, num_pages + 1):
        print(f"   📡 Receiving data for Page {page}...")
        
        params = {
            'open_to[]': 'public',
            'order_by': 'recently-added',
            'page': page
        }

        try:
            response = requests.get(base_url, headers=headers, params=params)
            
            if response.status_code != 200:
                print(f"   ⚠️ Request Failed (Status: {response.status_code})")
                continue
            
            data = response.json()
            hackathon_list = data.get('hackathons', [])
            
            if not hackathon_list:
                print("   ⚠️ No more data available.")
                break

            for item in hackathon_list:
                try:
                    # (1) Hyperlink
                    url = item.get('url', 'N/A')
                    
                    # (2) Image Link
                    thumbnail = item.get('thumbnail_url', 'No Image')
                    if thumbnail and thumbnail.startswith("//"):
                        thumbnail = "https:" + thumbnail
                        
                    # (3) Title
                    title = item.get('title', 'No Title')
                    
                    # (4) Status
                    status = item.get('time_left_to_submission', 'N/A')
                    
                    # (5) Location
                    location_obj = item.get('displayed_location', {})
                    location = location_obj.get('location', 'Online') if location_obj else 'Online'
                    
                    # (6) Prize Breakdown (Modified Section) =========================
                    # 6-1. Prize Amount (Strip HTML tags)
                    raw_prize_amount = item.get('prize_amount', '0')
                    prize_amount = clean_html_tags(raw_prize_amount)
                    
                    # Get prizes_counts dictionary
                    counts_dict = item.get('prizes_counts', {})
                    if not counts_dict: counts_dict = {}

                    # 6-2. Prize Cash (Convert to int)
                    prize_cash = int(counts_dict.get('cash', 0))
                    
                    # 6-3. Prize Other (Convert to int)
                    prize_other = int(counts_dict.get('other', 0))
                    # ========================================================
                    
                    # (7) Host
                    host = item.get('organization_name', 'Unknown')
                    
                    # (8) Period
                    period = item.get('submission_period_dates', 'N/A')
                    
                    # (9) Theme
                    themes_list = item.get('themes', [])
                    themes = [t['name'] for t in themes_list if 'name' in t]
                    
                    # Save results (storing separate key values)
                    all_hackathons.append({
                        'title': title,
                        'url': url,
                        'thumbnail': thumbnail,
                        'status': status,
                        'location': location,
                        'prize_amount': prize_amount, # Modified
                        'prize_cash': prize_cash,     # Added
                        'prize_other': prize_other,   # Added
                        'host': host,
                        'period': period,
                        'themes': themes
                    })
                    
                except Exception as parse_err:
                    print(f"   ⚠️ Error during data parsing: {parse_err}")
                    continue
            
            time.sleep(2)

        except Exception as e:
            print(f"   ❌ Communication error occurred: {e}")
            break
            
    return all_hackathons

# --- Execution and Testing ---
if __name__ == "__main__":
    TARGET_PAGES = 1
    
    results = get_hackathons_via_api(num_pages=TARGET_PAGES)
    
    print(f"\n✅ [Verification Result] Collected a total of {len(results)} items via API.")
    
    if len(results) > 0:
        for i, item in enumerate(results, 1):
            print("\n" + "="*20 + f" [No.{i} API Data Details] " + "="*20)
            print(f"1. Title       : {item['title']}")
            print(f"2. Link        : {item['url']}")
            print(f"3. Image       : {item['thumbnail']}")
            print(f"4. Status      : {item['status']}")
            print(f"5. Location    : {item['location']}")
            
            # Modified output section
            print(f"6-1. Prize Amt : {item['prize_amount']}")
            print(f"6-2. Cash Cnt  : {item['prize_cash']}")
            print(f"6-3. Other Cnt : {item['prize_other']}")
            
            print(f"7. Host        : {item['host']}")
            print(f"8. Period      : {item['period']}")
            print(f"9. Themes      : {item['themes']}")
            print("="*60)