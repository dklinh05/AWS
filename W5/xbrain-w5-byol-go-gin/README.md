# Go + Gin — BYOL starter (NOT YET SERVERLESS)

This is a plain Gin app. It runs locally as a normal Go HTTP server.
**It does not run on Lambda yet.** Your group's job is to make it run on
Lambda with the **minimum** code/config changes.

```
go-gin/
├── server/server.go        ← The existing Gin router (Lambda-unaware — leave alone)
├── cmd/local/main.go       ← Local runner: `go run ./cmd/local` → http://localhost:8080
├── go.mod                  ← Only `gin` listed; add anything else you need
├── template.yaml           ← SAM scaffold — has TODO markers you must address
├── samconfig.toml          ← stack name + region (us-west-2) pre-set
└── README.md               ← this file
```

## Step 0 — Confirm the app works in its current "non-serverless" form

```bash
go mod tidy
go run ./cmd/local
# → listening on http://localhost:8080

# in another terminal:
curl http://localhost:8080/
curl http://localhost:8080/api/hello/Lan
curl -X POST http://localhost:8080/api/echo -H 'Content-Type: application/json' -d '{"hi":"there"}'
```

## Step 1 — Pick your strategy

| # | Strategy | What you add | Code-change cost | Cold start estimate |
|---|----------|--------------|------------------|---------------------|
| A | `aws-lambda-go-api-proxy/gin` | new `main.go` at root + 2 deps | ~8 lines | 50–150 ms |
| B | **AWS Lambda Web Adapter** | shell wrapper + edit `template.yaml` | 0 Go lines | +200 ms over A |
| C | Plain `aws-lambda-go` (manual routing) | new `main.go` + manual `events.APIGatewayV2HTTPRequest` → response translation | 30–80 lines | ~50 ms |

Document **why** you picked your option in `NOTES.md` (you'll need it for
worksheet Q4.1 + Q4.6).

## Step 2 — Implement

The repo intentionally leaves you these blanks:

- `go.mod` — only `gin` is declared. Add `github.com/aws/aws-lambda-go` and
  any adapter you choose. Run `go mod tidy` to regenerate `go.sum`.
- *New file(s)* at repo root with `package main` — required so SAM's
  `BuildMethod: go1.x` finds a build entrypoint.
- `template.yaml` — `BuildMethod` and the new file's presence are what
  drive `sam build`. If you go the Web Adapter route, switch `BuildMethod`
  to `makefile` and add a Makefile (see template comments).

> **Hard rule:** `server/server.go` must NOT import anything from
> `aws-lambda-go` or any adapter. Keep the framework layer clean.

## Step 3 — Build + deploy

```bash
sam build
sam deploy --guided          # first time only
sam deploy                   # subsequent
```

Region MUST be `us-west-2` if you're on the workshop participant account.

`sam build` produces `.aws-sam/build/GinFunction/bootstrap` (a static
linux/arm64 binary) — that's what Lambda runs.

## Step 4 — Smoke-test the live URL

```bash
export API=$(aws cloudformation describe-stacks \
  --stack-name byol-go-gin --region us-west-2 \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' --output text)

curl $API
curl $API/api/hello/Lan
curl -X POST $API/api/echo -H 'Content-Type: application/json' -d '{"hi":"there"}'
```

Responses MUST match the local versions byte-for-byte (same JSON keys).

## Step 5 — Measure cold start

```bash
sam logs --stack-name byol-go-gin --region us-west-2 -t
```

Find the `REPORT` line. Go cold starts are typically **50–150 ms** —
the fastest of any mainstream Lambda runtime, ~10× faster than Python.

## Teardown

```bash
sam delete --stack-name byol-go-gin --region us-west-2
```

## Common pitfalls

| Symptom | Probably... |
|---------|-------------|
| `sam build` says "no main package in root" | You need a `package main` file at repo root (where `go.mod` lives) — `cmd/local/main.go` is in a subpackage, doesn't count |
| Build succeeds but Lambda 502s with "runtime exited without providing a reason" | Forgot `lambda.Start(handler)` in your `main()`; binary exits immediately |
| `go.sum: missing entry for ...` | Run `go mod tidy` after editing go.mod |
| Binary too big (>250 MB) | Use `arm64` (already set); avoid CGO; check you're not importing the whole AWS SDK when you only need `lambda-go` |
| Routes 404 in Lambda but work locally | Path stripping by API GW — `aws-lambda-go-api-proxy/gin` handles it; rolling your own means manual handling |
| AccessDenied on deploy | Wrong region — must be `us-west-2` on workshop role |
