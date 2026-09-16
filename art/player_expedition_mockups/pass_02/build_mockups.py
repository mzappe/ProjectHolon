"""Deterministic, indexed pixel mockups. Writes only beside this script. Requires Pillow."""
from pathlib import Path
from io import BytesIO
import hashlib
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
# Immutable originals: rebuilding must not reapply edits to the integrated sprites.
SOURCE_REVISION = '1b7f9ee3c14128e4d34958017e35470544e96f88'
PEOPLE = ('brendan', 'may')
WIDTHS = {'walking': 16, 'running': 16, 'mach_bike': 32, 'acro_bike': 32,
          'surfing': 32, 'fishing': 32, 'watering': 32, 'field_move': 32,
          'underwater': 32, 'decorating': 16}
BG = '#e9e6da'
INK = '#223f43'


def palette(source, who, underwater=False):
    colors = list(source.getpalette()[:48])
    replacements = {5: (112, 144, 171), 6: (61, 103, 141),
                    7: (220, 220, 219), 8: (132, 133, 134),
                    9: (115, 67, 42), 10: (240, 139, 48),
                    11: (178, 78, 29), 12: (35, 61, 96),
                    13: (63, 39, 29), 14: (250, 249, 245),
                    15: (12, 12, 14)}
    if who=='brendan':
        replacements[13]=(60,60,64)  # Dedicated neutral headband shade.
    if underwater:
        replacements = {5: (88, 90, 94), 6: (44, 47, 53),
                        7: (30, 39, 53), 8: (20, 27, 38),
                        9: (170, 172, 174), 15: (12, 12, 14)}
    for i, rgb in replacements.items():
        colors[i*3:i*3+3] = rgb
    return colors


def head_mask(source, limit):
    """Find the cap by connected material pixels, excluding small eye highlights."""
    candidates = {(x,y) for y in range(min(limit,source.height)) for x in range(source.width)
                  if source.getpixel((x,y)) in (9,10,11,14)}
    pending = set(candidates)
    groups = []
    while pending:
        seed = pending.pop()
        group, queue = {seed}, [seed]
        while queue:
            x,y = queue.pop()
            for n in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if n in pending:
                    pending.remove(n); group.add(n); queue.append(n)
        groups.append(group)
    if not groups:
        return set()
    main = max(groups, key=lambda g: (len(g), -min(y for x,y in g), -min(x for x,y in g)))
    top, bottom = min(y for x,y in main), max(y for x,y in main)
    left, right = min(x for x,y in main), max(x for x,y in main)
    # Include nearby bandana lobes, excluding raised gloves on the action frames.
    return set().union(*(g for g in groups if len(g)>4 and
                        min(y for x,y in g)>=top-3 and max(y for x,y in g)<=bottom
                        and min(x for x,y in g)>=left-16 and max(x for x,y in g)<=right+4))


def hair_pixel(source, x, y, who, head_bottom):
    if who != 'may' or y > head_bottom+12:
        return False
    v = source.getpixel((x,y))
    if v in (7,8):
        return True
    if v != 4:
        return False
    neighbors = [source.getpixel((xx,yy)) for xx,yy in
                 ((x-1,y),(x+1,y),(x,y-1),(x,y+1))
                 if 0<=xx<source.width and 0<=yy<source.height]
    return any(n in (7,8) for n in neighbors)


