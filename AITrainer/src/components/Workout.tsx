import React, { useState, useEffect } from 'react';
import Webcam from 'react-webcam';
import { Square } from 'lucide-react';

interface WorkoutProps {
  onFinish: (reps: number, duration: number) => void;
}

const Workout: React.FC<WorkoutProps> = ({ onFinish }) => {
  const [reps, setReps] = useState<number>(0);
  const [seconds, setSeconds] = useState<number>(0);

  // Timer
  useEffect(() => {
    const timer = setInterval(() => setSeconds(s => s + 1), 1000);
    return () => clearInterval(timer);
  }, []);

  // Simulator Tombol Spasi
  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.code === 'Space') setReps(r => r + 1);
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, []);

  const formatTime = (s: number) => {
    const m = Math.floor(s / 60).toString().padStart(2, '0');
    const sec = (s % 60).toString().padStart(2, '0');
    return `${m}:${sec}`;
  };

  return (
    <div className="flex flex-col md:flex-row h-screen w-full bg-black overflow-hidden animate-fade-in">
      {/* KIRI: KAMERA */}
      <div className="relative w-full md:w-3/4 h-1/2 md:h-full bg-gray-900 flex items-center justify-center">
        <div className="absolute top-6 left-6 z-20 flex items-center gap-2 bg-black/60 backdrop-blur-md px-4 py-2 rounded-full border border-white/10">
          <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
          <span className="text-xs font-mono font-bold tracking-widest text-white/90">AI LIVE TRACKING</span>
        </div>

        <Webcam 
            className="w-full h-full object-cover transform scale-x-[-1]" 
            audio={false}
            videoConstraints={{
              facingMode: "user"
            }}
        />

        <div className="absolute bottom-10 bg-black/40 backdrop-blur px-6 py-3 rounded-xl border border-white/10 text-white font-semibold animate-bounce">
          Posisi Siap. Mulai turun...
        </div>
      </div>

      {/* KANAN: STATS */}
      <div className="w-full md:w-1/4 h-1/2 md:h-full bg-[#020617] border-l border-gray-800 flex flex-col justify-between p-8 relative z-10">
        <div>
          <h3 className="text-gray-500 text-xs font-bold tracking-widest uppercase mb-1">TIMER</h3>
          <p className="text-5xl font-mono text-white tracking-tight">{formatTime(seconds)}</p>
        </div>

        <div className="flex flex-col items-center justify-center py-10">
          <h3 className="text-blue-500 text-sm font-bold tracking-widest uppercase mb-4">PUSHUPS</h3>
          <div className="text-[10rem] leading-none font-bold text-transparent bg-clip-text bg-gradient-to-b from-white to-gray-800 select-none">
            {reps}
          </div>
          <p className="mt-6 text-xs text-gray-600 bg-gray-900 px-4 py-2 rounded-full border border-gray-800">
            Tekan [SPASI] untuk simulasi
          </p>
        </div>

        <button
          onClick={() => onFinish(reps, seconds)}
          className="w-full bg-red-600 hover:bg-red-500 text-white font-bold py-5 rounded-2xl flex items-center justify-center gap-3 transition-all active:scale-95 shadow-lg shadow-red-900/20"
        >
          <Square fill="currentColor" size={20} />
          Selesai Latihan
        </button>
      </div>
    </div>
  );
};

export default Workout;