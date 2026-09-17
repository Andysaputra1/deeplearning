# 🏋️‍♂️ AI Trainer - Deep Learning Project

**AI Trainer** adalah aplikasi berbasis web yang memanfaatkan teknologi *Computer Vision* dan *Deep Learning* untuk mendeteksi, menghitung, dan menganalisis gerakan olahraga (Push-up, Pull-up, Squat, dll) secara real-time.

Proyek ini menggunakan arsitektur *Fullstack* dengan pemisahan antara Frontend (React) dan Backend (Python).

## 📂 Struktur Direktori

Berikut adalah gambaran struktur folder dalam repositori ini:

```text
deeplearning/
│
├── AITrainer/                  # [Frontend] Source code aplikasi Web
│   ├── src/                    
│   ├── public/                 
│   ├── tailwind.config.js      
│   └── vite.config.js          
│
├── Backend/                    # [Backend] Logika AI & Pemrosesan Video
│   ├── .venv/                  # Virtual Environment Python
│   ├── model/                  # Folder penyimpanan model AI
│   ├── main.py                 # Entry point backend server
│   ├── pushupmodel.ipynb       # Experiment  model Push-up
│   ├── pullupmodel.ipynb       # Experiment model Pull-up
│   ├── squatmodel.ipynb        # Experiment model Squat
│   └── requirements.txt        # Daftar library Python
│
├── git/                        # Konfigurasi version control
└── link_github_frontend.txt    # 🔗 Link Repositori Frontend (Submodule/Remote)
