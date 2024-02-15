from dataclasses import dataclass
from typing import Any

from adh_sample_library_preview import BaseEvent, BaseReferenceData


@dataclass
class SampleReferenceDataTypePython(BaseReferenceData):
    SomeValue: float = None

    @staticmethod
    def fromJson(content: dict[str, Any]) -> 'SampleReferenceDataTypePython':
        base = BaseEvent.fromJson(content)
        result = SampleReferenceDataTypePython()
        result.__dict__.update(base.__dict__)

        if 'someValue' in content:
            result.SomeValue = float(content['someValue'])

        return result

    def toDictionary(self) -> dict[str, Any]:
        result = super().toDictionary()

        if self.SomeValue is not None:
            result['someValue'] = self.SomeValue

        return result
