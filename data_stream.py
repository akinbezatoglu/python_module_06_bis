from abc import ABC, abstractmethod
from typing import Any, cast


class DataProcessor(ABC):
    def __init__(self, name: str) -> None:
        self._name: str = name
        self._storage: list[tuple[int, str]] = []
        self._rank: int = 0

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def _store(self, value: str) -> None:
        self._storage.append((self._rank, value))
        self._rank += 1

    def total_processed(self) -> int:
        return self._rank

    def remaining(self) -> int:
        return len(self._storage)

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


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            handled: bool = False
            for proc in self._processors:
                if proc.validate(element):
                    try:
                        proc.ingest(element)
                        handled = True
                    except ValueError:
                        continue
                    break
            if not handled:
                print(
                    "DataStream error - "
                    f"Can't process element in stream: {element}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        for proc in self._processors:
            print(
                f"{proc.name}: total {proc.total_processed()} items "
                f"processed, remaining {proc.remaining()} on processor"
            )


def consume(proc: DataProcessor, count: int) -> None:
    for _ in range(min(count, proc.remaining())):
        proc.output()


def main() -> None:
    print("=== Code Nexus - Data Stream ===")
    print()
    print("Initialize Data Stream...")
    stream: DataStream = DataStream()
    stream.print_processors_stats()
    print()
    print("Registering Numeric Processor")
    print()
    numeric: NumericProcessor = NumericProcessor()
    stream.register_processor(numeric)
    batch: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead",
            },
            {"log_level": "INFO", "log_message": "User wil is connected"},
        ],
        42,
        ["Hi", "five"],
    ]
    print(f"Send first batch of data on stream: {batch}")
    stream.process_stream(batch)
    stream.print_processors_stats()
    print()
    print("Registering other data processors")
    print()
    text: TextProcessor = TextProcessor()
    log: LogProcessor = LogProcessor()
    stream.register_processor(text)
    stream.register_processor(log)
    print("Send the same batch again")
    stream.process_stream(batch)
    stream.print_processors_stats()
    print()
    print(
        "Consume some elements from the data processors: "
        "Numeric 3, Text 2, Log 1"
    )
    consume(numeric, 3)
    consume(text, 2)
    consume(log, 1)
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
