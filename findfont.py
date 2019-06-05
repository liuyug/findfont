#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import argparse
import fontconfig


def list_font():
    for f in fontconfig.query():
        f = fontconfig.FcFont(f)
        for fa in f.family:
            print(fa[1], end=', ')
            break
    print()


def find_font(chars):
    """ return all fonts including char """
    ret = {}
    for f in fontconfig.query():
        f = fontconfig.FcFont(f)
        for string in chars:
            ch = string[0]
            if f.has_char(ch):
                families = [fa[1] for fa in f.family]
                if string not in ret:
                    ret[string] = []
                ret[string].append((families, f.file))
    for r in ret:
        ret[r] = sorted(ret[r], key=lambda x: x[0])
    return ret


def output_picture(findlist, margin=20, font_size=24):
    from PIL import Image, ImageDraw, ImageFont
    for ch in findlist:
        image = Image.new('RGB', (10000, 20000), 'white')
        draw = ImageDraw.Draw(image)
        h = margin
        max_w = margin
        for families, fontfile in findlist[ch]:
            font = ImageFont.truetype(fontfile, font_size)
            s = '[%s]: ' % (', '.join(['\'%s\'' % f for f in families]))
            fontname_width, fontname_height = font.getsize(s)
            font_width, font_height = font.getsize(ch)
            max_w = max((fontname_width + font_width + margin, max_w))
            x = margin
            y = h
            # font name
            draw.text((x, y), s, font=font, fill='black')
            # text
            x += fontname_width
            draw.text((x, y), ch, font=font, fill='black')
            h += (font_height + 10)
        image = image.crop((0, 0, max_w + margin, h + margin))
        ext = 'gif'
        output_name = '%s.%s' % (ch, ext)
        with open(output_name, 'wb') as f:
            image.save(f, ext)
        print('Output picture: ' % output_name)
        del image


def output_stdout(findlist):
    for ch in findlist:
        for fontname, fontfile in findlist[ch]:
            s = '%s: %s' % (fontname, ch)
            print(s)


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('chars', help='input characters',
                       nargs='*')
    parse.add_argument('--list',
                       help='list system fonts',
                       action='store_true')
    parse.add_argument('--outpic',
                       help='output as picture',
                       action='store_true')
    args = parse.parse_args()

    if args.list:
        list_font()
    elif args.outpic and args.chars:
        findlist = find_font(args.chars)
        output_picture(findlist)
    elif args.chars:
        findlist = find_font(args.chars)
        output_stdout(findlist)
    else:
        parse.print_help()


if __name__ == '__main__':
    main()
