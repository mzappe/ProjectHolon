#ifndef GUARD_SHINY_RATE_H
#define GUARD_SHINY_RATE_H

// Project Holon: player-selectable Shiny encounter rate, chosen once during the
// new-game intro and stored in gSaveBlock2Ptr->shinyRate. The per-level values
// returned by GetShinyRateOdds() are a numerator over 65536, the same scale as
// the vanilla SHINY_ODDS constant.

enum ShinyRateLevel
{
    SHINY_RATE_RARE,     // ~1/8192
    SHINY_RATE_UNCOMMON, // ~1/4096
    SHINY_RATE_CLASSIC,  // ~1/2048
    SHINY_RATE_FREQUENT, // ~1/512
    SHINY_RATE_COMMON,   // ~1/128
    SHINY_RATE_COUNT,
};

#define SHINY_RATE_DEFAULT SHINY_RATE_CLASSIC

u16 GetShinyRateOdds(u32 level);
u32 GetPlayerShinyOdds(void);

#endif // GUARD_SHINY_RATE_H
