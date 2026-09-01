export interface User {
  id: number;
  email: string;
  full_name?: string | null;
  grade_level?: string | null;
  learning_goal?: string | null;
  avatar_url?: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Topic {
  id: number;
  title: string;
  description?: string | null;
  status?: string | null;
  created_at: string;
  progress_percentage: number;
  has_roadmap: boolean;
}

export interface RoadmapStep {
  id: number;
  order_number: number;
  title: string;
  description?: string | null;
  completed: boolean;
  lesson_id?: number | null;
}

export interface Roadmap {
  id: number;
  topic_id: number;
  title: string;
  difficulty?: string | null;
  estimated_hours?: number | null;
  created_at: string;
  steps: RoadmapStep[];
  completion_percentage: number;
  mode?: string | null;
}

export interface Lesson {
  id: number;
  roadmap_step_id: number;
  content?: string | null;
  source?: string | null;
  video_urls?: VideoItem[] | null;
  step_title?: string | null;
  step_description?: string | null;
  topic_title?: string | null;
  topic_id?: number | null;
  created_at: string;
}

export interface VideoItem {
  title: string;
  url: string;
  description?: string | null;
}

export interface ChatResponse {
  answer: string;
  session_id: number;
  mode: string;
  remaining: number;
}

export interface ChatMessageItem {
  id: number;
  role: "user" | "assistant";
  message: string;
  created_at: string;
}

export interface ChatHistory {
  id: number;
  topic_id: number;
  title?: string | null;
  created_at: string;
  messages: ChatMessageItem[];
}

export interface QuizQuestion {
  id: number;
  question: string;
  options?: string[] | null;
  explanation?: string | null;
}

export interface Quiz {
  id: number;
  topic_id: number;
  title: string;
  generated_by_ai: boolean;
  created_at: string;
  mode?: string | null;
  questions: QuizQuestion[];
}

export interface QuizAttemptResult {
  id: number;
  quiz_id: number;
  score: number;
  total: number;
  feedback?: string | null;
  created_at: string;
  details?: Array<{
    question_id: number;
    question: string;
    your_answer: number | null;
    correct: boolean;
    correct_answer: number | null;
    explanation?: string | null;
  }>;
}

export interface ProgressStat {
  study_hours: number;
  topics: number;
  streak: number;
  completion: number;
  chat_remaining: number;
  roadmap_remaining: number;
  quiz_remaining: number;
}

export interface ProgressItem {
  topic_id: number;
  topic_title: string;
  completion_percentage: number;
  study_minutes: number;
  last_access?: string | null;
  current_step?: string | null;
}

export interface Usage {
  chat_remaining: number;
  roadmap_remaining: number;
  quiz_remaining: number;
  reset_date: string;
  limits: { chat: number; roadmap: number; quiz: number };
}

export interface Settings {
  theme: string;
  notification: boolean;
  language: string;
  daily_goal: number;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}
