<div align="center">

# Aayush Prakash

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=16&duration=2200&pause=900&color=A8E6A1&center=true&vCenter=true&width=650&lines=T-09%3A00%3A00+AND+COUNTING;SYSTEM%3A+NOMINAL;PAYLOAD%3A+CURIOSITY;GO+FOR+LAUNCH" alt="Typing animation" />

</div>

I got into programming to understand how systems work under the hood. I tend to take things apart until they fully click, then rebuild them from first principles. Most of what I build comes from that process.

---

## Currently

- Studying Computer Science
- Building a hardware-in-the-loop flight dynamics testbed
- Tinkering with a small evolution simulator on the side

---

## Live Feed

<!--LIVE:START-->
```
┌─ LIVE FEED ─────────────────────────────────────┐
  last commit   aayushpx: Delete flight_trace.s…
  streak        6 days                          
  commits       1079 this year                  
  as of         2026-06-30 11:51 UTC            
└──────────────────────────────────────────────────┘
```
<!--LIVE:END-->

---

## [Project Aphelion](https://github.com/aayushpx/project-aphelion)

Hardware-in-the-loop flight dynamics testbed for simulating and validating spacecraft motion. An ESP32 runs as a lightweight flight computer streaming live sensor telemetry, while Python handles trajectory propagation, state estimation, and mission-side analysis.

Currently implementing a 3DOF propagator using RK4 integration, with quaternion attitude kinematics and a J2 perturbation model.

`Embedded C++` `ESP-IDF v5.2` `Python` `NumPy` `ESP32-WROOM`

<p align="center">
  <img src="https://raw.githubusercontent.com/aayushpx/aayushpx/main/flight_trace.svg" width="500" alt="suborbital flight trace" />
  <br>
  <sub>RK4 powered ascent and ballistic flight, regenerated daily from the propagator model</sub>
</p>

---

## Hackathons

**[OrbitGuard](https://github.com/CelestiAI-Org/Orbitguard), ActInSpace New Zealand 2026**
<br>AI system for satellite collision avoidance decision-making. Skip-connection LSTM modeling how collision risk evolves over time, built in 24 hours.
<br>Role: Team Lead, product direction, system design, pitch
<br>`Python` `PyTorch` `TypeScript`

**[Exoplanet Explorer](https://github.com/CelestiAI-Org/nasa-hackathon-2025), NASA Space Apps New Zealand 2025, 2nd Place**
<br>ML pipeline converting telescope data into 3D habitability visualisations.
<br>Role: Team Lead, ML pipeline, Random Forest modelling, habitability scoring
<br>`Python` `scikit-learn` `Flask` `Three.js` `Docker`

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
<br>**ML & Data:** scikit-learn, PyTorch, Pandas
<br>**Embedded & Tools:** ESP-IDF, Git, Docker, Linux

---

<div align="center">

### Contribution Activity

<img src="https://raw.githubusercontent.com/aayushpx/aayushpx/output/github-contribution-grid-snake-dark.svg" width="800" />

</div>
