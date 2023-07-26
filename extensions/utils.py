from . import jalali
from django.utils import timezone
import convert_numbers

def jalali_convertor(time):
    jmonths = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی",
                "بهمن", "اسفند"]
    time = timezone.localtime(time)
    time_to_str = "{},{},{}".format(time.year, time.month, time.day)
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    output = "{} {} {}، ساعت {}:{}".format(
        convert_numbers.english_to_persian(time_to_tuple[2]),
        jmonths[time_to_tuple[1] - 1],
        convert_numbers.english_to_persian(time_to_tuple[0]),
        convert_numbers.english_to_persian(time.hour),
        convert_numbers.english_to_persian(time.minute)
    )
    return output