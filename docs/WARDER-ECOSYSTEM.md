# One Warder ecosystem

Warder is the project identity. FullHDGlass, PiconHub and GSU are its applications, not separate brands with independent data or visual rules. The owner explicitly confirmed this direction on 27 October 2026.

DAB uses one approved catalog in the PiconHub repository and the same exact-reference PNGs. Full satellite packages include the DAB services carried by their owning positions. The standalone DAB selection is an additional way to request the same images. No fake orbital position or provider is created.

`warderRadioCore/` contains exact pinned copies of the canonical Warder picon engine, parser and translation data; `SOURCE.json` records the source commit and every hash. FullHDGlass supplies only its host UI adapter in `warderRadio.py`. The engine uses the same installation lock as PiconHub. Changes to the shared engine must be made in the canonical source, tested there, and synchronized with a new pin rather than independently rewritten in the skin.

Both applications keep the existing picon destination conventions and official/owner-approved logo composition rules. Prepared but unverified station IDs must not enter production packages.
