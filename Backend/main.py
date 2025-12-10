from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import tensorflow as tf
import keras
import joblib
import os
from typing import List

# Inisialisasi App
app = FastAPI()

# Konfigurasi CORS (Agar Frontend bisa akses)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1. GLOBAL RESOURCES & CONFIG ---
RESOURCES = {}
EXERCISES = ['plank', 'pushup', 'pullup', 'squat']

print(f"\nINFO: Running with TensorFlow {tf.__version__} and Keras {keras.__version__}")
print("🚀 SERVER AI STARTING...")

def load_resources():
    """
    Meload Model (.keras), Scaler (.pkl), dan Stats (.npy)
    Menangani variasi nama file (Huruf Besar/Kecil)
    """
    for ex in EXERCISES:
        # Coba cari file dengan awalan huruf kecil atau besar
        # Contoh: plank_autoencoder.keras ATAU Plank_autoencoder.keras
        candidates = [
            f"model/{ex}", 
            f"model/{ex.capitalize()}"
        ]
        
        model_path = None
        base_name = None

        # Cari file model yang eksis
        for c in candidates:
            if os.path.exists(f"{c}_autoencoder.keras"):
                model_path = f"{c}_autoencoder.keras"
                base_name = c
                break
        
        if model_path and base_name:
            scaler_path = f"{base_name}_scaler.pkl"
            stats_path = f"{base_name}_train_mse_stats.npy"

            try:
                # 1. Load Scaler
                scaler = joblib.load(scaler_path)
                
                # 2. Load Model (compile=False mempercepat load untuk inferensi)
                model = tf.keras.models.load_model(model_path, compile=False)
                
                # 3. Load Thresholds dari file .npy
                if os.path.exists(stats_path):
                    train_mse = np.load(stats_path)
                    # Logika Threshold:
                    # Low: Persentil 5 (Gerakan sangat sempurna di training)
                    # High: Persentil 95 * 4.0 (Batas toleransi untuk webcam yang agak shaky)
                    thresh_low = np.percentile(train_mse, 5)
                    thresh_high = np.percentile(train_mse, 95) * 4.0
                else:
                    # Fallback jika file stats hilang
                    print(f"⚠️ Stats missing for {ex}, using default thresholds.")
                    thresh_low, thresh_high = 0.02, 0.15

                RESOURCES[ex] = {
                    "model": model,
                    "scaler": scaler,
                    "thresholds": (thresh_low, thresh_high),
                    "input_dim": scaler.n_features_in_
                }
                print(f"✅ {ex.upper()} READY! (Input Dim: {scaler.n_features_in_})")
                
            except Exception as e:
                print(f"❌ Failed loading {ex}: {e}")
        else:
            print(f"⚠️ Model file not found for: {ex}")

# Panggil fungsi load saat script jalan
load_resources()

# --- 2. MATH & LOGIC HELPERS ---

def calculate_angle(a, b, c):
    """Menghitung sudut 3 titik (2D)"""
    if not a or not b or not c: return 0.0
    
    vba = np.array([a['x'] - b['x'], a['y'] - b['y']])
    vbc = np.array([c['x'] - b['x'], c['y'] - b['y']])
    
    dot = np.dot(vba, vbc)
    mag = np.linalg.norm(vba) * np.linalg.norm(vbc)
    
    if mag == 0: return 0.0
    # Clip untuk mencegah error arccos
    rad = np.arccos(np.clip(dot / mag, -1.0, 1.0))
    return np.degrees(rad)

def get_stats(seq):
    """Menghasilkan 5 statistik: Mean, Std, Min, Max, Range"""
    if len(seq) == 0: return [0.0] * 5
    return [np.mean(seq), np.std(seq), np.min(seq), np.max(seq), np.ptp(seq)]

def smooth_data(data, window_size=5):
    """Smoothing sederhana untuk mengurangi noise webcam"""
    if len(data) < window_size: return data
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

# --- 3. FEATURE EXTRACTION (MOVENET -> MEDIAPIPE LOGIC) ---

