#!/usr/bin/env python3
"""
CRS Rule Command Executor
=========================
Scans YAML files under yamls/<version>/<type>/, lists them grouped by release,
lets the user select by index/range, and executes the commands inside a single
long-running pod via kubectl exec.

Usage:
    python run_rules.py [--namespace <ns>] [--pod-image <image>] [--delay <seconds>]
    python run_rules.py -rules          # regenerate command_notebook.txt
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import time
import yaml as pyyaml


# ── defaults ────────────────────────────────────────────────────────────────
YAMLS_ROOT      = os.path.join(os.path.dirname(os.path.abspath(__file__)), "yamls")
POD_NAME        = "crs-rule-executor"
DEFAULT_IMAGE   = "angelrita/base-ubuntu:latest"
DEFAULT_NS      = "default"
DEFAULT_DELAY   = 3          # seconds between commands
RULE_TYPES      = ["process", "fim", "network"]
SKIP_DIRS       = {"deprecated", "exploit-yamls", "testing", "not-fired"}
EXP_SUBDIR      = "experimental"
NOT_FIRED_DIR   = "not-fired"
NOTEBOOK_FILE   = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "command_notebook.txt")


# ── helpers ─────────────────────────────────────────────────────────────────
def run_kubectl(args: list[str], capture=True, timeout=60):
    """Run a kubectl command and return (returncode, stdout, stderr)."""
    cmd = ["kubectl"] + args
    try:
        r = subprocess.run(cmd, capture_output=capture, text=False, timeout=timeout)
        stdout = r.stdout.decode("utf-8", errors="replace").strip() if r.stdout else ""
        stderr = r.stderr.decode("utf-8", errors="replace").strip() if r.stderr else ""
        return r.returncode, stdout, stderr
    except subprocess.TimeoutExpired:
        return 1, "", "kubectl command timed out"
    except FileNotFoundError:
        print("ERROR: kubectl not found on PATH.")
        sys.exit(1)


def parse_selection(selection_str: str, max_index: int) -> list[int]:
    """Parse '1-3,5,7-9' into a sorted list of unique integers."""
    indices = set()
    for part in selection_str.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            tokens = part.split("-", 1)
            try:
                lo, hi = int(tokens[0].strip()), int(tokens[1].strip())
            except ValueError:
                print(f"  [!] Invalid range: '{part}', skipping.")
                continue
            if lo > hi:
                lo, hi = hi, lo
            for i in range(lo, hi + 1):
                if 1 <= i <= max_index:
                    indices.add(i)
                else:
                    print(f"  [!] Index {i} out of range (1-{max_index}), skipping.")
        else:
            try:
                i = int(part)
            except ValueError:
                print(f"  [!] Invalid index: '{part}', skipping.")
                continue
            if 1 <= i <= max_index:
                indices.add(i)
            else:
                print(f"  [!] Index {i} out of range (1-{max_index}), skipping.")
    return sorted(indices)


def extract_command_from_yaml(filepath: str) -> str | None:
    """Read a YAML file and return the shell command string from args."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            doc = pyyaml.safe_load(f)
    except Exception as e:
        print(f"  [!] Failed to parse {filepath}: {e}")
        return None

    try:
        containers = doc["spec"]["containers"]
        args = containers[0].get("args", [])
        # args is typically ["-c", "<command>"] or ['-c', '<command>']
        if len(args) >= 2 and args[0] == "-c":
            return args[1]
        elif len(args) == 1:
            return args[0]
        else:
            return " ".join(args)
    except (KeyError, IndexError, TypeError):
        return None


def strip_sleep(cmd: str) -> str:
    """Remove trailing '; sleep infinity' from command."""
    cmd = re.sub(r";\s*sleep\s+infinity\s*$", "", cmd).strip()
    return cmd


