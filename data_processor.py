from abc import ABC, abstractmethod
from typing import Any, cast


class DataProcessor(ABC):
    def __init__(self, name: str) -> None:
        self._name: str = name
        self._storage: list[tuple[int, str]] = []
        self._rank: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def _store(self, value: str) -> None:
        self._storage.append((self._rank, value))
        self._rank += 1

    def output(self) -> tuple[int, str]:
        if not self._storage:
            raise IndexError(f"{self._name}: no data left to output")
        return self._storage.pop(0)


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__("Numeric Processor")

    @staticmethod
    def _is_number(value: Any) -> bool:
        return isinstance(value, (int, float)) and not isinstance(value, bool)

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            items = cast(list[Any], data)
            return len(items) > 0 and all(self._is_number(v) for v in items)
        return self._is_number(data)

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        values: list[int | float] = data if isinstance(data, list) else [data]
        for value in values:
            self._store(str(value))


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__("Text Processor")

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            items = cast(list[Any], data)
            return len(items) > 0 and all(isinstance(v, str) for v in items)
        return isinstance(data, str)

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        values: list[str] = data if isinstance(data, list) else [data]
        for value in values:
            self._store(value)


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__("Log Processor")

    @staticmethod
    def _is_log(value: Any) -> bool:
        if not isinstance(value, dict):
            return False
        entry = cast(dict[Any, Any], value)
        return len(entry) > 0 and all(
            isinstance(k, str) and isinstance(v, str) for k, v in entry.items()
        )

    @staticmethod
    def _format(entry: dict[str, str]) -> str:
        if "log_level" in entry and "log_message" in entry:
            return f"{entry['log_level']}: {entry['log_message']}"
        return ", ".join(f"{k}: {v}" for k, v in entry.items())

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            items = cast(list[Any], data)
            return len(items) > 0 and all(self._is_log(v) for v in items)
        return self._is_log(data)

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        values: list[dict[str, str]] = (
            data if isinstance(data, list) else [data]
        )
        for value in values:
            self._store(self._format(value))


def extract(processor: DataProcessor, count: int, label: str) -> None:
    plural: str = "value" if count == 1 else "values"
    print(f"Extracting {count} {plural}...")
    for _ in range(count):
        try:
            rank, value = processor.output()
        except IndexError as err:
            print(f"Got exception: {err}")
            return
        print(f"{label} {rank}: {value}")


def test_numeric() -> None:
    print("Testing Numeric Processor...")
    processor: NumericProcessor = NumericProcessor()
    print(f"Trying to validate input '42': {processor.validate(42)}")
    print(f"Trying to validate input 'Hello': {processor.validate('Hello')}")
    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        processor.ingest("foo")
    except ValueError as err:
        print(f"Got exception: {err}")
    data: list[int | float] = [1, 2, 3, 4, 5]
    print(f"Processing data: {data}")
    processor.ingest(data)
    extract(processor, 3, "Numeric value")


def test_text() -> None:
    print("Testing Text Processor...")
    processor: TextProcessor = TextProcessor()
    print(f"Trying to validate input '42': {processor.validate(42)}")
    data: list[str] = ["Hello", "Nexus", "World"]
    print(f"Processing data: {data}")
    processor.ingest(data)
    extract(processor, 1, "Text value")


def test_log() -> None:
    print("Testing Log Processor...")
    processor: LogProcessor = LogProcessor()
    print(f"Trying to validate input 'Hello': {processor.validate('Hello')}")
    data: list[dict[str, str]] = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    print(f"Processing data: {data}")
    processor.ingest(data)
    extract(processor, 2, "Log entry")


def main() -> None:
    print("=== Code Nexus - Data Processor ===")
    print()
    test_numeric()
    print()
    test_text()
    print()
    test_log()


if __name__ == "__main__":
    main()
