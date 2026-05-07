# CRS Testbed - Container Runtime Security Testing

A collection of Kubernetes manifests and commands for testing container runtime security detection coverage across 25 real-world attack techniques.

---

## Prerequisites

- A running Kubernetes cluster
- `kubectl` configured and pointing to your cluster
- Cluster permissions to create pods and deployments

---

## Getting Started

### Step 1 — Deploy the Testbed Pod

```bash
kubectl apply -f secops-testbed.yaml
```

### Step 2 — Verify the Pod is Running

```bash
kubectl get pods -l app=secops-testbed
```

### Step 3 — Shell into the Pod

```bash
kubectl exec -it deploy/secops-testbed -- /bin/bash
```

### Step 4 — Run Test Commands

Once inside the shell, run the commands from `secops-testbed-runbook.txt` one by one and verify your detection platform raises the expected alert for each.

### Step 5 — Cleanup

```bash
kubectl delete deployment secops-testbed
```

---

## Repository Structure

```
secops-testbed/
├── README.md
├── secops-testbed.yaml          # Main deployment — run this first
├── secops-testbed-runbook.txt   # All 25 test commands with descriptions
└── manifests/
    ├── 0.9.10/                  # 14 test case manifests (v0.9.10)
    └── 0.9.11/                  # 11 test case manifests (v0.9.11)
```

---

## Test Coverage

| Version  | Tests      | Count |
|----------|------------|-------|
| v0.9.10  | 01 – 14    | 14    |
| v0.9.11  | 15 – 25    | 11    |
| **Total**|            | **25**|

### MITRE ATT&CK Tactics Covered

- Defense Evasion
- Privilege Escalation
- Credential Access
- Discovery & Reconnaissance
- Persistence
- Command and Control
- Execution
- Exfiltration
- Impact / Resource Hijacking

---

## Disclaimer

These test cases are intended solely for use in **authorized and isolated lab environments**.  
Do not execute against production workloads or any system without explicit written authorization.
