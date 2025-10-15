from dataclasses import dataclass


@dataclass
class DailyUsage:
    date: str
    total_seconds: float

    @classmethod
    def from_row(cls, row):
        return cls(date=row[0], total_seconds=row[1])


@dataclass
class AppUsage:
    app_name: str
    date: str
    total_seconds: float

    @classmethod
    def from_row(cls, row):
        return cls(app_name=row[0], date=row[1], total_seconds=row[2])


@dataclass
class AppLimit:
    app_name: str
    limit_seconds: int

    @classmethod
    def from_row(cls, row):
        return cls(app_name=row[0], limit_seconds=row[1])
