"use client";

export default function Pricing() {
  async function subscribe() {
    const res = await fetch("/api/checkout", { method: "POST" });
    const { url } = await res.json();
    window.location.href = url;
  }
  return (
    <main>
      <h1>NoteSnap Pro: $9/month</h1>
      <button onClick={subscribe}>Subscribe</button>
    </main>
  );
}
