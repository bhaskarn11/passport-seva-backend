from datetime import date, datetime
from uuid import uuid4


def generate_arn():
    now = datetime.utcnow()
    timestamp = str(datetime.timestamp(now)).split(".")
    timestamp = "".join(timestamp)
    arn = f"{now.strftime('%y')}-{timestamp}"
    return arn
