# Apartment Hunt

A reusable agent skill for comparing rentals without hiding unknown bills. It grew out of Harssha's Grokbot-assisted Padova room search. Grokbot gets credit for the original workflow; this repo packages a portable version.

Choose your city, currency and all-in budget. Give your agent listing links, screenshots or pasted text. The skill builds a source-backed shortlist, keeps missing costs visible and prepares map data only for supported locations.

## Install

Copy this folder into your agent's skills directory as `apartment-hunt`. For a shared Mac/Linux setup, use `~/.agents/skills/apartment-hunt`.

Ask: `Use apartment-hunt to compare these rooms against my all-in monthly budget.`

## Demo

[Three fictional Padova listings and the expected shortlist](examples/padova-demo.md). A EUR 550 all-in room fits a fictional EUR 600 budget. A EUR 430 room with unknown bills stays unconfirmed. A EUR 630 room is over budget. [GeoJSON example](examples/demo-shortlist.geojson) includes one approximate neighborhood pin.

A [reproducible launch demo](demo/README.md) processes those fictional sources into persisted Markdown, JSON and GeoJSON. Its graphical workflow presentation makes missing bills, separate deposits and approximate pins explicit.

This is an instruction skill. It uses the browsing and file tools available to your agent; it does not bundle a scraper, browser session, tracker backend or landlord messaging service. The original Padova Rooms app is separate and remains Padova-specific.

MIT licensed.
