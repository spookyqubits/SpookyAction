# Spooky Action · SpookyQubits

Collection 04: short classroom activities about quantum correlations. Play **Ghost Trio first, then Ghost Twins**. Both games support Solo mode and private Pass & Play turns on one shared phone. They use the established bold red, blue, purple, and cream SpookyQubits theme.

- **Ghost Trio** (`games/ghost-trio/`): three-player GHZ challenge. Build and lock a local response plan, audit all four question cases, and compare with the ideal GHZ joint distribution.
- **Ghost Twins** (`games/ghost-twins/`): two-player CHSH challenge. Compare the four-case plan audit with sampled quantum-model outcomes, then use the classroom lab to explore fresh random batches and finite-sample variation.

Each game includes a printable facilitator guide, an exact strategy enumeration, a question about common misconceptions, optional random-batch statistics, and browser-local saved progress. Private screens are covered on reload. No accounts, ads, analytics, external libraries, or network requests are needed to play. Different phones do not share a live session.

## What is being compared

The quick four-card challenge visits each permitted setting exactly once in a shuffled order. The plan stays fixed for the entire deck, so its score is an exhaustive audit rather than a random estimate. No fixed local strategy covers all four cases. The best covers three. There are 64 deterministic plans for Trio and 16 for Twins.

The separate classroom lab independently samples fresh uniform question cases each round. Its quantum outputs are sampled from the ideal joint distribution. A finite classical run can exceed 75% by chance. The ideal GHZ win probability is 1. The ideal CHSH probability is cos²(π/8), about 85.36%. Each individual modeled result has a fair marginal. The ordinary phone centrally sees every question: this is a classical teaching simulation, not a physical Bell test or evidence of entangled phones.

## Build and preview

The development source is `SpookyAction/src/` in the workspace. The published collection carries the same files under `source/`.

```sh
python3 build.py
python3 -m http.server 8080 --directory dist
```

The builder uses Python's standard library only. It creates `dist/`, `spooky-action-site.zip`, and `release-manifest.json`. `--output PATH` selects another generated directory. `--repository NAME` changes the repository name used in collection links. It publishes an explicit list of files, excluding conflict copies, verification files, and unrelated workspace documents.

Every game `index.html` contains its scripts and styles, so it can be opened or downloaded by itself. Use the complete classroom ZIP for working local navigation between both games and their guides. Saving can be unavailable when local storage is blocked.

## GitHub Pages

The intended separate repository is `spookyqubits/SpookyAction`, alongside `Ghosts_and_Gates`, `SpookySignals`, and `Spooky-Utilities`. Publish the contents of `dist/` at the root of `main`, and configure Pages to deploy from `main` → `/(root)`. `.nojekyll` is included.

## Sources and verification

- [Girish et al., Parallel Repetition for the GHZ Game: A Simpler Proof](https://arxiv.org/abs/2107.06156): definition and classical/quantum values of the GHZ game.
- [IBM Quantum Learning: CHSH game](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/chsh-game): local strategies, the entangled strategy, and its probabilities.

Mathematical checks enumerate all local response plans, compare the joint distributions against independent Born-rule calculations, verify local marginals and the GHZ pair marginals, and check sampling and scoring. UI checks cover complete Solo and Pass & Play runs, private handoffs, plan locking, comparison, the lab, persistence, and invalid saved data.

The game names and classroom sequence draw on two SpookyQubits proposal documents. The interface and code were prepared for SpookyQubits on 3 November 2026. No learning-gain or first-of-its-kind claim is made. No blanket license is assigned to existing artwork or linked research.
