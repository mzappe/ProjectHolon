#ifndef GUARD_INTRO_STARFIELD_H
#define GUARD_INTRO_STARFIELD_H

void InitIntroStarfield(s16 platformOffset, bool8 showPlatform);
// Menu variant uses BG2/BG3, character block 0, maps 4/5/7, palettes 8/9.
void InitMenuStarfield(void);
void FadeInIntroPlatform(u8 delay);
void MoveIntroPlatform(s16 platformOffset);
void FreeIntroStarfield(void);

#endif // GUARD_INTRO_STARFIELD_H
