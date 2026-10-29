import random

CHEAP_BELOW = 1.50  # kr/kWh
GREEN = "\033[92m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def fake_price():
    return round(random.uniform(0.40, 3.50), 2)


def render(price):
    color = GREEN if price < CHEAP_BELOW else RED
    label = "cheap" if price < CHEAP_BELOW else "expensive"
    return f"{BOLD}{color}Price now: {price:.2f} kr/kWh ({label}){RESET}"


if __name__ == "__main__":
    print(render(fake_price()))
