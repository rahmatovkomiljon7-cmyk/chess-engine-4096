# engine.py — a 4,096-byte chess engine

A complete chess engine in Python that fits strictly within 4,096 bytes of source.

`engine.py` is **4,023 bytes** (1,991 bytes gzipped), contains no third-party
imports (standard library only), and still plays legal, reasonably strong chess:
verified move generation against `python-chess` perft on 9 positions, correct
mate detection, and a working iterative-deepening search.

## Run it

```bash
python engine.py            # depth 5 from the starting position
python engine.py 6          # think deeper
python engine.py 4 "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -"
```

Output is one line per iterative-deepening depth — `depth score bestmove`, score
in centipawns from the side to move — then the chosen move:

```
1 4 a2a4
2 0 a2a4
3 4 a2a4
4 0 a2a4
5 114 c2c4
bestmove c2c4
```

## What is inside

| Part | Implementation |
| --- | --- |
| Board | 12 bitboards (one per piece per colour), castling-rights and en-passant byte |
| Move encoding | one int per move: `from \| to << 6 \| promo << 12` (promo 1..4 = N,B,R,Q) |
| Attack tables | precomputed knight/king/pawn masks, ray tables walked at generation time (no magic bitboards — the constants would not fit) |
| Move generation | pseudo-legal generation + make/unmake legality filter via the undo stack |
| Search | alpha-beta with iterative deepening, a dict transposition table keyed on `(bitboards, side, castling, ep)` with depth/score/bound/best-move entries, and best-move ordering |
| Evaluation | material + piece-square tables, baked into one table per piece type; tapered king safety, bishop/knight centralisation, pawn advancement |

## Verified

- **Perft** exact against `python-chess` on 9 positions, depths 1–4:
  start position (20 / 400 / 8,902 / 197,281), Kiwipete (48 / 2,039 / 97,862),
  position 3 (14 / 191 / 2,812 / 43,238), position 4 (6 / 264 / 9,467),
  position 5 (44 / 1,486 / 62,379), position 6 (46 / 2,079 / 89,890), plus three
  promotion/en-passant/castling stress positions.
- **Mate in 1** found with score `99999`; free-queen capture found.
- Clean import under `python -W error` (no syntax warnings, nothing deprecated).

## Known limits (deliberate, to stay under the cap)

- No quiescence search, so scores oscillate on odd/even depths and tactics beyond
  the horizon are missed.
- No repetition or fifty-move detection, no UCI front end, single threaded.
- Search is pure Python: depth 6 from the start position takes ~12 s.

## Licence

MIT — see `LICENSE`.
