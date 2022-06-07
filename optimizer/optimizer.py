import typing

import attr
import numpy
from scipy import optimize

from diffusion_curve import DiffusionCurve, DiffusionCurves


@attr.s(auto_attribs=True)
class Measurement:
    x: float
    t: float
    p: float


@attr.s(auto_attribs=True)
class Measurements:
    data: typing.List[Measurement]

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, item: int) -> Measurement:
        return self.data[item]

    def __add__(self, other):
        return Measurements(data=self.data + other.data)

    @classmethod
    def from_diffusion_curve_first(cls, curve: DiffusionCurve) -> "Measurements":
        return Measurements(
            data=[
                Measurement(
                    x=curve.feed_compositions[i].first,
                    t=curve.feed_temperature,
                    p=curve.permeances[i][0].value,
                )
                for i in range(len(curve))
            ]
        )

    @classmethod
    def from_diffusion_curve_second(cls, curve: DiffusionCurve) -> "Measurements":
        return Measurements(
            data=[
                Measurement(
                    x=curve.feed_compositions[i].first,
                    t=curve.feed_temperature,
                    p=curve.permeances[i][1].value,
                )
                for i in range(len(curve))
            ]
        )

    @classmethod
    def from_diffusion_curves_first(cls, curves: DiffusionCurves) -> "Measurements":
        output = Measurements(data=[])
        for curve in curves:
            output += cls.from_diffusion_curve_first(curve)
        return output

    @classmethod
    def from_diffusion_curves_second(cls, curves: DiffusionCurves) -> "Measurements":
        output = Measurements(data=[])
        for curve in curves:
            output += cls.from_diffusion_curve_second(curve)
        return output


@attr.s(auto_attribs=True)
class PervaporationFunction:
    n: int
    m: int

    alpha: float
    a: typing.List[float]
    b: typing.List[float]

    @classmethod
    def from_array(
        cls, array: typing.Union[typing.List[float], numpy.ndarray], n: int, m: int
    ) -> "PervaporationFunction":
        assert len(array) == 3 + n + m
        return cls(
            n=n,
            m=m,
            alpha=array[0],
            a=array[1: n + 2],
            b=array[n + 2:],
        )

    def __call__(self, x: float, t: float) -> float:
        return self.alpha * (
            numpy.exp(
                sum(self.a[i] * x**i for i in range(len(self.a)))
                - sum(self.b[i] * x**i for i in range(len(self.b))) / t
            )
        )


def get_initial_guess(n: int, m: int) -> typing.List[float]:
    return [1] * (3 + n + m)


def objective(data: Measurements, params: typing.List[float], n: int, m: int) -> float:
    error = 0
    foo = PervaporationFunction.from_array(array=params, n=n, m=m)
    for d in data:
        error += (foo(d.x, d.t) - d.p) ** 2
    return numpy.sqrt(error / len(data))


def fit(data: Measurements, n: int, m: int) -> PervaporationFunction:
    result = optimize.minimize(
        lambda params: objective(data, params, n=n, m=m),
        x0=numpy.array([1] * (3 + n + m)),
        method="Powell",
    )
    return PervaporationFunction.from_array(array=result.x, n=n, m=m)