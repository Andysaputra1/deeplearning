import React from 'react';
import { CheckCircle, LogIn } from 'lucide-react';
import { WorkoutResult } from '../types';

interface SummaryProps {
  data: WorkoutResult | null;
  onSave: () => void;
  onDiscard: () => void;
  isLoggedIn: boolean;
}

const Summary: React.FC<SummaryProps> = ({ data, onSave, onDiscard, isLoggedIn }) => {
  return (
    <div className="min-h-screen flex items-center justify-center p-4 animate-fade-in">
      <div className="bg-[#0f172a] border border-gray-800 w-full max-w-md p-10 rounded-[2rem] shadow-2xl text-center relative">

        <div className="mx-auto w-24 h-24 bg-green-500/10 rounded-full flex items-center justify-center mb-8 border border-green-500/20 animate-pulse">
          <CheckCircle size={48} className="text-green-500" />
        </div>

        <h2 className="text-3xl font-bold text-white mb-2">Latihan Selesai!</h2>
        <p className="text-gray-400 mb-10">
          {isLoggedIn ? 'Hasil telah direkam.' : 'Login untuk menyimpan permanen.'}
        </p>

        <div className="grid grid-cols-2 gap-4 mb-10">
          <div className="bg-[#1e293b] p-6 rounded-2xl border border-gray-700/50">
            <span className="text-xs text-gray-500 font-bold uppercase block mb-2">Total Reps</span>
            <span className="text-5xl font-bold text-blue-400">{data?.reps || 0}</span>
          </div>
          <div className="bg-[#1e293b] p-6 rounded-2xl border border-gray-700/50">
            <span className="text-xs text-gray-500 font-bold uppercase block mb-2">Durasi</span>
            <span className="text-5xl font-bold text-white font-mono">
              {Math.floor((data?.duration || 0) / 60)}:{(data?.duration || 0) % 60 ? ((data?.duration || 0) % 60).toString().padStart(2, '0') : '00'}
            </span>
          </div>
        </div>

        <button onClick={onSave} className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-4 rounded-xl mb-4 flex items-center justify-center gap-2 transition-all shadow-lg shadow-blue-900/20">
          {isLoggedIn ? 'Simpan Progress' : <><LogIn size={20} /> Simpan Progress (Login)</>}
        </button>

        <button onClick={onDiscard} className="text-sm text-gray-500 hover:text-red-400 transition-colors py-2">
          Kembali ke Home (Data Hilang)
        </button>
      </div>
    </div>
  );
};

export default Summary;