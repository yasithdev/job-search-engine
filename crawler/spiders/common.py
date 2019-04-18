import datetime


def approximate_datetime(time, relative):
    # using simplistic year (no leap months are 30 days long.
    # WARNING: 12 months != 1 year
    unit_mapping = [('mic', 'microseconds', 1),
                    ('millis', 'microseconds', 1000),
                    ('sec', 'seconds', 1),
                    ('hour', 'hours', 1),
                    ('day', 'days', 1),
                    ('week', 'days', 7),
                    ('mon', 'days', 30),
                    ('year', 'days', 365)]
    try:
        tokens = relative.lower().split(' ')
        past = False
        if len(tokens) == 1:
            if tokens[0] == 'today':
                return time.strftime("%Y-%m-%d %H:%M")
            if tokens[0] == 'yesterday':
                return (time + datetime.timedelta(days=-1)).strftime("%Y-%m-%d %H:%M")
        elif tokens[-1] == 'ago':
            past = True
            tokens = tokens[:-1]
        elif tokens[0] == 'in':
            tokens = tokens[1:]

        units = dict(days=0, hours=0, seconds=0, microseconds=0)
        # we should always get pairs, if not we let this die and throw an exception
        while len(tokens) > 0:
            value = tokens.pop(0)
            if value == 'and':  # just skip this token
                continue
            else:
                value = float(value)

            unit = tokens.pop(0)
            for match, time_unit, time_constant in unit_mapping:
                if unit.startswith(match):
                    units[time_unit] += value * time_constant
            # negate timedelta if in past
            if past:
                for key in units.keys():
                    units[key] = -units[key]
        return (time + datetime.timedelta(**units)).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return None
