# Research Report

**Exercise Quality Assessment Using Autoencoder and Pose-Derived Statistical Features**

[Read the original report (PDF)](2702234094_ANDY%20SAPUTRA_20260122231752_COMP6826001_LG01_SBFN_conf.pdf)

Authors: Andy Saputra, Bren Alden, and Jonathan Carlo. Bina Nusantara University, Deep Learning, academic year 2025/2026. The PDF is preserved unchanged.

## Methodology

The report studies push-up, pull-up, squat, and plank assessment using an autoencoder trained on correct movements. The training pipeline uses MediaPipe Pose with 33 landmarks, calculates joint angles, and summarizes angle sequences using mean, standard deviation, minimum, maximum, and range (PTP).

The described autoencoder uses Gaussian noise (0.02), dense encoder layers of 64 and 32 units, a 16-unit bottleneck, decoder layers of 32 and 64 units, and a linear reconstruction output. It includes L2 regularization and dropout. Training uses Adam, MSE loss, early stopping, and learning-rate reduction.

## Reported results and limitations

The report describes reconstruction MSE around 0.03-0.05, closely aligned training and validation curves for push-up and plank, more variation for squat, and a small validation gap for pull-up. These are the authors' reported training observations, not independently reproduced benchmarks or classification accuracy measurements.

Limitations include sensitivity to camera viewpoint, limited dataset diversity, variation in correct exercise form, and threshold calibration. Proposed future work includes multiple-view pose estimation, more diverse datasets, error classification, and adaptive thresholds.

## Differences from the repository implementation

| Aspect | Report | Current source |
| --- | --- | --- |
| API framework | Flask | FastAPI in `Backend/main.py` |
| Pose pipeline | MediaPipe with 33 landmarks | Backend expects MoveNet-style keypoint histories |
| Quality score range | 5-100 | 10-100 |
| Upper error threshold | 95th percentile multiplied by 3 | 95th percentile multiplied by 4 |
| Feature dimensions | Describes a 30-dimensional vector | Backend extracts 30 features for plank/push-up/squat and 40 for pull-up before dimension adjustment |
| Web integration | Describes recording/uploading videos and receiving model scores | Imported upstream frontend is a standalone push-up demo with mocked authentication/history and no backend API calls |

The backend pads squat ankle-angle features with zeros because MoveNet lacks the MediaPipe foot landmarks. These differences should be considered when comparing the report with this checkout.

## Included artifacts

- [Trained models, scalers, and training-error arrays](../Backend/model/).
- [Push-up training notebook](../Backend/pushupmodel.ipynb).
- [Pull-up training notebook](../Backend/pullupmodel.ipynb).
- [Squat training notebook](../Backend/squatmodel.ipynb).
- Original report linked above, including references and team contributions.

The full training dataset and a plank training notebook are not included. Backend videos are experiment assets rather than a complete dataset. See the [project README](../README.md) for setup instructions.
