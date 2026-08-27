def s_spark(d, c, rng, w, p, cx, cy, s):
    pulse = 1 + 0.05 * math.sin(p * math.tau)
    for k in range(4):
        a = math.tau * k / 4 + math.tau * p * 0.05
        pts = []
        for i in range(24):
            t = i / 23
            r = s * 0.42 * pulse * (1 - t) ** 1.6
            ang = a + (t - 0.5) * 0.5
            pts.append((cx + math.cos(ang) * r * 1.0, cy + math.sin(ang) * r * 1.0))
        wob(d, pts, c, rng, w, 2.4)
    pts = []
    for i in range(40):
        t = math.tau * i / 39
        r = s * 0.10 * pulse
        pts.append((cx + math.cos(t) * r, cy + math.sin(t) * r))
    wob(d, pts, c, rng, w, 2.0)


def s_cup(d, c, rng, w, p, cx, cy, s):
    top = s * 0.34
    bot = s * 0.20
    h = s * 0.40
    body = [(cx - top, cy - h), (cx + top, cy - h),
            (cx + bot, cy + h), (cx - bot, cy + h), (cx - top, cy - h)]
    wob(d, body, c, rng, w, 2.6)
    rim = []
    for i in range(40):
        t = math.tau * i / 39
        rim.append((cx + math.cos(t) * top, cy - h + math.sin(t) * s * 0.09))
    wob(d, rim, c, rng, w, 2.4)
    for k in range(3):
        bob = 0.03 * s * math.sin(p * math.tau + k * 1.9)
        bx = cx + (k - 1) * s * 0.16
        by = cy - h - s * 0.10 + bob
        blob = []
        for i in range(26):
            t = math.tau * i / 25
            blob.append((bx + math.cos(t) * s * 0.085, by + math.sin(t) * s * 0.075))
        wob(d, blob, c, rng, w, 2.2)


def s_coin(d, c, rng, w, p, cx, cy, s):
    pulse = 1 + 0.03 * math.sin(p * math.tau)
    for rr in (0.40, 0.31):
        pts = []
        for i in range(56):
            t = math.tau * i / 55
            pts.append((cx + math.cos(t) * s * rr * pulse, cy + math.sin(t) * s * rr * pulse))
        wob(d, pts, c, rng, w, 2.5)
    bar = s * 0.15
    wob(d, [(cx - bar, cy - s * 0.06), (cx + bar, cy - s * 0.06)], c, rng, w, 2.0)
    wob(d, [(cx - bar, cy + s * 0.04), (cx + bar, cy + s * 0.04)], c, rng, w, 2.0)
    wob(d, [(cx - bar * 0.75, cy - s * 0.20), (cx, cy + s * 0.16),
            (cx + bar * 0.75, cy - s * 0.20)], c, rng, w, 2.4)


def s_scale(d, c, rng, w, p, cx, cy, s):
    tilt = 0.13 * math.sin(p * math.tau)
    wob(d, [(cx, cy + s * 0.34), (cx, cy - s * 0.26)], c, rng, w, 2.6)
    wob(d, [(cx - s * 0.20, cy + s * 0.36), (cx + s * 0.20, cy + s * 0.36)], c, rng, w, 2.4)
    lx, ly = cx - s * 0.34, cy - s * 0.26 + tilt * s
    rx, ry = cx + s * 0.34, cy - s * 0.26 - tilt * s
    wob(d, [(lx, ly), (rx, ry)], c, rng, w, 2.5)
    for px, py, dp in ((lx, ly, 0.16), (rx, ry, 0.10)):
        wob(d, [(px, py), (px, py + s * 0.11)], c, rng, w, 2.0)
        pan = []
        for i in range(24):
            t = math.pi * i / 23
            pan.append((px + math.cos(math.pi + t) * s * 0.15,
                        py + s * 0.11 + math.sin(math.pi + t) * -s * dp))
        wob(d, pan, c, rng, w, 2.3)


def s_period(d, c, rng, w, p, cx, cy, s):
    pulse = 1 + 0.06 * math.sin(p * math.tau)
    pts = []
    for i in range(44):
        t = math.tau * i / 43
        pts.append((cx + math.cos(t) * s * 0.085 * pulse, cy + math.sin(t) * s * 0.085 * pulse))
    wob(d, pts, c, rng, w, 2.2)
