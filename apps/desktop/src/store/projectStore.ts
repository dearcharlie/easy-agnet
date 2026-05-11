export interface Project {
  name: string;
  path: string;
  chapters: number;
  drafts: number;
}

export interface Chapter {
  number: number;
  path: string;
  title: string;
  isDraft: boolean;
}
