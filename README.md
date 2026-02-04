# Aayush Prakash

**`Embedded Systems | ML for Aerospace | Spacecraft Telemetry`**

I'm a first-year CS student in New Zealand obsessed with rockets and spacecraft. Currently teaching myself embedded C++ by building a rocket flight computer from scratch, and applying ML to real space problems through hackathons. Long-term goal: flight dynamics engineer working on actual spacecraft systems.

---

## 🚀 What I'm Building Right Now

**[Rocket Telemetry System](https://github.com/aayushpx/rocket-telemetry-system)** - Because reading datasheets is more fun than it should be

Building a complete flight computer for model rockets using ESP32 and bare-metal C++. No Arduino libraries, no shortcuts. Currently writing custom sensor drivers with manual bit-banging because that's apparently how you actually learn this stuff. The goal is real-time sensor fusion, physics simulation, and eventually ML-based computer vision for autonomous recovery.

Right now: Writing microsecond-accurate C++ drivers for ultrasonic landing radar and implementing safe hardware-level interfacing to bridge 5V sensors with 3.3V ESP32 logic.

**Stack:** Embedded C++ • ESP-IDF v5.2 • ESP32-WROOM • Hardware Integration

---

## 🏆 Stuff I've Built at Hackathons

### [🛰️ OrbitGuard](https://github.com/CelestiAI-Org/Orbitguard)
**ActInSpace 2026** | Team Lead

Satellite operators get flooded with thousands of collision warnings daily. Most are noise. We built an AI system that learns which warnings actually matter by watching how risk evolves over time.

I led a team of 4 (aerospace engineer, ML engineer, software engineer, and me) over 24 hours to build both the tech and a business model. As team lead, I coordinated the technical work, helped shape the product direction, and pitched the final solution. Mostafa (ML engineer) designed the skip-connection LSTM that gave us 5x better accuracy, while I worked on understanding the problem space and making sure all the pieces fit together.

The hackathon was focused on space startups, so we didn't just build tech. We developed a business model canvas and pitched it as a SaaS product to judges. Nathan (aerospace engineer) brought the domain expertise, Jonty (software engineer) built the backend, and I made sure we had a story that made sense.

**What I did:** Team coordination, product direction, business model, final pitch  
**Tech stack:** Python, PyTorch, TypeScript

---

### [🌌 Exoplanet Explorer](https://github.com/CelestiAI-Org/nasa-hackathon-2025)
**NASA Space Apps Auckland 2025** | 2nd Place | Team Lead

We took 2nd place building a web app that detects exoplanets from telescope data and visualizes them in 3D. I was team lead and ML engineer for a group of 4. My job was to design the detection pipeline, train the Random Forest model on Kepler mission data, and build the habitability classifier.

The coolest part was seeing our model's predictions rendered as interactive 3D visualizations using Three.js. We deployed it live during the hackathon and showed the demo working.

Also learned a lot about leading a team under time pressure. Making quick decisions about what's realistic in 48 hours vs what's nice-to-have is harder than it sounds.

**What I worked on:** ML pipeline design, Random Forest training, habitability prediction, task allocation  
**Tech:** Python, scikit-learn, Flask, Three.js, Docker

---

## 🛠️ Technical Skills

### Languages & Frameworks
![C++](https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![C](https://img.shields.io/badge/C-00599C?style=for-the-badge&logo=c&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)

### ML & Data Science
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)

### Embedded & Hardware
![ESP-IDF](https://img.shields.io/badge/ESP--IDF-E7352C?style=for-the-badge&logo=espressif&logoColor=white)
![Arduino](https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=arduino&logoColor=white)

### Tools & Platforms
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

---

<p align="left">
  <img src="https://komarev.com/ghpvc/?username=aayushpx&label=Profile%20Views&color=blue" alt="Profile Views" />
</p>

---

*Currently balancing uni coursework with building things that might actually fly someday. If you're working on anything space-related, I'd love to hear about it.*
