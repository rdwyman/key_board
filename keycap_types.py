from typing import TypedDict, NotRequired

# 6 dot braille
D1 = 1 << 0
D2 = 1 << 1
D3 = 1 << 2
D4 = 1 << 3
D5 = 1 << 4
D6 = 1 << 5

# 8 dot braille
D7 = 1 << 6
D8 = 1 << 7


class Glyph(TypedDict):
    pass


class BrailleGlyph(Glyph):
    encoding: str


class LetterGlyph(Glyph):
    fontFile: str


class KeyCapData(TypedDict):
    letter: str
    cap: CapData
    stems: list[StemData]
    glyphs: list[Glyph]
    children: list[KeyCapData]


class PartialKeyCap(TypedDict, total=False):
    pass
