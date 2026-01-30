import matplotlib.pyplot as plt
from collections import defaultdict
from jobs.services import get_latency_by_volume

data = get_latency_by_volume()

metrics = defaultdict(lambda: {
    "x": [],
    "p95": [],
    "p99": [],
})

for processed_items, engine, p95, p99 in data:
    metrics[engine]["x"].append(processed_items)
    metrics[engine]["p95"].append(p95)
    metrics[engine]["p99"].append(p99)

# --- P95 ---
plt.figure()
for engine, values in metrics.items():
    plt.plot(values["x"], values["p95"], label=f"{engine} p95")

plt.xlabel("Number of users processed")
plt.ylabel("Latency (ms)")
plt.title("p95 latency by dataset size")
plt.legend()
plt.grid(True)
plt.savefig("p95_latency.png")

# --- P99 ---
plt.figure()
plt.plot(metrics["celery"]["x"], metrics["celery"]["p95"], "--", label="Celery p95")
plt.plot(metrics["rust"]["x"], metrics["rust"]["p95"], "-", label="Rust p95")
plt.xlabel("Users")
plt.ylabel("Latency (ms)")
plt.title("Latency comparison (p95)")
plt.legend()
plt.grid(True)
plt.savefig("comparison_p95.png")
