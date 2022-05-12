import attr
import yaml
import numpy
import typing

from pathlib import Path

from utils import AntoineConstants, R


@attr.s(auto_attribs=True)
class Component:
    name: str
    molecular_weight: float = attr.ib(converter=lambda value: float(value))
    antoine_constants: AntoineConstants

    @classmethod
    def from_dict(cls, d: typing.Mapping) -> 'Component':
        return Component(
            name=d['name'],
            molecular_weight=d['molecular_weight'],
            antoine_constants=AntoineConstants(**d['antoine_constants'])
        )

    def get_antoine_pressure(self, temperature: float) -> float:
        """
        Calculation of saturated pressure in kPa at a given temperature in K using Antoine equation (by the basis of 10)
        :param temperature: temperature in K
        :return: saturated pressure in kPa calculated with respect to constants and given temperature
        """
        return 10 ** (
            self.antoine_constants.a
            - self.antoine_constants.b / (temperature + self.antoine_constants.c)
        )

    def get_vaporisation_heat(self, temperature: float) -> float:
        """
        Calculation of Vaporisation heat in kJ/mol using Clapeyron-Clausius equation
        :param temperature: temperature in K
        :return: Vaporisation heat in kJ/mol
        """
        return (
            (temperature / (temperature + self.antoine_constants.c)) ** 2
            * R
            * self.antoine_constants.b
            * numpy.log(10)
        )


@attr.s(auto_attribs=True)
class Components:
    components: typing.Mapping[str, Component]

    @classmethod
    def load(cls, path: Path) -> 'Components':
        with open(path, 'r') as handle:
            _components = yaml.load(handle, Loader=yaml.FullLoader)

        output = Components(
            components={
                name: Component.from_dict(value) for name, value in _components.items()
            }
        )

        for name, component in output.components.items():
            setattr(output, name, component)

        return output