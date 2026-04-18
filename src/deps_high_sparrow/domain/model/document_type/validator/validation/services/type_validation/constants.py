DATE_FORMATS = (
    "%d.%m.%Y",  # Day.Month.Year (e.g., 05.06.2025)
    "%d-%m-%Y",  # Day-Month-Year (e.g., 05-06-2025)
    "%m.%d.%Y",  # Month.Day.Year (e.g., 06.05.2025)
    "%m-%d-%Y",  # Month-Day-Year (e.g., 06-05-2025)
    "%m/%d/%Y",  # Month/Day/Year (e.g., 06/05/2025)
    "%d/%m/%Y",  # Day/Month/Year (e.g., 05/06/2025)
    "%d %b %Y",  # Day AbbreviatedMonth Year (e.g., 05 Jun 2025)
    "%Y-%m-%d",  # ISO 8601 date
    "%Y/%m/%d",  # Slash-separated ISO format
    "%d %B %Y",  # Day FullMonth Year
    "%b %d, %Y",  # AbbreviatedMonth Day, Year
    "%B %d, %Y",  # FullMonth Day, Year
    "%Y.%m.%d",  # Dot-separated ISO format
    "%Y %b %d",  # Year AbbreviatedMonth Day
    "%d-%b-%Y",  # Day-AbbreviatedMonth-Year
    "%d-%B-%Y",  # Day-FullMonth-Year
    "%Y%m%d",  # Compact ISO format
    "%d%m%Y",  # Compact DayMonthYear
    "%m%d%Y",  # Compact MonthDayYear
    "%d/%m/%y",  # Day/Month/2-digit Year
    "%m/%d/%y",  # Month/Day/2-digit Year
    "%d-%m-%y",  # Day-Month-2-digit Year
    "%m-%d-%y",  # Month-Day-2-digit Year
    "%d.%m.%y",  # Day.Month.2-digit Year
    "%m.%d.%y",  # Month.Day.2-digit Year
    "%Y-%m-%dT%H:%M:%S",  # ISO 8601 datetime
    "%Y-%m-%d %H:%M:%S",  # Space-separated datetime
    "%d %b %Y %H:%M:%S",  # Day AbbreviatedMonth Year Time
    "%d %B %Y %H:%M:%S",  # Day FullMonth Year Time
    "%Y-%m-%dT%H:%M:%S.%f",  # ISO 8601 datetime with microseconds
    "%Y-%m-%d %H:%M:%S.%f",  # Space-separated datetime with microseconds
    "%d/%m/%Y %H:%M:%S",  # Day/Month/Year Time
    "%m/%d/%Y %H:%M:%S",  # Month/Day/Year Time
    "%d-%m-%Y %H:%M:%S",  # Day-Month-Year Time
    "%m-%d-%Y %H:%M:%S",  # Month-Day-Year Time
    "%d.%m.%Y %H:%M:%S",  # Day.Month.Year Time
    "%m.%d.%Y %H:%M:%S",  # Month.Day.Year Time
    "%Y/%m/%d %H:%M:%S",  # Slash-separated ISO datetime
    "%Y.%m.%d %H:%M:%S",  # Dot-separated ISO datetime
    "%Y%m%dT%H%M%S",  # Compact ISO datetime
    "%Y-%m-%dT%H:%M:%S%z",  # ISO 8601 datetime with timezone offset
    "%Y-%m-%d %H:%M:%S%z",  # Space-separated datetime with timezone offset
    "%Y-%m-%dT%H:%M:%SZ",  # ISO 8601 UTC datetime
    "%Y-%m-%d %H:%M:%SZ",  # Space-separated UTC datetime
    "%a, %d %b %Y %H:%M:%S",  # RFC 2822 format
    "%A, %d %B %Y %H:%M:%S",  # Full weekday, day, full month, year, time
    "%a %b %d %H:%M:%S %Y",  # ctime() format
    "%d %b %Y %I:%M %p",  # Day AbbreviatedMonth Year 12-hour time
    "%d %B %Y %I:%M %p",  # Day FullMonth Year 12-hour time
    "%m/%d/%Y %I:%M %p",  # Month/Day/Year 12-hour time
    "%d/%m/%Y %I:%M %p",  # Day/Month/Year 12-hour time
    "%Y-%m-%d %I:%M %p",  # ISO date with 12-hour time
    "%Y/%m/%d %I:%M %p",  # Slash-separated ISO date with 12-hour time
    "%Y.%m.%d %I:%M %p",  # Dot-separated ISO date with 12-hour time
    "%Y%m%d %H%M%S",  # Compact datetime
    "%Y%m%d %I%M%p",  # Compact date with 12-hour time
    "%Y-%j",  # Year and day of the year
    "%Y-%m-%dT%H:%M:%S.%fZ",  # ISO 8601 UTC datetime with microseconds
    "%Y-%m-%dT%H:%M:%S.%f%z",  # ISO 8601 datetime with microseconds and timezone
    "%Y-%m-%dT%H:%M:%S%z",  # ISO 8601 datetime with timezone
    "%Y-%m-%dT%H:%M:%S.%f",  # ISO 8601 datetime with microseconds
    "%Y-%m-%dT%H:%M:%S",  # ISO 8601 datetime
    "%Y-%m-%d",  # ISO 8601 date
    "%Y/%m/%d",  # Slash-separated ISO date
    "%Y.%m.%d",  # Dot-separated ISO date
    "%d-%b-%Y",  # Day-AbbreviatedMonth-Year
    "%d-%B-%Y",  # Day-FullMonth-Year
    "%b %d, %Y",  # AbbreviatedMonth Day, Year
    "%B %d, %Y",  # FullMonth Day, Year
    "%d %b %Y",  # Day AbbreviatedMonth Year
    "%d %B %Y",  # Day FullMonth Year
    "%Y%m%d",  # Compact ISO date
    "%d%m%Y",  # Compact DayMonthYear
    "%m%d%Y",  # Compact MonthDayYear
    "%d/%m/%y",  # Day/Month/2-digit Year
    "%m/%d/%y",  # Month/Day/2-digit Year
    "%d-%m-%y",  # Day-Month-2-digit Year
    "%m-%d-%y",  # Month-Day-2-digit Year
    "%d.%m.%y",  # Day.Month.2-digit Year
    "%m.%d.%y",  # Month.Day.2-digit Year
)
