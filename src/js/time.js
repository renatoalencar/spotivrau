export function formatTime(time) {
  if (time === undefined || time === null) {
    return "--:--";
  }

  const parts = [];

  do {
    parts.push(time % 60);
    time = Math.floor(time / 60);
  } while (time > 0);

  if (parts.length === 1) {
    parts.push(0);
  }

  parts.reverse();

  return parts.map((p) => p.toString().padStart(2, "0")).join(":");
}
