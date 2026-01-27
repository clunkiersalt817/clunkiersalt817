import requests
import re
import os

CREDLY_USER = "kshitiz-sharma.e63cbb0f"
CREDLY_URL = f"https://www.credly.com/users/{CREDLY_USER}/badges.json"
README_PATH = "README.md"
START_MARKER = "<!--START_SECTION:badges-->"
END_MARKER = "<!--END_SECTION:badges-->"

def fetch_badges():
    try:
        response = requests.get(CREDLY_URL)
        response.raise_for_status()
        data = response.json()
        return data['data']
    except Exception as e:
        print(f"Error fetching badges: {e}")
        return []

def generate_html(badges):
    html_parts = [START_MARKER]
    
    # Sort badges if needed, currently taking latest
    # Credly API returns them, usually newest first. 
    # We can take top 5 or all. Let's take data directly.
    
    for badge in badges:
        image_url = badge.get('badge_template', {}).get('image_url')
        badge_id = badge.get('id')
        badge_name = badge.get('badge_template', {}).get('name')
        
        # Construct public badge URL
        # Format often: https://www.credly.com/badges/{id}
        badge_link = f"https://www.credly.com/badges/{badge_id}"
        
        # Replace image size in URL if possible to get a better optimized image 
        # (Credly images often have /size/110x110/ in path if resized, but source is clean)
        # We will use the source or default URL and force height in HTML.
        
        if image_url:
            html_parts.append(
                f'<a href="{badge_link}" target="_blank">'
                f'<img src="{image_url}" height="110" alt="{badge_name}">'
                f'</a>'
            )
            
    html_parts.append(END_MARKER)
    return "\n".join(html_parts)

def update_readme(new_content):
    if not os.path.exists(README_PATH):
        print(f"{README_PATH} not found.")
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex to replace content between markers
    pattern = re.compile(
        f"{re.escape(START_MARKER)}.*{re.escape(END_MARKER)}",
        re.DOTALL
    )
    
    if not pattern.search(content):
        print("Markers not found in README.md")
        return

    updated_content = pattern.sub(new_content, content)
    
    if updated_content != content:
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print("README.md updated successfully.")
    else:
        print("No changes needed.")

if __name__ == "__main__":
    badges = fetch_badges()
    if badges:
        html_content = generate_html(badges)
        update_readme(html_content)
    else:
        print("No badges found or API error.")
