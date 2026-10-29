# Cryptopals exercises

Python implementations of introductory cryptographic exercises: byte encodings, XOR analysis, repeated-key attacks, AES-ECB and padding.

## Contents

| File | Topics |
| --- | --- |
| `set1.py` | Hex/Base64, fixed XOR, single-byte XOR scoring, repeating-key XOR, Hamming-distance analysis, AES-ECB decryption and detection |
| `2.1.py` | PKCS#7 padding example |
| `4.txt`, `6.txt`, `7.txt`, `8.txt` | Challenge inputs |

The scripts are learning exercises with intermediate output, not a reusable cryptographic library. The fixed example keys are challenge fixtures.

## Run

Use Python 3 and install PyCryptodome in a virtual environment:

```bash
python -m pip install pycryptodome
python set1.py
python 2.1.py
```

Run from the repository root so the relative input-file paths resolve. `set1.py` executes its challenge examples sequentially and prints candidate keys and decrypted text.

## Reading guide

Start with encoding and XOR helpers, then inspect `break_repeating_key_xor` and `detect_ecb`. The interesting algorithmic steps are scoring candidate plaintexts, estimating key length from normalized Hamming distance, and recognizing repeated cipher blocks.

Original exercises: [Cryptopals](https://cryptopals.com/). This repository contains solutions and therefore spoilers. No comprehensive automated regression suite is included.
