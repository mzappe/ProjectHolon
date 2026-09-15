#include "global.h"
#include "config/quickstart.h"
#include "quickstart.h"
#include "title_screen.h"
#include "sprite.h"
#include "gba/m4a_internal.h"
#include "clear_save_data_menu.h"
#include "decompress.h"
#include "event_data.h"
#include "intro.h"
#include "m4a.h"
#include "main.h"
#include "main_menu.h"
#include "palette.h"
#include "reset_rtc_screen.h"
#include "berry_fix_program.h"
#include "sound.h"
#include "task.h"
#include "scanline_effect.h"
#include "gpu_regs.h"
#include "graphics.h"
#include "constants/rgb.h"
#include "constants/songs.h"

#define TAG_HOLON_PRESS_START 1000

#define CLEAR_SAVE_BUTTON_COMBO (B_BUTTON | SELECT_BUTTON | DPAD_UP)
#define RESET_RTC_BUTTON_COMBO (B_BUTTON | SELECT_BUTTON | DPAD_LEFT)
#define BERRY_UPDATE_BUTTON_COMBO (B_BUTTON | SELECT_BUTTON)

// Mode 0: three independent, stationary text backgrounds.
// BG0: 8bpp landscape at 0x0000 (up to 0xC000 bytes), map at 0xE800.
// BG1: 4bpp Pokemon at 0xC000 (up to 0x1000 bytes), map at 0xF000.
// BG2: 4bpp Holon Legends at 0xD000 (up to 0x1000 bytes), map at 0xF800.
// BG1/BG2 share character base 3, using palette banks 15/14. Subtitle map tile
// numbers start at 128, addressing 0xD000. The builder checks all budgets.
#define HOLON_SUBTITLE_TILES ((void *)(BG_CHAR_ADDR(3) + 0x1000))

static const u16 sHolonPalette[] = INCGFX_U16("graphics/title_screen/holon.pal", ".gbapal");
static const u32 sHolonLandscapeGfx[] = INCGFX_U32("graphics/title_screen/holon_landscape.png", ".8bpp.smol");
static const u32 sHolonLandscapeMap[] = INCGFX_U32("graphics/title_screen/holon_landscape.bin", ".smolTM");
static const u32 sHolonPokemonGfx[] = INCGFX_U32("graphics/title_screen/holon_pokemon.png", ".4bpp.smol");
static const u32 sHolonPokemonMap[] = INCGFX_U32("graphics/title_screen/holon_pokemon.bin", ".smolTM");
static const u32 sHolonLegendsGfx[] = INCGFX_U32("graphics/title_screen/holon_legends.png", ".4bpp.smol");
static const u32 sHolonLegendsMap[] = INCGFX_U32("graphics/title_screen/holon_legends.bin", ".smolTM");

static void MainCB2(void);
static void Task_TitleScreen(u8 taskId);
static void SpriteCB_PressStart(struct Sprite *sprite);
static void CB2_GoToMainMenu(void);
static void CB2_GoToClearSaveDataScreen(void);
static void CB2_GoToResetRtcScreen(void);
static void CB2_GoToBerryFixScreen(void);
static void CB2_GoToCopyrightScreen(void);

// Shared with the Game Freak intro; preserve its original blend table.
const u16 gTitleScreenAlphaBlend[64] =
{
    BLDALPHA_BLEND(16, 0),
    BLDALPHA_BLEND(16, 1),
    BLDALPHA_BLEND(16, 2),
    BLDALPHA_BLEND(16, 3),
    BLDALPHA_BLEND(16, 4),
    BLDALPHA_BLEND(16, 5),
    BLDALPHA_BLEND(16, 6),
    BLDALPHA_BLEND(16, 7),
    BLDALPHA_BLEND(16, 8),
    BLDALPHA_BLEND(16, 9),
    BLDALPHA_BLEND(16, 10),
    BLDALPHA_BLEND(16, 11),
    BLDALPHA_BLEND(16, 12),
    BLDALPHA_BLEND(16, 13),
    BLDALPHA_BLEND(16, 14),
    BLDALPHA_BLEND(16, 15),
    BLDALPHA_BLEND(15, 16),
    BLDALPHA_BLEND(14, 16),
    BLDALPHA_BLEND(13, 16),
    BLDALPHA_BLEND(12, 16),
    BLDALPHA_BLEND(11, 16),
    BLDALPHA_BLEND(10, 16),
    BLDALPHA_BLEND(9, 16),
    BLDALPHA_BLEND(8, 16),
    BLDALPHA_BLEND(7, 16),
    BLDALPHA_BLEND(6, 16),
    BLDALPHA_BLEND(5, 16),
    BLDALPHA_BLEND(4, 16),
    BLDALPHA_BLEND(3, 16),
    BLDALPHA_BLEND(2, 16),
    BLDALPHA_BLEND(1, 16),
    BLDALPHA_BLEND(0, 16),
    [32 ... 63] = BLDALPHA_BLEND(0, 16)
};

