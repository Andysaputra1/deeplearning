export interface User {
  id: string;
  email: string;
}

export interface Session {
  user: User;
}

export interface WorkoutRecord {
  id: number;
  user_id: string;
  reps: number;
  duration: number;
  created_at: string;
}

export interface WorkoutResult {
  reps: number;
  duration: number;
}