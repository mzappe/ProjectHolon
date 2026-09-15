#include "global.h"
#include "bg.h"
#include "gpu_regs.h"
#include "intro_starfield.h"
#include "palette.h"
#include "task.h"
#include "constants/rgb.h"

// BG1 holds the stars; BG2 scrolls a small meteor over them. BG3 holds the
// original platform in front of the sky, behind the portraits and BG0 text.
// Sky tiles/maps use character block 0; the platform uses character block 1.
#define METEOR_FIRST_TILE 17
#define METEOR_WAIT_FRAMES 360
#define PLATFORM_PALETTE 3 // Slot 2 belongs to the text-window border.

enum
{
    PLATFORM_FADE_COEFF = 8,
    PLATFORM_FADE_TIMER,
    PLATFORM_FADE_DELAY,
    PLATFORM_FADE_ACTIVE,
};

static const u32 sPlatformTiles[] = INCGFX_U32("graphics/birch_speech/shadow.png", ".4bpp");
// Keep the center close to the original charcoal (5, 6, 6). Equal channels
// prevent colored steps as this very dark fill fades on the GBA's 5-bit palette.
// The lilac rim retains its original muted green accent.
static const u16 sPlatformPalette[16] =
{
    RGB_BLACK, RGB(6, 6, 6), RGB(9, 9, 13), RGB(14, 13, 16),
    RGB(12, 12, 18), RGB(14, 14, 21), RGB(17, 17, 25),
    RGB(21, 23, 21), RGB(27, 26, 27),
};

static const struct BgTemplate sPlatformBg =
{
    .bg = 3,
    .charBaseIndex = 1,
    .mapBaseIndex = 15,
    .screenSize = 0,
    .paletteMode = 0,
    .priority = 1,
    .baseTile = 0,
};

static const struct BgTemplate sMeteorBg =
{
    .bg = 2,
    .charBaseIndex = 0,
    .mapBaseIndex = 4,
    .screenSize = 1, // 512 pixels wide, so the streak never wraps onscreen.
    .paletteMode = 0,
    .priority = 2,
    .baseTile = 0,
};

static const u16 sMeteorPalette[16] =
{
    RGB_BLACK, RGB(5, 7, 11), RGB(10, 14, 19), RGB(19, 23, 28), RGB_WHITE,
};

static void UpdateStarPalette(u16 frame)
{
    u16 colors[16] = {RGB_BLACK};
    u32 i;

    for (i = 0; i < 8; i++)
    {
        // Stagger eight slow brightness waves, keeping the sky itself black.
        u32 phase = ((frame >> 2) + i * 9) & 63;
        u32 light = 6 + (phase < 32 ? phase : 63 - phase) * 3 / 4;
        colors[i + 1] = RGB(light - 2, light - 1, light);
    }
    LoadPalette(colors, BG_PLTT_ID(0), sizeof(colors));
}

static void UpdatePlatformPalette(u8 darkness)
{
    u16 colors[16];
    u32 i;

    for (i = 0; i < ARRAY_COUNT(colors); i++)
    {
        u32 color = sPlatformPalette[i];
        u32 light = 16 - darkness;
        u32 r = (color & 31) * light / 16;
        u32 g = ((color >> 5) & 31) * light / 16;
        u32 b = ((color >> 10) & 31) * light / 16;
        colors[i] = RGB(r, g, b);
    }
    // Keep both buffers current so later scene fades start from this color.
    LoadPalette(colors, BG_PLTT_ID(PLATFORM_PALETTE), sizeof(colors));
}

static void Task_IntroStarfield(u8 taskId)
{
    s16 *data = gTasks[taskId].data;

    // Leave the palette buffers alone while the scene fades to/from black.
    if (gPaletteFade.active)
        return;

    if (data[PLATFORM_FADE_ACTIVE])
    {
        if (data[PLATFORM_FADE_TIMER])
            data[PLATFORM_FADE_TIMER]--;
        else
        {
            data[PLATFORM_FADE_TIMER] = data[PLATFORM_FADE_DELAY];
            UpdatePlatformPalette(--data[PLATFORM_FADE_COEFF]);
            if (data[PLATFORM_FADE_COEFF] == 0)
                data[PLATFORM_FADE_ACTIVE] = FALSE;
        }
    }

    if (data[6] != data[7])
    {
        s16 step = data[6] < data[7] ? 2 : -2;
        s16 remaining = data[7] - data[6];
        data[6] += abs(remaining) < 2 ? remaining : step;
        SetGpuReg(REG_OFFSET_BG3HOFS, -data[6]);
    }

    data[0] = (data[0] + 1) & 255;
    if ((data[0] & 3) == 0)
        UpdateStarPalette(data[0]);

    if (data[1] > 0)
    {
        data[1]--;
        return;
    }

    if (data[2] == 0)
    {
        data[3] = -32;
        data[4] = data[5] * 13;
        data[2] = 1;
    }
    else
    {
        data[3] += 4;
        data[4]++;
    }

    if (data[3] >= DISPLAY_WIDTH)
    {
        HideBg(2);
        data[2] = 0;
        data[5] = (data[5] + 1) % 4;
        data[1] = METEOR_WAIT_FRAMES + data[5] * 67;
    }
    else
    {
        SetGpuReg(REG_OFFSET_BG2HOFS, (-data[3]) & 511);
        SetGpuReg(REG_OFFSET_BG2VOFS, (-data[4]) & 255);
        ShowBg(2);
    }
}