# ── discovery ───────────────────────────────────────────────────────────────
def discover_rules(yamls_root: str) -> list[dict]:
    """Walk the yamls directory tree and collect rule entries.
    Returns a list sorted: all production (non-experimental) rules first,
    then all experimental rules — each group ordered by version."""
    production = []
    experimental = []
    versions = sorted(
        [d for d in os.listdir(yamls_root)
         if os.path.isdir(os.path.join(yamls_root, d)) and d not in SKIP_DIRS],
        key=lambda v: [int(x) if x.isdigit() else x for x in v.split(".")]
    )

    for version in versions:
        ver_path = os.path.join(yamls_root, version)
        # Production rules: <version>/<rtype>/
        for rtype in RULE_TYPES:
            type_path = os.path.join(ver_path, rtype)
            if not os.path.isdir(type_path):
                continue
            yamls = sorted([f for f in os.listdir(type_path) if f.endswith(".yaml")])
            for yf in yamls:
                full = os.path.join(type_path, yf)
                cmd = extract_command_from_yaml(full)
                production.append({
                    "version": version,
                    "type": rtype,
                    "file": yf,
                    "path": full,
                    "name": yf.replace(".yaml", ""),
                    "command": cmd,
                    "experimental": False,
                })
        # Experimental rules: <version>/<rtype>/experimental/
        for rtype in RULE_TYPES:
            exp_type_path = os.path.join(ver_path, rtype, EXP_SUBDIR)
            if not os.path.isdir(exp_type_path):
                continue
            yamls = sorted([f for f in os.listdir(exp_type_path) if f.endswith(".yaml")])
            for yf in yamls:
                full = os.path.join(exp_type_path, yf)
                cmd = extract_command_from_yaml(full)
                experimental.append({
                    "version": version,
                    "type": rtype,
                    "file": yf,
                    "path": full,
                    "name": yf.replace(".yaml", ""),
                    "command": cmd,
                    "experimental": True,
                })
    return production + experimental


def discover_not_fired(yamls_root: str) -> list[dict]:
    """Discover rules in the not-fired directory.
    Returns non-experimental first, then experimental — each ordered by version."""
    nf_root = os.path.join(yamls_root, NOT_FIRED_DIR)
    if not os.path.isdir(nf_root):
        return []
    production = []
    experimental = []
    versions = sorted(
        [d for d in os.listdir(nf_root)
         if os.path.isdir(os.path.join(nf_root, d))],
        key=lambda v: [int(x) if x.isdigit() else x for x in v.split(".")]
    )
    for version in versions:
        ver_path = os.path.join(nf_root, version)
        # Non-experimental: <version>/<rtype>/
        for rtype in RULE_TYPES:
            type_path = os.path.join(ver_path, rtype)
            if not os.path.isdir(type_path):
                continue
            yamls = sorted([f for f in os.listdir(type_path) if f.endswith(".yaml")])
            for yf in yamls:
                full = os.path.join(type_path, yf)
                cmd = extract_command_from_yaml(full)
                production.append({
                    "version": version,
                    "type": rtype,
                    "file": yf,
                    "path": full,
                    "name": yf.replace(".yaml", ""),
                    "command": cmd,
                    "experimental": False,
                    "not_fired": True,
                })
        # Experimental: <version>/<rtype>/experimental/
        for rtype in RULE_TYPES:
            exp_type_path = os.path.join(ver_path, rtype, EXP_SUBDIR)
            if not os.path.isdir(exp_type_path):
                continue
            yamls = sorted([f for f in os.listdir(exp_type_path) if f.endswith(".yaml")])
            for yf in yamls:
                full = os.path.join(exp_type_path, yf)
                cmd = extract_command_from_yaml(full)
                experimental.append({
                    "version": version,
                    "type": rtype,
                    "file": yf,
                    "path": full,
                    "name": yf.replace(".yaml", ""),
                    "command": cmd,
                    "experimental": True,
                    "not_fired": True,
                })
    return production + experimental


def display_rules(rules: list[dict]):
    """Print rules grouped by category (Production first, then Experimental),
    sub-grouped by version and type, with a global 1-based index.
    Not-fired rules get a single NOT-FIRED header instead."""
    is_not_fired = any(r.get("not_fired") for r in rules)
    current_category = None
    current_version = None
    current_type = None
    prod_count = sum(1 for r in rules if not r.get("experimental"))
    exp_count = sum(1 for r in rules if r.get("experimental"))
    prefix = "NOT-FIRED " if is_not_fired else ""

    for idx, rule in enumerate(rules, 1):
        is_exp = rule.get("experimental", False)
        cat_label = f"{prefix}EXPERIMENTAL" if is_exp else f"{prefix}PRODUCTION"

        if cat_label != current_category:
            current_category = cat_label
            current_version = None
            current_type = None
            count = exp_count if is_exp else prod_count
            print(f"\n{'#'*60}")
            print(f"  {cat_label} RULES  ({count} rules)")
            print(f"{'#'*60}")

        if rule["version"] != current_version:
            current_version = rule["version"]
            current_type = None
            print(f"\n  {'─'*50}")
            print(f"  Release: {current_version}")
            print(f"  {'─'*50}")

        if rule["type"] != current_type:
            current_type = rule["type"]
            print(f"\n  [{current_type.upper()}]")

        status = "OK" if rule["command"] else "NO CMD"
        print(f"    {idx:>4}. {rule['name']}  [{status}]")
    print()


