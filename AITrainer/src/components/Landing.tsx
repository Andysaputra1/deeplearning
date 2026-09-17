import React from 'react';
import { Activity, Play, Lock, Trophy } from 'lucide-react';
import { Session, WorkoutRecord } from '../types';

interface LandingProps {
  session: Session | null;
  history: WorkoutRecord[];
  onStart: () => void;
  onLogin: () => void;
  onLogout: () => void;
}

const Landing: React.FC<LandingProps> = ({ session, history, onStart, onLogin, onLogout }) => {
  return (
    <div className="flex flex-col items-center animate-fade-in pb-20">
      {/* NAVBAR */}
      <nav className="w-full max-w-6xl p-6 flex justify-between items-center sticky top-0 z-50 bg-[#020617]/80 backdrop-blur-md">
        <div className="flex items-center gap-2 font-bold text-xl cursor-pointer">
          <div className="bg-blue-600 p-1 rounded-lg">
            <Activity className="text-white" size={20} />
          </div>
          <span>AI<span className="text-blue-500">Trainer</span></span>
        </div>
        <div>
          {session ? (
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-400 hidden md:block">
                Halo, {session.user.email.split('@')[0]}
              </span>
              <button onClick={onLogout} className="text-sm font-semibold text-red-400 hover:text-red-300 transition-colors">
                Keluar
              </button>
            </div>
          ) : (
            <button onClick={onLogin} className="bg-blue-600/10 text-blue-400 border border-blue-500/20 px-5 py-2 rounded-full text-sm font-bold hover:bg-blue-600 hover:text-white transition-all">
              Masuk Akun &rarr;
            </button>
          )}
        </div>
      </nav>

      {/* HERO */}
      <header className="text-center mt-12 mb-16 px-4">
        <div className="inline-flex items-center gap-2 border border-blue-500/30 bg-blue-500/10 text-blue-400 text-xs font-bold px-3 py-1 rounded-full mb-6">
          <span className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></span> AI POWERED FITNESS
        </div>
        <h1 className="text-5xl md:text-7xl font-extrabold mb-6 leading-tight tracking-tight">
          Hitung Push-up <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-400 to-teal-400">
            Tanpa Curang.
          </span>
        </h1>
        <p className="text-gray-400 text-lg max-w-2xl mx-auto mb-10 leading-relaxed">
          Menggunakan model Deep Learning canggih untuk menganalisa postur tubuhmu secara real-time.
          <span className="text-white font-semibold"> Bisa dicoba langsung tanpa login!</span>
        </p>

        <button onClick={onStart} className="bg-blue-600 hover:bg-blue-500 text-white text-lg font-bold py-4 px-10 rounded-full shadow-[0_0_30px_-5px_rgba(37,99,235,0.4)] transition-transform hover:-translate-y-1">
          Mulai Sekarang &gt;
        </button>
      </header>

      {/* DEMO CARD */}
      <section className="w-full max-w-4xl px-4 mb-24">
        <div onClick={onStart} className="group cursor-pointer relative bg-gradient-to-b from-[#1e293b] to-[#0f172a] border border-gray-800 rounded-3xl p-12 text-center overflow-hidden hover:border-blue-500/50 transition-all">
          <div className="absolute inset-0 bg-blue-600/5 group-hover:bg-blue-600/10 transition-colors"></div>

          <h2 className="text-3xl font-bold mb-3 relative z-10">Coba Sekarang, Gratis!</h2>
          <p className="text-gray-400 mb-10 relative z-10">Posisikan perangkat di lantai, pastikan seluruh tubuh terlihat.</p>

          <div className="relative z-10 w-24 h-24 bg-blue-600 rounded-full flex items-center justify-center mx-auto shadow-2xl shadow-blue-500/40 group-hover:scale-110 transition-transform duration-300">
            <Play fill="white" size={40} className="ml-2" />
          </div>
          <p className="relative z-10 mt-8 text-xs font-bold tracking-[0.2em] text-blue-400 uppercase">Mulai Sesi Tamu</p>
        </div>
      </section>

      {/* HISTORY TABLE */}
      <section className="w-full max-w-4xl px-4">
        <h3 className="text-xl font-bold mb-6 flex items-center gap-2 border-b border-gray-800 pb-4">
          <Trophy className="text-yellow-500" size={24} /> Riwayat Progress
        </h3>

        <div className="bg-[#0f172a] border border-gray-800 rounded-2xl overflow-hidden min-h-[250px] relative">
          {!session ? (
            // LOCKED STATE
            <div className="absolute inset-0 flex flex-col items-center justify-center bg-black/60 backdrop-blur-sm z-20">
              <div className="bg-gray-800 p-4 rounded-full mb-4 border border-gray-700">
                <Lock className="text-blue-400" size={32} />
              </div>
              <h4 className="text-xl font-bold mb-2">Riwayat Terkunci</h4>
              <p className="text-gray-400 text-sm mb-6">Masuk untuk menyimpan & melihat progress.</p>
              <button onClick={onLogin} className="bg-blue-600 hover:bg-blue-500 text-white px-8 py-3 rounded-lg font-bold text-sm transition-all">
                Masuk Untuk Melihat
              </button>
            </div>
          ) : (
            // TABLE DATA
            <div className="w-full">
              {history.length === 0 ? (
                <div className="p-16 text-center text-gray-500 flex flex-col items-center">
                  <Activity className="mb-4 opacity-20" size={48} />
                  Belum ada data latihan. Yuk mulai!
                </div>
              ) : (
                <table className="w-full text-left text-sm text-gray-400">
                  <thead className="bg-gray-900/50 text-gray-500 uppercase font-bold text-xs tracking-wider">
                    <tr>
                      <th className="p-5">Tanggal</th>
                      <th className="p-5">Jumlah</th>
                      <th className="p-5">Durasi</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-800/50">
                    {history.map((h) => (
                      <tr key={h.id} className="hover:bg-gray-800/30 transition-colors">
                        <td className="p-5 text-gray-300">{new Date(h.created_at).toLocaleDateString()}</td>
                        <td className="p-5 text-white font-bold text-lg">{h.reps}</td>
                        <td className="p-5 font-mono text-blue-400">{Math.floor(h.duration / 60)}:{(h.duration % 60).toString().padStart(2, '0')}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}

          {/* FAKE BACKGROUND (Biar kelihatan ada isinya pas dilock) */}
          {!session && (
            <div className="opacity-10 pointer-events-none p-6 space-y-6 filter blur-sm">
              {[1, 2, 3].map(i => (
                <div key={i} className="flex justify-between items-center">
                  <div className="h-4 bg-gray-500 rounded w-24"></div>
                  <div className="h-4 bg-gray-500 rounded w-12"></div>
                  <div className="h-4 bg-gray-500 rounded w-16"></div>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>
    </div>
  );
};

export default Landing;