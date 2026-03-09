# 👾 Space Invaders — Pygame

A feature-rich **Space Invaders** arcade game built with Python and [Pygame](https://www.pygame.org/). Battle through escalating waves of diverse alien enemies, collect power-ups, and survive as long as you can!

---

## 🎮 Features

### Core Gameplay
- 🚀 Smooth animated player space ship with idle, move, and attack frames
- 💥 Explosion animations on enemy destruction
- ❤️ Lives system with red-flash damage feedback
- ⏸️ Pause / resume functionality
- 🔄 Instant restart on game over
- 🏆 Live HUD: score, lives, wave number, active power-ups
- 🛡️ Dynamic animated shield around the player when collected

### Enemy Types
- 👾 **Normal** — Standard animated aliens, 1 HP
- ⚡ **Fast** — 2× speed, fast-moving animated sprite, 1 HP
- 🛡️ **Tank** — Slow-moving, 3 HP, HP bar, large tank sprite
- 🔫 **Shooter** — Fires bombs at timed intervals, 2 HP
- 〰️ **ZigZag** — Unpredictable zigzag movement, unique ship sprite

### Wave System
- 📊 Hand-crafted waves 1–4 (wave 4 = **boss wave**)
- 📈 Formula-generated waves 5+ with increasing enemy variety
- 🎯 "WAVE X" and "BOSS WAVE" announcements between waves
- ⚙️ Dynamic difficulty scaling (enemy speed & fire rate increase per wave)

### Power-Ups (15% drop chance)
- **D** — DoubleShot (8s): fire two bullets simultaneously
- **R** — RapidFire (8s): halved shooting cooldown
- **S** — Shield: absorbs one hit
- **+** — Extra Life (up to 5 max)
- **B** — Bomb: destroys all enemies on screen

---

## 🕹️ Controls

| Key | Action |
|-----|--------|
| ← → Arrow Keys | Move player left / right |
| Space | Fire bullet |
| P | Pause / Resume |
| R | Restart (on Game Over screen) |

---

## 📦 Installation

### Prerequisites
- **Python 3.8+**
- **Pygame 2.x** or **Pygame-CE**

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-username/Mini-Projects.git
cd Mini-Projects/Space_Invader

# 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install pygame-ce     # or: pip install pygame

# 4. Run the game
python main.py
```

---

## 📁 Project Structure

```
Space_Invader/
│
├── main.py              # Entry point
├── game_manager.py      # Game loop, events, collisions, HUD, state
├── settings.py          # All constants, paths, colors, tuning values
├── player.py            # Player class (movement, power-up state, shield)
├── enemy.py             # Enemy hierarchy (Enemy, Fast, Tank, Shooter, ZigZag)
├── bullet.py            # BulletPool & EnemyBulletPool (multi-bullet support)
├── wave_manager.py      # Wave progression, difficulty scaling
├── powerup.py           # Power-up system (5 types, drop logic)
│
├── utils/
│   ├── __init__.py
│   ├── collision.py     # Collision detection helpers
│   └── helpers.py       # Safe asset loading utilities
│
├── assets/
│   └── images/          # All game sprites
│
└── README.md
```

---

## 🧠 Architecture

| Module | Responsibility |
|--------|---------------|
| `settings.py` | Centralized constants and configuration |
| `player.py` | Player entity (movement, power-up state, shield) |
| `enemy.py` | Enemy AI hierarchy (5 types with HP system) |
| `bullet.py` | Object-pooled bullet management |
| `wave_manager.py` | Wave progression and difficulty scaling |
| `powerup.py` | Power-up drops, effects, and collection |
| `game_manager.py` | Orchestrator (game loop, collisions, HUD, state) |
| `utils/` | Reusable helpers (collision math, asset loading) |

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