# ── notebook generation ─────────────────────────────────────────────────────
def generate_notebook(rules: list[dict], notebook_path: str):
    """Write command_notebook.txt in the standard grouped format.
    Backs up the existing file to a timestamped .bak before overwriting."""
    prod = [r for r in rules if not r.get("experimental")]
    exp = [r for r in rules if r.get("experimental")]
    nl = "\r\n"
    out = [
        "=" * 80,
        "CRS RULE COMMAND NOTEBOOK",
        "=" * 80,
        f"Total rules: {len(rules)}",
        f"Production: {len(prod)}",
        f"Experimental: {len(exp)}",
        "=" * 80,
        "",
    ]

    idx = 0
    for label, group in (("PRODUCTION", prod), ("EXPERIMENTAL", exp)):
        if not group:
            continue
        out += ["#" * 80, f"  {label} RULES  ({len(group)} rules)", "#" * 80, ""]
        current_version = None
        for r in group:
            if r["version"] != current_version:
                current_version = r["version"]
                out += [f"  --- Release: {current_version} ---", ""]
            idx += 1
            cat = "Experimental" if r.get("experimental") else "Production"
            cmd = strip_sleep(r["command"]) if r["command"] else "NO CMD"
            out += [
                f"{idx:>6}. {r['name']}",
                f"        Version : {r['version']}",
                f"        Type    : {r['type']}",
                f"        Category: {cat}",
                f"        Command : {cmd}",
                "",
            ]

    out += ["=" * 80, "END OF NOTEBOOK", "=" * 80]

    if os.path.exists(notebook_path):
        backup_dir = os.path.join(os.path.dirname(notebook_path), "commands")
        os.makedirs(backup_dir, exist_ok=True)
        ts = time.strftime("%Y%m%d_%H%M%S")
        base = os.path.splitext(os.path.basename(notebook_path))[0]
        backup = os.path.join(backup_dir, f"{base}_{ts}.bak")
        shutil.copy2(notebook_path, backup)
        print(f"  [+] Backed up existing notebook -> {backup}")

    with open(notebook_path, "w", encoding="utf-8", newline="") as f:
        f.write(nl.join(out) + nl)
    print(f"  [+] Wrote {len(rules)} rules -> {notebook_path}")


# ── pod management ──────────────────────────────────────────────────────────
def ensure_pod(namespace: str, image: str) -> bool:
    """Make sure the executor pod is running. Returns True on success."""
    # check if pod already exists and is running
    rc, out, _ = run_kubectl([
        "get", "pod", POD_NAME, "-n", namespace,
        "-o", "jsonpath={.status.phase}"
    ])
    if rc == 0 and out == "Running":
        print(f"  [+] Pod '{POD_NAME}' already running in namespace '{namespace}'.")
        return True

    if rc == 0:
        # pod exists but not running — delete and recreate
        print(f"  [~] Pod '{POD_NAME}' exists but status is '{out}'. Recreating...")
        run_kubectl(["delete", "pod", POD_NAME, "-n", namespace, "--grace-period=0", "--force"],
                     timeout=30)
        time.sleep(2)

    # create the pod
    print(f"  [+] Creating pod '{POD_NAME}' with image '{image}' ...")
    pod_manifest = f"""
apiVersion: v1
kind: Pod
metadata:
  name: {POD_NAME}
spec:
  restartPolicy: Never
  containers:
  - name: executor
    image: {image}
    command: ['sh']
    args: ['-c', 'sleep infinity']
""".strip()

    proc = subprocess.run(
        ["kubectl", "apply", "-n", namespace, "-f", "-"],
        input=pod_manifest, capture_output=True, text=True, timeout=30
    )
    if proc.returncode != 0:
        print(f"  [!] Failed to create pod: {proc.stderr}")
        return False

    # wait for pod to be ready
    print(f"  [~] Waiting for pod to be ready ...")
    rc, out, err = run_kubectl([
        "wait", "--for=condition=Ready", f"pod/{POD_NAME}",
        "-n", namespace, "--timeout=120s"
    ], timeout=130)
    if rc != 0:
        print(f"  [!] Pod did not become ready: {err}")
        return False

    print(f"  [+] Pod '{POD_NAME}' is ready.")
    return True


def execute_command(namespace: str, cmd: str, rule_name: str, delay: float):
    """Run a command inside the executor pod and print output."""
    clean_cmd = strip_sleep(cmd)
    print(f"\n{'─'*60}")
    print(f"  Rule   : {rule_name}")
    print(f"  Command: {clean_cmd}")
    print(f"{'─'*60}")

    rc, out, err = run_kubectl([
        "exec", POD_NAME, "-n", namespace, "--",
        "sh", "-c", clean_cmd
    ], timeout=60)

    if out:
        print(f"  [stdout]\n{out}")
    if err:
        print(f"  [stderr]\n{err}")
    if rc != 0:
        print(f"  [exit code: {rc}]")
    else:
        print(f"  [exit code: 0 - OK]")

    if delay > 0:
        time.sleep(delay)


