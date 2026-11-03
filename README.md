<div align="center">

# 🛡️ CRS Threat Detection Testbed

**Simulate real-world container attacks on Kubernetes and confirm your runtime security raises an alert for each one.**

![Kubernetes](https://img.shields.io/badge/Kubernetes-ready-326CE5?logo=kubernetes&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Rules](https://img.shields.io/badge/detection%20rules-102-success)
![MITRE ATT&CK](https://img.shields.io/badge/MITRE%20ATT%26CK-11%20tactics%20·%2039%20techniques-red)
![Releases](https://img.shields.io/badge/releases-0.9.10%20→%200.9.14-informational)

[Quick Start](#-quick-start) •
[ATT&CK Coverage](#-mitre-attck-coverage) •
[How It Works](#-how-it-works) •
[Options](#-command-line-options) •
[Rule Catalog](#-rule-catalog) •
[Troubleshooting](#-troubleshooting)

</div>

---

> [!WARNING]
> These tests **imitate attacker behaviour**: container escapes, credential theft, log tampering, cryptominers, reverse shells and more.
> Run them **only on an isolated, non-production cluster** that you own or are authorised to test.

---

## 📖 What is this?

This repository contains **102 attack simulations** for testing **Container Runtime Security (CRS)** detections, plus a small interactive tool that runs them for you.

- **No manual typing.** Pick tests from a numbered menu and the tool runs them for you.
- **One pod, no clutter.** Every test runs inside a single short-lived pod that you delete when you're done.
- **Organised by release.** Rules are grouped by the detection release that introduced them, from `0.9.10` to `0.9.14`.
- **Production and experimental.** ✅ Production rules are generally available; 🧪 experimental rules are newer detections.

| Release | ✅ Production | 🧪 Experimental | Total |
|:-------:|:------------:|:---------------:|:-----:|
| 0.9.10 | 14 | – | 14 |
| 0.9.11 | 11 | – | 11 |
| 0.9.12 | 11 | 8 | 19 |
| 0.9.13 | 17 | 26 | 43 |
| 0.9.14 | 1 | 14 | 15 |
| **Total** | **54** | **48** | **102** |

---

## 🎯 MITRE ATT&CK Coverage

The 102 main tests cover **11 of the 14 MITRE ATT&CK Enterprise tactics** and **39 techniques**, with a strong focus on container-specific behaviour such as escape to host, abuse of the container runtime socket, and theft of Kubernetes tokens.

| Tactic | Tests | Techniques |
|---|:--:|---|
| ➖ Reconnaissance | – | *not covered* |
| ➖ Resource Development | – | *not covered* |
| 🚪 **Initial Access** | 44 | [T1190](https://attack.mitre.org/techniques/T1190/) |
| ⚡ **Execution** | 6 | [T1059.004](https://attack.mitre.org/techniques/T1059/004/), [T1059.006](https://attack.mitre.org/techniques/T1059/006/), [T1609](https://attack.mitre.org/techniques/T1609/), [T1610](https://attack.mitre.org/techniques/T1610/) |
| 📌 **Persistence** | 5 | [T1053.003](https://attack.mitre.org/techniques/T1053/003/), [T1098](https://attack.mitre.org/techniques/T1098/), [T1136](https://attack.mitre.org/techniques/T1136/), [T1136.001](https://attack.mitre.org/techniques/T1136/001/), [T1547.006](https://attack.mitre.org/techniques/T1547/006/) |
| 🔺 **Privilege Escalation** | 14 | [T1068](https://attack.mitre.org/techniques/T1068/), [T1611](https://attack.mitre.org/techniques/T1611/) |
| 🥷 **Defense Evasion** | 8 | [T1027.003](https://attack.mitre.org/techniques/T1027/003/), [T1027.004](https://attack.mitre.org/techniques/T1027/004/), [T1055.008](https://attack.mitre.org/techniques/T1055/008/), [T1070.002](https://attack.mitre.org/techniques/T1070/002/), [T1222.002](https://attack.mitre.org/techniques/T1222/002/), [T1562.001](https://attack.mitre.org/techniques/T1562/001/), [T1564](https://attack.mitre.org/techniques/T1564/) |
| 🔑 **Credential Access** | 11 | [T1003](https://attack.mitre.org/techniques/T1003/), [T1003.008](https://attack.mitre.org/techniques/T1003/008/), [T1040](https://attack.mitre.org/techniques/T1040/), [T1528](https://attack.mitre.org/techniques/T1528/), [T1552](https://attack.mitre.org/techniques/T1552/), [T1552.001](https://attack.mitre.org/techniques/T1552/001/), [T1552.003](https://attack.mitre.org/techniques/T1552/003/), [T1552.004](https://attack.mitre.org/techniques/T1552/004/), [T1552.005](https://attack.mitre.org/techniques/T1552/005/), [T1552.007](https://attack.mitre.org/techniques/T1552/007/) |
| 🔍 **Discovery** | 3 | [T1046](https://attack.mitre.org/techniques/T1046/), [T1083](https://attack.mitre.org/techniques/T1083/), [T1613](https://attack.mitre.org/techniques/T1613/) |
| ➖ Lateral Movement | – | *not covered* |
| 🗃 **Collection** | 1 | [T1560.001](https://attack.mitre.org/techniques/T1560/001/) |
| 📡 **Command and Control** | 2 | [T1090](https://attack.mitre.org/techniques/T1090/), [T1105](https://attack.mitre.org/techniques/T1105/) |
| 📤 **Exfiltration** | 1 | [T1041](https://attack.mitre.org/techniques/T1041/) |
| 💥 **Impact** | 7 | [T1485](https://attack.mitre.org/techniques/T1485/), [T1496](https://attack.mitre.org/techniques/T1496/), [T1499.004](https://attack.mitre.org/techniques/T1499/004/) |

<details>
<summary><b>Technique-by-technique breakdown</b> (click to expand)</summary>

| Technique | Name | Tactic | Test # |
|---|---|---|---|
| [T1190](https://attack.mitre.org/techniques/T1190/) | Exploit Public-Facing Application | Initial Access | 27, 33, 37–39, 45–52, 54, 63–67, 69–72, 76–93, 100–102 |
| [T1059.004](https://attack.mitre.org/techniques/T1059/004/) | Unix Shell | Execution | 9, 35, 57 |
| [T1059.006](https://attack.mitre.org/techniques/T1059/006/) | Python | Execution | 12 |
| [T1609](https://attack.mitre.org/techniques/T1609/) | Container Administration Command | Execution | 98 |
| [T1610](https://attack.mitre.org/techniques/T1610/) | Deploy Container | Execution | 42 |
| [T1053.003](https://attack.mitre.org/techniques/T1053/003/) | Cron | Persistence | 13 |
| [T1098](https://attack.mitre.org/techniques/T1098/) | Account Manipulation | Persistence | 31 |
| [T1136](https://attack.mitre.org/techniques/T1136/) | Create Account | Persistence | 8 |
| [T1136.001](https://attack.mitre.org/techniques/T1136/001/) | Local Account | Persistence | 62 |
| [T1547.006](https://attack.mitre.org/techniques/T1547/006/) | Kernel Modules and Extensions | Persistence | 60 |
| [T1068](https://attack.mitre.org/techniques/T1068/) | Exploitation for Privilege Escalation | Privilege Escalation | 21, 24 |
| [T1611](https://attack.mitre.org/techniques/T1611/) | Escape to Host | Privilege Escalation | 2–4, 16, 17, 26, 41, 53, 94–97 |
| [T1027.003](https://attack.mitre.org/techniques/T1027/003/) | Steganography | Defense Evasion | 25 |
| [T1027.004](https://attack.mitre.org/techniques/T1027/004/) | Compile After Delivery | Defense Evasion | 56 |
| [T1055.008](https://attack.mitre.org/techniques/T1055/008/) | Ptrace System Calls | Defense Evasion | 28 |
| [T1070.002](https://attack.mitre.org/techniques/T1070/002/) | Clear Linux or Mac System Logs | Defense Evasion | 1, 32 |
| [T1222.002](https://attack.mitre.org/techniques/T1222/002/) | Linux and Mac File and Directory Permissions Modification | Defense Evasion | 59 |
| [T1562.001](https://attack.mitre.org/techniques/T1562/001/) | Disable or Modify Tools | Defense Evasion | 14 |
| [T1564](https://attack.mitre.org/techniques/T1564/) | Hide Artifacts | Defense Evasion | 11 |
| [T1003](https://attack.mitre.org/techniques/T1003/) | OS Credential Dumping | Credential Access | 18, 58 |
| [T1003.008](https://attack.mitre.org/techniques/T1003/008/) | /etc/passwd and /etc/shadow | Credential Access | 15 |
| [T1040](https://attack.mitre.org/techniques/T1040/) | Network Sniffing | Credential Access | 61 |
| [T1528](https://attack.mitre.org/techniques/T1528/) | Steal Application Access Token | Credential Access | 99 |
| [T1552](https://attack.mitre.org/techniques/T1552/) | Unsecured Credentials | Credential Access | 20 |
| [T1552.001](https://attack.mitre.org/techniques/T1552/001/) | Credentials In Files | Credential Access | 19 |
| [T1552.003](https://attack.mitre.org/techniques/T1552/003/) | Shell History | Credential Access | 5 |
| [T1552.004](https://attack.mitre.org/techniques/T1552/004/) | Private Keys | Credential Access | 23 |
| [T1552.005](https://attack.mitre.org/techniques/T1552/005/) | Cloud Instance Metadata API | Credential Access | 55 |
| [T1552.007](https://attack.mitre.org/techniques/T1552/007/) | Container API | Credential Access | 74 |
| [T1046](https://attack.mitre.org/techniques/T1046/) | Network Service Discovery | Discovery | 10 |
| [T1083](https://attack.mitre.org/techniques/T1083/) | File and Directory Discovery | Discovery | 22 |
| [T1613](https://attack.mitre.org/techniques/T1613/) | Container and Resource Discovery | Discovery | 43 |
| [T1560.001](https://attack.mitre.org/techniques/T1560/001/) | Archive via Utility | Collection | 36 |
| [T1090](https://attack.mitre.org/techniques/T1090/) | Proxy | Command and Control | 7 |
| [T1105](https://attack.mitre.org/techniques/T1105/) | Ingress Tool Transfer | Command and Control | 30 |
| [T1041](https://attack.mitre.org/techniques/T1041/) | Exfiltration Over C2 Channel | Exfiltration | 75 |
| [T1485](https://attack.mitre.org/techniques/T1485/) | Data Destruction | Impact | 34 |
| [T1496](https://attack.mitre.org/techniques/T1496/) | Resource Hijacking | Impact | 6, 29 |
| [T1499.004](https://attack.mitre.org/techniques/T1499/004/) | Application or System Exploitation | Impact | 40, 44, 68, 73 |

</details>

> [!NOTE]
> Each test is mapped to the **one ATT&CK technique that best describes the behaviour it simulates**. This is a guide to what the test set exercises, not the detection product's official rule mapping. Many tests also touch secondary techniques; for example, a reverse shell also involves command and control. The 26 [not-fired rules](#-not-fired-rules) are not included in these counts.

---

## 🔄 How it works

```mermaid
flowchart LR
    A["📂 yamls/<br/>rule manifests"] --> B["🐍 run_rules.py<br/>numbered menu"]
    B -->|you pick tests| C["📦 crs-rule-executor<br/>pod"]
    C -->|kubectl exec runs<br/>each attack command| D["🛡️ Your runtime<br/>security sensor"]
    D --> E["🚨 Alert in your<br/>detection console"]
```

1. `run_rules.py` reads every rule in `yamls/` and shows them as a numbered list.
2. You choose which tests to run.
3. The tool creates a pod called `crs-rule-executor` (or reuses it if it's already running).
4. Each test's command is run inside that pod, with a short pause between tests.
5. You check your detection console for a matching alert for each test.

---

## ✅ Prerequisites

| Requirement | Check with |
|---|---|
| A Kubernetes cluster with your runtime security sensor installed | – |
| `kubectl` installed and pointing at that cluster | `kubectl get nodes` |
| Permission to create, exec into and delete pods | `kubectl auth can-i create pods` |
| Python **3.10 or newer** | `python3 --version` |
| The PyYAML package | `pip install pyyaml` |
| The cluster can pull `angelrita/base-ubuntu:latest` from Docker Hub | see [Troubleshooting](#-troubleshooting) if not |

---

## 🚀 Quick Start

**1. Download the repository**

```bash
git clone https://github.com/amanjangid26/qualys-crs-threat-detection.git
cd qualys-crs-threat-detection
pip install pyyaml
```

**2. Start the tool**

```bash
python3 run_rules.py
```

**3. Choose the tests to run**

You'll see every rule with a number. Type your choice and press <kbd>Enter</kbd>:

| You type | It runs |
|---|---|
| `5` | test number 5 |
| `1-14` | tests 1 to 14 |
| `1-3,7,20-25` | a mix of single tests and ranges |
| `all` | every test |
| `q` | nothing; exits |

Confirm with `y`, and the tests run one by one.

**4. Check your detection console**

Each test's rule name is printed as it runs. Look for an alert with the same name in your console. The [Rule Catalog](#-rule-catalog) lists every test number and rule.

**5. Finish up**

When the run finishes, you're asked what to do next:

| Key | Action |
|:---:|---|
| `c` | Go back to the menu and run more tests |
| `d` | Delete the test pod and exit (recommended when you're done) |
| `q` | Exit and leave the pod running |

---

## 🖥️ Example session

```text
$ python3 run_rules.py

[*] Scanning YAML rules ...
  Found 102 fired rules.

############################################################
  PRODUCTION RULES  (54 rules)
############################################################

  ──────────────────────────────────────────────────
  Release: 0.9.10
  ──────────────────────────────────────────────────

  [PROCESS]
       1. clear-system-logs  [OK]
       2. container-escape-using-docker-socket  [OK]
       3. container-escape-using-runtime-socket  [OK]
       ...

Select rules (e.g. 1-3,5,7-9) or 'q' to quit: 1-3

  Selected 3 rule(s):
       1. [0.9.10/process] clear-system-logs (PROD)
       2. [0.9.10/process] container-escape-using-docker-socket (PROD)
       3. [0.9.10/process] container-escape-using-runtime-socket (PROD)

  Proceed? (y/n): y

[*] Ensuring executor pod is running ...
  [+] Pod 'crs-rule-executor' is ready.

[*] Executing 3 command(s) with 3.0s delay ...

────────────────────────────────────────────────────────────
  Rule   : clear-system-logs
  Command: rm /var/log/syslog; rm /var/log/messages; ...
────────────────────────────────────────────────────────────
  ...

  [c]ontinue selecting / [d]elete pod & exit / [q]uit: d
  [+] Pod deleted.
```

> [!NOTE]
> A test that prints errors or a non-zero exit code hasn't necessarily failed. Many tests imitate attacks against targets that don't exist in the test pod. **Your detection console decides whether a test passed**, not the command output.

---

## 🧰 Command-line options

```bash
python3 run_rules.py [options]
```

| Option | Default | What it does |
|---|---|---|
| `-n`, `--namespace` | `default` | Namespace to create the test pod in |
| `--pod-image` | `angelrita/base-ubuntu:latest` | Container image for the test pod |
| `--delay` | `3` | Seconds to wait between tests |
| `--yamls-root` | `./yamls` | Folder containing the rule manifests |
| `-d`, `--not-fired` | off | Show the [not-fired rules](#-not-fired-rules) instead |
| `-rules`, `--rules` | off | Rebuild `command_notebook.txt` and exit |

**Common examples**

```bash
# Run in a dedicated namespace
kubectl create namespace crs-test
python3 run_rules.py -n crs-test

# Give each alert more time to arrive before the next test
python3 run_rules.py --delay 10
```

---

## 📚 Rule Catalog

The numbers below match the numbers in the tool's menu, and each rule links to its mapped ATT&CK technique. Production rules are numbered first (1–54), then experimental rules (55–102). Click a release to expand it.

`command_notebook.txt` lists the exact command each test runs.

<details>
<summary><b>Release 0.9.10</b> — 14 production</summary>

| # | Rule | Stage | ATT&CK | Manifest |
|--:|------|:-----:|---|----------|
| 1 | `clear-system-logs` | ✅ Production | [T1070.002](https://attack.mitre.org/techniques/T1070/002/) | [clear-system-logs.yaml](yamls/0.9.10/process/clear-system-logs.yaml) |
| 2 | `container-escape-using-docker-socket` | ✅ Production | [T1611](https://attack.mitre.org/techniques/T1611/) | [container-escape-using-docker-socket.yaml](yamls/0.9.10/process/container-escape-using-docker-socket.yaml) |
| 3 | `container-escape-using-runtime-socket` | ✅ Production | [T1611](https://attack.mitre.org/techniques/T1611/) | [container-escape-using-runtime-socket.yaml](yamls/0.9.10/process/container-escape-using-runtime-socket.yaml) |
| 4 | `container-escape-via-cgroup` | ✅ Production | [T1611](https://attack.mitre.org/techniques/T1611/) | [container-escape-via-cgroup.yaml](yamls/0.9.10/process/container-escape-via-cgroup.yaml) |
| 5 | `credential-access-bash-history` | ✅ Production | [T1552.003](https://attack.mitre.org/techniques/T1552/003/) | [credential-access-bash-history.yaml](yamls/0.9.10/process/credential-access-bash-history.yaml) |
| 6 | `cryptominer-execution` | ✅ Production | [T1496](https://attack.mitre.org/techniques/T1496/) | [cryptominer-execution.yaml](yamls/0.9.10/process/cryptominer-execution.yaml) |
| 7 | `curl-using-socks-proxy` | ✅ Production | [T1090](https://attack.mitre.org/techniques/T1090/) | [curl-using-socks-proxy.yaml](yamls/0.9.10/process/curl-using-socks-proxy.yaml) |
| 8 | `kubernetes-service-account-token-created-in-container` | ✅ Production | [T1136](https://attack.mitre.org/techniques/T1136/) | [kubernetes-service-account-token-created-in-container.yaml](yamls/0.9.10/process/kubernetes-service-account-token-created-in-container.yaml) |
| 9 | `netcat-reverse-shell-execution` | ✅ Production | [T1059.004](https://attack.mitre.org/techniques/T1059/004/) | [netcat-reverse-shell-execution.yaml](yamls/0.9.10/process/netcat-reverse-shell-execution.yaml) |
| 10 | `network-scanning-utility` | ✅ Production | [T1046](https://attack.mitre.org/techniques/T1046/) | [network-scanning-utility.yaml](yamls/0.9.10/process/network-scanning-utility.yaml) |
| 11 | `process-hidden-using-mount-hidepid` | ✅ Production | [T1564](https://attack.mitre.org/techniques/T1564/) | [process-hidden-using-mount-hidepid.yaml](yamls/0.9.10/process/process-hidden-using-mount-hidepid.yaml) |
| 12 | `python-executed-with-suspicious-arguments` | ✅ Production | [T1059.006](https://attack.mitre.org/techniques/T1059/006/) | [python-executed-with-suspicious-arguments.yaml](yamls/0.9.10/process/python-executed-with-suspicious-arguments.yaml) |
| 13 | `schedule-cron-jobs` | ✅ Production | [T1053.003](https://attack.mitre.org/techniques/T1053/003/) | [schedule-cron-jobs.yaml](yamls/0.9.10/process/schedule-cron-jobs.yaml) |
| 14 | `stop-antimalware-process` | ✅ Production | [T1562.001](https://attack.mitre.org/techniques/T1562/001/) | [stop-antimalware-process.yaml](yamls/0.9.10/process/stop-antimalware-process.yaml) |

</details>

<details>
<summary><b>Release 0.9.11</b> — 11 production</summary>

| # | Rule | Stage | ATT&CK | Manifest |
|--:|------|:-----:|---|----------|
| 15 | `create-symlink-or-hardlink-over-sensitive-files` | ✅ Production | [T1003.008](https://attack.mitre.org/techniques/T1003/008/) | [create-symlink-or-hardlink-over-sensitive-files.yaml](yamls/0.9.11/process/create-symlink-or-hardlink-over-sensitive-files.yaml) |
| 16 | `debugfs-launched-in-privileged-container` | ✅ Production | [T1611](https://attack.mitre.org/techniques/T1611/) | [debugfs-launched-in-privileged-container.yaml](yamls/0.9.11/process/debugfs-launched-in-privileged-container.yaml) |
| 17 | `dind-escape-attempt-using-sock` | ✅ Production | [T1611](https://attack.mitre.org/techniques/T1611/) | [dind-escape-attempt-using-sock.yaml](yamls/0.9.11/process/dind-escape-attempt-using-sock.yaml) |
| 18 | `dump-memory-for-credentials` | ✅ Production | [T1003](https://attack.mitre.org/techniques/T1003/) | [dump-memory-for-credentials.yaml](yamls/0.9.11/process/dump-memory-for-credentials.yaml) |
| 19 | `find-aws-credentials` | ✅ Production | [T1552.001](https://attack.mitre.org/techniques/T1552/001/) | [find-aws-credentials.yaml](yamls/0.9.11/process/find-aws-credentials.yaml) |
| 20 | `k8s-printenv-execution` | ✅ Production | [T1552](https://attack.mitre.org/techniques/T1552/) | [k8s-printenv-execution.yaml](yamls/0.9.11/process/k8s-printenv-execution.yaml) |
| 21 | `polkit-local-privilege-escalation` | ✅ Production | [T1068](https://attack.mitre.org/techniques/T1068/) | [polkit-local-privilege-escalation.yaml](yamls/0.9.11/process/polkit-local-privilege-escalation.yaml) |
| 22 | `recon-suid-binaries-search` | ✅ Production | [T1083](https://attack.mitre.org/techniques/T1083/) | [recon-suid-binaries-search.yaml](yamls/0.9.11/process/recon-suid-binaries-search.yaml) |
| 23 | `search-private-keys-and-passwords` | ✅ Production | [T1552.004](https://attack.mitre.org/techniques/T1552/004/) | [search-private-keys-and-passwords.yaml](yamls/0.9.11/process/search-private-keys-and-passwords.yaml) |
| 24 | `sudo-potential-privilege-escalation` | ✅ Production | [T1068](https://attack.mitre.org/techniques/T1068/) | [sudo-potential-privilege-escalation.yaml](yamls/0.9.11/process/sudo-potential-privilege-escalation.yaml) |
| 25 | `usage-of-steganography-tools` | ✅ Production | [T1027.003](https://attack.mitre.org/techniques/T1027/003/) | [usage-of-steganography-tools.yaml](yamls/0.9.11/process/usage-of-steganography-tools.yaml) |

</details>

<details>
<summary><b>Release 0.9.12</b> — 11 production, 8 experimental</summary>

| # | Rule | Stage | ATT&CK | Manifest |
|--:|------|:-----:|---|----------|
| 26 | `container-escape-using-runc` | ✅ Production | [T1611](https://attack.mitre.org/techniques/T1611/) | [container-escape-using-runc.yaml](yamls/0.9.12/process/container-escape-using-runc.yaml) |
| 27 | `exploit-vsftpd-vulnerability` | ✅ Production | [T1190](https://attack.mitre.org/techniques/T1190/) | [exploit-vsftpd-vulnerability.yaml](yamls/0.9.12/process/exploit-vsftpd-vulnerability.yaml) |
| 28 | `gdb-executed-in-container` | ✅ Production | [T1055.008](https://attack.mitre.org/techniques/T1055/008/) | [gdb-executed-in-container.yaml](yamls/0.9.12/process/gdb-executed-in-container.yaml) |
| 29 | `known-cryptominer-process-executed` | ✅ Production | [T1496](https://attack.mitre.org/techniques/T1496/) | [known-cryptominer-process-executed.yaml](yamls/0.9.12/process/known-cryptominer-process-executed.yaml) |
| 30 | `launch-remote-file-copy-tools-in-container` | ✅ Production | [T1105](https://attack.mitre.org/techniques/T1105/) | [launch-remote-file-copy-tools-in-container.yaml](yamls/0.9.12/process/launch-remote-file-copy-tools-in-container.yaml) |
| 31 | `local-account-password-binary-execution` | ✅ Production | [T1098](https://attack.mitre.org/techniques/T1098/) | [local-account-password-binary-execution.yaml](yamls/0.9.12/process/local-account-password-binary-execution.yaml) |
| 32 | `log-file-symlink-to-null` | ✅ Production | [T1070.002](https://attack.mitre.org/techniques/T1070/002/) | [log-file-symlink-to-null.yaml](yamls/0.9.12/process/log-file-symlink-to-null.yaml) |
| 33 | `redis-server-launches-suspicious-tooling-possible-cve-2025-49844-exploitation` | ✅ Production | [T1190](https://attack.mitre.org/techniques/T1190/) | [redis-server-launches-suspicious-tooling-possible-cve-2025-49844-exploitation.yaml](yamls/0.9.12/process/redis-server-launches-suspicious-tooling-possible-cve-2025-49844-exploitation.yaml) |
| 34 | `remove-bulk-data-from-disk` | ✅ Production | [T1485](https://attack.mitre.org/techniques/T1485/) | [remove-bulk-data-from-disk.yaml](yamls/0.9.12/process/remove-bulk-data-from-disk.yaml) |
| 35 | `reverse-shell-from-web-server` | ✅ Production | [T1059.004](https://attack.mitre.org/techniques/T1059/004/) | [reverse-shell-from-web-server.yaml](yamls/0.9.12/process/reverse-shell-from-web-server.yaml) |
| 36 | `sensitive-files-compression-inside-a-container` | ✅ Production | [T1560.001](https://attack.mitre.org/techniques/T1560/001/) | [sensitive-files-compression-inside-a-container.yaml](yamls/0.9.12/process/sensitive-files-compression-inside-a-container.yaml) |
| 55 | `cloud-credentials-accessed-by-network-utility` | 🧪 Experimental | [T1552.005](https://attack.mitre.org/techniques/T1552/005/) | [cloud-credentials-accessed-by-network-utility.yaml](yamls/0.9.12/process/experimental/cloud-credentials-accessed-by-network-utility.yaml) |
| 56 | `compiler-executed-in-container` | 🧪 Experimental | [T1027.004](https://attack.mitre.org/techniques/T1027/004/) | [compiler-executed-in-container.yaml](yamls/0.9.12/process/experimental/compiler-executed-in-container.yaml) |
| 57 | `db-program-spawned-process` | 🧪 Experimental | [T1059.004](https://attack.mitre.org/techniques/T1059/004/) | [db-program-spawned-process.yaml](yamls/0.9.12/process/experimental/db-program-spawned-process.yaml) |
| 58 | `dump-memory-utilities` | 🧪 Experimental | [T1003](https://attack.mitre.org/techniques/T1003/) | [dump-memory-utilities.yaml](yamls/0.9.12/process/experimental/dump-memory-utilities.yaml) |
| 59 | `file-made-executable-via-chmod-inside-a-container` | 🧪 Experimental | [T1222.002](https://attack.mitre.org/techniques/T1222/002/) | [file-made-executable-via-chmod-inside-a-container.yaml](yamls/0.9.12/process/experimental/file-made-executable-via-chmod-inside-a-container.yaml) |
| 60 | `insmod-executed-in-container` | 🧪 Experimental | [T1547.006](https://attack.mitre.org/techniques/T1547/006/) | [insmod-executed-in-container.yaml](yamls/0.9.12/process/experimental/insmod-executed-in-container.yaml) |
| 61 | `suspicious-network-utility-executed` | 🧪 Experimental | [T1040](https://attack.mitre.org/techniques/T1040/) | [suspicious-network-utility-executed.yaml](yamls/0.9.12/process/experimental/suspicious-network-utility-executed.yaml) |
| 62 | `user-mgmt-binaries` | 🧪 Experimental | [T1136.001](https://attack.mitre.org/techniques/T1136/001/) | [user-mgmt-binaries.yaml](yamls/0.9.12/process/experimental/user-mgmt-binaries.yaml) |

</details>

<details>
<summary><b>Release 0.9.13</b> — 17 production, 26 experimental</summary>

| # | Rule | Stage | ATT&CK | Manifest |
|--:|------|:-----:|---|----------|
| 37 | `apache-airflow-edge-provider-rce-cve-2025-67895` | ✅ Production | [T1190](https://attack.mitre.org/techniques/T1190/) | [apache-airflow-edge-provider-rce-cve-2025-67895.yaml](yamls/0.9.13/process/apache-airflow-edge-provider-rce-cve-2025-67895.yaml) |
| 38 | `apache-kafka-oauth-jndi-rce-cve-2025-27817` | ✅ Production | [T1190](https://attack.mitre.org/techniques/T1190/) | [apache-kafka-oauth-jndi-rce-cve-2025-27817.yaml](yamls/0.9.13/process/apache-kafka-oauth-jndi-rce-cve-2025-27817.yaml) |
| 39 | `apache-zookeeper-spawns-suspicious-process` | ✅ Production | [T1190](https://attack.mitre.org/techniques/T1190/) | [apache-zookeeper-spawns-suspicious-process.yaml](yamls/0.9.13/process/apache-zookeeper-spawns-suspicious-process.yaml) |
| 40 | `coredns-remote-dos-cve-2026-26018` | ✅ Production | [T1499.004](https://attack.mitre.org/techniques/T1499/004/) | [coredns-remote-dos-cve-2026-26018.yaml](yamls/0.9.13/process/coredns-remote-dos-cve-2026-26018.yaml) |
| 41 | `docker-container-escape-via-engine-api-cve-2025-9074` | ✅ Production | [T1611](https://attack.mitre.org/techniques/T1611/) | [docker-container-escape-via-engine-api-cve-2025-9074.yaml](yamls/0.9.13/process/docker-container-escape-via-engine-api-cve-2025-9074.yaml) |
| 42 | `docker-model-runner-flag-injection-cve-2026-28400` | ✅ Production | [T1610](https://attack.mitre.org/techniques/T1610/) | [docker-model-runner-flag-injection-cve-2026-28400.yaml](yamls/0.9.13/process/docker-model-runner-flag-injection-cve-2026-28400.yaml) |
| 43 | `docker-unauthenticated-engine-api-access-cve-2025-9074` | ✅ Production | [T1613](https://attack.mitre.org/techniques/T1613/) | [docker-unauthenticated-engine-api-access-cve-2025-9074.yaml](yamls/0.9.13/process/docker-unauthenticated-engine-api-access-cve-2025-9074.yaml) |
| 44 | `golang-ssh-agent-malformed-identity-dos-cve-2025-47914` | ✅ Production | [T1499.004](https://attack.mitre.org/techniques/T1499/004/) | [golang-ssh-agent-malformed-identity-dos-cve-2025-47914.yaml](yamls/0.9.13/process/golang-ssh-agent-malformed-identity-dos-cve-2025-47914.yaml) |
| 45 | `haproxy-spawns-suspicious-process` | ✅ Production | [T1190](https://attack.mitre.org/techniques/T1190/) | [haproxy-spawns-suspicious-process.yaml](yamls/0.9.13/process/haproxy-spawns-suspicious-process.yaml) |
| 46 | `harbor-registry-spawns-suspicious-process` | ✅ Production | [T1190](https://attack.mitre.org/techniques/T1190/) | [harbor-registry-spawns-suspicious-process.yaml](yamls/0.9.13/process/harbor-registry-spawns-suspicious-process.yaml) |
| 47 | `jenkins-git-parameter-command-injection-cve-2025-53652` | ✅ Production | [T1190](https://attack.mitre.org/techniques/T1190/) | [jenkins-git-parameter-command-injection-cve-2025-53652.yaml](yamls/0.9.13/process/jenkins-git-parameter-command-injection-cve-2025-53652.yaml) |
| 48 | `kubernetes-ingressnightmare-rce-cve-2025-1974` | ✅ Production | [T1190](https://attack.mitre.org/techniques/T1190/) | [kubernetes-ingressnightmare-rce-cve-2025-1974.yaml](yamls/0.9.13/process/kubernetes-ingressnightmare-rce-cve-2025-1974.yaml) |
| 49 | `mariadb-json-schema-crash-rce-cve-2026-32710` | ✅ Production | [T1190](https://attack.mitre.org/techniques/T1190/) | [mariadb-json-schema-crash-rce-cve-2026-32710.yaml](yamls/0.9.13/process/mariadb-json-schema-crash-rce-cve-2026-32710.yaml) |
| 50 | `mcp-server-command-injection-cve-2025-6514` | ✅ Production | [T1190](https://attack.mitre.org/techniques/T1190/) | [mcp-server-command-injection-cve-2025-6514.yaml](yamls/0.9.13/process/mcp-server-command-injection-cve-2025-6514.yaml) |
| 51 | `nginx-ui-spawns-shell-post-exploitation-cve-2026-27944` | ✅ Production | [T1190](https://attack.mitre.org/techniques/T1190/) | [nginx-ui-spawns-shell-post-exploitation-cve-2026-27944.yaml](yamls/0.9.13/process/nginx-ui-spawns-shell-post-exploitation-cve-2026-27944.yaml) |
| 52 | `nvidia-container-toolkit-suspicious-host-mount-cve-2025-23266` | ✅ Production | [T1190](https://attack.mitre.org/techniques/T1190/) | [nvidia-container-toolkit-suspicious-host-mount-cve-2025-23266.yaml](yamls/0.9.13/process/nvidia-container-toolkit-suspicious-host-mount-cve-2025-23266.yaml) |
| 53 | `runc-masked-path-symlink-container-escape-cve-2025-31133` | ✅ Production | [T1611](https://attack.mitre.org/techniques/T1611/) | [runc-masked-path-symlink-container-escape-cve-2025-31133.yaml](yamls/0.9.13/process/runc-masked-path-symlink-container-escape-cve-2025-31133.yaml) |
| 63 | `apache-solr-rce-configset-cve-2025-24814` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [apache-solr-rce-configset-cve-2025-24814.yaml](yamls/0.9.13/process/experimental/apache-solr-rce-configset-cve-2025-24814.yaml) |
| 64 | `apache-tomcat-deserialization-rce-cve-2025-24813` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [apache-tomcat-deserialization-rce-cve-2025-24813.yaml](yamls/0.9.13/process/experimental/apache-tomcat-deserialization-rce-cve-2025-24813.yaml) |
| 65 | `elasticsearch-spawns-suspicious-process` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [elasticsearch-spawns-suspicious-process.yaml](yamls/0.9.13/process/experimental/elasticsearch-spawns-suspicious-process.yaml) |
| 66 | `envoy-istio-request-smuggling-cve-2025-66220` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [envoy-istio-request-smuggling-cve-2025-66220.yaml](yamls/0.9.13/process/experimental/envoy-istio-request-smuggling-cve-2025-66220.yaml) |
| 67 | `ghost-cms-spawns-suspicious-process` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [ghost-cms-spawns-suspicious-process.yaml](yamls/0.9.13/process/experimental/ghost-cms-spawns-suspicious-process.yaml) |
| 68 | `golang-ssh-gssapi-memory-exhaustion-cve-2025-58181` | 🧪 Experimental | [T1499.004](https://attack.mitre.org/techniques/T1499/004/) | [golang-ssh-gssapi-memory-exhaustion-cve-2025-58181.yaml](yamls/0.9.13/process/experimental/golang-ssh-gssapi-memory-exhaustion-cve-2025-58181.yaml) |
| 69 | `java-se-jsse-access-control-bypass-cve-2025-21587` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [java-se-jsse-access-control-bypass-cve-2025-21587.yaml](yamls/0.9.13/process/experimental/java-se-jsse-access-control-bypass-cve-2025-21587.yaml) |
| 70 | `jetty-path-traversal-rce` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [jetty-path-traversal-rce.yaml](yamls/0.9.13/process/experimental/jetty-path-traversal-rce.yaml) |
| 71 | `keycloak-spawns-suspicious-process` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [keycloak-spawns-suspicious-process.yaml](yamls/0.9.13/process/experimental/keycloak-spawns-suspicious-process.yaml) |
| 72 | `kibana-expr-eval-rce-cve-2025-12735` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [kibana-expr-eval-rce-cve-2025-12735.yaml](yamls/0.9.13/process/experimental/kibana-expr-eval-rce-cve-2025-12735.yaml) |
| 73 | `kibana-fleet-resource-exhaustion-cve-2026-0528` | 🧪 Experimental | [T1499.004](https://attack.mitre.org/techniques/T1499/004/) | [kibana-fleet-resource-exhaustion-cve-2026-0528.yaml](yamls/0.9.13/process/experimental/kibana-fleet-resource-exhaustion-cve-2026-0528.yaml) |
| 74 | `kubernetes-api-server-token-theft` | 🧪 Experimental | [T1552.007](https://attack.mitre.org/techniques/T1552/007/) | [kubernetes-api-server-token-theft.yaml](yamls/0.9.13/process/experimental/kubernetes-api-server-token-theft.yaml) |
| 75 | `mcp-server-tool-poisoning-data-exfiltration` | 🧪 Experimental | [T1041](https://attack.mitre.org/techniques/T1041/) | [mcp-server-tool-poisoning-data-exfiltration.yaml](yamls/0.9.13/process/experimental/mcp-server-tool-poisoning-data-exfiltration.yaml) |
| 76 | `memcached-unauthorized-access` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [memcached-unauthorized-access.yaml](yamls/0.9.13/process/experimental/memcached-unauthorized-access.yaml) |
| 77 | `minio-spawns-suspicious-process` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [minio-spawns-suspicious-process.yaml](yamls/0.9.13/process/experimental/minio-spawns-suspicious-process.yaml) |
| 78 | `nexus-repository-spawns-suspicious-process` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [nexus-repository-spawns-suspicious-process.yaml](yamls/0.9.13/process/experimental/nexus-repository-spawns-suspicious-process.yaml) |
| 79 | `odoo-erp-spawns-suspicious-process` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [odoo-erp-spawns-suspicious-process.yaml](yamls/0.9.13/process/experimental/odoo-erp-spawns-suspicious-process.yaml) |
| 80 | `postgresql-sql-injection-rce-cve-2025-1094` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [postgresql-sql-injection-rce-cve-2025-1094.yaml](yamls/0.9.13/process/experimental/postgresql-sql-injection-rce-cve-2025-1094.yaml) |
| 81 | `rabbitmq-erlang-otp-ssh-rce-cve-2025-32433` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [rabbitmq-erlang-otp-ssh-rce-cve-2025-32433.yaml](yamls/0.9.13/process/experimental/rabbitmq-erlang-otp-ssh-rce-cve-2025-32433.yaml) |
| 82 | `sentry-spawns-suspicious-process` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [sentry-spawns-suspicious-process.yaml](yamls/0.9.13/process/experimental/sentry-spawns-suspicious-process.yaml) |
| 83 | `sonarqube-scanner-code-execution-cve-2025-58178` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [sonarqube-scanner-code-execution-cve-2025-58178.yaml](yamls/0.9.13/process/experimental/sonarqube-scanner-code-execution-cve-2025-58178.yaml) |
| 84 | `spring-boot-actuator-rce` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [spring-boot-actuator-rce.yaml](yamls/0.9.13/process/experimental/spring-boot-actuator-rce.yaml) |
| 85 | `traefik-spawns-suspicious-process` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [traefik-spawns-suspicious-process.yaml](yamls/0.9.13/process/experimental/traefik-spawns-suspicious-process.yaml) |
| 86 | `varnish-cache-spawns-suspicious-process` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [varnish-cache-spawns-suspicious-process.yaml](yamls/0.9.13/process/experimental/varnish-cache-spawns-suspicious-process.yaml) |
| 87 | `vault-arbitrary-code-execution-cve-2025-6000` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [vault-arbitrary-code-execution-cve-2025-6000.yaml](yamls/0.9.13/process/experimental/vault-arbitrary-code-execution-cve-2025-6000.yaml) |
| 88 | `vault-ldap-auth-bypass-cve-2025-13357` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [vault-ldap-auth-bypass-cve-2025-13357.yaml](yamls/0.9.13/process/experimental/vault-ldap-auth-bypass-cve-2025-13357.yaml) |

</details>

<details>
<summary><b>Release 0.9.14</b> — 1 production, 14 experimental</summary>

| # | Rule | Stage | ATT&CK | Manifest |
|--:|------|:-----:|---|----------|
| 54 | `php2shell-possible-exploit-attempt` | ✅ Production | [T1190](https://attack.mitre.org/techniques/T1190/) | [php2shell-possible-exploit-attempt.yaml](yamls/0.9.14/process/php2shell-possible-exploit-attempt.yaml) |
| 89 | `activemq-classinfo-rce-cve-2023-46604` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [activemq-classinfo-rce-cve-2023-46604.yaml](yamls/0.9.14/process/experimental/activemq-classinfo-rce-cve-2023-46604.yaml) |
| 90 | `apache-apisix-dashboard-rce-cve-2021-45232` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [apache-apisix-dashboard-rce-cve-2021-45232.yaml](yamls/0.9.14/process/experimental/apache-apisix-dashboard-rce-cve-2021-45232.yaml) |
| 91 | `apache-cxf-ssrf-cve-2024-28752` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [apache-cxf-ssrf-cve-2024-28752.yaml](yamls/0.9.14/process/experimental/apache-cxf-ssrf-cve-2024-28752.yaml) |
| 92 | `apache-druid-rce-cve-2021-25646` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [apache-druid-rce-cve-2021-25646.yaml](yamls/0.9.14/process/experimental/apache-druid-rce-cve-2021-25646.yaml) |
| 93 | `apache-struts-rce-cve-2023-50164` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [apache-struts-rce-cve-2023-50164.yaml](yamls/0.9.14/process/experimental/apache-struts-rce-cve-2023-50164.yaml) |
| 94 | `container-escape-chroot-host-filesystem` | 🧪 Experimental | [T1611](https://attack.mitre.org/techniques/T1611/) | [container-escape-chroot-host-filesystem.yaml](yamls/0.9.14/process/experimental/container-escape-chroot-host-filesystem.yaml) |
| 95 | `container-escape-nsenter-host-namespace` | 🧪 Experimental | [T1611](https://attack.mitre.org/techniques/T1611/) | [container-escape-nsenter-host-namespace.yaml](yamls/0.9.14/process/experimental/container-escape-nsenter-host-namespace.yaml) |
| 96 | `container-escape-unshare-namespace-creation` | 🧪 Experimental | [T1611](https://attack.mitre.org/techniques/T1611/) | [container-escape-unshare-namespace-creation.yaml](yamls/0.9.14/process/experimental/container-escape-unshare-namespace-creation.yaml) |
| 97 | `container-runtime-socket-command-execution` | 🧪 Experimental | [T1611](https://attack.mitre.org/techniques/T1611/) | [container-runtime-socket-command-execution.yaml](yamls/0.9.14/process/experimental/container-runtime-socket-command-execution.yaml) |
| 98 | `kubectl-exec-lateral-movement` | 🧪 Experimental | [T1609](https://attack.mitre.org/techniques/T1609/) | [kubectl-exec-lateral-movement.yaml](yamls/0.9.14/process/experimental/kubectl-exec-lateral-movement.yaml) |
| 99 | `kubectl-token-minting-serviceaccount-abuse` | 🧪 Experimental | [T1528](https://attack.mitre.org/techniques/T1528/) | [kubectl-token-minting-serviceaccount-abuse.yaml](yamls/0.9.14/process/experimental/kubectl-token-minting-serviceaccount-abuse.yaml) |
| 100 | `langflow-rce-cve-2026-33017` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [langflow-rce-cve-2026-33017.yaml](yamls/0.9.14/process/experimental/langflow-rce-cve-2026-33017.yaml) |
| 101 | `n8n-rce-cve-2025-68613` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [n8n-rce-cve-2025-68613.yaml](yamls/0.9.14/process/experimental/n8n-rce-cve-2025-68613.yaml) |
| 102 | `pgadmin-rce-cve-2025-2945` | 🧪 Experimental | [T1190](https://attack.mitre.org/techniques/T1190/) | [pgadmin-rce-cve-2025-2945.yaml](yamls/0.9.14/process/experimental/pgadmin-rce-cve-2025-2945.yaml) |

</details>


---

## ❔ Not-fired rules

The `yamls/not-fired/` folder holds **26 rules** that did not raise an alert during internal testing. They're kept separately so that the main list contains only rules that are expected to alert. To run them:

```bash
python3 run_rules.py --not-fired
```

These use their own numbering, shown below.

<details>
<summary><b>Release 0.9.12</b> — 7 production, 4 experimental</summary>

| # | Rule | Stage | Manifest |
|--:|------|:-----:|----------|
| 1 | `defense-evasion-via-rootkit` | ✅ Production | [defense-evasion-via-rootkit.yaml](yamls/not-fired/0.9.12/process/defense-evasion-via-rootkit.yaml) |
| 2 | `diamorphine-process-hiding` | ✅ Production | [diamorphine-process-hiding.yaml](yamls/not-fired/0.9.12/process/diamorphine-process-hiding.yaml) |
| 3 | `dns-lookup-for-often-security-tool-domain-detected` | ✅ Production | [dns-lookup-for-often-security-tool-domain-detected.yaml](yamls/not-fired/0.9.12/process/dns-lookup-for-often-security-tool-domain-detected.yaml) |
| 4 | `process-capability-enumeration` | ✅ Production | [process-capability-enumeration.yaml](yamls/not-fired/0.9.12/process/process-capability-enumeration.yaml) |
| 5 | `redis-xackdel-with-large-ids-count-possible-cve-2025-62507-attempt` | ✅ Production | [redis-xackdel-with-large-ids-count-possible-cve-2025-62507-attempt.yaml](yamls/not-fired/0.9.12/process/redis-xackdel-with-large-ids-count-possible-cve-2025-62507-attempt.yaml) |
| 6 | `root-shell-via-sudo-cve-2025-32463` | ✅ Production | [root-shell-via-sudo-cve-2025-32463.yaml](yamls/not-fired/0.9.12/process/root-shell-via-sudo-cve-2025-32463.yaml) |
| 7 | `sudo-chroot-privilege-escalation-cve-2025-32463` | ✅ Production | [sudo-chroot-privilege-escalation-cve-2025-32463.yaml](yamls/not-fired/0.9.12/process/sudo-chroot-privilege-escalation-cve-2025-32463.yaml) |
| 13 | `decoding-payload-in-container` | 🧪 Experimental | [decoding-payload-in-container.yaml](yamls/not-fired/0.9.12/process/experimental/decoding-payload-in-container.yaml) |
| 14 | `network-traffic-capture-via-cap-net-raw` | 🧪 Experimental | [network-traffic-capture-via-cap-net-raw.yaml](yamls/not-fired/0.9.12/process/experimental/network-traffic-capture-via-cap-net-raw.yaml) |
| 15 | `potential-privilege-escalation-via-linux-dac-permissions` | 🧪 Experimental | [potential-privilege-escalation-via-linux-dac-permissions.yaml](yamls/not-fired/0.9.12/process/experimental/potential-privilege-escalation-via-linux-dac-permissions.yaml) |
| 16 | `redis-cli-eval-script-usage-possible-cve-2025-49844-attempt` | 🧪 Experimental | [redis-cli-eval-script-usage-possible-cve-2025-49844-attempt.yaml](yamls/not-fired/0.9.12/process/experimental/redis-cli-eval-script-usage-possible-cve-2025-49844-attempt.yaml) |

</details>

<details>
<summary><b>Release 0.9.13</b> — 5 production, 7 experimental</summary>

| # | Rule | Stage | Manifest |
|--:|------|:-----:|----------|
| 8 | `gitlab-runner-spawns-suspicious-process` | ✅ Production | [gitlab-runner-spawns-suspicious-process.yaml](yamls/not-fired/0.9.13/process/gitlab-runner-spawns-suspicious-process.yaml) |
| 9 | `glibc-dns-memory-leak-cve-2026-0915` | ✅ Production | [glibc-dns-memory-leak-cve-2026-0915.yaml](yamls/not-fired/0.9.13/process/glibc-dns-memory-leak-cve-2026-0915.yaml) |
| 10 | `mongodb-unauthorized-data-exfiltration-cve-2025-14847` | ✅ Production | [mongodb-unauthorized-data-exfiltration-cve-2025-14847.yaml](yamls/not-fired/0.9.13/process/mongodb-unauthorized-data-exfiltration-cve-2025-14847.yaml) |
| 11 | `postgresql-copy-to-program-execution-cve-2025-1094` | ✅ Production | [postgresql-copy-to-program-execution-cve-2025-1094.yaml](yamls/not-fired/0.9.13/process/postgresql-copy-to-program-execution-cve-2025-1094.yaml) |
| 12 | `redis-output-buffer-dos-cve-2025-21605` | ✅ Production | [redis-output-buffer-dos-cve-2025-21605.yaml](yamls/not-fired/0.9.13/process/redis-output-buffer-dos-cve-2025-21605.yaml) |
| 17 | `argocd-api-unauthorized-access-cve-2025-55190` | 🧪 Experimental | [argocd-api-unauthorized-access-cve-2025-55190.yaml](yamls/not-fired/0.9.13/process/experimental/argocd-api-unauthorized-access-cve-2025-55190.yaml) |
| 18 | `coredns-acl-bypass-toctou-cve-2026-26017` | 🧪 Experimental | [coredns-acl-bypass-toctou-cve-2026-26017.yaml](yamls/not-fired/0.9.13/process/experimental/coredns-acl-bypass-toctou-cve-2026-26017.yaml) |
| 19 | `couchdb-spawns-suspicious-process` | 🧪 Experimental | [couchdb-spawns-suspicious-process.yaml](yamls/not-fired/0.9.13/process/experimental/couchdb-spawns-suspicious-process.yaml) |
| 20 | `gitea-spawns-suspicious-process` | 🧪 Experimental | [gitea-spawns-suspicious-process.yaml](yamls/not-fired/0.9.13/process/experimental/gitea-spawns-suspicious-process.yaml) |
| 21 | `gitlab-saml-auth-bypass-cve-2025-25291` | 🧪 Experimental | [gitlab-saml-auth-bypass-cve-2025-25291.yaml](yamls/not-fired/0.9.13/process/experimental/gitlab-saml-auth-bypass-cve-2025-25291.yaml) |
| 22 | `grafana-enterprise-privilege-escalation-cve-2025-41115` | 🧪 Experimental | [grafana-enterprise-privilege-escalation-cve-2025-41115.yaml](yamls/not-fired/0.9.13/process/experimental/grafana-enterprise-privilege-escalation-cve-2025-41115.yaml) |
| 23 | `tekton-pipeline-resolver-dos-cve-2026-33022` | 🧪 Experimental | [tekton-pipeline-resolver-dos-cve-2026-33022.yaml](yamls/not-fired/0.9.13/process/experimental/tekton-pipeline-resolver-dos-cve-2026-33022.yaml) |

</details>

<details>
<summary><b>Release 0.9.14</b> — 3 experimental</summary>

| # | Rule | Stage | Manifest |
|--:|------|:-----:|----------|
| 24 | `container-escape-cgroup-release-agent` | 🧪 Experimental | [container-escape-cgroup-release-agent.yaml](yamls/not-fired/0.9.14/process/experimental/container-escape-cgroup-release-agent.yaml) |
| 25 | `container-escape-sensitive-host-path-access` | 🧪 Experimental | [container-escape-sensitive-host-path-access.yaml](yamls/not-fired/0.9.14/process/experimental/container-escape-sensitive-host-path-access.yaml) |
| 26 | `react-xss-cve-2025-55182` | 🧪 Experimental | [react-xss-cve-2025-55182.yaml](yamls/not-fired/0.9.14/process/experimental/react-xss-cve-2025-55182.yaml) |

</details>


---

## 🧩 Running a single test without the tool

Every rule file is also a standalone pod manifest that runs its attack command when created:

```bash
kubectl apply -f yamls/0.9.12/process/gdb-executed-in-container.yaml
# ...check your detection console...
kubectl delete -f yamls/0.9.12/process/gdb-executed-in-container.yaml
```

---

## 📁 Repository layout

```text
.
├── 📄 README.md
├── 🐍 run_rules.py            ← the interactive test runner
├── 📝 command_notebook.txt    ← every rule and the command it runs
└── 📂 yamls/
    ├── 0.9.10/process/            14 rules
    ├── 0.9.11/process/            11 rules
    ├── 0.9.12/process/            11 rules + experimental/ (8)
    ├── 0.9.13/process/            17 rules + experimental/ (26)
    ├── 0.9.14/process/             1 rule  + experimental/ (14)
    └── not-fired/                 26 rules that did not alert in testing
```

---

## 🔧 Troubleshooting

<details>
<summary><b><code>ModuleNotFoundError: No module named 'yaml'</code></b></summary>

Install PyYAML:

```bash
pip install pyyaml
```
</details>

<details>
<summary><b><code>ERROR: kubectl not found on PATH.</code></b></summary>

Install `kubectl` and make sure `kubectl get nodes` works from the same terminal.
</details>

<details>
<summary><b><code>Pod did not become ready</code></b></summary>

The test pod didn't start within 2 minutes. This is usually because the cluster can't pull the image. Check what happened:

```bash
kubectl describe pod crs-rule-executor
```

If your cluster can't reach Docker Hub, copy the image to your own registry and point the tool at it:

```bash
python3 run_rules.py --pod-image <your-registry>/base-ubuntu:latest
```
</details>

<details>
<summary><b>No alert appeared for a test</b></summary>

- Confirm your runtime security sensor is running on the node where `crs-rule-executor` was scheduled (`kubectl get pod crs-rule-executor -o wide`).
- Alerts can take a little while to reach the console. Try a longer `--delay`, or wait and refresh.
- Check whether the rule is a 🧪 experimental rule, and whether it's enabled in your policy.
</details>

<details>
<summary><b>Syntax error when starting the tool</b></summary>

The tool needs Python 3.10 or newer. Check with `python3 --version`.
</details>

---

## 🧹 Cleanup

If you exited with `q`, or the run was interrupted, the test pod is still running. Remove it with:

```bash
kubectl delete pod crs-rule-executor -n <namespace>
```

If you used the [single-test method](#-running-a-single-test-without-the-tool), delete each pod with `kubectl delete -f <file>`.