static void InitIntroPlatform(s16 offset, bool8 visible)
{
    vu32 *tiles = (vu32 *)BG_CHAR_ADDR(1);
    vu16 *map = (vu16 *)BG_SCREEN_ADDR(15);
    static const u8 rowTiles[] = {16, 32, 24, 40};
    u32 i, x, y;

    InitBgFromTemplate(&sPlatformBg);
    DmaFill16(3, 0, (void *)BG_SCREEN_ADDR(15), 0x800);
    // Tile zero is transparent. Tiles 1-15 belonged to the old sky gradient.
    DmaFill32(3, 0, (void *)BG_CHAR_ADDR(1), 16 * TILE_SIZE_4BPP);
    for (i = 16 * TILE_SIZE_4BPP / sizeof(u32); i < ARRAY_COUNT(sPlatformTiles); i++)
    {
        u32 pixels = sPlatformTiles[i];
        u32 shift;

        // The original disc's outside fill used opaque black (index 15).
        // Make that fill transparent so the stars show around its curved rim.
        for (shift = 0; shift < 32; shift += 4)
        {
            if (((pixels >> shift) & 15) == 15)
                pixels &= ~(15u << shift);
        }
        tiles[i] = pixels;
    }
    // Reuse the original mirrored disc layout, centered at (120, 88).
    for (y = 0; y < ARRAY_COUNT(rowTiles); y++)
    {
        for (x = 0; x < 8; x++)
        {
            map[(9 + y) * 32 + 7 + x] = (rowTiles[y] + x) | (PLATFORM_PALETTE << 12);
            map[(9 + y) * 32 + 22 - x] = (rowTiles[y] + x) | (1 << 10) | (PLATFORM_PALETTE << 12);
        }
    }
    UpdatePlatformPalette(visible ? 0 : 16);
    SetGpuReg(REG_OFFSET_BG3HOFS, -offset);
    SetGpuReg(REG_OFFSET_BG3VOFS, 0);
    if (visible)
        ShowBg(3);
    else
        HideBg(3);
}

void InitIntroStarfield(s16 platformOffset, bool8 showPlatform)
{
    u32 tiles[25][8] = {0};
    vu16 *stars = (vu16 *)BG_SCREEN_ADDR(7);
    vu16 *meteor = (vu16 *)BG_SCREEN_ADDR(4);
    u32 seed = 0x484F4C4E;
    u32 i;
    u8 taskId;

    InitBgFromTemplate(&sMeteorBg);
    HideBg(2);
    SetGpuReg(REG_OFFSET_BG1HOFS, 0);
    SetGpuReg(REG_OFFSET_BG1VOFS, 0);

    for (i = 1; i <= 8; i++)
    {
        tiles[i][3] = i << 12;
        tiles[i + 8][2] = i << 12;
        tiles[i + 8][3] = (i << 8) | (i << 12) | (i << 16);
        tiles[i + 8][4] = i << 12;
    }
    // A 32x16 streak, with a dim tail leading into a bright two-pixel head.
    for (i = 0; i < 30; i++)
    {
        u32 x = i + 1;
        u32 y = 3 + i / 4;
        u32 color = 1 + i / 8;
        u32 tile = METEOR_FIRST_TILE + (y / 8) * 4 + x / 8;
        tiles[tile][y & 7] |= color << ((x & 7) * 4);
    }
    CpuCopy32(tiles, (void *)VRAM, sizeof(tiles));
    DmaFill16(3, 0, (void *)BG_SCREEN_ADDR(7), 0x800);
    DmaFill16(3, 0, (void *)BG_SCREEN_ADDR(4), 0x1000);

    // Jitter a sparse grid using a private seed, without touching gameplay RNG.
    for (i = 0; i < 60; i++)
    {
        u32 x, y, tile;
        seed = seed * 1664525 + 1013904223;
        x = (i % 10) * 3 + ((seed >> 16) % 3);
        y = (i / 10) * 3 + ((seed >> 24) % 3);
        tile = 1 + ((seed >> 8) % 8);
        if (i % 11 == 0)
            tile += 8;
        stars[y * 32 + x] = tile | ((seed & 3) << 10);
    }
    for (i = 0; i < 8; i++)
        meteor[(i / 4) * 32 + i % 4] = (METEOR_FIRST_TILE + i) | (1 << 12);

    UpdateStarPalette(0);
    LoadPalette(sMeteorPalette, BG_PLTT_ID(1), sizeof(sMeteorPalette));
    InitIntroPlatform(platformOffset, showPlatform);
    taskId = CreateTask(Task_IntroStarfield, 1);
    gTasks[taskId].data[1] = METEOR_WAIT_FRAMES;
    gTasks[taskId].data[6] = platformOffset;
    gTasks[taskId].data[7] = platformOffset;
}

void FadeInIntroPlatform(u8 delay)
{
    u8 taskId = FindTaskIdByFunc(Task_IntroStarfield);

    if (taskId == TASK_NONE)
        return;

    gTasks[taskId].data[PLATFORM_FADE_COEFF] = 16;
    gTasks[taskId].data[PLATFORM_FADE_TIMER] = delay;
    gTasks[taskId].data[PLATFORM_FADE_DELAY] = delay;
    gTasks[taskId].data[PLATFORM_FADE_ACTIVE] = TRUE;
    UpdatePlatformPalette(16);
    ShowBg(3);
}

void MoveIntroPlatform(s16 platformOffset)
{
    u8 taskId = FindTaskIdByFunc(Task_IntroStarfield);

    if (taskId != TASK_NONE)
        gTasks[taskId].data[7] = platformOffset;
}

void FreeIntroStarfield(void)
{
    u8 taskId = FindTaskIdByFunc(Task_IntroStarfield);

    if (taskId != TASK_NONE)
        DestroyTask(taskId);
    HideBg(2);
    HideBg(3);
}
