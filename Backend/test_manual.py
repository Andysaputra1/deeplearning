import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import joblib
import os

# --- KONFIGURASI ---
VIDEO_PATH = "test_plank.mp4" # Pastikan file video ini ada di folder backend atau berikan path lengkap
TYPE = "plank" # Ubah tipe latihan di sini (plank, pushup, pullup, squat)

print(f"\n[INFO] TESTING VIDEO: {VIDEO_PATH} ({TYPE})")

# --- 1. LOAD RESOURCES (MODEL & SCALER) ---
# Fungsi load resources mirip dengan di main.py backend
def load_model_and_scaler(ex_type):
    # Coba cari file dengan awalan huruf kecil atau besar
    candidates = [
        f"model/{ex_type}_autoencoder.keras",
        f"model/{ex_type.capitalize()}_autoencoder.keras"
    ]
    
    model_path = None
    for c in candidates:
        if os.path.exists(c):
            model_path = c
            break
            
    scaler_paths = [
        f"model/{ex_type}_scaler.pkl",
        f"model/{ex_type.capitalize()}_scaler.pkl"
    ]
    scaler_path = None
    for p in scaler_paths:
        if os.path.exists(p):
            scaler_path = p
            break

    if not model_path or not scaler_path:
        print(f"[ERROR] Model or Scaler not found for {ex_type}")
        return None, None, None

    try:
        scaler = joblib.load(scaler_path)
        # compile=False mempercepat load untuk inferensi
        model = tf.keras.models.load_model(model_path, compile=False)
        input_dim = scaler.n_features_in_
        print(f"[OK] Model Loaded from {model_path}. Features: {input_dim}")
        return model, scaler, input_dim
    except Exception as e:
        print(f"[ERROR] Failed to load model/scaler: {e}")
        return None, None, None

# Load Model
model, scaler, input_dim = load_model_and_scaler(TYPE)
if not model:
    exit()

# --- 2. MEDIAPIPE SETUP ---
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1, enable_segmentation=False)

# --- 3. MATH HELPERS ---
def get_angle(a, b, c):
    """Menghitung sudut antara 3 titik (a, b, c) dengan b sebagai titik pusat."""
    # Pastikan input adalah numpy array untuk operasi vektor
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    vba = a - b
    vbc = c - b
    
    # Menghitung dot product dan magnitude
    dot = np.dot(vba, vbc)
    mag = np.linalg.norm(vba) * np.linalg.norm(vbc)
    
    if mag == 0: return 0.0
    
    # Menghitung sudut dalam radian dan konversi ke derajat
    rad = np.arccos(np.clip(dot / mag, -1.0, 1.0))
    return np.degrees(rad)

def get_stats(seq):
    """Menghasilkan statistik dasar dari urutan data."""
    if len(seq) == 0: return [0.0]*5
    return [np.mean(seq), np.std(seq), np.min(seq), np.max(seq), np.ptp(seq)]

# --- 4. VIDEO PROCESSING ---
if not os.path.exists(VIDEO_PATH):
    print(f"[ERROR] Video file not found: {VIDEO_PATH}")
    exit()

cap = cv2.VideoCapture(VIDEO_PATH)
# Siapkan list untuk menyimpan urutan sudut. Jumlah slot disesuaikan dengan maksimum kemungkinan fitur.
# Plank: 6 sudut, Pushup: 6 sudut, Squat: 6 sudut, Pullup: 8 sudut.
# Kita buat cukup besar (8) untuk menampung semuanya.
angle_seqs = [[] for _ in range(8)] 

frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    
    frame_count += 1
    # Opsional: Skip frame untuk mempercepat (misal proses setiap frame ke-2)
    # if frame_count % 2 != 0: continue 

    # Konversi BGR ke RGB untuk MediaPipe
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = pose.process(image_rgb)
    
    if res.pose_landmarks:
        # Ambil landmarks (33 titik)
        lm = [np.array([l.x, l.y, l.z]) for l in res.pose_landmarks.landmark]
        
        # Ekstraksi Sudut Berdasarkan Tipe Latihan (Logika MediaPipe)
        # Indeks MediaPipe:
        # 11: L_Shoulder, 12: R_Shoulder
        # 13: L_Elbow, 14: R_Elbow
        # 15: L_Wrist, 16: R_Wrist
        # 23: L_Hip, 24: R_Hip
        # 25: L_Knee, 26: R_Knee
        # 27: L_Ankle, 28: R_Ankle
        
        if TYPE == 'plank':
            # Logic: Torso, Knee, Elbow (6 Sudut)
            angle_seqs[0].append(get_angle(lm[11], lm[23], lm[25])) # L_Torso
            angle_seqs[1].append(get_angle(lm[12], lm[24], lm[26])) # R_Torso
            angle_seqs[2].append(get_angle(lm[23], lm[25], lm[27])) # L_Knee
            angle_seqs[3].append(get_angle(lm[24], lm[26], lm[28])) # R_Knee
            angle_seqs[4].append(get_angle(lm[13], lm[11], lm[23])) # L_ElbowAngle
            angle_seqs[5].append(get_angle(lm[14], lm[12], lm[24])) # R_ElbowAngle
        
        elif TYPE == 'pushup':
            # Logic: Elbow, Shoulder, Hip (6 Sudut)
            angle_seqs[0].append(get_angle(lm[11], lm[13], lm[15])) # L_Elbow
            angle_seqs[1].append(get_angle(lm[12], lm[14], lm[16])) # R_Elbow
            angle_seqs[2].append(get_angle(lm[13], lm[11], lm[23])) # L_Shoulder
            angle_seqs[3].append(get_angle(lm[14], lm[12], lm[24])) # R_Shoulder
            angle_seqs[4].append(get_angle(lm[11], lm[23], lm[25])) # L_Hip
            angle_seqs[5].append(get_angle(lm[12], lm[24], lm[26])) # R_Hip

        elif TYPE == 'pullup':
            # Logic: Elbow, Shoulder, Hip, Knee (8 Sudut)
            angle_seqs[0].append(get_angle(lm[11], lm[13], lm[15])) # L_Elbow
            angle_seqs[1].append(get_angle(lm[12], lm[14], lm[16])) # R_Elbow
            angle_seqs[2].append(get_angle(lm[23], lm[11], lm[13])) # L_Shoulder (H-S-E) - Perhatikan urutan titik di notebook asli mungkin beda
            angle_seqs[3].append(get_angle(lm[24], lm[12], lm[14])) 
            angle_seqs[4].append(get_angle(lm[11], lm[23], lm[25])) # L_Hip
            angle_seqs[5].append(get_angle(lm[12], lm[24], lm[26])) 
            angle_seqs[6].append(get_angle(lm[23], lm[25], lm[27])) # L_Knee
            angle_seqs[7].append(get_angle(lm[24], lm[26], lm[28])) 

        elif TYPE == 'squat':
            # Logic: Knee, Hip, Ankle (6 Sudut)
            angle_seqs[0].append(get_angle(lm[23], lm[25], lm[27])) # L_Knee
            angle_seqs[1].append(get_angle(lm[24], lm[26], lm[28])) 
            angle_seqs[2].append(get_angle(lm[11], lm[23], lm[25])) # L_Hip
            angle_seqs[3].append(get_angle(lm[12], lm[24], lm[26])) 
            angle_seqs[4].append(get_angle(lm[25], lm[27], lm[31])) # L_Ankle (Foot index 31/32 ada di MediaPipe)
            angle_seqs[5].append(get_angle(lm[26], lm[28], lm[32]))

cap.release()
print(f"[INFO] Processed {frame_count} frames.")

# --- 5. PREDICT & SCORE ---
feats = []
# Filter sequence kosong & ambil sesuai jumlah fitur yang diharapkan
if TYPE == 'pullup': valid_seqs = angle_seqs[:8]
else: valid_seqs = angle_seqs[:6]

# Flatten features: [mean, std, min, max, ptp] untuk setiap sudut
for s in valid_seqs: 
    feats.extend(get_stats(s))

# Padding/Cutting jika dimensi tidak sesuai dengan scaler
current_dim = len(feats)
if current_dim < input_dim:
    feats += [0.0] * (input_dim - current_dim)
elif current_dim > input_dim:
    feats = feats[:input_dim]

# Konversi ke array 2D untuk input model
input_arr = np.array([feats])

# Prediksi
try:
    scaled = scaler.transform(input_arr)
    recon = model.predict(scaled, verbose=0)
    mse = np.mean(np.square(scaled - recon))
    
    # Scoring (Gunakan Threshold Default atau Load dari .npy jika mau lebih akurat seperti main.py)
    # Di sini kita pakai default atau hardcoded sementara untuk tes manual
    # Agar lebih canggih, kamu bisa copy logika load .npy dari main.py
    
    # Coba load npy untuk threshold dinamis
    stats_path = f"model/{TYPE}_train_mse_stats.npy"
    if not os.path.exists(stats_path):
         stats_path = f"model/{TYPE.capitalize()}_train_mse_stats.npy"

    if os.path.exists(stats_path):
        train_mse = np.load(stats_path)
        LOW = np.percentile(train_mse, 5)
        HIGH = np.percentile(train_mse, 95) * 4.0 # Multiplier toleransi
        print(f"[INFO] Using Dynamic Thresholds from .npy: LOW={LOW:.5f}, HIGH={HIGH:.5f}")
    else:
        LOW, HIGH = 0.02, 0.15 # Fallback default
        print(f"[INFO] Using Default Thresholds: LOW={LOW}, HIGH={HIGH}")

    # Logika Skor Linear
    if mse <= LOW:
        score = 100
    elif mse >= HIGH:
        score = 10
    else:
        score = 100 - 90 * (mse - LOW) / (HIGH - LOW)

    print("\n" + "="*30)
    print(f"MSE   : {mse:.5f}")
    print(f"SCORE : {int(score)}")
    print("="*30)

except Exception as e:
    print(f"[ERROR] Prediction failed: {e}")