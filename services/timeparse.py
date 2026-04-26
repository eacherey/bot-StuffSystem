import re
from datetime import timedelta, datetime, timezone

def parse_time(timestr: str) -> timedelta:
    pattern = r"(?:(?P<weeks>\d+)w)?(?:(?P<days>\d+)d)?(?:(?P<hours>\d+)h)?(?:(?P<minutes>\d+)m)?(?:(?P<seconds>\d+)s)?"
    match = re.fullmatch(pattern, timestr.strip().lower())
    if not match or not match.group(0):
        raise ValueError("Неверный формат времени. Пример: 2h30m, 1d, 10m, 1w2d3h4m5s")
    kw = {k: int(v) if v else 0 for k, v in match.groupdict().items()}
    return timedelta(weeks=kw['weeks'], days=kw['days'], hours=kw['hours'], minutes=kw['minutes'], seconds=kw['seconds'])

def get_until_from_now(timestr: str) -> datetime:
    return datetime.now(timezone.utc) + parse_time(timestr)