def outfit_frame(source, who, kind):
    out = source.copy()
    cap = head_mask(source, 18 if kind=='front' else 38 if kind=='back' else 25)
    cap_bottom = max((y for x,y in cap), default=15)
    # The inherited blue antialiasing pixels sit OUTSIDE the white/green cap mask.
    # Walk their connected edge explicitly; neutralizing the cap interior alone
    # left the blue halo that the user rejected.
    head_edge=set(cap)
    queue=list(cap)
    while queue:
        x,y=queue.pop()
        for xx in range(max(0,x-1),min(source.width,x+2)):
            for yy in range(max(0,y-1),min(source.height,y+2)):
                p=(xx,yy)
                edge_pixel = source.getpixel(p) in (5,6) and yy<=cap_bottom+1
                highlight = source.getpixel(p) in (9,14) and yy<=cap_bottom
                if p not in head_edge and (edge_pixel or highlight):
                    head_edge.add(p);queue.append(p)
    for y in range(source.height):
        for x in range(source.width):
            v = source.getpixel((x,y))
            # Reserve white/gray indices for hair; keep shared clothing/eye indices dark.
            n = {7:12, 8:15, 9:5, 12:6, 13:12}.get(v,v)
            if (x,y) in head_edge:
                n = {9:7,14:14,10:7,11:8,5:8,6:15}.get(v,n)
                if who=='brendan' and v in (10,11):
                    n = 13
            elif v in (10,11):
                n = {10:6,11:12}[v]  # Fabric straps/packs; leather is a small trim.
            # Small isolated whites in faces retain neutral highlights.
            if v in (9,14) and (x,y) not in head_edge and y<=cap_bottom+8:
                n = 14
            if hair_pixel(source,x,y,who,cap_bottom+(12 if kind=='back' else 0)):
                n = {7:14,8:8,4:7}[v]
            if who=='brendan' and cap_bottom<y<=cap_bottom+7 and v==8:
                n = 8
            if kind=='back' and who=='brendan' and cap_bottom-8<=y<=cap_bottom+5:
                # The original back uses solid black *inside* the hair shadow.
                # Lift that interior to gray while retaining the silhouette outline.
                neighbors=[source.getpixel((xx,yy)) for xx,yy in
                           ((x-1,y),(x+1,y),(x,y-1),(x,y+1))
                           if 0<=xx<64 and 0<=yy<64]
                if v==8:
                    n=8
                if v==15 and len(neighbors)==4 and all(z not in (0,1,2,3) for z in neighbors):
                    n=8
            if kind=='back' and who=='may' and y<=cap_bottom+10 and v==4:
                # Hair's broad brown shadow regions extend beyond the edge pixels.
                neighbors=[source.getpixel((xx,yy)) for xx,yy in
                           ((x-1,y),(x+1,y),(x,y-1),(x,y+1))
                           if 0<=xx<64 and 0<=yy<64]
                if not any(z in (1,2,3) for z in neighbors):
                    n=7
            if kind=='front':
                if who=='brendan':
                    if 39<=y<=51:
                        n = {5:6,6:12,7:15}.get(v,n)
                    if y>=52:
                        n = {5:12,6:15,8:15,10:9,11:13,12:9,13:13}.get(v,n)
                    if 52<=y<=54 and v in (5,6):
                        n = {5:9,6:13}[v]
                    # Move the orange from the collar to the waist and wrist.
                    if 37<=y<=38 and 24<=x<=36 and v in (5,6,12,13):
                        n = 10 if y==37 else 11
                    if 29<=y<=36 and 25<=x<=29 and v in (12,13):
                        n = {12:10,13:11}[v]  # Clean orange lower-jacket panel.
                    if 36<=y<=39 and x<22 and v in (10,11):
                        n = {10:10,11:11}[v]
                    if x>=42 and 27<=y<=35 and v in (12,13):
                        n = {12:10,13:11}[v]
                else:
                    # May's lip shading shares the jacket's original red indices.
                    if 16<=y<=24 and 24<=x<=34 and v in (12,13):
                        n = {12:3,13:4}[v]
                    if 43<=y<=53 and 20<=x<=39:
                        n = {1:6,2:6,3:12,4:15}.get(v,n)
                    if y>=54:
                        n = {5:12,6:15,12:9,13:13}.get(v,n)
                    if 54<=y<=55 and v in (5,6):
                        n = {5:9,6:13}[v]
                    if 34<=y<=35 and v in (10,11):
                        n = {10:10,11:11}[v]
                    if 35<=y<=39 and 38<=x<=40 and v in (5,6):
                        n = {5:10,6:11}[v]
                    if 29<=y<=39 and 33<=x<=35 and v in (12,13):
                        n = {12:10,13:11}[v]  # Matching orange side panel.
                    if x<=16 and 27<=y<=30 and v in (12,13):
                        n = {12:10,13:11}[v]
            elif kind=='back':
                if who=='brendan' and v in (10,11) and y>=38:
                    xs=[xx for xx in range(64) if source.getpixel((xx,y)) in (10,11)]
                    if x in (min(xs),max(xs)):
                        n=9 if v==10 else 13
                    bottom=max(yy for yy in range(38,64) for xx in range(64)
                               if source.getpixel((xx,yy)) in (10,11))
                    if y>=bottom-3:
                        n=10 if v==10 else 11
                if who=='may' and y>=40 and v in (12,13):
                    xs=[xx for xx in range(64) if source.getpixel((xx,y)) in (12,13)]
                    if len(xs)>=7 and (x-min(xs)==2 or max(xs)-x==2):
                        n=9 if v==12 else 13
                    elif len(xs)>=7:
                        bottom=max(yy for yy in range(40,64) for xx in range(64)
                                   if source.getpixel((xx,yy)) in (12,13))
                        if y>=bottom-1:
                            n=10 if v==12 else 11
                        elif len(xs)>=10 and x-min(xs) in (3,4):
                            n=10 if v==12 else 11
            elif who=='may' and kind in ('walking','running','decorating') and y>=28:
                n={1:6,2:6,3:12}.get(v,n)
            # Overworld irises are the dark pixels enclosed by skin on both sides.
            # The old hair remap had incorrectly turned these shared indices gray.
            if kind not in ('front','back') and v==8 and 0<x<source.width-1:
                if source.getpixel((x-1,y)) in (1,2,3) and source.getpixel((x+1,y)) in (1,2,3):
                    n=6
            if kind=='back' and v in (5,7) and (x,y) not in head_edge:
                neighbors=[source.getpixel((xx,yy)) for xx in range(max(0,x-1),min(64,x+2))
                           for yy in range(max(0,y-1),min(64,y+2))]
                if 14 in neighbors and any(z in (1,2) for z in neighbors):
                    n=6
            out.putpixel((x,y),n)
    allowed_head=(7,8,13,14,15) if who=='brendan' else (7,8,14,15)
    assert all(out.getpixel(p) in allowed_head for p in head_edge), 'Colored head edge'
    return out, cap_bottom


