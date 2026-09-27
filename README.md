# STM32 PWM Player

An audio synthesizer made from things that should never have become an audio synthesizer.

Generate SINE wave from STM32 timer PWM.

No DAC.

No Sigma-Delta.

No low-pass filter.

No amplifier.

**No wires.**

Just raw GPIO energy directly injected into reality.

Signal transmission medium:

- human body
- static electricity
- regret

Put one hand on GND.

Hold a 3.5mm EarPods jack with the other.

Touch PE9.

The waveform travels through your flesh.

This should not work.

It works anyway.

Now with DTMF support.

## Features

- Timer PWM audio output
- JSON-driven playback
- Flesh-conducted signal path
- Extremely cursed signal integrity
- Probably FCC illegal in at least one timeline

## Usage

1. Build firmware:

```bash
make
```

Target board: `stm32f103zet6`

(modify as needed for your chip)

2. Flash firmware to STM32.

3. Human interface protocol:

- left hand -> GND
- right hand -> EarPods 3.5mm jack second pin
- PE9 -> audio source

Touch the EarPods pin to PE9.

If the stars align, you will hear DTMF tones leaking out of the void.

4. Play JSON music data:

```bash
python3 play_json.py /dev/ttyUSB0 harunoumi.json
```

## Warning

Do not use this project for medical, industrial, military, spiritual, metaphysical, or demon-summoning applications.

Incorrect usage may result in:

- loud noise
- undefined waveform behavior
- temporal DTMF leakage
- user absorption into hell

You have been informed.