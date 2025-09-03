#!/bin/bash
# GNS3 PyTgen Setup Script
# Run this on each Linux node in your GNS3 topology

echo "=== PyTgen GNS3 Setup ==="

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "Please run as regular user (not root)"
    exit 1
fi

# Install dependencies
echo "Installing Python dependencies..."
sudo apt update -qq
sudo apt install -y python3-pip python3-dev python3-setuptools
pip3 install --user paramiko pycryptodome pythonping

# Create directories
mkdir -p ~/pytgen_logs
mkdir -p ~/pytgen_data

# Set up network discovery
echo "Discovering network interfaces..."
ip addr show | grep -E "inet.*scope global" | awk '{print $2}' > ~/pytgen_networks.txt

# Get default gateway
ip route | grep default | awk '{print $3}' > ~/pytgen_gateway.txt

echo "Network configuration saved to ~/pytgen_networks.txt and ~/pytgen_gateway.txt"

# Create node-specific config based on IP
NODE_IP=$(hostname -I | awk '{print $1}')
NODE_NAME=$(hostname)

echo "Node IP: $NODE_IP"
echo "Node Name: $NODE_NAME"

# Create custom config file for this node
cat > ~/PyTgen-master/configs/${NODE_NAME}.py << EOF
'''
Auto-generated GNS3 configuration for node: $NODE_NAME
IP: $NODE_IP
'''

import logging

class Conf:
    maxthreads = 20
    loglevel = logging.INFO
    
    # Node-specific network targets
    local_ip = '$NODE_IP'
    gateway_ip = '$(cat ~/pytgen_gateway.txt)'
    
    jobs = [
        # Basic connectivity tests
        ('ping_gen', [(0, 0), (23, 59), (1, 0)], [gateway_ip, 3]),
        ('ping_gen', [(0, 0), (23, 59), (2, 0)], ['8.8.8.8', 2]),
        
        # Local network discovery
        ('ping_gen', [(0, 0), (23, 59), (3, 0)], ['$(echo $NODE_IP | cut -d. -f1-3).1', 2]),
        
        # File operations
        ('copy_gen', [(0, 0), (23, 59), (5, 0)], [None, '/tmp/pytgen_${NODE_NAME}.dat', 25]),
    ]
EOF

echo "Created node-specific config: ~/PyTgen-master/configs/${NODE_NAME}.py"

# Make PyTgen executable
chmod +x ~/PyTgen-master/run.py

# Create start script
cat > ~/start_pytgen.sh << 'EOF'
#!/bin/bash
cd ~/PyTgen-master
NODE_NAME=$(hostname)
echo "Starting PyTgen on node: $NODE_NAME"
python3 run.py
EOF

chmod +x ~/start_pytgen.sh

echo "=== Setup Complete ==="
echo "Run: ./start_pytgen.sh to start PyTgen"
echo "Logs will be in: ~/PyTgen-master/logs/"
