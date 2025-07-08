import { useEffect, useState } from "react";

export default function DarkModeToggle() {
  const [isDark, setIsDark] = useState(false); // default to light mode

  useEffect(() => {
    console.log(isDark);
    const html = document.documentElement;

    if (isDark) {
        html.classList.add("dark");
    } else {
        html.classList.remove("dark");
    }
    }, [isDark]);

  return (
    <button
      onClick={() => setIsDark((prev) => !prev)}
      className="px-4 py-2 text-sm rounded-md border border-gray-400 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700 transition"
    >
      {isDark ? "☀️ Light Mode" : "🌙 Dark Mode"}
    </button>
  );
}
