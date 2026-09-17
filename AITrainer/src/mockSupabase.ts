import { User, WorkoutRecord } from './types';

// Helper untuk LocalStorage
const getLocalData = <T>(key: string): T[] => {
  const item = localStorage.getItem(key);
  return item ? JSON.parse(item) : [];
};

const setLocalData = <T>(key: string, data: T[]) => {
  localStorage.setItem(key, JSON.stringify(data));
};

export const supabase = {
  auth: {
    getSession: async () => {
      const userStr = localStorage.getItem('mock_user');
      const user: User | null = userStr ? JSON.parse(userStr) : null;
      return { data: { session: user ? { user } : null }, error: null };
    },
    signInWithPassword: async ({ email }: { email: string }) => {
      const user: User = { id: 'user_123', email };
      localStorage.setItem('mock_user', JSON.stringify(user));
      return { data: { session: { user } }, error: null };
    },
    signUp: async ({ email }: { email: string }) => {
      // Mock signup sama dengan signin
      const user: User = { id: 'user_123', email };
      localStorage.setItem('mock_user', JSON.stringify(user));
      return { data: { session: { user } }, error: null };
    },
    signOut: async () => {
      localStorage.removeItem('mock_user');
      return { error: null };
    },
  },
  
  from: (table: string) => {
    return {
      select: (columns: string = '*') => ({
        order: (col: string, { ascending }: { ascending: boolean } = { ascending: false }) => {
          const data = getLocalData<WorkoutRecord>('mock_workouts');
          // Simple sorting mock
          data.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
          return { data, error: null };
        }
      }),
      insert: async (rows: Partial<WorkoutRecord>[]) => {
        const current = getLocalData<WorkoutRecord>('mock_workouts');
        const newRows = rows.map(r => ({
          ...r,
          id: Date.now(),
          created_at: new Date().toISOString()
        })) as WorkoutRecord[];
        
        setLocalData('mock_workouts', [...current, ...newRows]);
        return { error: null };
      }
    };
  }
};