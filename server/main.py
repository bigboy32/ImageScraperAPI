from flask import *

from bs4 import BeautifulSoup as soup
import urllib.request as urllib

app = Flask(__name__)

@app.route("/")
def shift_to_api():
    return redirect("/api")

@app.route("/api")
def render_usage():
    return """<center>
    <h1>API</h1><br>
    <p>Get to: /api/ImageScraper?url=URL_HERE<br>Example: http://sampleapp.com/api/ImageScraper?url=https://www.google.com/</p>
</center>"""

@app.route("/api/ImageScraper")
def extract_images():
    try:
        url = request.args.get("url")
        assert url != "" and url != None
    except:
        return "<h1>Invalid URL Parameter</h1>"
    
    if list(url)[len(list(url)) - 1] == "/":
        lurl = list(url)[0:len(list(url))-2]
        url = ''.join(lurl)

    try:
        html_page = urllib.urlopen(url)
        sp = soup(html_page)

        return_list = {
            "images":[]
        }

        for img in sp.findAll('img'):
            src = img.get('src')

            if list(src)[0] == "/":
                return_list["images"].append(url + src)

        return jsonify(return_list)

    except urrlib.Error.HTTPError:
        return "<h1>Cannot GET Page! (Either forbidden or non-existent)</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5080", debug=True)