# 10-deeper (baseline)

**Pass if:** Turn 1: plain explanation with an everyday analogy. Turn 2: goes one step deeper with a small diagram (ASCII or mermaid) instead of repeating the same words.

## Turn 1: `I don't get what an API is`

An API (Application Programming Interface) is a way for two pieces of software to talk to each other through a defined set of rules.

**A simple analogy:** Think of a restaurant. You (the customer) don't walk into the kitchen to cook your own food. You look at a menu, tell the waiter what you want, and the waiter brings it back. The **menu + waiter** is the API — it defines what you can ask for and handles the request without you needing to know how the kitchen works.

**A concrete example:** When a weather app on your phone shows today's forecast, it doesn't have weather data built in. It sends a request to a weather service's API like:

```
GET https://api.weather.com/forecast?city=NYC
```

The weather service sends back something like:

```json
{ "temp": 58, "condition": "cloudy" }
```

The app then displays that nicely. The API is the agreed-upon "you ask like this, I'll answer like that" contract.

**Why APIs matter:**
- They let apps use features without rebuilding them (login with Google, pay with Stripe, show a map).
- They hide complexity — you don't need to know *how* it works, only how to ask.
- They work across languages — a Python app can call an API written in Java.

Want me to show you a tiny working example in a language you know, or walk through a specific API you've heard of?

## Turn 2: `still don't get it`

Okay, let me try a different angle — forget software for a second.

**A light switch is an "API" for electricity.**

You flip the switch up → light turns on. You flip it down → light turns off.

You have no idea what's happening behind the wall. There are wires, a power grid, a plant burning gas somewhere, voltage, circuits. You don't need to know any of it. Someone decided: *"up means on, down means off"* — and that's the only thing you need to learn.

That agreement — **"here's what you can do, and here's what happens"** — is the API.

---

**Another one: a vending machine.**

- You can put in money (one thing it accepts)
- You can press a button like "B4" (another thing it accepts)
- It gives you a soda (what you get back)

You can't ask it to make you a sandwich. You can't reach inside and grab stuff. The machine *defines* what requests it understands and what it will give you in return. That's its API.

---

**Now software:**

Instagram has an API. It basically says: "If you send me a username, I'll send you back their profile picture." That's it. A different app can use that to show Instagram photos without being Instagram.

The API is just **the list of things you're allowed to ask for, and what you'll get back.**

Does the vending machine version click? If not, tell me what part feels fuzzy — "what you send," "what you get back," or "why anyone would want this" — and I'll zoom in there.

## File changes

```diff
(no file changes)
```