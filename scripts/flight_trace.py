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
    points = [(0.0, 0.0)]
    apogee = (0.0, 0.0, 0.0)  # x, z, t

    while True:
        state = rk4_step(t, state, DT)
        t += DT
        x, z, vx, vz = state
        if z < 0:
            break
        points.append((x, z))
        if z > apogee[1]:
            apogee = (x, z, t)
        if t > 60:
            break

    return points, apogee


def render_svg(points, apogee, path="flight_trace.svg"):
    width, height = 600, 360
    margin = 50

    xs = [p[0] for p in points]
    zs = [p[1] for p in points]
    max_x = max(xs) * 1.08
    max_z = max(zs) * 1.25

    def to_svg(x, z):
        sx = margin + (x / max_x) * (width - 2 * margin)
        sy = (height - margin) - (z / max_z) * (height - 2 * margin)
        return sx, sy

    path_data = ""
    for i, (x, z) in enumerate(points):
        sx, sy = to_svg(x, z)
        path_data += f"{'M' if i == 0 else 'L'} {sx:.2f} {sy:.2f} "

    ground_y = to_svg(0, 0)[1]
    apo_x, apo_z, apo_t = apogee
    apo_sx, apo_sy = to_svg(apo_x, apo_z)
    impact_x, impact_z = points[-1]
    impact_sx, _ = to_svg(impact_x, 0)

    svg = f'''<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <line x1="{margin}" y1="{ground_y:.2f}" x2="{width - margin}" y2="{ground_y:.2f}" stroke="#4a4a4a" stroke-width="1"/>
  <path d="{path_data}" fill="none" stroke="#A8E6A1" stroke-width="1.8"/>
  <circle cx="{margin:.2f}" cy="{ground_y:.2f}" r="3" fill="#ffffff"/>
  <circle cx="{apo_sx:.2f}" cy="{apo_sy:.2f}" r="3" fill="#ffd166"/>
  <circle cx="{impact_sx:.2f}" cy="{ground_y:.2f}" r="3" fill="#ef476f"/>
  <text x="{apo_sx:.2f}" y="{apo_sy - 8:.2f}" fill="#ffd166" font-family="monospace" font-size="11" text-anchor="middle">apogee {apo_z:.0f}m @ t={apo_t:.1f}s</text>
  <text x="{impact_sx:.2f}" y="{ground_y - 8:.2f}" fill="#ef476f" font-family="monospace" font-size="11" text-anchor="middle">impact {impact_x:.0f}m downrange</text>
  <text x="{margin}" y="{height - 12}" fill="#888888" font-family="monospace" font-size="10">RK4, dt=0.01s, gravity + exponential drag + mass depletion</text>
</svg>'''

    with open(path, "w") as f:
        f.write(svg)


if __name__ == "__main__":
    pts, apo = simulate()
    render_svg(pts, apo)
