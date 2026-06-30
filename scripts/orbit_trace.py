"""
Runs a real RK4 numerical integration of a 2-body orbit and renders the
resulting trajectory as a standalone SVG. No external plotting libraries,
the SVG path is built directly from the simulation output so the image
genuinely reflects the math, not a canned graphic.

Outputs to: orbit_trace.svg
"""

import math

MU = 398600.4418  # earth standard gravitational parameter, km^3/s^2

# initial state: a simple eccentric orbit, position (km) and velocity (km/s)
state0 = [8000.0, 0.0, 0.0, 7.2]  # x, y, vx, vy


def derivatives(state):
    x, y, vx, vy = state
    r = math.sqrt(x * x + y * y)
    ax = -MU * x / r**3
    ay = -MU * y / r**3
    return [vx, vy, ax, ay]


def rk4_step(state, dt):
    k1 = derivatives(state)
    k2 = derivatives([state[i] + dt / 2 * k1[i] for i in range(4)])
    k3 = derivatives([state[i] + dt / 2 * k2[i] for i in range(4)])
    k4 = derivatives([state[i] + dt * k3[i] for i in range(4)])
    return [
        state[i] + dt / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
        for i in range(4)
    ]


def simulate(steps=1500, dt=20.0):
    state = state0[:]
    points = []
    for _ in range(steps):
        state = rk4_step(state, dt)
        points.append((state[0], state[1]))
    return points


def render_svg(points, path="orbit_trace.svg"):
    size = 500
    margin = 40
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    max_extent = max(max(abs(v) for v in xs), max(abs(v) for v in ys))
    scale = (size / 2 - margin) / max_extent

    def to_svg(x, y):
        return size / 2 + x * scale, size / 2 - y * scale

    path_data = ""
    for i, (x, y) in enumerate(points):
        sx, sy = to_svg(x, y)
        path_data += f"{'M' if i == 0 else 'L'} {sx:.2f} {sy:.2f} "

    earth_x, earth_y = to_svg(0, 0)
    earth_r = 6371 * scale  # earth radius drawn to scale

    svg = f'''<svg viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{size}" height="{size}" fill="none"/>
  <circle cx="{earth_x:.2f}" cy="{earth_y:.2f}" r="{earth_r:.2f}" fill="#3a6ea5" opacity="0.85"/>
  <path d="{path_data}" fill="none" stroke="#A8E6A1" stroke-width="1.6"/>
  <circle cx="{points[0][0]*scale + size/2:.2f}" cy="{size/2 - points[0][1]*scale:.2f}" r="3" fill="#ffffff"/>
</svg>'''

    with open(path, "w") as f:
        f.write(svg)


if __name__ == "__main__":
    pts = simulate()
    render_svg(pts)
