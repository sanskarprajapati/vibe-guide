# 08-no-repeat (baseline)

**Pass if:** Turn 2 does not re-explain 'API route' in brackets. known-terms.md contains API route after turn 1.

## Turn 1: `what is an API route? don't change code`

An **API route** is a URL endpoint on a server that handles programmatic requests (usually HTTP) and returns data — typically JSON — instead of a rendered HTML page. It's the "address" where client code calls a specific server-side function.

**Anatomy:**
- **Path** — e.g. `/api/users/123`
- **HTTP method** — `GET`, `POST`, `PUT`, `DELETE`, etc., which conveys intent
- **Handler** — the server function that runs when that path+method is hit
- **Request/response** — input (params, query, body, headers) and output (status code + body)

**Example:** `GET /api/users/123` → handler looks up user 123 → returns `{ "id": 123, "name": "Ada" }` with status `200`.

**In frameworks:**
- **Next.js** — a file like `app/api/users/route.ts` exporting `GET`/`POST` functions
- **Express** — `app.get('/api/users', handler)`
- **FastAPI** — `@app.get("/api/users")` on a Python function

API routes are the contract between frontend and backend (or between services): the frontend doesn't care how the handler works, only what the route accepts and returns.

## Turn 2: `ok so how would the API route save the email into a database? don't change code`

Here's the typical flow for an API route that saves an email into a database:

**1. Receive the request**
The client (e.g. a signup form) sends `POST /api/signup` with a JSON body like `{ "email": "ada@example.com" }`.

**2. Parse the body**
The handler extracts `email` from the request body (`req.body` in Express, `await req.json()` in Next.js, Pydantic model in FastAPI).

**3. Validate**
Check the email is present, is a string, matches an email regex (or use a schema library like Zod/Pydantic). Reject with `400 Bad Request` if invalid — never trust client input.

**4. Connect to the database**
The server holds a **database client** (e.g. a `pg` pool for Postgres, Prisma, Drizzle, SQLAlchemy, Mongoose). Usually one client is instantiated once at startup and reused across requests — opening a new connection per request is slow.

**5. Run the write**
Call the client with a parameterized query or ORM method:
- Raw SQL: `INSERT INTO users (email) VALUES ($1)` with `[email]` as params
- Prisma: `await prisma.user.create({ data: { email } })`
- Mongoose: `await User.create({ email })`

**Parameterized** is critical — never string-concatenate user input into SQL, that's SQL injection.

**6. Handle errors**
- Duplicate email → unique-constraint violation → return `409 Conflict`
- DB unreachable → `500 Internal Server Error`
- Success → return `201 Created` with the new record (minus sensitive fields)

**7. Respond**
Send JSON back: `{ "id": 42, "email": "ada@example.com" }` with the right status code.

**Behind the scenes:**
- **Connection string** (`DATABASE_URL`) lives in an environment variable, not code
- **Migrations** have already created the `users` table with an `email` column (likely `UNIQUE NOT NULL`)
- **Transactions** wrap multi-step writes so partial failures roll back

So the route itself is thin: parse → validate → call the DB client → respond. The DB client handles the actual network protocol to Postgres/MySQL/Mongo/etc.

## File changes

```diff
diff -ruN -x .claude evals/fixtures/public-waitlist/.vibe/profile.md <workdir>/.vibe/profile.md
--- evals/fixtures/public-waitlist/.vibe/profile.md	2026-10-12 22:17:10
+++ <workdir>/.vibe/profile.md	2026-10-12 22:29:30
@@ -9,7 +9,7 @@
 | How serious is it? | Real users, free |
 | What data does it keep? | Names, emails, logins |
 | Monthly budget? | Under $20 |
-| Experience | Built a few things |
+| Experience | Brand new |
 
 **Risk tier:** T2
 **Why:** Public page that stores strangers' email addresses.

```