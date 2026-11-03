# CRS Testbed - Container Runtime Security Testing

A collection of Kubernetes pod manifests and an interactive runner for testing container runtime security (CRS) detection coverage across real-world attack techniques.

Each YAML file under `yamls/` describes one detection rule and the command that should trigger it. `run_rules.py` finds those rules, lets you pick which ones to run, and executes their commands inside a single long-running pod via `kubectl exec`, so you can check that your detection platform raises the expected alert for each one.

---

## Coverage

| Release | Production | Experimental | Total |
|---------|-----------:|-------------:|------:|
| 0.9.10  | 14 | – | 14 |
| 0.9.11  | 11 | – | 11 |
| 0.9.12  | 11 | 8 | 19 |
| 0.9.13  | 17 | 26 | 43 |
| 0.9.14  | 1 | 14 | 15 |
| **Total** | **54** | **48** | **102** |

A further **26 rules** are kept in `yamls/not-fired/` (0.9.12: 11, 0.9.13: 12, 0.9.14: 3). Those are rules whose test commands did not raise an alert during testing.

---

## Prerequisites

- A running Kubernetes cluster
- `kubectl` configured and pointing to your cluster
- Permission to create, exec into, and delete pods in the target namespace
- Python 3.10+ with PyYAML (`pip install pyyaml`)

---

## Quick Start

```bash
git clone https://github.com/amanjangid26/qualys-crs-threat-detection.git
cd qualys-crs-threat-detection
pip install pyyaml
python3 run_rules.py
```

The script will:

1. Scan `yamls/` and list every rule, grouped by release and tagged `PROD` or `EXP`.
2. Prompt you to select rules by index: `5`, `1-3,7,9-12`, or `all`.
3. Create (or reuse) an executor pod named `crs-rule-executor`.
4. Run each selected rule's command inside the pod, with a delay between commands.
5. Ask whether to **[c]ontinue** selecting, **[d]elete** the pod and exit, or **[q]uit** and leave the pod running.

---

## Usage

```
python3 run_rules.py [options]
```

| Option | Default | Description |
|--------|---------|-------------|
| `-n`, `--namespace` | `default` | Kubernetes namespace for the executor pod |
| `--pod-image` | `angelrita/base-ubuntu:latest` | Image used for the executor pod |
| `--delay` | `3` | Seconds to wait between commands |
| `--yamls-root` | `./yamls` | Root directory containing the rule YAMLs |
| `-d`, `--not-fired` | off | List and run rules from `yamls/not-fired/` instead |
| `-rules`, `--rules` | off | Regenerate `command_notebook.txt` and exit (backs up the existing file) |

Examples:

```bash
# Run rules in a dedicated namespace with a 5s gap between commands
python3 run_rules.py -n crs-test --delay 5

# Re-test rules that previously did not fire
python3 run_rules.py --not-fired

# Refresh the command notebook after adding or editing YAMLs
python3 run_rules.py -rules
```

### Running a single manifest directly

Each YAML is also a standalone pod manifest that runs its trigger command when applied:

```bash
kubectl apply -f yamls/0.9.12/process/gdb-executed-in-container.yaml
kubectl delete pod gdb-executed-in-container
```

---

## Repository Structure

```
.
├── README.md
├── run_rules.py              # Interactive rule runner
├── command_notebook.txt      # Reference list of every rule and its command (generated)
└── yamls/
    ├── 0.9.10/process/       # 14 rules
    ├── 0.9.11/process/       # 11 rules
    ├── 0.9.12/process/       # 11 rules + experimental/ (8)
    ├── 0.9.13/process/       # 17 rules + experimental/ (26)
    ├── 0.9.14/process/       # 1 rule  + experimental/ (14)
    └── not-fired/            # Rules that did not trigger an alert
        ├── 0.9.12/process/
        ├── 0.9.13/process/
        └── 0.9.14/process/
```

### Adding a rule

1. Create a pod manifest at `yamls/<version>/<type>/<rule-name>.yaml`, where `<type>` is `process`, `fim`, or `network`. Put it in an `experimental/` subfolder if the rule is experimental.
2. Put the trigger command in the container's `args`, for example `args: ['-c', '<command>; sleep infinity']`. The runner extracts the command and strips the trailing `sleep`.
3. Run `python3 run_rules.py -rules` to regenerate `command_notebook.txt`.

---

## ⚠️ Safety

These commands simulate attacker behaviour, including container escapes, credential access, log tampering, cryptominer activity, and reverse shells. Run them **only on isolated, non-production test clusters that you own or are authorised to test**. Some commands are destructive inside the pod (for example, deleting logs or bulk data), and some reach out to the network.

---

## Cleanup

```bash
kubectl delete pod crs-rule-executor -n <namespace>
```
