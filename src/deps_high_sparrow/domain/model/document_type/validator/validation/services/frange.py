from typing import Union


class frange:  # noqa: N801
    def __init__(
        self,
        start: Union[int, float],
        end: Union[int, float, None] = None,
        step: Union[int, float] = 1,
    ):
        self.start, self.end = (float(start), float(end)) if (end is not None) else (0.0, float(start))  # noqa: WPS358
        self.step = step
        self.pos = self.start

    def __contains__(self, value_to_check: Union[int, float]) -> bool:
        return self.start <= value_to_check <= self.end

    def __eq__(self, other_frange):
        return self.start == other_frange.start and self.end == other_frange.end

    def __str__(self):
        return f"frange [{self.start}; {self.end}]"

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return self

    def __next__(self):
        if (self.step > 0 and self.pos <= self.end) or (self.step < 0 and self.pos >= self.end):
            self.pos += self.step
            return round(self.pos - self.step, 6)
        raise StopIteration
