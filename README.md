# Modelling_Cortex

This repository is your research workspace for modelling cortical-style working-memory dynamics, with a strong focus on:

- diffusion-based sequential decision models (`ddpm/`)
- teacher ablations and student recovery experiments
- geometry/topology analysis of latent neural trajectories (ring structure, Procrustes, MDS, Wasserstein)
- supporting baselines and experiments (`drl/`, `ddm/`, `dynamic_observer/`)

---

## What this repository is for

The core experimental loop in this repo is:

1. Train or load a **teacher** model.
2. Build **ablated teacher variants** (nullspace directions or PCA directions).
3. Train **student** models on teacher targets.
4. Extract internal states/trajectories from teachers and students.
5. Compare model behaviour and internal geometry with:
   - sliced Wasserstein distances
   - ring/plane geometry metrics
   - Procrustes residuals
   - unified MDS embeddings

This makes it easier to answer questions like:

- which ablation directions most strongly alter representational geometry?
- which students recover teacher behaviour best?
- how do healthy vs ablated models separate target/distractor representations?

---

## Repository layout

Top-level structure (high-signal directories/scripts):

- `ddpm/` — main diffusion-model code, tasks, training, configs, and analysis tooling.
- `drl/` — RL-related model/training utilities.
- `ddm/` — drift-diffusion model baseline scripts.
- `dynamic_observer/` — additional observer/score-matching experiments.
- `analysis/` — extra analysis scripts and tests.
- `results/`, `results_link_sampler/`, `results_link_drl/`, `results_link_sampler_ext/` — experiment outputs/caches (some ignored/symlinked depending on machine).

Useful root scripts:

- `m-t-m_multiepoch.py` — train with targets sampled from a source model (supports ablation settings).
- `compare_model_responses.py` — compare sampling outputs across teacher/student runs; supports single-trial and full-sweep modes.
- `extract_teacher_states.py` — extract neural states from healthy/ablated teacher runs into `.npz`.
- `generate_all_ablated_teachers.sh` — generate 14 ablated teacher model folders.
- `extract_all_teacher_states.sh` — batch extraction for healthy + all ablated teachers.
- `run_all_teacher_student_sweeps.py` — automated teacher-student comparison sweeps across teacher seeds and ablations.
- `MDS.py`, `MDS_nonmetric.py`, `MDS_wasserstein.py` — dimensionality-reduction visualizations of inter-model distances.

---

## Environment and dependencies

There is no single pinned root dependency file yet, so environment setup is currently code-driven.

### Core Python dependencies used across scripts

- `python` 3.10+ (recommended)
- `torch`
- `numpy`
- `scipy`
- `scikit-learn`
- `pandas`
- `matplotlib`
- `tqdm`

### Project-specific dependency

Several scripts import `purias_utils` modules (for config loading, plotting/logging helpers, circle conversions).  
Make sure that package is available in your Python path/environment before running pipelines.

### Path assumptions to be aware of

Some analysis/training scripts currently contain machine-specific absolute paths (for example `/scratch3/.../behaviour_ddpm`).  
If you run on a different machine, update those constants or adapt scripts to resolve paths dynamically from repository root.

---

## Quick start

> Run from repository root.

### 1) Train from a config (DDPM)

```bash
ddpm.train.multiepoch ddpm/configs/<your_config>.yaml
```

### 2) Train a student against a source teacher (with optional ablation)

```bash
python m-t-m_multiepoch.py ddpm/configs/recovery/index_cued_first_diffusion_0.3_swap_recovery.yaml \
  --source_run_path results_link_sampler/index_cued_first_diffusion_0.3_swap_7 \
  --ablate_neuron 7
```

### 3) Compare teacher vs student responses

```bash
python compare_model_responses.py \
  --run_paths results_link_sampler/index_cued_first_diffusion_0.3_swap_7 results_link_sampler/<student_run> \
  --labels "Teacher" "Student" \
  --num_samples 512 \
  --out_dir results/comparison
```

### 4) Generate ablated teacher set

```bash
bash generate_all_ablated_teachers.sh
```

### 5) Extract teacher neural states (healthy + ablated)

```bash
bash extract_all_teacher_states.sh
```

### 6) Run cross-teacher student sweep comparisons

```bash
python run_all_teacher_student_sweeps.py
```

### 7) Build MDS visualizations

```bash
python MDS.py --kind all
```

---

## Key analysis outputs

Typical generated outputs include:

- per-run comparison plots and logs in `results/...`
- extracted state archives (`.npz`, `.pt`) for teacher/student trajectory analysis
- cached pairwise-distance matrices (Wasserstein / Procrustes / feature-space)
- 2D MDS projections for model-space visualization and interpretation

Supporting explanatory notes currently included in the repository:

- `FEATURE_VARIANCE_EXPLAINED.txt`
- `MATHEMATICAL_EXPLANATION.txt`
- `MDS_COMPARISON.txt`

These documents summarize interpretation choices and metric behavior behind the MDS workflows.

---

## Validation and testing status

This repository includes experiment/test scripts (for example `test_prep_ablation.py`, `validate_ablation.py`, `hazard_rate_test.py`, `dynamic_observer/*test.py`), but there is no single unified root test runner documented yet.

Recommended practice:

1. validate each workflow with the script-specific commands you are running,
2. keep output paths isolated per experiment,
3. save logs for long sweeps to make metric comparisons reproducible.

---

This README is tailored to the current repository structure and workflow conventions in `ShaiqAhmed17/Modelling_Cortex`, with emphasis on your ablation/recovery + representational-geometry analysis pipeline.
