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