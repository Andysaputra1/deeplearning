# AI Trainer - Deep Learning Project

**AI Trainer is a computer vision and deep learning project for assessing exercise technique from body poses.** It focuses on four exercises: **push-ups, pull-ups, squats, and planks**. The research aims to turn movement patterns into a quality score that helps users assess their exercise form using video, without wearable sensors.

### AI model and approach

The core model is a **dense feed-forward autoencoder**, implemented with **TensorFlow/Keras**, with a separate trained model for each exercise. It learns to reconstruct features from examples of correct movements. During assessment, a larger reconstruction error indicates a greater deviation from the learned movement patterns; the backend converts that error into a quality score.

The model operates on **pose-derived statistical features**: joint angles summarized by their mean, standard deviation, minimum, maximum, and range. The report uses **MediaPipe Pose** to extract body landmarks for training. Its described autoencoder compresses the features through **64 and 32 neurons into a 16-neuron bottleneck**, then reconstructs them through **32 and 64 neurons**. Training uses Mean Squared Error (MSE), Adam, Gaussian noise, dropout, and L2 regularization. Pose estimation supplies the landmarks; the autoencoder performs the exercise-quality assessment through anomaly detection.

### Report at a glance

The report, **Exercise Quality Assessment Using Autoencoder and Pose-Derived Statistical Features**, investigates whether statistical joint-angle features and autoencoders can capture correct exercise patterns. It reports reconstruction **MSE around 0.03-0.05**, with more stable training behavior for push-up and plank and greater variation for squat and pull-up. These results describe reconstruction performance, not a classification accuracy percentage. Main limitations include camera viewpoint, limited training-data diversity, and the choice of scoring thresholds.

[Read the full report (PDF)](research/2702234094_ANDY%20SAPUTRA_20260122231752_COMP6826001_LG01_SBFN_conf.pdf) · [Read the research summary](research/README.md)

This repository contains the frontend, backend, trained models, notebooks, and report for the Deep Learning course at Bina Nusantara University (2025/2026). **The imported frontend is currently a standalone demo with a simulated counter; it is not connected to the backend's AI scoring API.** The backend also differs from the reported pipeline by accepting MoveNet-style keypoints and using FastAPI; see the research summary for the implementation differences.

## Repository structure

```text
AITrainer/                 Frontend imported from the original GitHub repository
Backend/                   FastAPI service and training notebooks
  model/                   Four Keras models, scalers, and training-error arrays
research/                  Original PDF report and research summary
link_github_frontend.txt    Original frontend repository reference
```

The frontend is a regular folder, so a normal clone includes its source without a submodule checkout. Its files match [Andysaputra1/AiTrainer](https://github.com/Andysaputra1/AiTrainer) at commit `d76f3dc`. Uncommitted local frontend changes are not included.

## Current implementation

- **Frontend:** React, TypeScript, Vite, Tailwind CSS, and a webcam preview with a simulated push-up counter (press Space to increment). Authentication and workout history use a localStorage mock in `src/mockSupabase.ts`.
- **Backend:** FastAPI and TensorFlow/Keras inference for plank, push-up, pull-up, and squat quality assessment.
- **Research:** autoencoder training and evaluation using pose-derived joint-angle statistics.

The imported frontend does not currently call the backend analysis API. It is the original repository version, and should not be confused with the complete integrated application described in the report. Its authentication is a local demonstration, not a real Supabase connection. The original frontend README is preserved with the upstream source; this root README documents the actual combined repository.

## Getting started

Prerequisites: Git, Python 3.11, Node.js 22.12+ and npm.

```powershell
git clone https://github.com/Andysaputra1/deeplearning.git
cd deeplearning
```

### Frontend

Run from the repository root:

```powershell
cd AITrainer
npm ci
npm run dev
```

Open the address printed by Vite, normally `http://localhost:5173`, and allow webcam access. No Supabase credentials are required for this upstream version. Use `npm run build` to create a production build and `npm run preview` to preview it.

Validation: `npm ci` and `npm run build` completed successfully for the unchanged upstream frontend. Webcam behavior and backend inference were not tested end to end during this repository consolidation.

### Backend

Open another terminal at the repository root:

```powershell
cd Backend
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Start the service from `Backend/` because model paths are relative to the working directory. Visit `http://127.0.0.1:8000/` to check `loaded_models`, which should include all four exercises. Interactive API documentation is at `http://127.0.0.1:8000/docs`.

`POST /analyze` accepts an exercise `type` (`plank`, `pushup`, `pullup`, or `squat`) and `history`, an array of frames containing MoveNet keypoints in their original order. Each keypoint has `x`, `y`, optional `score`, and optional `name`. Successful responses contain `score`, `mse`, `thresholds`, and `message`. Model-loading or analysis problems can return a zero score and a message; inspect the response body as well as the HTTP status.

The backend extracts joint angles, smooths angle sequences, computes five statistics, scales the feature vector, and calculates autoencoder reconstruction error. Its current score range is 10-100.

## Research and reproducibility

Read the [research summary and original PDF](research/README.md): **Exercise Quality Assessment Using Autoencoder and Pose-Derived Statistical Features**.

The report describes reconstruction MSE around **0.03-0.05**. These are reported reconstruction errors, not classification accuracy percentages, and have not been independently reproduced during repository consolidation.

Trained models for all four exercises are included in `Backend/model/`. The repository contains push-up, pull-up, and squat notebooks, but no plank notebook or complete training dataset. Notebook paths and training dependencies require separate setup. `Backend/test_manual.py` is a standalone video experiment requiring OpenCV and MediaPipe in addition to inference dependencies; it is not an automated API test.

## Team

| Name | Student ID | Contribution stated in the report |
| --- | --- | --- |
| Andy Saputra | 2702234094 | Web development, report |
| Bren Alden | 2702242594 | Model development, report |
| Jonathan Carlo | 2702210213 | Video editing, report, model development |

Deep Learning, COMP6826001, class LG01, Bina Nusantara University.
