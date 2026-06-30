# Aayush Prakash

**Embedded Systems / ML / Aerospace Software**

I got into programming to understand how systems work under the hood. I tend to take things apart until they fully click, then rebuild them from first principles. Most of what I build comes from that process.

---

## Currently

- Studying Computer Science
- Building Project Aphelion, a flight dynamics testbed
- Building an evolution simulator, an agent based ecosystem model

---

## Live Feed

<!--LIVE:START-->
```
last commit     aayushpx: Merge pull request #1 from aayushpx/aayushpx-patch-1 (0m ago)
streak          6 days
total commits   1059 contributions in the last year
as of           2026-06-30 11:02 UTC
```
<!--LIVE:END-->

---

## Project Aphelion

Hardware-in-the-loop flight dynamics testbed for simulating and validating spacecraft motion. An ESP32 runs as a lightweight flight computer streaming live sensor telemetry, while Python handles trajectory propagation, state estimation, and mission-side analysis.

Currently implementing a 3DOF propagator using RK4 integration, with quaternion attitude kinematics and a J2 perturbation model.

`Embedded C++` `ESP-IDF v5.2` `Python` `NumPy` `ESP32-WROOM`

[github.com/aayushpx/project-aphelion](https://github.com/aayushpx/project-aphelion)

---

## Evolution Simulator

Agent based ecosystem simulator exploring how simple survival and reproduction rules produce emergent population dynamics over generations.

---

## Hackathons

**OrbitGuard, ActInSpace New Zealand 2026**
AI system for satellite collision avoidance decision-making. Skip-connection LSTM modeling how collision risk evolves over time, built in 24 hours.
Role: Team Lead, product direction, system design, pitch
`Python` `PyTorch` `TypeScript`
[github.com/CelestiAI-Org/Orbitguard](https://github.com/CelestiAI-Org/Orbitguard)

**Exoplanet Explorer, NASA Space Apps New Zealand 2025, 2nd Place**
ML pipeline converting telescope data into 3D habitability visualisations.
Role: Team Lead, ML pipeline, Random Forest modelling, habitability scoring
`Python` `scikit-learn` `Flask` `Three.js` `Docker`
[github.com/CelestiAI-Org/nasa-hackathon-2025](https://github.com/CelestiAI-Org/nasa-hackathon-2025)

---

## Systems Built From Scratch

No frameworks, no shortcuts. The point was understanding the machine, not shipping fast.

| Project | What it does | Stack |
|---|---|---|
| [16-bit CPU Simulator](https://github.com/aayushpx/16bit-cpu-simulator) | Custom ISA with a full fetch-decode-execute cycle, registers, and memory. | C++ |
| [Connected Component Detector](https://github.com/aayushpx/connected-component-detector) | DFS flood-fill on raw PPM images to detect and classify connected regions. No libraries. | C++ |
| [C++ Software Rasterizer](https://github.com/aayushpx/cpp-rasterizer) | 2D renderer built from raw pixel writes. No graphics API, just math and memory. | C++ |
| [Binary / Decimal Converter](https://github.com/aayushpx/binary-decimal-converter) | CLI base conversion tool with input validation and error handling. | C++ |
| [Discrete Math Notes and Proofs](https://github.com/aayushpx/mathematical-proofs-and-discrete-structures) | Structured LaTeX system formalising mathematical reasoning across logic, algebra, coding theory, and discrete structures. | LaTeX |
| [MUITSA Website](https://aayushpx.github.io/muitsa-site/) | Student association site with modular architecture and GitHub Actions deployment. | HTML/CSS/JS |

---

## Skills

**Languages:** C++, Python, R, LaTeX
**ML & Data:** scikit-learn, PyTorch, Pandas
**Embedded & Tools:** ESP-IDF, Git, Docker, Linux
