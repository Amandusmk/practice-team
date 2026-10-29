import random
from datetime import datetime, timedelta

CHEAP_BELOW = 1.50  # kr/kWh
HOURS_BACK = 24
HOURS_AHEAD = 24
BAR_WIDTH_PER_KR = 8  # bar characters per kr/kWh
DIVIDER_WIDTH = 40
GREEN = "\033[92m"
RED = "\033[91m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"


def fake_price():
    return round(random.uniform(0.40, 3.50), 2)


def start_of_hour(moment):
    return moment.replace(minute=0, second=0, microsecond=0)


def fake_hourly_prices(now, hours_back=HOURS_BACK, hours_ahead=HOURS_AHEAD):
    """Return [(hour_start, price)] from hours_back ago up to hours_ahead from now."""
    this_hour = start_of_hour(now)
    return [
        (this_hour + timedelta(hours=offset), fake_price())
        for offset in range(-hours_back, hours_ahead + 1)
    ]


def color_for(price):
    return GREEN if price < CHEAP_BELOW else RED


def render_current(price):
    label = "cheap" if price < CHEAP_BELOW else "expensive"
    return f"{BOLD}{color_for(price)}Price now: {price:.2f} kr/kWh ({label}){RESET}"


def render_row(hour, price, is_now):
    bar = "█" * round(price * BAR_WIDTH_PER_KR)
    marker = f" {BOLD}◀ now{RESET}" if is_now else ""
    return f"{hour:%a %H:%M} {color_for(price)}{bar} {price:.2f}{RESET}{marker}"


def render(now, hourly_prices):
    current_hour = start_of_hour(now)
    current_price = next(price for hour, price in hourly_prices if hour == current_hour)
    divider = f"{DIM}{'-' * DIVIDER_WIDTH}{RESET}"

    lines = [render_current(current_price), ""]
    for hour, price in hourly_prices:
        is_now = hour == current_hour
        if is_now:
            lines.append(divider)
        lines.append(render_row(hour, price, is_now))
        if is_now:
            lines.append(divider)
    return "\n".join(lines)


if __name__ == "__main__":
    now = datetime.now()
    print(render(now, fake_hourly_prices(now)))
