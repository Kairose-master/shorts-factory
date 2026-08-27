def s_bowl(d, c, rng, w, p, cx, cy, s):
    bw = s * 0.44
    bot = s * 0.26
    h = s * 0.26
    body = [(cx - bw, cy - h * 0.2), (cx + bw, cy - h * 0.2),
            (cx + bot, cy + h), (cx - bot, cy + h), (cx - bw, cy - h * 0.2)]
    wob(d, body, c, rng, w, 2.6)
    rim = []
    for i in range(44):
        t = math.tau * i / 43
        rim.append((cx + math.cos(t) * bw, cy - h * 0.2 + math.sin(t) * s * 0.07))
    wob(d, rim, c, rng, w, 2.4)
    for k in range(3):
        ph = p * math.tau + k * 2.1
        pts = []
        for i in range(30):
            t = i / 29
            x = cx - bw * 0.55 + t * bw * 1.1
            y = cy - h * 0.2 + s * (0.02 + 0.02 * k) + math.sin(t * 9 + ph) * s * 0.018
            pts.append((x, y))
        wob(d, pts, c, rng, w, 2.0)


def s_steam(d, c, rng, w, p, cx, cy, s):
    for k in range(3):
        ph = p * math.tau * 1.5 + k * 2.0
        pts = []
        for i in range(36):
            t = i / 35
            x = cx + (k - 1) * s * 0.22 + math.sin(t * 5 + ph) * s * 0.07 * (1 - t * 0.4)
            y = cy + s * 0.35 - t * s * 0.75
            pts.append((x, y))
        wob(d, pts, c, rng, w, 2.4)


def s_signboard(d, c, rng, w, p, cx, cy, s):
    sway = 0.05 * math.sin(p * math.tau)
    tx, ty = cx, cy - s * 0.42
    bx, by = cx + sway * s, cy + s * 0.05
    wob(d, [(tx - s * 0.3, ty), (tx + s * 0.3, ty)], c, rng, w, 2.4)
    wob(d, [(tx - s * 0.16, ty), (bx - s * 0.16, by - s * 0.28)], c, rng, w, 2.0)
    wob(d, [(tx + s * 0.16, ty), (bx + s * 0.16, by - s * 0.28)], c, rng, w, 2.0)
    box_pts = [(bx - s * 0.34, by - s * 0.28), (bx + s * 0.34, by - s * 0.28),
               (bx + s * 0.34, by + s * 0.14), (bx - s * 0.34, by + s * 0.14),
               (bx - s * 0.34, by - s * 0.28)]
    wob(d, box_pts, c, rng, w, 2.6)
    for i in range(3):
        y = by - s * 0.20 + i * s * 0.11
        wob(d, [(bx - s * 0.24, y), (bx + s * 0.24 - i * s * 0.1, y)], c, rng, w, 1.8)


def s_queue(d, c, rng, w, p, cx, cy, s):
    for k in range(6):
        drift = math.sin(p * math.tau + k) * s * 0.012
        px = cx - s * 0.42 + k * s * 0.17
        py = cy + s * 0.1 + drift
        r = s * 0.055
        pts = []
        for i in range(26):
            t = math.tau * i / 25
            pts.append((px + math.cos(t) * r, py - s * 0.16 + math.sin(t) * r))
        wob(d, pts, c, rng, w, 2.0)
        wob(d, [(px, py - s * 0.16 + r), (px, py + s * 0.14)], c, rng, w, 2.2)
    wob(d, [(cx - s * 0.5, cy + s * 0.2), (cx + s * 0.5, cy + s * 0.2)], c, rng, w, 2.4)


def s_period(d, c, rng, w, p, cx, cy, s):
    pulse = 1 + 0.06 * math.sin(p * math.tau)
    pts = []
    for i in range(44):
        t = math.tau * i / 43
        pts.append((cx + math.cos(t) * s * 0.085 * pulse, cy + math.sin(t) * s * 0.085 * pulse))
    wob(d, pts, c, rng, w, 2.2)
