# Photo licenses

Two sources: the **shop's own Instagram photos** (real JR Liquor Mart, owner-approved) and
**licensed stock** for category imagery. Stock shots are CATEGORY imagery with generic
captions, never captioned as the real store; the owner photos below ARE the real store and
may be captioned as such.

## Owner photos (the shop's own Instagram)

Pulled 2026-07-26 from the shop's own public account
[@jrliquormart](https://www.instagram.com/jrliquormart/) via the Apify actor
`data-slayer/instagram-posts`, at Wyatt's direction. Only posts authored by @jrliquormart
were used. Images were **downloaded** (fbcdn URLs are signed and expire, so never hotlink).

### Owner sign-off — 2026-07-26
The shop owner has **explicitly approved** use of these images on this site (confirmed to
Wyatt, 2026-07-26). They are the shop's own published posts used for the shop's own site.

| File (assets/) | Post | Shows | Notes |
|---|---|---|---|
| `sign-welcome.jpg` | [link](https://www.instagram.com/p/DKx2xklTrcE/) | A-frame chalkboard, "Welcome to JR Liquor Mart" | 1080x810. Cropped below the `@JRLiquorMart` line to drop a Homer Simpson chalk drawing (third-party IP, not the shop's to license), then trimmed at the TOP to exactly 4:3 — the gallery tile is 4/3 `object-fit:cover`, and at the original 1080x940 that centered crop sliced the `@JRLiquorMart` line in half. Keep this file at 4:3. |
| `frey-ranch-rye.jpg` | [link](https://www.instagram.com/p/DaTilDfy1fy/) | Frey Ranch Bottled-in-Bond Rye, in-store product shot | 1080x1440, uncropped. Best of the set. |
| `amigos-display.jpg` | [link](https://www.instagram.com/p/DahHoDAMiIw/) | Amigos Tóxicos floor display + store interior | 1080x1080, uncropped. |
| `cooler-case.jpg` | [link](https://www.instagram.com/p/DIMj6VOS8f8/) | Lit spirits case (Elijah Craig visible) | 720x700. Frame from a Reel, so soft; cropped to drop a burned-in "and POS360" subtitle. Small tiles only, not a hero. |

**No employee faces** are used, per Wyatt (2026-07-26). One post in the account features a
named staff member; only a frame with no person in it was taken from it.

Not used: 8 of the 12 posts are Reels whose captions are burned into the video ("POV: you
just walked into beer heaven" etc.), and their still frames top out at 720p. Reel grid
thumbnails from the API are only 360x640, so any Reel-derived still must be extracted from
the video with ffmpeg.

## Licensed stock

Free for commercial use with no attribution required
([Pexels license](https://www.pexels.com/license/),
[Unsplash license](https://unsplash.com/license)); credited here anyway, per the PLAYBOOK
convention of recording every licensed asset.

| File (assets/) | Photographer | Source |
|---|---|---|
| beer-cooler.jpg (Unsplash; cropped to 16:10 and warm-graded to match the site palette) | wang binghua | https://unsplash.com/photos/a-refrigerator-filled-with-lots-of-bottles-of-beer-CCq5riDV9FM |

## Pexels

| File (assets/) | Photographer | Source |
|---|---|---|
| hero-shelf.jpg, og-image.jpg (crop) | Aleksandar Andreev | https://www.pexels.com/photo/bottles-of-alcohol-on-illuminated-shelf-14663635/ |
| backbar-glow.jpg | Raphael Loquellano | https://www.pexels.com/photo/bar-shelves-filled-with-bottles-8980827/ |
| back-bar.jpg | Kathrine Birch | https://www.pexels.com/photo/liquor-bottles-on-shelves-in-a-bar-15945661/ |
| backlit-bottles.jpg | Barış Karagöz | https://www.pexels.com/photo/bottles-of-alcohol-on-the-shelves-in-a-bar-17903465/ |
| top-shelf.jpg | Chris F | https://www.pexels.com/photo/assorted-wine-bottles-1283219/ |
| night-window.jpg | Brett Sayles | https://www.pexels.com/photo/pile-of-labeled-bottles-2606387/ |
| beer-ice.jpg | Maor Attias | https://www.pexels.com/photo/bottles-and-ice-in-a-wheelbarrow-5175351/ |
| bottle-on-ice.jpg | Ron Martinez | https://www.pexels.com/photo/beer-bottle-in-a-bucket-of-ice-4044674/ |
| ice-cold-can.jpg | Tamba Budiarsana | https://www.pexels.com/photo/beer-can-cold-drink-171205 |
| tequila-limes.jpg | Denys Gromov | https://www.pexels.com/photo/tequila-drink-with-slices-of-lime-on-the-top-of-shot-glass-4762727/ |
| wine-dark.jpg | Atlantic Ambience | https://www.pexels.com/photo/wine-bottles-on-display-in-wooden-shelves-9397571/ |
| wine-cubbies.jpg | yağız uçal | https://www.pexels.com/photo/wooden-wine-rack-with-diverse-bottles-in-cellar-32551644/ |
| wine-rack.jpg | Ata Ebem | https://www.pexels.com/photo/bottles-of-wine-stacked-on-shelf-11021166/ |
| snack-wall.jpg | Allen Boguslavsky | https://www.pexels.com/photo/a-shelf-with-snacks-and-snacks-on-it-27939229/ |
| snack-run.jpg | Rosse Marie Beringuel | https://www.pexels.com/photo/assorted-snacks-10114270/ |
| delivery-bag.jpg | Cup of Couple | https://www.pexels.com/photo/bottle-of-wine-in-brown-paper-bag-8472741/ |

Generated assets (not photographs): favicon.ico, assets/favicon.png,
assets/apple-touch-icon.png, assets/logo.png (Pillow-generated JR monogram).
