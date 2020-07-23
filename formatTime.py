# import statements
from datetime import datetime, timedelta

# returns the current formatted date according to the ISO 8601 standard which is what Marketo uses as standard
def formattedDateNow():
    return datetime.now().replace(microsecond=0).astimezone().isoformat()

# returns the formatted date of n days ago according to the ISO 8601 standard which is what Marketo uses as standard
def formattedDateNDaysAgo(n):
    return (datetime.now() - timedelta(days=n)).replace(microsecond=0).astimezone().isoformat()
