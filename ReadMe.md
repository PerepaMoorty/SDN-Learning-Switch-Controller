# SDN Learning Switch Controller (POX + Mininet)

## 📌 Project Overview

This project implements a **Software Defined Networking (SDN) Learning Switch Controller** using the **POX controller framework** and **Mininet network emulator**.

The controller mimics a traditional Layer 2 switch by:
- Dynamically learning MAC addresses
- Installing forwarding rules
- Reducing unnecessary flooding
- Enabling efficient packet delivery

---

## 🎯 Objectives

- Implement MAC address learning logic  
- Perform dynamic flow rule installation  
- Validate packet forwarding behavior  
- Inspect flow tables in Open vSwitch  

---

## 🧠 Key Concepts

- **SDN (Software Defined Networking):** Separation of control and data plane  
- **Controller:** Central logic managing network behavior  
- **OpenFlow:** Protocol between controller and switches  
- **Learning Switch:** Learns MAC → Port mappings dynamically  

---

## 🏗️ Project Structure

```text
pox/
├── pox/
│   └── ext/
│       ├── learning_switch.py
│       └── __init__.py
│
├── simple_topo.py
└── README.md
```

---

## ⚙️ Prerequisites

Install required dependencies:

```bash
sudo apt update
sudo apt install git python3.9 python3.9-venv python3.9-distutils openvswitch-switch net-tools
```

---

## 📥 Install Mininet

```bash
git clone https://github.com/mininet/mininet
cd mininet
sudo ./util/install.sh -a
```

Verify installation:

```bash
sudo mn --test pingall
```

---

## 📥 Install POX

```bash
cd ~
git clone https://github.com/noxrepo/pox
```

---

## 📂 Setup Project Files

### 1. Create controller file

```bash
cd ~/pox/pox
mkdir -p ext
cd ext
nano learning_switch.py
```

Paste your controller code.

---

### 2. Create init file

```bash
touch ~/pox/pox/ext/__init__.py
```

---

### 3. Create Mininet topology

```bash
cd ~/pox
nano simple_topo.py
```

Paste:

```python
from mininet.topo import Topo

class SimpleTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)

topos = {'simpletopo': (lambda: SimpleTopo())}
```

---

## 🚀 Running the Project

### 🔴 Step 1: Clean previous runs

```bash
sudo mn -c
pkill -f pox
```

---

### 🧠 Step 2: Start POX Controller (Terminal 1)

```bash
cd ~/pox
python3.9 pox.py log.level --DEBUG openflow.of_01 ext.learning_switch
```

Expected output:
```
INFO:openflow.of_01:Listening on 0.0.0.0:6633
```

---

### 🌐 Step 3: Start Mininet (Terminal 2)

```bash
cd ~/pox
sudo mn --custom simple_topo.py --topo simpletopo \
--controller=remote,ip=127.0.0.1,port=6633 \
--switch ovs,protocols=OpenFlow10
```

---

## 🧪 Testing

### 1. Connectivity Test

```bash
mininet> pingall
```

Expected:
```
0% dropped
```

---

### 2. MAC Learning

```bash
mininet> h1 ping h2
```

Check POX logs:
```
Learned MAC ...
```

---

### 3. Flow Installation

Run ping again:

```bash
mininet> h1 ping h2
```

Logs:
```
Flow installed ...
```

---

### 4. Flow Table Inspection

```bash
mininet> sh ovs-ofctl dump-flows s1
```

---

## 🔍 Working Mechanism

1. Switch sends Packet-In to controller  
2. Controller learns source MAC  
3. If destination known → install flow rule  
4. If unknown → flood packet  
5. Future packets use installed flows  

---

## ⚠️ Important Notes

- POX supports **OpenFlow 1.0 only**  
- Always use:
  ```
  --switch ovs,protocols=OpenFlow10
  ```
- Use **Python 3.9**, not newer versions  

---

## 🧹 Cleanup

```bash
sudo mn -c
pkill -f pox
```