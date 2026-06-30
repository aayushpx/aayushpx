# Aayush Prakash

```
SYSTEM      Embedded Systems / ML / Aerospace Software
LOCATION    New Zealand
STATUS      See live feed below
```

I got into programming to understand how systems work under the hood, I tend to take things apart until they fully click, then rebuild them from first principles. Most of what I build comes from that process.

---

## Currently

```
> studying            Computer Science
> building            Project Aphelion, flight dynamics testbed
> building            Evolution Simulator, agent based ecosystem model
```

---

## Live Feed

<!--LIVE:START-->
```
last commit     loading...
streak          loading...
total commits   loading...
```
<!--LIVE:END-->

*Updates automatically via GitHub Actions, see [the workflow](.github/workflows/update-readme.yml).*

---

## Active — Project Aphelion

Hardware-in-the-loop flight dynamics testbed for simulating and validating spacecraft motion. An ESP32 runs as a lightweight flight computer streaming live sensor telemetry, while Python handles trajectory propagation, state estimation, and mission-side analysis.

```
PROPAGATOR    3DOF, RK4 integration
TARGET        Quaternion attitude kinematics, J2 perturbation model
HARDWARE      ESP32-WROOM, ESP-IDF v5.2
GROUND        Python, NumPy
```

→ [github.com/aayushpx/project-aphelion](https://github.com/aayushpx/project-aphelion)

---

## Active — Evolution Simulator

Agent based ecosystem simulator exploring how simple survival and reproduction rules produce emergent population dynamics over generations.

→ link coming soon

---

## Hackathons

**OrbitGuard** — ActInSpace New Zealand 2026
AI system for satellite collision avoidance decision-making. Skip-connection LSTM modeling how collision risk evolves over time, built in 24 hours.
`Team Lead, product direction, system design, pitch`
`Python · PyTorch · TypeScript`
→ [github.com/CelestiAI-Org/Orbitguard](https://github.com/CelestiAI-Org/Orbitguard)

**Exoplanet Explorer** — NASA Space Apps New Zealand 2025 · 2nd Place
ML pipeline converting telescope data into 3D habitability visualizations.
`Team Lead, ML pipeline, Random Forest modelling, habitability scoring`
`Python · scikit-learn · Flask · Three.js · Docker`
→ [github.com/CelestiAI-Org/nasa-hackathon-2025](https://github.com/CelestiAI-Org/nasa-hackathon-2025)

---

## Systems Built From Scratch

No frameworks, no shortcuts, the point was understanding the machine, not shipping fast.

| Project | Detail |
|---|---|
| [16-bit CPU Simulator](https://github.com/aayushpx/16bit-cpu-simulator) | Custom ISA. Full fetch-decode-execute cycle, registers, memory. |
| [Connected Component Detector](https://github.com/aayushpx/connected-component-detector) | DFS flood-fill on raw PPM images. No image libraries. |
| [C++ Software Rasterizer](https://github.com/aayushpx/cpp-rasterizer) | 2D renderer from raw pixel writes. No graphics API. |
| [Binary / Decimal Converter](https://github.com/aayushpx/binary-decimal-converter) | CLI base conversion with full input validation. |
| [Discrete Math: Notes & Proofs](https://github.com/aayushpx/mathematical-proofs-and-discrete-structures) | LaTeX system formalizing reasoning across logic, algebra, coding theory. |

**Also:** [MUITSA Website](https://aayushpx.github.io/muitsa-site/), student association site, modular architecture, CI/CD via GitHub Actions.

---

## Stack

```
Languages         C++ · Python · R · LaTeX
ML / Data         scikit-learn · PyTorch · Pandas
Embedded / Tools  ESP-IDF · Git · Docker · Linux
```
