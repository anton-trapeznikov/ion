import time

period_width = 4
duty_ratio = 0.5

opened_widh = period_width * duty_ratio / 100

start_time = time.time()
end_time = start_time + period_width * 3

periods = (end_time - start_time) // period_width
desired = opened_widh * periods

overflow = 0.0
cicle_count = 0

total_opened_width = 0

prev_open_time = None

while True:
    current_time = time.time()
    if current_time >= end_time:
        break

    period = 1 + (current_time - start_time) // period_width
    can_be_dropped = opened_widh * period

    if prev_open_time:
        total_opened_width += current_time - prev_open_time

    if total_opened_width < can_be_dropped:
        # open
        prev_open_time = time.time()
    else:
        # close
        prev_open_time = None

    time.sleep(0.02)

print('ШИМ %s' % duty_ratio)
print('Ожидание %s' % desired)
print('Отбор %s' % total_opened_width)
