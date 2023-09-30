import click
import io
import subprocess

from terminaltables import AsciiTable
import pandas as pd
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


from typing import List, cast, Tuple, Dict, Any
import datetime as dt

from timewreport.parser import TimeWarriorParser  # type: ignore
from timewreport.interval import TimeWarriorInterval  # type: ignore

from dateutil.relativedelta import relativedelta


class TWI:
    pass


def date_to_string(date: dt.date) -> str:
    """Format date as YYYY-MM-DD"""
    return date.strftime("%Y-%m-%d")


def get_intervals(tags: List[str]) -> List[TWI]:
    output = subprocess.run(["timew", "export", *tags], capture_output=True)
    json = io.StringIO(output.stdout.decode("utf-8"))
    result = cast(
        List[TWI], TimeWarriorParser._TimeWarriorParser__parse_intervals_section(json)
    )
    return result


def days_in_month(day: dt.date) -> List[dt.date]:
    """Given a <day> return a list of all days that are in the same month"""

    result: List[dt.date] = []
    first_day = day.replace(day=1)
    last_day = first_day + relativedelta(months=1, days=-1)

    offset = 0
    while True:
        new_day = first_day + relativedelta(days=offset)
        if new_day <= last_day:
            result.append(new_day)
            offset += 1
        else:
            break
    return result


def get_duration_per_day(
    intervals: List[TWI], days: List[dt.date]
) -> Dict[dt.date, dt.timedelta]:
    result: Dict[dt.date, dt.timedelta] = {}
    for day in days:
        result[day] = dt.timedelta(seconds=0)
    for interval in intervals:
        day = cast(dt.date, interval.get_start_date())
        if day in days:
            result[day] += cast(dt.timedelta, interval.get_duration())

    return result


def round(input: float, decimals: int) -> float:
    return int(input * 10**decimals) / 10**decimals


def get_date_and_hours_rows(
    intervals: List[TWI], day: dt.date
) -> List[Tuple[Any, Any]]:
    result: List[Tuple[str, float]] = []
    days = days_in_month(day)
    duration_per_day = get_duration_per_day(intervals, days)

    for day, duration in duration_per_day.items():
        result.append((date_to_string(day), round(duration.seconds / 3600, 2)))
    return result


# Export the csv + a sum row as PDF


def make_pdf_table(rows: List[Tuple[str, int]], output: str):
    #    data = pd.read_csv("your_file.csv").values.tolist()
    pdf = SimpleDocTemplate(output, pagesize=A4)

    # # Add Table to PDF
    table = Table(rows)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 14),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )

    pdf.build([table])


@click.command()
@click.option("--year", default=dt.date.today().year, help="What year")
@click.option("--month", default=dt.date.today().month, help="What month")
def main(year: int, month: int):
    output = "/tmp/reason_hours_oivvio_polite.pdf"
    intervals: List[TWI] = get_intervals(["§reasonstudios"])

    day = dt.date(year, month, 1)

    rows = get_date_and_hours_rows(intervals, day)
    total_duration = round(sum([duration for (_, duration) in rows]),2)

    rows.append(("total", total_duration))
    rows.insert(0, ("date", "hours"))

    table = AsciiTable(rows)
    print(table.table)

    make_pdf_table(rows, output)
    print(f"PDF report in {output}")


if __name__ == "__main__":
    main()
