# AI Usage Log

## Entry 1 — Generating dummy book data
**What I was doing:** Creating 20-30 dummy book entries for the sandbox site's items.json.
**Tool & approach:** Used Claude, asked it to generate books matching my BookNook theme with id, title, author, genre, price, rating, description fields.
**What it got right / wrong:** Got the structure and field consistency right on the first try (id, title, author, genre, price, rating, description). Kept genres varied and added recurring authors across multiple books for a bit of realism.
**What I learned:** Generating structured dummy data this way is much faster than writing it by hand, and having a consistent tone across entries makes the demo feel more polished.
## Entry 2 — Building the Flask listing site
**What I was doing:** Building the Flask app, listing page, and detail page with search/pagination.
**Tool & approach:** Used Claude to generate the initial app.py and templates, then ran and tested each route myself before moving on.
**What it got right / wrong:** Structure and Jinja templating worked correctly on first try; verified search and pagination logic manually in the browser.
**What I learned:** Testing each piece (listing, search, detail, borrow flow) immediately after building it — rather than writing everything then testing at the end — made it much easier to know exactly what was working.
## Entry 3 — Building the chaos engine and popup scenario
**What I was doing:** Designing chaos.json config structure and wiring in the first scenario (popup/modal).
**Tool & approach:** Used Claude to design the config schema and scenario_active() helper function, then implemented the popup HTML/logic myself and tested toggling it on/off.
**What it got right / wrong:** Initial code had an indentation mismatch when I added a new line manually — a good reminder that Python is strict about consistent spacing, unlike VB.
**What I learned:** Testing the on/off toggle immediately after building confirms the chaos config actually controls behavior, not just that the code runs without errors.
## Entry 4 — Cookie banner scenario
**What I was doing:** Adding the second chaos scenario (cookie/consent banner) using the same pattern as the popup.
**Tool & approach:** Reused the established pattern (chaos.json flag → app.py check → template conditional) with Claude's guidance, implemented and tested independently.
**What it got right / wrong:** Went smoothly since the pattern was already established from scenario 1 — no errors this time.
**What I learned:** Having a consistent pattern for wiring in scenarios makes each new one faster to build and test than the last.
## Entry 5 — Theming popup and cookie banner
**What I was doing:** Reworking the popup and cookie banner scenarios to fit the BookNook theme instead of generic copy.
**Tool & approach:** Used Claude to draft in-universe copy and dynamic book title logic (random.choice from loaded data).
**What it got right / wrong:** Worked correctly first try; made the popup feel like part of the actual site instead of a generic template.
**What I learned:** Small thematic touches like this cost almost no extra time but make the demo feel like a real product, not just a checklist of required features.
## Entry 6 — Captcha gate scenario
**What I was doing:** Building the simulated captcha scenario as a knowledge-neutral riddle gate.
**Tool & approach:** Initially built it as "guess the book title from its description," but caught that this was illogical for a first-time visitor who wouldn't know the book yet — redesigned it as a generic riddle instead.
**What it got right / wrong:** First version had a real logic flaw (asking users to already know what they were trying to discover). Also hit a subtle bug where seeding the shared random generator for chaos probability checks accidentally locked in the next random pick too, making the riddle repeat — fixed by giving chaos rolls their own isolated random instance.
**What I learned:** Good design critique doesn't just come from AI — catching that the captcha logic didn't make sense from a user's perspective was something I noticed myself, not something Claude flagged. Also learned that sharing one random generator across unrelated features can cause invisible bugs.
## Entry 7 — Server error scenario + probability fix
**What I was doing:** Adding the site-down/server-error scenario, which needed probability-based triggering rather than always-on.
**Tool & approach:** Realized manual mode's original always-on behavior didn't make sense for a scenario meant to happen "sometimes" — updated scenario_active() to respect probability in all modes, not just random mode.
**What it got right / wrong:** Initial chaos engine design assumed manual mode = always-on, which worked fine for popup/banner but broke down for a scenario that needs to be intermittent even during manual testing.
**What I learned:** Some scenarios are naturally binary (a banner is either showing or not) while others are inherently probabilistic (a server doesn't fail 100% of the time) — the chaos engine needed to support both properly, not just one pattern.
## Entry 8 — Slow response scenario
**What I was doing:** Adding random delay injection for the slow response/timeout scenario.
**Tool & approach:** Reused the probability-based pattern from server_error, added a time.sleep() call with a randomized duration range from chaos.json.
**What it got right / wrong:** Worked cleanly first try since the pattern was already established. Noticed that multiple independent scenarios (delay + error) can both roll on the same request mix, which is actually realistic — real flaky servers show a mix of symptoms, not one at a time.
**What I learned:** Building scenarios as independent, composable checks (rather than one big if/elif chain) means they naturally combine in realistic ways without extra work.
## Entry 9 — Redirection scenario
**What I was doing:** Adding the unexpected redirection scenario — book clicks sometimes land on a promo page instead.
**Tool & approach:** Reused the established probability-check pattern, added a skip_redirect query param so the "take me back" link doesn't loop into the same promo page again.
**What it got right / wrong:** Worked cleanly first try; the skip_redirect param was an important detail to avoid an infinite redirect loop on the way back.
**What I learned:** Building the escape hatch (skip_redirect) into a chaos scenario is just as important as building the chaos itself — otherwise the sandbox becomes unusable for anyone trying to actually get past it.
## Entry 10 — DOM drift scenario
**What I was doing:** Building the DOM change/selector drift scenario — an alternate page layout for the same content.
**Tool & approach:** Created a second template with completely different tags, classes, and structure, then randomly picked between the two templates in the route based on probability.
**What it got right / wrong:** Worked cleanly first try; the key was making sure both templates receive the exact same data so only the structure differs, not the content.
**What I learned:** This scenario is a good preview of why the bot needs resilient selectors — a bot hardcoded to look for `<ul><li>` would completely break on the alt layout, even though the actual book data is identical.
## Entry 11 — Blocked click scenario (all 8 core scenarios complete!)
**What I was doing:** Building the final core scenario — a sticky overlay intercepting clicks on the borrow button.
**Tool & approach:** Positioned an absolutely-positioned overlay div directly over the button using relative/absolute CSS, toggled by the same probability pattern as other scenarios.
**What it got right / wrong:** Worked cleanly first try; the overlay genuinely blocks real clicks on the underlying button until dismissed, which is exactly the real-world pattern this scenario represents.
**What I learned:** All 8 core scenarios are now done in the sandbox. The consistent pattern (chaos.json flag → scenario_active() check → template conditional) made each successive scenario faster to build than the last — a good argument for establishing a clean pattern early rather than one-off solutions per scenario.
## Entry 12 — Happy-path bot working end-to-end
**What I was doing:** Building the core Playwright bot: search for books, open top 3 results, complete the borrow flow, log everything, produce a run summary.
**Tool & approach:** Used Claude to scaffold selectors.py, reporting.py, and run.py, hit some file-creation hiccups (files not saving properly) but resolved by creating them via terminal first, then pasting content.
**What it got right / wrong:** Worked correctly on the very first real run — no errors, all 3 items processed, screenshots and run log saved automatically.
**What I learned:** Having reporting.py as a separate, reusable module (rather than inline logging) means every future scenario handler can just call log_event() and save_screenshot() without rewriting logging logic each time.
## Entry 13 — Bot handles popup and cookie banner
**What I was doing:** Building the first two disruption handlers (popup, cookie banner) into the bot.
**Tool & approach:** Used Claude to scaffold the handler pattern (check visibility, click dismiss, wait for hidden).
**What it got right / wrong:** First attempt had the popup and cookie banner overlapping on screen, so the bot tried clicking the cookie banner's Accept button while the popup was still covering it, causing a 30-second timeout. Fixed by reordering: dismiss popup first, then cookie banner.
**What I learned:** Real disruption handling isn't just "does the code exist" — the order handlers run in matters when disruptions can visually overlap, exactly like the brief describes for real-world automation.