def draw_front(source, who):
    out,_ = outfit_frame(source,who,'front')
    # Small leather pockets and neutral ID tabs; orange now lives at waist/cuffs.
    patches = {
        'brendan': [(29,33,'99'),(29,34,'DD'),(35,28,'E'),(35,29,'6')],
        'may': [(25,30,'99'),(25,31,'DD'),(33,28,'E'),(33,29,'6')],
    }
    for x,y,row in patches[who]:
        for dx,value in enumerate(row):
            if source.getpixel((x+dx,y)):
                out.putpixel((x+dx,y),int(value,16))
    # Keep the original pupils and white glints; give each iris its blue pixel.
    irises={'brendan':[(26,18),(32,19)], 'may':[(25,17),(30,18)]}
    for point in irises[who]:
        out.putpixel(point,6)
    return out


def may_bandana_mask(source, kind):
    """Isolate May's original fabric and bow edges, excluding white hair and eyes."""
    cap=head_mask(source,18 if kind=='front' else 38 if kind=='back' else 25)
    if not cap:
        return set()
    bottom=max(y for x,y in cap)
    left,right=min(x for x,y in cap),max(x for x,y in cap)
    # The front-facing bow contains tiny disconnected green islands (four
    # pixels each); include those rather than leaving them in the outfit blue.
    cap.update((x,y) for y in range(bottom+1)
               for x in range(max(0,left-4),min(source.width,right+5))
               if source.getpixel((x,y)) in (10,11))
    mask=set(cap)
    for x,y in cap:
        for xx in range(max(0,x-1),min(source.width,x+2)):
            for yy in range(max(0,y-1),min(source.height,y+2)):
                v=source.getpixel((xx,yy))
                if yy>bottom:
                    continue
                neighbors=[source.getpixel((nx,ny))
                           for nx in range(max(0,xx-1),min(source.width,xx+2))
                           for ny in range(max(0,yy-1),min(source.height,yy+2))]
                # Original brown hair uses index 7; keep its adjoining outline.
                if v in (5,6) or (v in (4,8) and 7 not in neighbors
                                  and not any(n in (1,2,3) for n in neighbors)):
                    mask.add((xx,yy))
    return mask


