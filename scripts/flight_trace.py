"""
Runs a real RK4 numerical integration of a suborbital sounding rocket flight,
modeled after Project Aphelion's actual propagator: powered ascent with mass
depletion, gravity, exponential-density drag, then ballistic coast and descent.
Renders the resulting downrange vs altitude profile as a standalone SVG.

No external plotting libraries, the SVG path is built directly from the
simulation output, so the image reflects the real physics, not a stock graphic.

Outputs to: flight_trace.svg
"""

import math

G = 9.81  # m/s^2
DT = 0.01  # s, matches Aphelion's propagator step size

# vehicle config, matches the baseline profile in the project README
DRY_MASS = 1.0       # kg
PROP_MASS = 0.3       # kg
THRUST = 80.0         # N
BURN_TIME = 3.5        # s
PITCH_DEG = 85.0       # degrees from horizontal

# aerodynamic / atmosphere model
RHO0 = 1.225          # kg/m^3, sea level density
H_SCALE = 8500.0       # m, atmospheric scale height
CD = 0.5              # drag coefficient
AREA = 0.003           # m^2, reference area

mdot = PROP_MASS / BURN_TIME


def mass_at(t):
    if t < BURN_TIME:
        return DRY_MASS + PROP_MASS - mdot * t
    return DRY_MASS


def air_density(z):
    z = max(z, 0.0)
    return RHO0 * math.exp(-z / H_SCALE)


def derivatives(t, state):
    x, z, vx, vz = state
    m = mass_at(t)
    speed = math.hypot(vx, vz)

    ax_thrust = az_thrust = 0.0
    if t < BURN_TIME:
        pitch = math.radians(PITCH_DEG)
        ax_thrust = (THRUST / m) * math.cos(pitch)
        az_thrust = (THRUST / m) * math.sin(pitch)

    ax_drag = az_drag = 0.0
    if speed > 0:
        rho = air_density(z)
        drag_mag = 0.5 * rho * speed**2 * CD * AREA
        ax_drag = -drag_mag * (vx / speed) / m
        az_drag = -drag_mag * (vz / speed) / m

    ax = ax_thrust + ax_drag
    az = az_thrust + az_drag - G

    return [vx, vz, ax, az]


def rk4_step(t, state, dt):
    k1 = derivatives(t, state)
    k2 = derivatives(t + dt / 2, [state[i] + dt / 2 * k1[i] for i in range(4)])
    k3 = derivatives(t + dt / 2, [state[i] + dt / 2 * k2[i] for i in range(4)])
    k4 = derivatives(t + dt, [state[i] + dt * k3[i] for i in range(4)])
    return [
        state[i] + dt / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
        for i in range(4)
    ]


def simulate():
    state = [0.0, 0.0, 0.0, 0.0]  # x, z, vx, vz
    t = 0.0
    points = [(0.0, 0.0, 0.0)]  # x, z, t
    apogee = (0.0, 0.0, 0.0)  # x, z, t
    burnout = None

    while True:
        state = rk4_step(t, state, DT)
        t += DT
        x, z, vx, vz = state
        if z < 0:
            break
        points.append((x, z, t))
        if z > apogee[1]:
            apogee = (x, z, t)
        if burnout is None and t >= BURN_TIME:
            burnout = (x, z, t)
        if t > 60:
            break

    return points, apogee, burnout


