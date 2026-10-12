"use client";
import { useState } from "react";

export default function Home() {
  const [email, setEmail] = useState("");
  const [done, setDone] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    await fetch("/api/signup", { method: "POST", body: JSON.stringify({ email }) });
    setDone(true);
  }

  return (
    <main>
      <h1>Plantpal: never kill a houseplant again</h1>
      {done ? (
        <p>You're on the list.</p>
      ) : (
        <form onSubmit={submit}>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <button type="submit">Join waitlist</button>
        </form>
      )}
    </main>
  );
}