static const struct OamData sPressStartOam =
{
    .affineMode = ST_OAM_AFFINE_OFF,
    .objMode = ST_OAM_OBJ_NORMAL,
    .bpp = ST_OAM_4BPP,
    .shape = SPRITE_SHAPE(32x8),
    .size = SPRITE_SIZE(32x8),
    .priority = 0,
};

static const union AnimCmd sPressStartAnim0[] = { ANIMCMD_FRAME(1, 4), ANIMCMD_END };
static const union AnimCmd sPressStartAnim1[] = { ANIMCMD_FRAME(5, 4), ANIMCMD_END };
static const union AnimCmd sPressStartAnim2[] = { ANIMCMD_FRAME(9, 4), ANIMCMD_END };
static const union AnimCmd sPressStartAnim3[] = { ANIMCMD_FRAME(13, 4), ANIMCMD_END };
static const union AnimCmd sPressStartAnim4[] = { ANIMCMD_FRAME(17, 4), ANIMCMD_END };
static const union AnimCmd *const sPressStartAnims[] =
{
    sPressStartAnim0, sPressStartAnim1, sPressStartAnim2,
    sPressStartAnim3, sPressStartAnim4,
};

static const struct SpriteTemplate sPressStartTemplate =
{
    .tileTag = TAG_HOLON_PRESS_START,
    .paletteTag = TAG_HOLON_PRESS_START,
    .oam = &sPressStartOam,
    .anims = sPressStartAnims,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCB_PressStart,
};

static const struct CompressedSpriteSheet sPressStartSheet =
{
    .data = gTitleScreenPressStartGfx,
    .size = 48 * TILE_SIZE_4BPP,
    .tag = TAG_HOLON_PRESS_START,
};

static const struct SpritePalette sPressStartPalette =
{
    .data = gTitleScreenPressStartPal,
    .tag = TAG_HOLON_PRESS_START,
};

static void SpriteCB_PressStart(struct Sprite *sprite)
{
    // Only the input prompt blinks; all three background layers stay fixed.
    sprite->invisible = (++sprite->data[0] & 16) == 0;
}

static void VBlankCB(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

void CB2_InitTitleScreen(void)
{
    u32 i;

    if (IS_FRLG)
    {
        CB2_InitTitleScreenFrlg();
        return;
    }

    switch (gMain.state)
    {
    case 0:
        SetVBlankCallback(NULL);
        SetHBlankCallback(NULL);
        ScanlineEffect_Stop();
        SetGpuReg(REG_OFFSET_DISPCNT, 0);
        SetGpuReg(REG_OFFSET_BLDCNT, 0);
        SetGpuReg(REG_OFFSET_BLDALPHA, 0);
        SetGpuReg(REG_OFFSET_BLDY, 0);
        SetGpuReg(REG_OFFSET_MOSAIC, 0);
        SetGpuReg(REG_OFFSET_WIN0H, 0);
        SetGpuReg(REG_OFFSET_WIN0V, 0);
        SetGpuReg(REG_OFFSET_WIN1H, 0);
        SetGpuReg(REG_OFFSET_WIN1V, 0);
        SetGpuReg(REG_OFFSET_WININ, 0);
        SetGpuReg(REG_OFFSET_WINOUT, 0);
        SetGpuReg(REG_OFFSET_BG0HOFS, 0);
        SetGpuReg(REG_OFFSET_BG0VOFS, 0);
        SetGpuReg(REG_OFFSET_BG1HOFS, 0);
        SetGpuReg(REG_OFFSET_BG1VOFS, 0);
        SetGpuReg(REG_OFFSET_BG2HOFS, 0);
        SetGpuReg(REG_OFFSET_BG2VOFS, 0);
        DmaFill16(3, 0, (void *)VRAM, VRAM_SIZE);
        DmaFill32(3, 0, (void *)OAM, OAM_SIZE);
        DmaFill16(3, 0, (void *)PLTT, PLTT_SIZE);
        ResetPaletteFade();
        ResetTasks();
        ResetSpriteData();
        FreeAllSpritePalettes();
        gReservedSpritePaletteCount = 0;
        gMain.state++;
        break;
    case 1:
        DecompressDataWithHeaderVram(sHolonLandscapeGfx, (void *)BG_CHAR_ADDR(0));
        DecompressDataWithHeaderVram(sHolonLandscapeMap, (void *)BG_SCREEN_ADDR(29));
        DecompressDataWithHeaderVram(sHolonPokemonGfx, (void *)BG_CHAR_ADDR(3));
        DecompressDataWithHeaderVram(sHolonPokemonMap, (void *)BG_SCREEN_ADDR(30));
        DecompressDataWithHeaderVram(sHolonLegendsGfx, HOLON_SUBTITLE_TILES);
        DecompressDataWithHeaderVram(sHolonLegendsMap, (void *)BG_SCREEN_ADDR(31));
        LoadPalette(sHolonPalette, BG_PLTT_ID(0), sizeof(sHolonPalette));
        LoadCompressedSpriteSheet(&sPressStartSheet);
        LoadSpritePalette(&sPressStartPalette);
        for (i = 0; i < ARRAY_COUNT(sPressStartAnims); i++)
        {
            u8 spriteId = CreateSprite(&sPressStartTemplate, 64 + 32 * i, 148, 0);
            StartSpriteAnim(&gSprites[spriteId], i);
        }
        if (QUICKSTART && QUICKSTART_HUD)
            CreateQuickstartHud();
        gMain.state++;
        break;
    case 2:
        SetGpuReg(REG_OFFSET_BG0CNT, BGCNT_PRIORITY(2) | BGCNT_CHARBASE(0) | BGCNT_SCREENBASE(29) | BGCNT_256COLOR | BGCNT_TXT256x256);
        SetGpuReg(REG_OFFSET_BG1CNT, BGCNT_PRIORITY(1) | BGCNT_CHARBASE(3) | BGCNT_SCREENBASE(30) | BGCNT_16COLOR | BGCNT_TXT256x256);
        SetGpuReg(REG_OFFSET_BG2CNT, BGCNT_PRIORITY(0) | BGCNT_CHARBASE(3) | BGCNT_SCREENBASE(31) | BGCNT_16COLOR | BGCNT_TXT256x256);
        BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
        BuildOamBuffer();
        SetVBlankCallback(VBlankCB);
        EnableInterrupts(INTR_FLAG_VBLANK);
        SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_0 | DISPCNT_OBJ_1D_MAP
                  | DISPCNT_BG0_ON | DISPCNT_BG1_ON | DISPCNT_BG2_ON | DISPCNT_OBJ_ON);
        m4aSongNumStart(MUS_OCEANIC_MUSEUM);
        CreateTask(Task_TitleScreen, 0);
        SetMainCallback2(MainCB2);
        break;
    }
}