def render_svg(points, apogee, burnout, path="flight_trace.svg"):
    width, height = 620, 380
    margin_left, margin_right, margin_top, margin_bottom = 60, 30, 30, 50

    xs = [p[0] for p in points]
    zs = [p[1] for p in points]
    max_x = max(xs) * 1.08
    max_z = max(zs) * 1.25

    plot_w = width - margin_left - margin_right
    plot_h = height - margin_top - margin_bottom

    def to_svg(x, z):
        sx = margin_left + (x / max_x) * plot_w
        sy = (height - margin_bottom) - (z / max_z) * plot_h
        return sx, sy

    # split the path into powered (burn) and unpowered (coast + descent) segments
    burn_path = ""
    coast_path = ""
    for i, (x, z, t) in enumerate(points):
        sx, sy = to_svg(x, z)
        if t <= BURN_TIME:
            burn_path += f"{'M' if i == 0 else 'L'} {sx:.2f} {sy:.2f} "
        else:
            if not coast_path:
                coast_path += f"M {sx:.2f} {sy:.2f} "
            else:
                coast_path += f"L {sx:.2f} {sy:.2f} "

    ground_y = to_svg(0, 0)[1]
    apo_x, apo_z, apo_t = apogee
    apo_sx, apo_sy = to_svg(apo_x, apo_z)
    impact_x, impact_z, _ = points[-1]
    impact_sx, _ = to_svg(impact_x, 0)
    burn_sx, burn_sy = to_svg(burnout[0], burnout[1])

    # background grid, four horizontal and vertical divisions
    grid_lines = ""
    for i in range(1, 4):
        gy = margin_top + (plot_h / 4) * i
        grid_lines += f'<line x1="{margin_left}" y1="{gy:.2f}" x2="{width - margin_right}" y2="{gy:.2f}" stroke="#2a2a2a" stroke-width="1"/>\n  '
    for i in range(1, 5):
        gx = margin_left + (plot_w / 5) * i
        grid_lines += f'<line x1="{gx:.2f}" y1="{margin_top}" x2="{gx:.2f}" y2="{height - margin_bottom}" stroke="#2a2a2a" stroke-width="1"/>\n  '

    # altitude axis labels
    axis_labels = ""
    for i in range(0, 5):
        val = max_z * (i / 4)
        gy = (height - margin_bottom) - (plot_h / 4) * i
        axis_labels += f'<text x="{margin_left - 8}" y="{gy + 3:.2f}" fill="#666666" font-family="monospace" font-size="9" text-anchor="end">{val:.0f}m</text>\n  '

    svg = f'''<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <rect x="{margin_left}" y="{margin_top}" width="{plot_w}" height="{plot_h}" fill="#161616"/>
  {grid_lines}
  {axis_labels}
  <line x1="{margin_left}" y1="{ground_y:.2f}" x2="{width - margin_right}" y2="{ground_y:.2f}" stroke="#666666" stroke-width="1.2"/>
  <path d="{burn_path}" fill="none" stroke="#ff7b54" stroke-width="2"/>
  <path d="{coast_path}" fill="none" stroke="#A8E6A1" stroke-width="2"/>
  <circle cx="{margin_left:.2f}" cy="{ground_y:.2f}" r="3.5" fill="#ffffff"/>
  <circle cx="{burn_sx:.2f}" cy="{burn_sy:.2f}" r="3" fill="#ff7b54"/>
  <circle cx="{apo_sx:.2f}" cy="{apo_sy:.2f}" r="3.5" fill="#ffd166"/>
  <circle cx="{impact_sx:.2f}" cy="{ground_y:.2f}" r="3.5" fill="#ef476f"/>
  <text x="{burn_sx + 6:.2f}" y="{burn_sy - 6:.2f}" fill="#ff7b54" font-family="monospace" font-size="10">burnout t={burnout[2]:.1f}s</text>
  <text x="{apo_sx:.2f}" y="{apo_sy - 10:.2f}" fill="#ffd166" font-family="monospace" font-size="11" text-anchor="middle">apogee {apo_z:.0f}m @ t={apo_t:.1f}s</text>
  <text x="{impact_sx:.2f}" y="{ground_y - 10:.2f}" fill="#ef476f" font-family="monospace" font-size="11" text-anchor="middle">impact {impact_x:.0f}m downrange</text>
  <text x="{margin_left}" y="{height - 14}" fill="#888888" font-family="monospace" font-size="10">RK4, dt=0.01s · powered ascent</text>
  <rect x="{margin_left + 168}" y="{height - 22}" width="10" height="10" fill="#ff7b54"/>
  <text x="{margin_left + 230}" y="{height - 14}" fill="#888888" font-family="monospace" font-size="10">coast + descent</text>
  <rect x="{margin_left + 348}" y="{height - 22}" width="10" height="10" fill="#A8E6A1"/>
</svg>'''

    with open(path, "w") as f:
        f.write(svg)


if __name__ == "__main__":
    pts, apo, burn = simulate()
    render_svg(pts, apo, burn)
