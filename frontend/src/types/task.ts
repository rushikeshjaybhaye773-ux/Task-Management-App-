export interface User {
  id: string;
  name: string;
  email: string;
  profile_image?: string;
}

export interface Task {
  id: string;
  title: string;
  description: string;
  status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED';
  created_by: User;
  assigned_to?: User;
  created_at: string;
  completed_at?: string;
}
