from flask import Flask, request, render_template
import hashlib
from bs4 import BeautifulSoup
import requests
import psycopg2

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form.get('url')
        is_valid_url = url.startswith('http://') or url.startswith('https://')
        #  if not is_valid_url: show error

        # Fetch the page title
        title = fetch_page_title(url)

        # Shortened the URL
        shortened_url = shorten_url(url)

        # Save the shortened URL to the database
        conn = create_conn()
        save_shortened_url(url, shortened_url, conn)

        # Get top 100 URLs from the database
        top_100_urls = get_top_100(conn)
        print(top_100_urls)

        conn.close()

        return render_template('result.html', title=title, urls=top_100_urls,  original_url=url, shortened_url=shortened_url)
    else:
        return render_template('index.html')


def shorten_url(url):
    # Create a hash of the URL
    url_hash = hashlib.md5(url.encode()).hexdigest()

    # Use the first few characters of the hash as the short code
    short_code = url_hash[:6]

    # Return the short URL
    return 'http://rt.com/' + short_code


def fetch_page_title(url):
    # Send a GET request to the page
    response = requests.get(url)

    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the title
    title = soup.title.string

    # Return the title
    return title


"""
    Database functions
"""


def create_conn():
    conn = psycopg2.connect(
        host="localhost",
        database="test",
        user="romantolmachev",
        password="admin"
    )
    return conn


def save_shortened_url(original_url, shortened_url, conn):
    cur = conn.cursor()
    try:
        cur.execute("""
                INSERT INTO shortened_url (shortened_url, original_url)
                VALUES (%s, %s)
                ON CONFLICT (shortened_url) DO UPDATE SET counter = shortened_url.counter + 1
            """, (shortened_url, original_url))
        conn.commit()
    except Exception as e:
        print(f'Error while inserting the row: {e}')
        conn.rollback()


def get_top_100(conn):
    # Assuming that conn is a psycopg2 connection
    cur = conn.cursor()
    cur.execute("SELECT * FROM shortened_url ORDER BY counter DESC LIMIT 100")
    rows = cur.fetchall()
    return rows