# ── cleanup ─────────────────────────────────────────────────────────────────
def cleanup_pod(namespace: str):
    """Delete the executor pod."""
    print(f"\n  [~] Deleting pod '{POD_NAME}' ...")
    rc, _, err = run_kubectl([
        "delete", "pod", POD_NAME, "-n", namespace, "--grace-period=5"
    ], timeout=30)
    if rc == 0:
        print(f"  [+] Pod deleted.")
    else:
        print(f"  [!] Failed to delete pod: {err}")


# ── main ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="CRS Rule Command Executor")
    parser.add_argument("-n", "--namespace", default=DEFAULT_NS,
                        help=f"Kubernetes namespace (default: {DEFAULT_NS})")
    parser.add_argument("--pod-image", default=DEFAULT_IMAGE,
                        help=f"Image for the executor pod (default: {DEFAULT_IMAGE})")
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY,
                        help=f"Delay in seconds between commands (default: {DEFAULT_DELAY})")
    parser.add_argument("--yamls-root", default=YAMLS_ROOT,
                        help=f"Root directory for YAML files (default: {YAMLS_ROOT})")
    parser.add_argument("-d", "--not-fired", action="store_true",
                        help="Show and run NOT-FIRED rules instead of fired rules")
    parser.add_argument("-rules", "--rules", action="store_true",
                        help="Generate command_notebook.txt from discovered rules "
                             "(backs up existing file) and exit")
    args = parser.parse_args()

    # notebook generation mode — writes the file and exits
    if args.rules:
        print("\n[*] Scanning YAML rules ...")
        rules = discover_rules(args.yamls_root)
        if not rules:
            print("  No rules found. Check yamls directory.")
            sys.exit(1)
        print(f"  Found {len(rules)} rules.")
        generate_notebook(rules, NOTEBOOK_FILE)
        sys.exit(0)

    # discover
    if args.not_fired:
        print("\n[*] Scanning NOT-FIRED YAML rules ...")
        rules = discover_not_fired(args.yamls_root)
        if not rules:
            print("  No not-fired rules found. Check yamls/not-fired directory.")
            sys.exit(1)
    else:
        print("\n[*] Scanning YAML rules ...")
        rules = discover_rules(args.yamls_root)
        if not rules:
            print("  No rules found. Check yamls directory.")
            sys.exit(1)

    total = len(rules)
    label = "not-fired" if args.not_fired else "fired"
    print(f"  Found {total} {label} rules.\n")

    # display
    display_rules(rules)

    # selection loop
    while True:
        try:
            sel = input(f"Select rules (e.g. 1-3,5,7-9) or 'q' to quit: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            sys.exit(0)

        if sel.lower() in ("q", "quit", "exit"):
            print("Exiting.")
            sys.exit(0)

        if sel.lower() == "all":
            selected = list(range(1, total + 1))
        else:
            selected = parse_selection(sel, total)

        if not selected:
            print("  No valid indices selected. Try again.\n")
            continue

        # confirm
        print(f"\n  Selected {len(selected)} rule(s):")
        for i in selected:
            r = rules[i - 1]
            tag = "EXP" if r.get("experimental") else "PROD"
            print(f"    {i:>4}. [{r['version']}/{r['type']}] {r['name']} ({tag})")

        try:
            confirm = input("\n  Proceed? (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            sys.exit(0)

        if confirm != "y":
            print("  Cancelled. Select again.\n")
            continue

        # ensure pod
        print("\n[*] Ensuring executor pod is running ...")
        if not ensure_pod(args.namespace, args.pod_image):
            print("  [!] Cannot proceed without a running pod.")
            continue

        # execute
        print(f"\n[*] Executing {len(selected)} command(s) with {args.delay}s delay ...\n")
        success, failed, skipped = 0, 0, 0
        for i in selected:
            r = rules[i - 1]
            if not r["command"]:
                print(f"\n  [!] Skipping {r['name']} — no command found in YAML.")
                skipped += 1
                continue
            execute_command(args.namespace, r["command"], r["name"], args.delay)
            success += 1

        print(f"\n{'='*60}")
        print(f"  Execution complete: {success} ran, {skipped} skipped, {failed} failed")
        print(f"{'='*60}")

        # ask to clean up or continue
        try:
            action = input("\n  [c]ontinue selecting / [d]elete pod & exit / [q]uit: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            action = "q"

        if action == "d":
            cleanup_pod(args.namespace)
            break
        elif action in ("q", "quit", "exit"):
            print(f"  Pod '{POD_NAME}' left running. Delete manually with:")
            print(f"    kubectl delete pod {POD_NAME} -n {args.namespace}")
            break
        else:
            # re-display and loop
            display_rules(rules)
            continue


if __name__ == "__main__":
    main()
