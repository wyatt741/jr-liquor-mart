# jr-liquor-mart — Project Entry

Marketing site for **JR Liquor Mart**, 2616 E Ventura Blvd Unit 106, Camarillo, CA 93010
(Old Town Camarillo, est. 1997). Phone 805-388-3288. Instagram @jrliquormart.
Built 2026-07-26 from Wyatt's `site-template` (its `PLAYBOOK.md` governs conventions).

**This IS the site's own repo** (`wyatt741/jr-liquor-mart`, public, deploy branch `master`),
split out on 2026-07-26 from the merged `wyatt741/site-template` PR #3 (the `jr-liquor-mart/`
folder there is a historical copy; THIS repo is the source of truth). GitHub Pages serves
`master` root once enabled in Settings; custom domain `jrliquormart.com` is still unregistered,
so `CNAME` is parked as `CNAME.hold` (rename back once the domain's DNS points at Pages).

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
| `assets/` | Licensed Pexels stock photos (credits in `LICENSES.md`) + monogram favicons + `og-image.jpg` + `logo.png`. Stock shots are CATEGORY imagery with generic captions, never presented as JR's own store. |
| `docs/RESEARCH_BRIEF.md` | The sourced research brief the whole site is built from. |
| `docs/PROJECT_STATE.md` | Status + open items. Read this to resume. |
| `CNAME.hold` | `jrliquormart.com`, parked. Rename to `CNAME` once the domain is registered and DNS points at GitHub Pages (until then a live CNAME would redirect the github.io preview to a dead domain). |

## Intake decisions (2026-07-26, confirmed with Wyatt)
- Dark default + amber bourbon palette, Fraunces display (light mode: cream + espresso).
- Pages: Home, What We Carry (5 category cards), Gallery (placeholder tiles), About, Contact.
- Reviews: 6 real verbatim quotes (3 named Yelp, 3 anonymous Google-mirror), stars per review.
- Hero badge: "Old Town Local, Est. 1997". No star-rating claims on the site.
- Marquee: category chips only (no brand names until the owner confirms a stock list).
- No order/delivery buttons (no live storefront link verified); delivery mentioned in copy only.
- Chatbot: hybrid AI worker tier. Sister shop JR Smoke Zone cross-mentioned.
- Hours shown: daily 8am-10pm (Apple Maps; only Sunday was Google-verified). Confirm with owner.

## Launch blockers (owner/Wyatt input needed)
0. **Enable GitHub Pages** (Settings > Pages > Deploy from a branch > `master` / root).
   Until this is clicked the site 404s at https://wyatt741.github.io/jr-liquor-mart/.
1. **Contact inbox**: `EMAIL` in `build.py` + `LEAD_URL` in `chat.js` are pending
   (`EMAIL_READY = False` hides email on the pages; the form will not deliver until the real
   lowercase inbox is set and FormSubmit's activation link is clicked).
2. **Domain**: register `jrliquormart.com`, point DNS at GitHub Pages, then rename
   `CNAME.hold` back to `CNAME`.
3. **Worker deploy** (chat AI): `cd worker && wrangler login && wrangler secret put
   ANTHROPIC_API_KEY && wrangler deploy`; once DNS is on Cloudflare, uncomment the
   `chat.jrliquormart.com` route block in `wrangler.jsonc` (PLAYBOOK §6). Set a spend cap.
4. **Owner photos**: licensed stock (see `LICENSES.md`) now fills every slot, og-image and
   logo.png exist. Still get real shots of the storefront, Beer Cave and bourbon wall; swap
   files in `GALLERY`/`_SVC_PHOTO`/hero/about and update captions to say "our" shelves
   (never caption stock as the real store). A real logo should replace the monogram.
5. **Verify hours + Google review count with the owner** before wider promotion; consider
   asking the owner about their Google listing.

## QA gate (must pass before any push, PLAYBOOK §11)
Playwright: every page at 1440x900 + 430x932, dark AND light, assert
`document.documentElement.scrollWidth <= viewport`, exercise theme toggle, hamburger,
gallery filters/lightbox, chat, callbar. Passed clean on 2026-07-26 (20/20 combos).
Mobile extras (also passed 2026-07-26): overflow at 320/360/390 too, 44px tap targets,
16px inputs (no iOS focus zoom), safe-area insets on the callbar/chat lift, footer
clears the fixed callbar at full scroll.
Note for remote sessions: the sandboxed browser cannot reach fonts.googleapis.com; route
font requests to locally curl-downloaded copies (see PROJECT_STATE).

## Resume
Read `docs/PROJECT_STATE.md`, then this file. Template conventions: `../PLAYBOOK.md`
(while in the site-template repo) or the site-template repo's PLAYBOOK.
