# Web Automation Lab - BookNook

A resilient web automation project built for the AI-Assisted Development Internship. This repo contains two connected pieces:

1. **BookNook** - a local sandbox bookstore listing site with a configurable "chaos engine" that can simulate 8 real-world disruptions on command.
2. **A Playwright bot** - searches the site, opens book results, completes a "Request to Borrow" workflow, and survives every disruption the chaos engine throws at it.

## Requirements

- Python 3.10+
- Git

## Setup

1. Clone the repo:
git clone https://github.com/AyselHaya/web-automation-lab.git
cd web-automation-lab

2. Create and activate a virtual environment:
python -m venv venv
venv\Scripts\Activate

3. Install dependencies:
pip install -r requirements.txt
playwright install

## Running the sandbox site
cd sandbox_site
python app.py

Open `http://127.0.0.1:5000` in your browser. The site works normally - search, browse, click into books, and "Request to Borrow."

### Controlling chaos

Edit `sandbox_site/chaos.json` to toggle any of the 8 disruption scenarios on/off, or adjust their probability:
"popup": { "enabled": true, "probability": 1.0 }

Set `"enabled": false` to turn a scenario off entirely. `"probability"` controls how often it triggers (1.0 = always, 0.3 = ~30% of the time).

## Running the bot

With the sandbox site running in one terminal, open a second terminal:
venv\Scripts\Activate
cd bot
python run.py

A real Chromium browser window will open and the bot will search for books, open the top 3 results, complete the borrow flow on each, and survive whatever disruptions are currently enabled in chaos.json. A run summary prints in the terminal and a full JSON log plus screenshots are saved to runs/.

## Running the tests

From the project root, with the sandbox site running:
pytest tests/ -v -s

This runs:
- **Unit tests** - resilience logic (error detection, backoff calculation) and dummy data validation
- **Scenario tests** - one test per core disruption scenario, confirming the bot completes its workflow under each
- **The chaos gauntlet** - all 8 scenarios enabled simultaneously, confirming the bot still completes successfully

## Project structure
web-automation-lab/
docs/
PLANNING.md - project spec, scenario list, architecture
SCENARIOS.md - the scenario coverage matrix (key deliverable)
AI_LOG.md - how AI was used throughout the project
screenshots/ - evidence screenshots for each scenario
sandbox_site/
app.py - Flask server plus chaos injection logic
chaos.json - per-scenario toggles and probabilities
data/items.json - dummy book data
templates/ - listing, detail, captcha, promo pages plus alt layout
bot/
run.py - bot entry point
bot_selectors.py - all selectors, with fallback chains for DOM drift
reporting.py - logging, screenshots, run summaries
handlers/ - one module per disruption category
tests/ - unit tests, scenario tests, chaos gauntlet
requirements.txt

## Known limitations

- The bot's search workflow is fixed to searching "Fiction" - not yet configurable via command line.
- The captcha handler solves riddles by reading a hidden form field rather than genuinely inferring the answer (an intentional simplification for a simulated challenge, not a real CAPTCHA bypass).
- Some chaos scenarios can compound in edge cases (e.g. a redirect immediately followed by a new captcha); the bot's recovery loop handles this but it can occasionally take a few extra cycles.

## Demo

Demoed live in the final call.