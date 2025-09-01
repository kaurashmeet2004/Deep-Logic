from flask import Flask, jsonify
import urllib.request
import re

app = Flask(__name__)

def get_latest_stories():
    # Fetch the HTML from Time.com
    url = "https://time.com"
    response = urllib.request.urlopen(url)
    html = response.read().decode("utf-8")

    # Regex to capture story links and titles
    # Stories are usually inside <a href="/<something>">Title</a>
    pattern = r'<a[^>]*href="(/[\d]+/[^"]+)"[^>]*>(.*?)</a>'
    matches = re.findall(pattern, html)

    stories = []
    seen = set()

    for link, title in matches:
        # Remove nested tags and trim
        clean_title = re.sub(r"<.*?>", "", title).strip()

        if clean_title and link not in seen:
            stories.append({
                "title": clean_title,
                "link": "https://time.com" + link
            })
            seen.add(link)

        if len(stories) == 6:  # Only keep 6 latest stories
            break

    return stories


@app.route("/getTimeStories", methods=["GET"])
def get_time_stories():
    try:
        stories = get_latest_stories()
        return jsonify(stories)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
