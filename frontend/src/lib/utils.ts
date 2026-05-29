import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Standard utility to conditionally merge Tailwind CSS classes
 * without style conflicts (using tailwind-merge under the hood).
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
