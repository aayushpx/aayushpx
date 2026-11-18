<img src="assets/header.svg" width="100%" alt="Aayush Prakash: simulation, embedded systems and machine learning">

I build things where software meets physics and hardware: microcontrollers, orbital mechanics and machine learning, mostly in C, C++ and Python. Studying Computer Science and Data Science in New Zealand.

<img src="assets/s1-launcher.svg" width="100%" alt="01 Launcher">

<img src="assets/launcher.webp" width="100%" alt="Launcher running on a LilyGO T-Display S3, wired up on a breadboard">

### [Launcher](https://github.com/aayushpx/Launcher)

A mission-control unit for the LilyGO T-Display S3. A state machine takes it from **SAFE → ARMED → COUNTDOWN → IN FLIGHT → LANDED**, with an abort path. An MPU6050 IMU feeds live acceleration and gyro data over I²C, telemetry streams out over Wi-Fi and MQTT, and every event lands in a ring-buffer mission log. Four screens, driven by a rotary encoder, all written in C on ESP-IDF.

`ESP-IDF` `C` `MPU6050` `I²C` `MQTT` `Wi-Fi` `PWM`

<img src="assets/s2-neo.svg" width="100%" alt="02 Neo">

<img src="assets/neo.webp" width="100%" alt="Neo on the T-Display S3: title screen, gameplay and the SYSTEM CRASH screen">

### [Neo](https://github.com/aayushpx/neo)

A Matrix dodge game for the T-Display S3. You're Neo, the bullets keep getting faster, and one hit is a **SYSTEM CRASH**. Procedural Matrix rain runs across 40 independent columns on the title screen, difficulty ramps bullet speed (120 → 600 px/s) and spawn rate together, and the high score is saved to flash, so it survives power-off. Custom sprites and two-button controls, written in C on ESP-IDF.

`ESP-IDF` `C` `Game loop` `NVS`

<img src="assets/s3-hackathons.svg" width="100%" alt="03 Hackathons">

<a href="https://github.com/CelestiAI-Org/spherex"><img src="assets/hk-spherex.svg" width="100%" alt="SPHERExPLORER: 3rd place, NASA Space Apps NZ 2026"></a>
<a href="https://github.com/CelestiAI-Org/nasa-hackathon-2025"><img src="assets/hk-exoplanet.svg" width="49%" alt="Exoplanet Explorer: 2nd place, NASA Space Apps NZ 2025"></a>
<a href="https://github.com/CelestiAI-Org/Orbitguard"><img src="assets/hk-orbitguard.svg" width="49%" alt="OrbitGuard: built in 24 hours at ActInSpace NZ 2026"></a>
<a href="https://github.com/CelestiAI-Org/midnight-hackathon"><img src="assets/hk-midnight.svg" width="49%" alt="Midnight HR: privacy-preserving salary verification, Midnight Hackathon 2026"></a>
<a href="https://github.com/aayushpx/forge"><img src="assets/hk-mlh-card.svg" width="49%" alt="MLH Global Hack Week: Agents 2026, six builds in one week"></a>

<sub>Hack Week builds: [FORGE](https://github.com/aayushpx/forge) · [TermGen](https://github.com/aayushpx/termgen) · [OrbitOps](https://github.com/aayushpx/orbitops) · [RepoLens](https://github.com/aayushpx/repolens) · [agent-memory](https://github.com/aayushpx/agent-memory) · [Commit Sage](https://github.com/aayushpx/commit-sage)</sub>

<img src="assets/s4-bench.svg" width="100%" alt="04 The bench">

| Project | What it is | Stack |
|:--|:--|:--|
| [Project Aphelion](https://github.com/aayushpx/project-aphelion) | Hardware-in-the-loop flight dynamics testbed: an ESP32 flight computer streams telemetry while Python propagates the trajectory. **Paused** while I study kinematics properly | C++ · Python |
| [16-bit CPU Simulator](https://github.com/aayushpx/16bit-cpu-simulator) | Custom ISA with a full fetch-decode-execute cycle, registers and memory | C++ |
| [Software Rasterizer](https://github.com/aayushpx/cpp-rasterizer) | A 2D renderer from raw pixel writes. No graphics API, just maths and memory | C++ |
| [Connected Component Detector](https://github.com/aayushpx/connected-component-detector) | DFS flood-fill over raw PPM images to find and classify regions. No libraries | C++ |
| [statsforensics](https://github.com/aayushpx/statistical-analysis-toolkit) | R package for EDA, hypothesis testing, regression and diagnostics | R |

<img src="assets/s5-telemetry.svg" width="100%" alt="05 Telemetry">

<!--LIVE:START-->
```text
┌─ LIVE FEED ───────────────────────────────────────────────┐
  last commit   aayushpx: chore: update live feed (1d ago)
  streak        5 days                                    
  commits       130 this month                            
  active repos  3 in last 30 days                         
  recent work   Python                                    
  as of         2026-11-17 15:36 UTC                      
└────────────────────────────────────────────────────────────┘
```
<!--LIVE:END-->

<img src="assets/s6-toolkit.svg" width="100%" alt="06 Toolkit">

**Languages** &nbsp; C · C++ · Python · TypeScript · JavaScript · R · Haskell · Rust · LaTeX
<br>**Embedded** &nbsp; ESP32 / ESP-IDF · I²C · MQTT · FreeRTOS · PlatformIO
<br>**ML & data** &nbsp; PyTorch · scikit-learn · Pandas · NumPy
<br>**Web & viz** &nbsp; Three.js · Flask · Streamlit
<br>**Tools** &nbsp; Git · Docker · Linux · Neovim
