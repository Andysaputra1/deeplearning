import React, { useState } from 'react';
import { supabase } from '../mockSupabase';
import { X, Activity } from 'lucide-react';

interface AuthProps {
  onSuccess: () => void;
  onCancel: () => void;
  isSaving: boolean;
}

const Auth: React.FC<AuthProps> = ({ onSuccess, onCancel, isSaving }) => {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    // Simulasi delay biar berasa loading
    setTimeout(async () => {
      await supabase.auth.signInWithPassword({ email });
      setLoading(false);
      onSuccess();
    }, 1000);
  };

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 animate-fade-in">
      <div className="bg-[#0f172a] border border-gray-800 w-full max-w-sm p-8 rounded-3xl relative shadow-2xl">
        <button onClick={onCancel} className="absolute top-4 right-4 p-2 bg-gray-800 rounded-full text-gray-400 hover:text-white transition-colors">
          <X size={18} />
        </button>

        <div className="flex justify-center mb-6">
          <div className="p-3 bg-blue-600/20 rounded-xl">
            <Activity className="text-blue-500" size={32} />
          </div>
        </div>

        <h2 className="text-2xl font-bold text-center text-white mb-2">
          {isSaving ? 'Simpan Hasilmu' : 'Selamat Datang'}
        </h2>
        <p className="text-center text-gray-500 text-sm mb-8">
          Masukkan email sembarang untuk simulasi masuk.
        </p>

        <form onSubmit={handleLogin} className="space-y-4">
          <input
            type="email"
            placeholder="Email (contoh: andy@binus.ac.id)"
            className="w-full bg-[#020617] border border-gray-700 rounded-xl p-4 text-white focus:border-blue-500 focus:outline-none transition-all placeholder:text-gray-700"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password (bebas)"
            className="w-full bg-[#020617] border border-gray-700 rounded-xl p-4 text-white focus:border-blue-500 focus:outline-none transition-all placeholder:text-gray-700"
          />

          <button disabled={loading} className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-4 rounded-xl transition-all shadow-lg disabled:opacity-50 disabled:cursor-not-allowed">
            {loading ? 'Memproses...' : 'Masuk / Daftar'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Auth;