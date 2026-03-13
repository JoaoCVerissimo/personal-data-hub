from pydantic import BaseModel


class ChartDataPoint(BaseModel):
    label: str
    value: int


class TimeSeriesPoint(BaseModel):
    date: str
    value: int
