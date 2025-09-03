#!/bin/sh
# Alpine Linux PyTgen Setup Script
# Run this on Alpine 2 (source node)

echo "=== PyTgen Alpine Linux Setup ==="

# Install Python and dependencies
echo "Installing Python dependencies..."
apk update
apk add python3 py3-pip python3-dev gcc musl-dev libffi-dev openssl-dev

# Install Python packages
pip3 install --user paramiko pycryptodome pythonping

# Create directories
mkdir -p ~/pytgen_logs
mkdir -p ~/pytgen_data

# Network discovery for Alpine
echo "Discovering network configuration..."
ip addr show | grep -E "inet.*scope global" | awk '{print $2}' > ~/pytgen_networks.txt
ip route | grep default | awk '{print $3}' > ~/pytgen_gateway.txt

# Get this node's IP
NODE_IP=$(ip route get 8.8.8.8 | grep -oP 'src \K\S+' 2>/dev/null || hostname -i | awk '{print $1}')
echo "Node IP: $NODE_IP"

# Create Alpine-specific test config
cat > ~/PyTgen-master/configs/$(hostname).py << EOF
'''
Auto-generated Alpine configuration for $(hostname)
IP: $NODE_IP
'''

import logging

class Conf:
    maxthreads = 8
    loglevel = logging.INFO
    
    # Network info
    local_ip = '$NODE_IP'
    gateway_ip = '$(cat ~/pytgen_gateway.txt 2>/dev/null || echo "192.168.1.1")'
    
    # Simple connectivity tests
    jobs = [
        ('ping_gen', [(0, 0), (23, 59), (1, 0)], [gateway_ip, 3]),
        ('copy_gen', [(0, 0), (23, 59), (5, 0)], [None, '/tmp/pytgen_$(hostname).dat', 10]),
    ]
EOF

echo "Setup complete! Node config created: ~/PyTgen-master/configs/$(hostname).py"
echo "To start PyTgen: cd ~/PyTgen-master && python3 run.py"