def extract_features(ex_type, history):
    """
    Mengubah raw keypoints MoveNet menjadi vektor fitur statistik.
    Menangani perbedaan logika tiap latihan.
    """
    
    # Helper akses keypoint aman
    # MoveNet Index: 5:L_Sh, 6:R_Sh, 7:L_Elb, 8:R_Elb, 11:L_Hip, 12:R_Hip, 13:L_Knee...
    def p(kp, i): return {'x': kp[i].x, 'y': kp[i].y} if i < len(kp) else {'x':0, 'y':0}

    raw_angles = []

    for kp in history:
        frame_angles = []
        
        if ex_type == 'plank':
            # 6 Sudut: Torso(L/R), Knee(L/R), Elbow(L/R)
            frame_angles.append(calculate_angle(p(kp,5), p(kp,11), p(kp,13))) 
            frame_angles.append(calculate_angle(p(kp,6), p(kp,12), p(kp,14))) 
            frame_angles.append(calculate_angle(p(kp,11), p(kp,13), p(kp,15))) 
            frame_angles.append(calculate_angle(p(kp,12), p(kp,14), p(kp,16))) 
            frame_angles.append(calculate_angle(p(kp,7), p(kp,5), p(kp,11)))   
            frame_angles.append(calculate_angle(p(kp,8), p(kp,6), p(kp,12)))   

        elif ex_type == 'pushup':
            # 6 Sudut: Elbow(L/R), Shoulder(L/R), Hip(L/R)
            frame_angles.append(calculate_angle(p(kp,5), p(kp,7), p(kp,9)))    
            frame_angles.append(calculate_angle(p(kp,6), p(kp,8), p(kp,10)))   
            frame_angles.append(calculate_angle(p(kp,7), p(kp,5), p(kp,11)))   
            frame_angles.append(calculate_angle(p(kp,8), p(kp,6), p(kp,12)))   
            frame_angles.append(calculate_angle(p(kp,5), p(kp,11), p(kp,13)))  
            frame_angles.append(calculate_angle(p(kp,6), p(kp,12), p(kp,14)))  

        elif ex_type == 'squat':
            # 6 Sudut: Knee, Hip, Ankle
            # NOTE: MoveNet tidak punya 'Foot Index' (31/32 di MediaPipe).
            # Kita isi 0.0 agar dimensi fitur tetap 30 (sesuai scaler notebook)
            frame_angles.append(calculate_angle(p(kp,11), p(kp,13), p(kp,15))) 
            frame_angles.append(calculate_angle(p(kp,12), p(kp,14), p(kp,16))) 
            frame_angles.append(calculate_angle(p(kp,5), p(kp,11), p(kp,13)))  
            frame_angles.append(calculate_angle(p(kp,6), p(kp,12), p(kp,14)))  
            frame_angles.append(0.0) # Padding Left Ankle
            frame_angles.append(0.0) # Padding Right Ankle

        elif ex_type == 'pullup':
            # 8 Sudut: Elbow, Shoulder, Hip, Knee
            frame_angles.append(calculate_angle(p(kp,5), p(kp,7), p(kp,9)))    
            frame_angles.append(calculate_angle(p(kp,6), p(kp,8), p(kp,10)))   
            frame_angles.append(calculate_angle(p(kp,11), p(kp,5), p(kp,7)))   
            frame_angles.append(calculate_angle(p(kp,12), p(kp,6), p(kp,8)))   
            frame_angles.append(calculate_angle(p(kp,5), p(kp,11), p(kp,13)))  
            frame_angles.append(calculate_angle(p(kp,6), p(kp,12), p(kp,14)))  
            frame_angles.append(calculate_angle(p(kp,11), p(kp,13), p(kp,15))) 
            frame_angles.append(calculate_angle(p(kp,12), p(kp,14), p(kp,16))) 

        if frame_angles:
            raw_angles.append(frame_angles)

    if not raw_angles: return None

    # Transpose & Calculate Statistics
    # Ubah [Frame][Angle] -> [Angle][Frame]
    angle_streams = np.array(raw_angles).T
    
    features = []
    for stream in angle_streams:
        # 1. Smooth data
        smoothed = smooth_data(stream)
        # 2. Get 5 stats (Mean, Std, Min, Max, Range)
        stats = get_stats(smoothed)
        features.extend(stats)
        
    return np.array([features])

# --- 4. API ENDPOINTS ---

class Keypoint(BaseModel):
    x: float
    y: float
    name: str = None
    score: float = 0

class AnalysisRequest(BaseModel):
    type: str 
    history: List[List[Keypoint]]

@app.get("/")
def read_root():
    return {
        "status": "AI Server Online",
        "loaded_models": list(RESOURCES.keys())
    }

@app.post("/analyze")
def analyze_movement(req: AnalysisRequest):
    ex_type = req.type.lower()
    
    # 1. Cek Ketersediaan Model
    if ex_type not in RESOURCES:
        return {"score": 0, "message": f"Model {ex_type} belum dimuat atau file tidak ada."}
    
    res = RESOURCES[ex_type]
    
    try:
        # 2. Ekstrak Fitur
        features = extract_features(ex_type, req.history)
        if features is None:
            return {"score": 0, "message": "Tidak ada data pose yang terdeteksi."}
            
        # 3. Validasi Dimensi Input (Safety Net)
        # Jika scaler mengharapkan 30 fitur tapi kita dapat 32 (atau sebaliknya),
        # lakukan padding atau cutting otomatis agar tidak crash.
        target_dim = res["input_dim"]
        current_dim = features.shape[1]
        
        if current_dim != target_dim:
            print(f"⚠️ Dimensi Mismatch untuk {ex_type}: Dapat {current_dim}, Butuh {target_dim}")
            if current_dim < target_dim:
                # Tambah nol (padding)
                features = np.pad(features, ((0,0), (0, target_dim - current_dim)))
            else:
                # Potong kelebihan
                features = features[:, :target_dim]

        # 4. Prediksi AI (Autoencoder)
        scaled_feat = res["scaler"].transform(features)
        reconstruction = res["model"].predict(scaled_feat, verbose=0)
        
        # Hitung MSE (Error antara Input vs Output)
        mse = np.mean(np.square(scaled_feat - reconstruction))
        
        # 5. Hitung Skor (Berdasarkan Threshold .npy)
        low, high = res["thresholds"]
        
        if mse <= low:
            score = 100
        elif mse >= high:
            score = 10
        else:
            # Rumus Interpolasi Linear
            score = 100 - 90 * (mse - low) / (high - low)
            
        return {
            "score": int(score),
            "mse": float(mse),
            "thresholds": {"best": float(low), "worst": float(high)},
            "message": "Analisa Sukses"
        }

    except Exception as e:
        print(f"❌ Error saat analisa: {e}")
        return {"score": 0, "message": "Terjadi kesalahan sistem AI."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)