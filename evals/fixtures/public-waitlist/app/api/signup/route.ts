export async function POST(req: Request) {
  const { email } = await req.json();
  // TODO: store the email somewhere
  console.log("signup", email);
  return Response.json({ ok: true });
}
