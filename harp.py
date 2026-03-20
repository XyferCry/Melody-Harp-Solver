import system.lib.minescript as m
from components.minescript_plus import Inventory
import time
import random

last_state = None
last_click_time = 0

CLICK_COOLDOWN = 0.05


def get_state(items):
    return tuple((it.slot, it.item) for it in items)


def find_quartz(items):
    for i in range(7):
        slot = 37 + i
        it = next((x for x in items if x.slot == slot), None)

        if it and it.item and "quartz_block" in it.item:
            return slot

    return None


def click(slot):
    global last_click_time

    now = time.time()
    if now - last_click_time < CLICK_COOLDOWN:
        return

    # minimale variation (~8–12ms)
    delay = 0.01 + random.uniform(-0.002, 0.002)
    time.sleep(max(0.006, delay))

    Inventory.click_slot(slot)

    last_click_time = time.time()


while True:
    if m.screen_name() is None:
        time.sleep(0.05)
        continue

    items = m.container_get_items() or []
    state = get_state(items)

    if state != last_state:
        slot = find_quartz(items)

        if slot is not None:
            click(slot)

    last_state = state

    time.sleep(0.005)       
