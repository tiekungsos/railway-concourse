# Meridian Terminus

An inspectable 3D Victorian railway concourse built with Three.js — a single-span arched trainshed (~64 m span, 30 m rise, 180 m long) with lattice arch ribs, platforms, animated trains, and passengers.

**Live demo:** https://railway-concourse.vercel.app

## Features

- 19 twin-chord lattice arch ribs on 10 m bays, alternating solid/glazed roof bands
- Two animated trains with arrive/dwell/depart cycles, headlamps and rumble audio
- Passengers (rigged Quaternius characters, CC0) with real Walk/Idle clips — they walk, chat in pairs, queue, and board/alight through train doors while stopped
- Surrounding city: plaza forecourt, main road with moving + parked cars, brick building row, houses, public park with trees, football pitch, street lamps and traffic signs — walk out through the south portals
- Camera presets: Nave, Platform, Arcade, The Vault, Buffers, Section, Forecourt (key 0)
- Walk modes: first-person (1P) and third-person (3P) with collisions, footsteps, pointer-lock mouse look
- Mobile: virtual joystick + drag-look + hold-to-run in walk modes
- Planar floor reflections, env-map sheen, bloom, sun shafts + dust, warm point lamps
- Procedural WebAudio ambience — crowd murmur, reverb, announcements, train sounds

## Controls

| Key | Action |
|---|---|
| 1–6, 0 | Orbit view presets (0 = Forecourt) |
| 7 / 8 | Walk 1P / Walk 3P |
| WASD | Move (Shift = run) |
| Click | Pointer-lock mouse look |
| Esc | Release cursor |
| M | Ambience on/off |

URL params: `?v=1..6` view preset, `?m=fp` / `?m=tp` walk mode.

## Run locally

```sh
python3 -m http.server 8123
# open http://localhost:8123/
```

Any static file server works — everything is vendored (`vendor/`) and models are local (`train.glb`, `people/*.glb`).

## Structure

- `index.html` — the whole scene (renderer, architecture, people, audio, UI)
- `train_gen.py` / `person_gen.py` — Blender headless generators for `train.glb` / `person.glb`
- `people/` — Quaternius Ultimate Animated Character Pack (CC0), converted to GLB
- `vendor/` — three.js r160 + addons
