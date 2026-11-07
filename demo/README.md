# Apartment hunting with Grokbot

[Watch the demo](apartment-hunt.mp4).

A 28.73-second editorial workflow film backed by a real, persisted run of this instruction skill on fictional inputs. It is a graphical presentation, not a recording of a housing app. Grokbot assisted the original Padova search; this present demo was processed with the portable skill by GPT-6.1 Sol in Codex / T3 Code. No Grokbot integration or historical actions are implied.

The demonstration reads [the existing fictional example](../examples/padova-demo.md), preserves its source quotes in [typed input](input/normalized.json), and writes a [shortlist](output/shortlist.md), [JSON](output/shortlist.json), and [GeoJSON](output/shortlist.geojson). [Provenance](provenance.json) records the method, source hashes, and limits. No example.com page was browsed. Those URLs are fixture identifiers.

## The decision

Against a EUR 600 all-in monthly budget and a private-room requirement:

- Centro: EUR 470 + EUR 80 covering all bills = EUR 550. Fits the stated requirements; availability still needs confirmation.
- Arcella: EUR 430 + unknown required bills. Known minimum EUR 430; all-in total, bills, and deposit remain `null`. Confirm costs/details. A lower base rent does not make it a confirmed better deal.
- Portello: EUR 520 + EUR 110 = EUR 630 all-in. Over budget.

Centro's EUR 940 refundable deposit stays separate. Its first month plus deposit is EUR 1,490, a known move-in minimum because one-time fees are unstated. An unstated cost is never treated as a quoted zero. Only Centro has source-supported coordinates, at neighborhood precision. The film's map is schematic; its pin illustrates the saved GeoJSON and does not imply a precise address. The GeoJSON includes an OpenStreetMap link. Neither of the other rooms is pinned.

## Reproduce

The normalized input was extracted by the agent from the preserved source text. The Python script computes costs and classifications from those fields; it is a bounded demo, not an automatic natural-language parser, a scraper, or the implementation of an agent runtime.

```sh
python3 demo/scripts/process.py
python3 demo/scripts/process.py --check
```

Rendering needs Python 3.9+, Pillow, ffmpeg, and Arial regular/bold TrueType fonts. Pillow is used only for this editorial presentation. Use your existing installation; this repo has no runtime package dependencies for the skill itself.

```sh
python3 demo/scripts/render.py --music /path/to/house-original.mp3 --output /path/to/demo.mp4
python3 demo/scripts/qa.py /path/to/demo.mp4 /path/to/qa
```

`--font-dir` overrides the default macOS supplemental font directory; supply `Arial.ttf` and `Arial Bold.ttf`. Fonts and music are not bundled. The final 1.30 MB MP4 is included for viewing; raw frames, source music and private QA are kept outside the repository. Scripts use only local files and ffmpeg; they make no network requests. QA verifies H.264/yuv420p, 1080 square, 30 fps, AAC 48 kHz, size under 15 MB, full decoding, audio peak, and faststart, then extracts encoded frames and a 1 fps contact sheet for visual review.

## Music and edit

The cut reuses `house-original.mp3`, an existing AI-generated ElevenLabs Music v2.5 instrumental obtained through Higgsfield (job `66d512b0-e91e-4f08-9b3d-0e00b496926c`). Source SHA-256: `d0a355b9eaf1af9c5d74589215a6b74b7a8e5f43e4edddbf60bd6420cca4e2a1`. No new music was generated or purchased. The render trims this source, normalizes loudness, fades the ends, and encodes AAC. Main scene changes follow measured source kick onsets at 3.6369, 7.2160, 12.5874, 17.9675, 20.6489, and 25.1272 seconds, rounded by the 30 fps frame grid. Crossfades last 0.16 seconds. This is numerical alignment; the agent does not claim to have listened.

The original provider terms govern reuse; this work makes no ownership, licensing clearance, or content-ID claim. Supply a suitable licensed track if sharing under different terms. Music is optional to understanding the story, which is fully captioned.

## Verification

[Encoded-media verification](verification.json) records the final hash and technical checks. Madeye’s `claude-haiku-4-5` vision API passed privacy, readability, story and disclosure on seven actual encoded frames plus a 1 fps contact sheet. This is sampled still-frame evidence, not a claim of continuous playback or listening.

## Scope and limits

No personal listings, contacts, exact addresses, private photos, browsing, agent chats, landlord messages, or availability checks are included. The source-backed cost comparison is the evidence; the film is a presentation of it. Still-frame visual review cannot prove audio quality or continuous motion. This demo neither changes the separately synced canonical skill nor connects the separate Padova Rooms app.
