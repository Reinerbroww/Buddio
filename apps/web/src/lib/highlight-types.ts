export type HighlightColor = "yellow" | "green" | "blue" | "red";

export interface HighlightData {
  id: string;
  lessonId: number;
  text: string;
  color: HighlightColor;
  note: string;
  createdAt: string;
}

export const HIGHLIGHT_COLORS: Record<HighlightColor, { bg: string; border: string; label: string; emoji: string }> = {
  yellow: { bg: "bg-amber-100", border: "border-amber-300", label: "Penting", emoji: "🟡" },
  green: { bg: "bg-emerald-100", border: "border-emerald-300", label: "Dipahami", emoji: "🟢" },
  blue: { bg: "bg-blue-100", border: "border-blue-300", label: "Perlu Dipelajari", emoji: "🔵" },
  red: { bg: "bg-rose-100", border: "border-rose-300", label: "Bingung", emoji: "🔴" },
};
