import Link from "next/link";
import { cn } from "@/lib/utils";

export function BuddioLogo({
  href = "/",
  size = "md",
  className,
  showWordmark = true,
}: {
  href?: string;
  size?: "sm" | "md";
  className?: string;
  showWordmark?: boolean;
}) {
  const box = size === "sm" ? "h-9 w-9 rounded-xl" : "h-10 w-10 rounded-xl";
  const svg = size === "sm" ? "w-6 h-6" : "w-6 h-6";
  const text = size === "sm" ? "text-lg" : "text-xl";

  const mark = (
    <div
      className={cn(
        "relative flex items-center justify-center bg-gradient-to-br from-[#4F8EF7] to-[#7C5CFF] text-white shadow-md shadow-[#4F8EF7]/20 shrink-0 select-none",
        box
      )}
    >
      <svg className={svg} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M12 21C16.9706 21 21 16.9706 21 12C21 7.02944 16.9706 3 12 3C7.02944 3 3 7.02944 3 12C3 13.9021 3.59393 15.6605 4.60501 17.102L3.5 20.5L6.898 19.395C8.33953 20.4061 10.0979 21 12 21Z"
          fill="white"
        />
        <path
          d="M8.5 7.5H11.8C12.8 7.5 13.5 8.1 13.5 9C13.5 9.7 13 10.2 12.3 10.4C13.1 10.6 13.7 11.2 13.7 12C13.7 12.9 12.9 13.5 11.8 13.5H8.5V7.5Z"
          fill="none"
          stroke="url(#buddio-logo-grad)"
          strokeWidth="1.8"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <circle cx="10.2" cy="9.2" r="0.6" fill="url(#buddio-logo-grad)" />
        <circle cx="11.8" cy="9.2" r="0.6" fill="url(#buddio-logo-grad)" />
        <path
          d="M10.2 12C10.5 12.5 11.5 12.5 11.8 12"
          stroke="url(#buddio-logo-grad)"
          strokeWidth="0.8"
          strokeLinecap="round"
        />
        <defs>
          <linearGradient id="buddio-logo-grad" x1="8.5" y1="7.5" x2="13.7" y2="13.5" gradientUnits="userSpaceOnUse">
            <stop stopColor="#4F8EF7" />
            <stop offset="1" stopColor="#7C5CFF" />
          </linearGradient>
        </defs>
      </svg>
    </div>
  );

  return (
    <Link href={href} className={cn("flex items-center gap-2.5 group", className)}>
      {mark}
      {showWordmark && (
        <span className={cn("font-bold tracking-tight text-slate-900", text)}>Buddio</span>
      )}
    </Link>
  );
}
