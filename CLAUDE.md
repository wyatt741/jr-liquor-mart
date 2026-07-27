# jr-liquor-mart — Project Entry

Marketing site for **JR Liquor Mart**, 2616 E Ventura Blvd Unit 106, Camarillo, CA 93010
(Old Town Camarillo, est. 1997). Phone 805-388-3288. Instagram @jrliquormart.
Built 2026-07-26 from Wyatt's `site-template` (its `PLAYBOOK.md` governs conventions).

**This IS the site's own repo** (`wyatt741/jr-liquor-mart`, public, deploy branch `master`),
split out on 2026-07-26 from `wyatt741/site-template` PR #3; the subfolder copy there was
later removed from site-template `main` (commit 396aa40, "Move jr-liquor-mart out to its
own repo"), so THIS repo is the sole home. GitHub Pages serves `master` root (LIVE at
https://wyatt741.github.io/jr-liquor-mart/); custom domain `jrliquormart.com` is still
unregistered, so `CNAME` is parked as `CNAME.hold` (rename back once DNS points at Pages).

## The one rule
Edit content in `build.py`, run `python3 build.py`, never hand-edit the generated `.html`.
House style: no em dashes in copy or chat, no fabricated content. Every factual claim on the
site traces to `docs/RESEARCH_BRIEF.md` (sourced) or the owner. Reviews are verbatim public
quotes; bracketed letters mark corrected typos only.

## Files
| Path | What |
|---|---|
| `build.py` | THE generator (works on Python 3.11+). CONFIG + content data at top. |
| `styles.css` | Theme v2 rethemed: "black and tan" dark default, amber/bourbon accents (`--pink` slots hold amber `#e2a33d`/`#9a6410`), Fraunces display + Plus Jakarta Sans. `?v=1`. |
| `app.js`, `chat.js` | Template JS. `chat.js` is in HYBRID AI mode: `WORKER_URL = https://chat.jrliquormart.com`, canned answers as automatic fallback (bot works before the worker deploys). `?v=1`. |
| `worker/` | Cloudflare Worker for the AI chat (filled for JR). Not yet deployed. |
| `assets/` | MIXED, credits in `LICENSES.md`: 4 real owner photos from the shop's Instagram (`sign-welcome`, `frey-ranch-rye`, `amigos-display`, `cooler-case`) + licensed Pexels/Unsplash stock + monogram favicons + `og-image.jpg` + `logo.png`. Owner photos ARE the store and may be captioned "our"; stock is CATEGORY imagery with generic captions, never presented as JR's own store. |
| `docs/RESEARCH_BRIEF.md` | The sourced research brief the whole site is built from. |
| `docs/PROJECT_STATE.md` | Status + open items. Read this to resume. |
| `CNAME.hold` | `jrliquormart.com`, parked. Rename to `CNAME` once the domain is registered and DNS points at GitHub Pages (until then a live CNAME would redirect the github.io preview to a dead domain). |

## Intake decisions (2026-07-26, confirmed with Wyatt)
- Dark default + amber bourbon palette, Fraunces display (light mode: cream + espresso).
- Layout: ONE-PAGE site (2026-07-26, Wyatt's call for mobile). index.html sections: hero,
  order band, marquee, What We Carry (6 cards: 5 categories + Delivery & Pickup), Gallery
  (licensed stock, lightbox), Why, About, Reviews, Contact + map. Old page URLs
  (services/gallery/about/contact.html) are noindexed redirect stubs into the sections;
  app.js re-anchors hash landings after the display font swaps in.
- ORDER buttons link VERIFIED delivery storefronts (checked 2026-07-26): Uber Eats and
  Postmates (listed as "JR Food Mart", shared storefront) and Grubhub ("Jr Liquor &
  Convenience"). No DoorDash storefront was found; add only with a real link from the owner.
- Reviews: 6 real verbatim quotes (3 named Yelp, 3 anonymous Google-mirror), stars per review.
- Hero badge: "Old Town Local, Est. 1997". No star-rating claims on the site.
- Marquee: category chips only (no brand names until the owner confirms a stock list).
- No order/delivery buttons (no live storefront link verified); delivery mentioned in copy only.
- Chatbot: hybrid AI worker tier. Sister shop JR Smoke Zone cross-mentioned.
- Hours shown: daily 8am-10pm (Apple Maps; only Sunday was Google-verified). Confirm with owner.

## Showing the store's real Instagram photos
**SOLVED 2026-07-26: use Apify.** Actor `data-slayer/instagram-posts`, input
`{"username":"jrliquormart","maxPages":3}`, ~$0.002/run. This is the same method that
sourced the jr-smoke-zone photos. Four photos are now live in `GALLERY` (see `LICENSES.md`
for provenance and the owner sign-off). To re-pull later, run the actor and download the
image URLs; **never hotlink** fbcdn URLs, they are signed and expire.

Hard-won details, so the next session does not redo this:
- **Direct scraping is genuinely impossible** and it is NOT an IP or datacenter problem.
  Every content endpoint returns a ~601KB login-gated JS shell, and a *known-real* post
  URL returns the identical shell (control-tested from Wyatt's own residential IP,
  2026-07-26). A fake shortcode is indistinguishable from a real one server-side, so
  codes can never be validated at build time.
- **Reels are the trap.** The actor's image field for a Reel is the grid thumbnail at only
  **360x640** (useless on a site). The real frame must be pulled from `video_url` with
  ffmpeg, which tops out at 720x1280. True photos come back at 1080px.
- Most of the account's Reels have their captions **burned into the video**, so frames from
  them are unusable no matter the resolution. Sampling frames at 15/50/85% of the clip does
  not help; the text sits there the whole way through.
- The actor emits ~586 fields per item. Request only what you need, and expect the MCP
  result to overflow to a file on disk (that is normal and convenient: parse it with Python
  rather than pulling it through context).
- Only use posts **authored by** @jrliquormart; discard posts by others that merely tag the
  shop. **No employee faces** (Wyatt, 2026-07-26).

Still valid alternatives:
1. **Owner sends files** (or Instagram > Settings > Your activity > Download your
   information, which returns every post at full resolution). Best quality by far, and the
   only route to the shots the account simply does not have.
2. **Official embeds (built, currently dormant)**: paste post URLs into `IG_POSTS` in
   `build.py` (Instagram app > Share > Copy Link). Empty list = the section does not
   render and IG's script never loads; app.js lazy-loads `embed.js` only when the section
   nears the viewport. Never guess shortcodes: a wrong one renders "Sorry, this page
   isn't available" to visitors and cannot be caught at build time.

## Gallery tile aspect ratios (bit us once)
Tiles are `4/3 object-fit:cover`, except `.gal-masonry .tile:nth-child(7n+1)` which is
`4/5` portrait. A source image whose ratio differs gets **centre-cropped**, which silently
cuts content off the edges: `sign-welcome.jpg` at 1080x940 had the `@JRLiquorMart` line
sliced in half. Either pre-crop the file to exactly 4:3, or put a tall image in a `7n+1`
slot (position 1 or 8), which is why `frey-ranch-rye.jpg` is tile 1.

## Launch blockers (owner/Wyatt input needed)
0. ~~Enable GitHub Pages~~ DONE. Live and serving 200 (re-verified 2026-07-26).
1. **Contact inbox**: `EMAIL` in `build.py` + `LEAD_URL` in `chat.js` are pending
   (`EMAIL_READY = False` hides email on the pages; the form will not deliver until the real
   lowercase inbox is set and FormSubmit's activation link is clicked).
2. **Domain**: register `jrliquormart.com`, point DNS at GitHub Pages, then rename
   `CNAME.hold` back to `CNAME`.
3. **Worker deploy** (chat AI): `cd worker && wrangler login && wrangler secret put
   ANTHROPIC_API_KEY && wrangler deploy`; once DNS is on Cloudflare, uncomment the
   `chat.jrliquormart.com` route block in `wrangler.jsonc` (PLAYBOOK §6). Set a spend cap.
4. **Owner photos**: PARTLY DONE. Four real photos from the shop's Instagram are in the
   gallery (2026-07-26, owner-approved). The account has **nothing** for the three slots
   that matter most, so these still have to come from the owner directly:
   **storefront exterior, the Beer Cave, and the bourbon wall** — currently licensed stock
   (which is better composed than anything the account had, so do not downgrade for the
   sake of "real"). Hero and `_SVC_PHOTO` are still stock. When real shots arrive, swap the
   files and let captions say "our" (never caption stock as the real store).
   A real **logo** still does not exist anywhere public: the chalkboard in
   `sign-welcome.jpg` is real branding but hand-lettered chalk, not artwork. Ask the owner
   for a logo file or a photo of the storefront sign; the monogram stays a placeholder.
5. **Verify hours + Google review count with the owner** before wider promotion; there is
   also a Google-listing item to raise with the owner (see the untracked local research
   brief, `docs/RESEARCH_BRIEF.md`).

## QA gate (must pass before any push, PLAYBOOK §11)
Playwright: every page at 1440x900 + 430x932, dark AND light, assert
`document.documentElement.scrollWidth <= viewport`, exercise theme toggle, hamburger,
gallery filters/lightbox, chat, callbar. Passed clean on 2026-07-26 (20/20 combos).
Mobile extras (also passed 2026-07-26): overflow at 320/360/390 too, 44px tap targets,
16px inputs (no iOS focus zoom), safe-area insets on the callbar/chat lift, footer
clears the fixed callbar at full scroll.
Note for remote sessions: the sandboxed browser cannot reach fonts.googleapis.com; route
font requests to locally curl-downloaded copies (see PROJECT_STATE).

## ⚠️ THIS IS A PUBLIC REPO
`wyatt741/jr-liquor-mart` is **public** (it has to be — GitHub Pages serves the live site
from it on a free plan). Therefore **`docs/` is gitignored and stays Mac-only**, same
convention as `jr-smoke-zone`: the research brief and session-state docs hold internal
consulting notes about a real client (competitor scan, negative-review analysis explicitly
marked "not for the site", Google-listing findings) and must never be pushed here.
**Never put client-confidential notes in any tracked file**, including this one. The
cross-machine handoff lives in the ⭐ block below, which is written to be safe if read by
anyone. (History was rewritten on 2026-07-26 to purge `docs/` and one such note; see the
local state doc.)

## ⭐ LATEST SESSION — 2026-07-26
Local detail (untracked): `docs/SESSION_STATE_2026-07-26.md`.

Pulled the shop's own Instagram via the Apify actor `data-slayer/instagram-posts` and put
**four real owner photos** into `GALLERY`, replacing stock (owner approved; provenance in
`LICENSES.md`). Only 4 of 12 posts were usable: the rest are Reels with captions burned
into the video whose API thumbnails are only 360x640. Direct Instagram scraping is
impossible for any non-browser client and is NOT an IP problem (control-tested).
Commits `16b2982`, `367e13c`; both live and verified.

**Gotchas:** gallery tiles are `4/3 object-fit:cover` and silently centre-crop — that
sliced the `@` handle off the sign photo until it was pre-cropped to exactly 4:3. The
browser pane screenshots this page all-black (it is ~8000px tall); measure the DOM and
simulate the crop in PIL instead.

**Later the same evening (commits `7088feb`, `9631bce`), all shipped and live:**
- **Repo made safe:** `docs/` is gitignored/untracked (this is a public repo) and a client
  note was scrubbed from this file. ❗**Unfinished: the git history still contains both** —
  31 blobs, plus old `docs/` blobs reachable by SHA. A `git filter-repo` rewrite + force
  push of `master` and `main` is pending **Wyatt's** decision (the classifier blocks the
  agent from running it). Making the repo private was rejected: on GitHub Free that
  unpublishes Pages and takes the live site down.
- **Beer Cave photo replaced** — `beer-cooler.jpg` (washed-out Budweiser in a domestic
  fridge) → **`beer-cave.jpg`, AI-generated**, pre-cropped to exactly 4:3. See `LICENSES.md`.
- **Delivery links added to Contact** as plain text links in a `cside-card`, deliberately
  not a second pill cluster (the merge audit cut duplicates for repetition).
- **Nav scrollspy shipped** (`app.js?v=4`). ⚠️ It failed its first test because the browser
  pane runs `visibilityState:"hidden"`, where **rAF and scroll events are suspended**. It
  now calls its handler straight from the scroll listener; to test it in the pane you must
  `dispatchEvent(new Event('scroll'))` by hand.

- **Mobile + SEO audit passed clean** (`85ed979`): Lighthouse mobile **Accessibility 100,
  SEO 100, Best Practices 100, Agentic Browsing 100, 0 failures**; **CLS 0.00**, LCP ~1.07s;
  zero horizontal overflow 320-1440. Fixed a skipped heading level (footer `h5`→`h4`), a
  WCAG 2.5.3 failure on the brand link (the monogram repeats the wordmark, so the visible
  text was "JRJR Liquor Mart" and no longer matched the aria-label — monogram is now
  `aria-hidden`), 41px gallery filters → 44px, and a 168-char meta description → 155.
  `styles.css?v=9`.
  ⚠️ **Do not "fix" these without re-measuring:** the 18 images have no `width`/`height`
  attributes but CLS is already **0.00** (CSS `aspect-ratio` reserves the space), and font
  preconnects already exist with render-blocking savings measured as "none". Also, at
  *desktop* width one input computes to 14.88px and looks like the iOS focus-zoom bug — it
  is not; the 16px rule is in a mobile media query and no input is under 16px on a phone.

- **Copy sweep + hero CTAs removed** (`601a85a`). "Call the store" and "See what we carry"
  are gone from the hero (the call action lives in the nav CTA and the mobile callbar; the
  order pills are now the hero's only action). "Free parking" was in **three** places and
  was cut from the hero and the Delivery card — but **deliberately kept in the chatbot**,
  where the "parking" keyword routes to that answer, so it responds to a question rather
  than volunteering an assumed fact; don't delete it there. The gallery subhead no longer
  exposes internal stock-photo housekeeping, and it describes the **shop, not the photos**
  on purpose — the per-tile captions ("Our spirits case" vs "Backlit bottles") are what
  keep stock from being passed off as the real store. Also fixed two stale facts: `chat.js`
  pointed at a "contact page" that has not existed since the one-page conversion
  (`chat.js?v=3`), and the `build.py` docstring still listed the deleted marquee/Why
  sections.

- **Bug hunt** (`2e5b002`, `eabbc01`, `c8dec37`). Console is now clean; Lighthouse still
  100/100/100/100. Audited and PASSING: every anchor/link, the 4 redirect stubs, gallery
  filter, lightbox, theme toggle + persistence, mobile menu, and the chat sending and
  receiving. Three real defects fixed:
  1. ❗**The contact form silently discarded messages.** It rendered unconditionally with
     `action="formsubmit.co/inbox@example.com"` — `EMAIL_READY` only ever hid the footer
     mailto, never the form. FormSubmit will not deliver to an unconfirmed address and
     `example.com` is IANA-reserved, so a real customer's message just vanished. The form
     is now behind `contact_form()` and gated on `EMAIL_READY`, showing a call/text panel
     instead. **Set a real lowercase `EMAIL`, click FormSubmit's activation, flip
     `EMAIL_READY = True`, and the form returns** (with the `autocomplete` attributes it
     was missing). Judgement call: a live form that eats messages is worse than no form.
  2. The chat said "In the live site this sends straight to us" *on* the live site.
     Reworded. `chat.js?v=4`. That phrase still appears **as a code comment** — a grep
     hit there is expected, not a regression.
  3. **`<title>` and `og:title` are now DIFFERENT on purpose** — `head(..., social_title=)`.
     `<title>` carries keywords for search (`Bourbon, Beer Cave & Wine in Camarillo, CA`);
     the share card shows the clean `JR Liquor Mart | Camarillo, CA`. Don't "unify" them.
  Not bugs: `sms:` links, the chat widget's `autocomplete="off"`, and `WORKER_URL` failing
  to resolve (by design — the canned answers take over until the domain and worker exist).

**Asset versions:** `styles.css?v=9` · `app.js?v=4` · `chat.js?v=4`. Bump on ANY change to
that file; a copy-only `build.py` edit needs no bump.

**NEXT:** decide on the history rewrite (the only open technical item), then the
owner-dependent launch blockers below. The site itself needs no further technical work.

## Resume
Say `resume jr-liquor-mart`. Read the ⭐ block above, then (on this Mac only)
`docs/SESSION_STATE_2026-07-26.md` and `docs/PROJECT_STATE.md`, which are untracked.
Template conventions: the site-template repo's PLAYBOOK.