static void MainCB2(void)
{
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    UpdatePaletteFade();
}

static void Task_TitleScreen(u8 taskId)
{
    if (gPaletteFade.active)
        return;

    if (QUICKSTART && JOY_NEW(SELECT_BUTTON) && !JOY_HELD(B_BUTTON))
    {
        Quickstart();
        return;
    }

    if (JOY_NEW(A_BUTTON) || JOY_NEW(START_BUTTON))
    {
        FadeOutBGM(4);
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        SetMainCallback2(CB2_GoToMainMenu);
    }
    else if (JOY_HELD(CLEAR_SAVE_BUTTON_COMBO) == CLEAR_SAVE_BUTTON_COMBO)
    {
        SetMainCallback2(CB2_GoToClearSaveDataScreen);
    }
    else if (JOY_HELD(RESET_RTC_BUTTON_COMBO) == RESET_RTC_BUTTON_COMBO
          && CanResetRTC() == TRUE)
    {
        FadeOutBGM(4);
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        SetMainCallback2(CB2_GoToResetRtcScreen);
    }
    else if (JOY_HELD(BERRY_UPDATE_BUTTON_COMBO) == BERRY_UPDATE_BUTTON_COMBO)
    {
        FadeOutBGM(4);
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        SetMainCallback2(CB2_GoToBerryFixScreen);
    }
    else if ((gMPlayInfo_BGM.status & 0xFFFF) == 0)
    {
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        SetMainCallback2(CB2_GoToCopyrightScreen);
    }
}

static void CB2_GoToMainMenu(void)
{
    if (!UpdatePaletteFade())
        SetMainCallback2(CB2_InitMainMenu);
}

static void CB2_GoToCopyrightScreen(void)
{
    if (!UpdatePaletteFade())
        SetMainCallback2(CB2_InitCopyrightScreenAfterTitleScreen);
}

static void CB2_GoToClearSaveDataScreen(void)
{
    if (!UpdatePaletteFade())
        SetMainCallback2(CB2_InitClearSaveDataScreen);
}

static void CB2_GoToResetRtcScreen(void)
{
    if (!UpdatePaletteFade())
        SetMainCallback2(CB2_InitResetRtcScreen);
}

static void CB2_GoToBerryFixScreen(void)
{
    if (!UpdatePaletteFade())
    {
        m4aMPlayAllStop();
        SetMainCallback2(CB2_InitBerryFixProgram);
    }
}