def clean_may_bandana(source, result, kind):
    """Post-process only the bandana; preserve every other approved pixel/color."""
    if kind=='underwater':
        return result
    width=64 if kind in ('front','back') else WIDTHS[kind]
    height=64 if kind in ('front','back') else 32
    out=result.copy()
    for start_y in range(0,source.height,height):
        for start_x in range(0,source.width,width):
            frame=source.crop((start_x,start_y,start_x+width,start_y+height))
            bandana=may_bandana_mask(frame,kind)
            for x,y in bandana:
                # Charcoal cloth with one consistent gray highlight, using the
                # existing palette so approved eyes, hair, and outfit stay exact.
                color=8 if kind in ('front','back') and frame.getpixel((x,y)) in (9,14) else 15
                out.putpixel((start_x+x,start_y+y),color)
            # Moving bandanas stay solid charcoal: tiny highlights read as speckles.
    return out


def may_hair_mask(source, result, kind):
    """Hair-only editing mask; front fringe/locks have explicit material boundaries."""
    bandana=may_bandana_mask(source,kind)
    if kind=='front':
        # Keep forehead gaps and iris pixels; include the isolated warm highlight
        # at (20,18) and the unmapped brown speckles in the ends of both locks.
        spans={12:[(25,33)],13:[(23,25),(27,34)],14:[(22,25),(28,34)],
               15:[(19,25),(28,35)],16:[(19,24),(29,29)],
               17:[(19,23),(33,36)],18:[(18,23),(33,36)],
               19:[(18,23),(33,37)],20:[(18,22),(32,37)],
               21:[(17,21),(34,38)],22:[(17,21),(34,38)],
               23:[(17,21),(33,37)],24:[(18,21),(34,35)]}
        return {(x,y) for y,runs in spans.items() for a,b in runs for x in range(a,b+1)
                if source.getpixel((x,y)) and (x,y) not in bandana}
    bottom=max((y for x,y in bandana),default=15)
    candidates=set()
    for y in range(min(source.height,bottom+(11 if kind=='back' else 10))):
        for x in range(source.width):
            if (x,y) in bandana:
                continue
            v=source.getpixel((x,y));current=result.getpixel((x,y))
            if v not in (4,7,8) or current not in (4,7,8,14):
                continue
            neighbors=[source.getpixel((xx,yy)) for xx,yy in
                       ((x-1,y),(x+1,y),(x,y-1),(x,y+1))
                       if 0<=xx<source.width and 0<=yy<source.height]
            if current==4 and any(n in (1,2,3) for n in neighbors):
                continue
            if y>bottom and any(n in (5,6,12,13) for n in neighbors):
                continue
            candidates.add((x,y))
    hair={p for p in candidates if source.getpixel(p)==7}
    queue=list(hair)
    while queue:
        x,y=queue.pop()
        for n in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if n in candidates and n not in hair:
                hair.add(n);queue.append(n)
    if kind!='back':
        # Original hair uses isolated skin-palette pixels as warm highlights.
        # Identify them by their hair neighbors, not by their misleading palette.
        for y in range(1,min(source.height-1,bottom+8)):
            for x in range(1,source.width-1):
                if source.getpixel((x,y)) not in (1,2,3,4):
                    continue
                neighbors=[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
                if (any(source.getpixel(n)==7 for n in neighbors)
                    and sum(result.getpixel(n) in (7,8,14) for n in neighbors)>=3):
                    hair.add((x,y))
    return hair


def clean_may_hair(source, result, kind):
    if kind=='underwater':
        return result
    width=64 if kind in ('front','back') else WIDTHS[kind]
    height=64 if kind in ('front','back') else 32
    out=result.copy()
    for sy in range(0,source.height,height):
        for sx in range(0,source.width,width):
            frame=source.crop((sx,sy,sx+width,sy+height))
            current=result.crop((sx,sy,sx+width,sy+height))
            hair=may_hair_mask(frame,current,kind)
            for x,y in hair:
                neighbors=[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
                # Broad white locks with a single light-gray boundary shade.
                # Keep the outer silhouette line, but remove all interior dark dots.
                outside=any(0<=xx<width and 0<=yy<height and frame.getpixel((xx,yy))==0
                            for xx,yy in neighbors)
                if frame.getpixel((x,y))==8 and outside:
                    color=8
                elif any(n not in hair for n in neighbors):
                    color=7
                else:
                    color=14
                out.putpixel((sx+x,sy+y),color)
    return out


def clean_may_fringe_speckles(result, kind):
    """Flatten the leftover white/peach pair above the front-facing blue eyes."""
    if kind=='front':
        out=result.copy()
        # Isolated skin-colored source highlight enclosed by the right fringe.
        out.putpixel((34,16),7)
        return out
    if kind in ('back', 'underwater'):
        return result
    out=result.copy()
    width=WIDTHS[kind]
    for sx in range(0,result.width,width):
        for y in range(result.height-2):
            for x in range(sx,sx+width-4):
                row=tuple(result.getpixel((x+k,y)) for k in range(5))
                if row not in ((7,14,7,2,7),(7,2,7,14,7)):
                    continue
                iris_x=x+(3 if row[1]==14 else 1)
                if result.getpixel((iris_x,y+2))!=6:
                    continue
                # Match both orientations, restricted to the fringe above an iris.
                out.putpixel((x+1,y),7)
                out.putpixel((x+3,y),7)
    return out


def brendan_back_head_edits(frame_index):
    """Hand-traced hair and wrapping headband, translated to each throwing pose."""
    dx,dy=((0,0),(5,1),(-6,2),(4,-1))[frame_index]
    hair_rows={26:(24,30),27:(24,30),28:(24,30),29:(23,30),30:(23,31),
               31:(22,34),32:(22,33),33:(21,32),34:(22,32),35:(23,32),
               36:(24,31),37:(25,31),38:(26,30),39:(27,30)}
    band_rows={29:(30,32),30:(28,32),31:(27,31),32:(25,29),33:(24,28),
               34:(24,26),35:(25,25)}
    hair={(x+dx,y+dy) for y,(a,b) in hair_rows.items() for x in range(a,b+1)}
    band={(x+dx,y+dy) for y,(a,b) in band_rows.items() for x in range(a,b+1)}
    return hair,band


def clean_brendan_back_head(source, frame, frame_index):
    out=frame.copy()
    hair,band=brendan_back_head_edits(frame_index)
    for x,y in hair:
        if frame.getpixel((x,y)) not in (7,8,14,15):
            continue
        neighbors=[source.getpixel((xx,yy)) for xx,yy in
                   ((x-1,y),(x+1,y),(x,y-1),(x,y+1))]
        # Retain the silhouette, but replace the abrupt solid-gray block with
        # the same light-gray shading used by the white hair above it.
        if 0 not in neighbors:
            out.putpixel((x,y),7)
    for p in band:
        if frame.getpixel(p) in (7,8,13,14,15) and source.getpixel(p):
            out.putpixel(p,13)
    return out


def draw_back(source, who):
    out=source.copy()
    for y in range(0,source.height,64):
        original=source.crop((0,y,64,y+64))
        frame,_=outfit_frame(original,who,'back')
        if who=='brendan':
            frame=clean_brendan_back_head(original,frame,y//64)
        out.paste(frame,(0,y))
    return out


def draw_overworld(source, who, mode):
    out=source.copy()
    if mode=='underwater':
        return out
    width=WIDTHS[mode]
    for start in range(0,source.width,width):
        original=source.crop((start,0,start+width,32))
        frame,cap_bottom=outfit_frame(original,who,mode)
        # Orange utility-belt/pouch trim, below the previous collar placement.
        cloth=[(x,y) for y in range(cap_bottom+4,min(cap_bottom+10,28))
               for x in range(max(0,width//2-3),min(width,width//2+4))
               if original.getpixel((x,y)) in (10,11,12,13)]
        if cloth:
            bottom=max(y for x,y in cloth)
            for x,y in cloth:
                if y==bottom:
                    frame.putpixel((x,y),11)
                elif y==bottom-1:
                    frame.putpixel((x,y),10)
        out.paste(frame,(start,0))
    return out


def rgba(im):
    out = im.convert('RGBA')
    out.putalpha(Image.frombytes('L', im.size, bytes(0 if x == 0 else 255 for x in im.tobytes())))
    return out


def paste_sprite(board, sprite, xy, scale):
    sprite = rgba(sprite).resize((sprite.width*scale,sprite.height*scale), Image.Resampling.NEAREST)
    board.paste(sprite, xy, sprite)


def overview(assets):
    board = Image.new('RGB', (1240, 1120), BG)
    d = ImageDraw.Draw(board)
    font = ImageFont.load_default(size=23)
    small = ImageFont.load_default(size=16)
    d.text((32,24), 'HOLON / EXPEDITION TEAM', font=font, fill=INK)
    d.text((32,59), 'CURRENT   |   White hair / blue eyes / steel blue + orange / leather accents', font=small, fill=INK)
    for col,who in enumerate(PEOPLE):
        x = 32+col*612
        d.text((x,108), who.upper()+' / FIELD RESEARCHER', font=font, fill=INK)
        d.text((x+65,150),'CURRENT',font=small,fill=INK)
        d.text((x+340,150),'MOCKUP',font=small,fill=INK)
        paste_sprite(board,assets[who]['front']['source'],(x,178),4)
        paste_sprite(board,assets[who]['front']['image'],(x+280,178),4)
        for row,mode in enumerate(('walking','running','mach_bike','surfing','fishing','underwater')):
            y=462+row*91
            d.text((x,y+30), mode.replace('_',' ').upper(),font=small,fill=INK)
            im=assets[who][mode]['image'];w=WIDTHS[mode]
            indices = (0,1,2) if mode not in ('surfing','fishing') else ((0,2,4) if mode=='surfing' else (0,4,8))
            for k,idx in enumerate(indices):
                fr=im.crop((idx*w,0,(idx+1)*w,32))
                paste_sprite(board,fr,(x+170+k*112,y),2)
    d.text((32,1060),'Both players: 10 movement sheets + battle front + 4-frame throwing back.',font=small,fill=INK)
    d.text((32,1087),'Open review.html for playback and inspection of every frame. Native sheets retain indexed palettes.',font=small,fill=INK)
    board.save(OUT/'overview.png')


def main():
    assets = {}
    hashes = {}
    records = []
    for who in PEOPLE:
        (OUT/who).mkdir(exist_ok=True)
        assets[who] = {}
        sources = {'front': ROOT/f'graphics/trainers/front_pics/{who}.png',
                   'back': ROOT/f'graphics/trainers/back_pics/{who}.png'}
        sources.update({m: ROOT/f'graphics/object_events/pics/people/{who}/{m}.png' for m in WIDTHS})
        for mode,path in sources.items():
            hashes[path] = hashlib.sha256(path.read_bytes()).hexdigest()
            original = subprocess.run(
                ['git', 'show', f'{SOURCE_REVISION}:{path.relative_to(ROOT).as_posix()}'],
                cwd=ROOT, check=True, capture_output=True).stdout
            source = Image.open(BytesIO(original))
            result = (draw_front(source,who) if mode=='front' else draw_back(source,who)
                      if mode=='back' else draw_overworld(source,who,mode))
            if who=='may':
                result=clean_may_bandana(source,result,mode)
                result=clean_may_hair(source,result,mode)
                result=clean_may_fringe_speckles(result,mode)
            result.putpalette(palette(source,who,mode=='underwater'))
            result.info.clear()
            result.save(OUT/who/f'{mode}.png', transparency=0, bits=4, optimize=False)
            saved = Image.open(OUT/who/f'{mode}.png')
            assert saved.mode == 'P' and saved.size == source.size
            assert max(saved.tobytes()) < 16
            assert all((a==0)==(b==0) for a,b in zip(source.tobytes(),saved.tobytes()))
            assert source.convert('RGB').tobytes() != saved.convert('RGB').tobytes()
            assets[who][mode] = {'source':source,'image':result}
            records.append({'who':who,'mode':mode,'width':64 if mode in ('front','back') else WIDTHS[mode],
                            'height':64 if mode in ('front','back') else 32,
                            'count':4 if mode=='back' else 1 if mode=='front' else source.width//WIDTHS[mode],
                            'vertical':mode=='back'})
    overview(assets)
    template = (OUT/'review.html').read_text()
    # Keep gallery data generated from the actual exported dimensions.
    start = template.index('/* ASSETS_START */')+len('/* ASSETS_START */')
    end = template.index('/* ASSETS_END */')
    (OUT/'review.html').write_text(template[:start]+'\nconst assets = '+json.dumps(records)+';\n'+template[end:])
    assert all(hashlib.sha256(p.read_bytes()).hexdigest()==h for p,h in hashes.items())
    print(f'Validated {len(records)} indexed sheets, {sum(r["count"] for r in records)} frames; source hashes unchanged.')


if __name__ == '__main__':
    main()
