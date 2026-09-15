#ifndef GUARD_INTRO_STARFIELD_H
#define GUARD_INTRO_STARFIELD_H

void InitIntroStarfield(s16 platformOffset, bool8 showPlatform);
void FadeInIntroPlatform(u8 delay);
void MoveIntroPlatform(s16 platformOffset);
void FreeIntroStarfield(void);

#endif // GUARD_INTRO_STARFIELD_H
