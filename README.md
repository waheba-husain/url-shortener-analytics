# URL Shortener analytics

A simple URL shortener built with FastAPI, SQLite, and SQLAlchemy.

## Features

- Shorten long URLs into compact, shareable links using base62 encoding
- Support for custom aliases (choose your own short code)
- Redirect from short code to original URL
- Click analytics (track visits to each shortened URL)

## Tech Stack

- **Backend:** FastAPI
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Frontend:** HTML/JS

## Getting Started

\`\`\`bash
# Clone the repo
git clone https://github.com/waheba-husain/url-shortener-analytics.git
cd url-shortener-analytics

# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn main:app --reload
\`\`\`

## License

MIT
