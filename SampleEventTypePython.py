from dataclasses import dataclass
from typing import Any

from adh_sample_library_preview import BaseEvent, UomValueInput

from SampleEnumerationPython import SampleEnumerationPython


@dataclass
class SampleEventTypePython(BaseEvent):
    SomeValueEnum: SampleEnumerationPython = None
    SomeValueUom: UomValueInput[float] = None
    SomeValueUnspecifiedUom: UomValueInput[float] = None
    SomeValueNoUom: float = None

    @staticmethod
    def fromJson(content: dict[str, Any]) -> 'SampleEventTypePython':
        base = BaseEvent.fromJson(content)
        result = SampleEventTypePython()
        result.__dict__.update(base.__dict__)

        if 'someValueEnum' in content:
            result.SomeValueEnum = SampleEnumerationPython[content['someValueEnum']]

        if 'someValueUom' in content:
            result.SomeValueUom = UomValueInput.fromJson(content['someValueUom'])

        if 'someValueUnspecifiedUom' in content:
            result.SomeValueUnspecifiedUom = UomValueInput.fromJson(
                content['someValueUnspecifiedUom']
            )

        if 'someValueNoUom' in content:
            result.SomeValueNoUom = float(content['someValueNoUom'])

        return result

    def toDictionary(self) -> dict[str, Any]:
        result = super().toDictionary()

        if self.SomeValueEnum is not None:
            result['someValueEnum'] = self.SomeValueEnum.name

        if self.SomeValueUom is not None:
            result['someValueUom'] = self.SomeValueUom.toDictionary()

        if self.SomeValueUnspecifiedUom is not None:
            result[
                'someValueUnspecifiedUom'
            ] = self.SomeValueUnspecifiedUom.toDictionary()

        if self.SomeValueNoUom is not None:
            result['someValueNoUom'] = self.SomeValueNoUom

        return result
