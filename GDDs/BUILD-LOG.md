# BUILD-LOG.md — Project Holon

Running log of technical decisions and how problems got solved.
One entry per solved problem. Newest at top.

Format:
```
## YYYY-MM-DD — Short title
- What was done
- Key decision or pattern used
- Gotchas / things that broke and why
```

---

## 2026-08-29 — Star and Lowercase Delta Naming Symbols
- Added `★` and `δ` as single-byte characters (`0x7D` and `0x92`), exposed them on the naming-screen symbols keyboard, and added glyphs to every Latin font variant.
- Reused available single-byte character slots because naming buffers store one byte per character; this avoided changing Pokémon name storage or save compatibility.
- The first glyph pass used the accent palette index, which rendered transparent on the naming screen. The visible glyphs must use foreground and shadow indices instead.
- Initial 6-pixel width values clipped artwork extending beyond the first six columns. Both symbols now use 8-pixel font widths and artwork constrained to the rendered cell.
- Current result is a functional first pass with limited in-game testing. Revisit the exact star and delta designs during a later UI polish review.
