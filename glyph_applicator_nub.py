import build123d as bd
from typing import TypedDict


class NubArgs(TypedDict):
    length: float


def make_nub(keyCap: bd.Compound, args: NubArgs) -> bd.Compound | None:
    # TODO: Implement
    return bd.Compound()
