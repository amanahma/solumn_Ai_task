# Ticket: Load-Testing Harness for Internal API Gateway

**Team:** Platform Reliability
**Component:** `api-load-tester`
**Priority:** Medium

---

## Background

The API gateway team has deployed a new middleware stack to our internal
service mesh. Before promoting it to production, the SRE team needs a
load-testing harness that can characterise the gateway's behaviour under
sustained traffic and produce a structured JSON report for review.

A partial implementation lives in `/app`. Configuration parsing, project
layout, and helper utilities are already in place. Your job is to complete
the three stubbed functions so the harness runs end-to-end and writes a
valid report.

---

## What to implement

### 1. `ratelimit.py` — `TokenBucket.acquire()`

Fill in the token-refill and wait logic so the bucket correctly throttles
callers to the rate configured at construction time. The class docstring
describes the expected contract.

### 2. `sender.py` — `send_requests(config: SenderConfig)`

Implement the async request loop. For each request record the HTTP status
code, round-trip latency in milliseconds, and wall-clock timestamp.
Return a `list[RequestResult]` for the collector.

### 3. `collector.py` — `compute_summary(results, percentiles)`

Aggregate the results list into a `Summary` object:

- `total_requests`: total number of requests made.
- `status_codes`: mapping of status code (as string) → count.
- `rejection_rate`: fraction of responses with status ≥ 400 (float, 0–1).
- `latency_percentiles`: mapping of `"p<N>"` → millisecond value for each
  percentile in the `percentiles` argument (e.g. `"p50"`, `"p90"`).

---

## Entry point

`controller.py` is already complete. Running

```
python /app/controller.py
```

reads `config.toml`, calls your three functions in order, and writes the
JSON report to the path specified under `[report] output_file`.

---

## Acceptance criteria

- The report file exists at the configured path after the run.
- `rejection_rate` is a float in `[0.0, 1.0]`.
- `latency_percentiles` contains a key for every percentile listed in
  `config.toml` (e.g. `p50`, `p90`, `p95`, `p99`).
- The process exits with code 0 after completing its run.

---

## Target service

The gateway stand-in is already running at `http://127.0.0.1:8000`.
You do not need to start or configure it.
