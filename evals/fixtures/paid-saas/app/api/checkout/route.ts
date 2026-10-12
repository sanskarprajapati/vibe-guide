import { stripe } from "@/lib/stripe";

export async function POST() {
  const session = await stripe.checkout.sessions.create({
    mode: "subscription",
    line_items: [{ price: process.env.STRIPE_PRICE_ID, quantity: 1 }],
    success_url: `${process.env.APP_URL}/dashboard`,
    cancel_url: `${process.env.APP_URL}/pricing`,
  });
  return Response.json({ url: session.url });
}
