from typing import Union
import datetime
import random


def add_time(datetime_obj: datetime.datetime, days: int, hours: int, minutes: int, seconds: int) -> datetime.datetime: ...
def generate(minimum: datetime.datetime, maximum: datetime.datetime, local_random: random.Random) -> Union[int, float]: ...
