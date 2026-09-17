import React, { useState, useEffect } from 'react';
import { supabase } from './mockSupabase';
import Landing from './components/Landing';
import Workout from './components/Workout';
import Summary from './components/Summary';
import Auth from './components/Auth';
import { Session, WorkoutRecord, WorkoutResult } from './types';

type ViewState = 'landing' | 'workout' | 'summary' | 'auth';

const App: React.FC = () => {
  const [session, setSession] = useState<Session | null>(null);
  const [view, setView] = useState<ViewState>('landing');
  const [workoutResult, setWorkoutResult] = useState<WorkoutResult | null>(null);
  const [history, setHistory] = useState<WorkoutRecord[]>([]);

  useEffect(() => {
    checkSession();
  }, []);

  const checkSession = async () => {
    const { data } = await supabase.auth.getSession();
    setSession(data.session);
    if (data.session) {
      fetchHistory();
    } else {
      setHistory([]);
    }
  };

  const fetchHistory = async () => {
    // Casting any karena mock return structure
    const { data } = await supabase.from('workouts').select('*').order('created_at');
    if (data) setHistory(data);
  };

  // --- HANDLERS ---
  const handleFinishWorkout = (reps: number, duration: number) => {
    setWorkoutResult({ reps, duration });
    setView('summary');
  };

  const handleSave = async () => {
    if (!session || !workoutResult) {
      setView('auth');
      return;
    }

    await supabase.from('workouts').insert([{
      user_id: session.user.id,
      reps: workoutResult.reps,
      duration: workoutResult.duration
    }]);

    setWorkoutResult(null);
    await fetchHistory();
    setView('landing');
  };

  const handleAuthSuccess = async () => {
    await checkSession();
    if (workoutResult) {
      handleSave();
    } else {
      setView('landing');
    }
  };

  const handleLogout = async () => {
    await supabase.auth.signOut();
    setSession(null);
    setHistory([]);
    setView('landing');
  };

  return (
    <div className="min-h-screen bg-[#020617] text-white font-sans">
      {view === 'landing' && (
        <Landing
          session={session}
          history={history}
          onStart={() => setView('workout')}
          onLogin={() => setView('auth')}
          onLogout={handleLogout}
        />
      )}

      {view === 'workout' && (
        <Workout onFinish={handleFinishWorkout} />
      )}

      {view === 'summary' && (
        <Summary
          data={workoutResult}
          onSave={handleSave}
          onDiscard={() => setView('landing')}
          isLoggedIn={!!session}
        />
      )}

      {view === 'auth' && (
        <Auth
          onSuccess={handleAuthSuccess}
          onCancel={() => setView(workoutResult ? 'summary' : 'landing')}
          isSaving={!!workoutResult}
        />
      )}
    </div>
  );
};

export default App;