"use client";

import { useCallback, useEffect, useState } from "react";
import type { HighlightData, HighlightColor } from "@/lib/highlight-types";

const STORAGE_PREFIX = "buddio_highlights_";

function getStorageKey(lessonId: number): string {
  return `${STORAGE_PREFIX}${lessonId}`;
}

export function useHighlights(lessonId: number) {
  const [highlights, setHighlights] = useState<HighlightData[]>([]);

  useEffect(() => {
    const raw = localStorage.getItem(getStorageKey(lessonId));
    if (raw) {
      try {
        setHighlights(JSON.parse(raw));
      } catch {
        setHighlights([]);
      }
    }
  }, [lessonId]);

  const persist = useCallback(
    (data: HighlightData[]) => {
      setHighlights(data);
      localStorage.setItem(getStorageKey(lessonId), JSON.stringify(data));
    },
    [lessonId]
  );

  const addHighlight = useCallback(
    (text: string, color: HighlightColor, note: string = ""): HighlightData => {
      const h: HighlightData = {
        id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
        lessonId,
        text,
        color,
        note,
        createdAt: new Date().toISOString(),
      };
      persist([...highlights, h]);
      return h;
    },
    [highlights, persist, lessonId]
  );

  const updateNote = useCallback(
    (id: string, note: string) => {
      persist(highlights.map((h) => (h.id === id ? { ...h, note } : h)));
    },
    [highlights, persist]
  );

  const updateColor = useCallback(
    (id: string, color: HighlightColor) => {
      persist(highlights.map((h) => (h.id === id ? { ...h, color } : h)));
    },
    [highlights, persist]
  );

  const removeHighlight = useCallback(
    (id: string) => {
      persist(highlights.filter((h) => h.id !== id));
    },
    [highlights, persist]
  );

  return { highlights, addHighlight, updateNote, updateColor, removeHighlight };
}
