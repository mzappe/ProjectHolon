#include "global.h"
#include "shiny_rate.h"

// Numerator over 65536; compared against GET_SHINY_VALUE() the same way SHINY_ODDS is.
static const u16 sShinyRateOdds[SHINY_RATE_COUNT] = {
    [SHINY_RATE_RARE]     =   8, // ~1/8192
    [SHINY_RATE_UNCOMMON] =  16, // ~1/4096
    [SHINY_RATE_CLASSIC]  =  32, // ~1/2048
    [SHINY_RATE_FREQUENT] = 128, // ~1/512
    [SHINY_RATE_COMMON]   = 512, // ~1/128
};

u16 GetShinyRateOdds(u32 level)
{
    if (level >= SHINY_RATE_COUNT)
        level = SHINY_RATE_DEFAULT;

    return sShinyRateOdds[level];
}

u32 GetPlayerShinyOdds(void)
{
    return GetShinyRateOdds(gSaveBlock2Ptr->shinyRate);
}
