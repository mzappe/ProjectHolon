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

## 2026-08-31 — START menu in-game clock
- Added a time-display window to the top-left of the START menu in `src/start_menu.c`. Design ported from `Pawkkie/pokeemerald-expansion:start-menu-clock`, but reimplemented against current expansion rather than merged — the branch targets 1.7.x and every file it touches (`start_menu.c`, `strings.c/h`, `README`) has been refactored here since, so a `git merge` was 100% conflicts for a ~80-line feature.
- Pattern: window created in `InitStartMenuStep` case 3 (next to the Safari/Pyramid windows), refreshed once per minute-rollover from `HandleStartMenuInput` via a cached `sStartClockLastMinute`, destroyed unconditionally in `RemoveExtraStartMenuWindows` (every menu-close path already calls it). Time from `gLocalTime` via the expansion's `FormatDecimalTimeWithoutSeconds`; no new strings (rtc.c already has AM/PM). Window `baseBlock 0x38` sits past the Safari/Pyramid windows (`0x8`) so both can render together; those were moved to `tilemapTop 5` to clear it.
- Window auto-sizes to the string: `width = ceil((GetStringWidth(...) + pad) / 8)` tiles, text centered in the tile-rounding slack — avoids a hardcoded tile count that breaks if the font or 12/24h format changes.
- Gotchas:
  - `EWRAM_DATA` must be zero-initialised (`.sbss`); a `= 0xFF` sentinel failed to compile. Reworked so `ShowStartClockWindow` always writes `sStartClockLastMinute` before any reader.
  - Weekday was dropped. `GetDayOfWeek()` is `gLocalTime.days` counted from 0 = Saturday, and the intro wall-clock only sets time-of-day (never the date), so a fresh clock always reads "Saturday" and just increments — misleading in a status readout.
  - Displays in-game time (`gLocalTime` = hardware RTC − the offset stamped when you set the clock), not wall-clock time. Set the in-game clock to the real current time for them to match. `OW_USE_FAKE_RTC` is FALSE, so the RTC is real.
  - Uses a local `u8 timeStr[16]`, not `gStringVar4`, to avoid shared-global coupling with the menu's own text formatting.
- `START_CLOCK_24_HOUR` define in the same block toggles 12h/24h. Normal ROM build succeeded; verified in emulator (renders, updates on the minute, tears down cleanly).

## 2026-08-29 — Star and Lowercase Delta Naming Symbols
- Added `★` and `δ` as single-byte characters (`0x7D` and `0x92`), exposed them on the naming-screen symbols keyboard, and added glyphs to every Latin font variant.
- Reused available single-byte character slots because naming buffers store one byte per character; this avoided changing Pokémon name storage or save compatibility.
- The first glyph pass used the accent palette index, which rendered transparent on the naming screen. The visible glyphs must use foreground and shadow indices instead.
- Initial 6-pixel width values clipped artwork extending beyond the first six columns. Both symbols now use 8-pixel font widths and artwork constrained to the rendered cell.
- Current result is a functional first pass with limited in-game testing. Revisit the exact star and delta designs during a later UI polish review.
