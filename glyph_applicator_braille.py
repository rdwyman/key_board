from typing import TypedDict


class BrailleApplicatorContext(TypedDict):
    datum: str
    encoding: str
    center: tuple[float, float]
    dotDiameter: float
    dotHeight: float
    dotHorizontalSpacing: float
    dotVerticalSpacing: float


def brailleApplicator(shape, context: BrailleApplicatorContext):
    pass
