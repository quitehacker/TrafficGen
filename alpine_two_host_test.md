# Alpine 2 → Alpine 3 Testing Guide

## Step 1: Prepare Alpine 3 (Target)

**Console into Alpine 3:**
```sh
# Start basic services for testing
# HTTP server
python3 -m http.server 8000 &

# SSH (should be running by default)
service sshd start

# Check IP address
ip addr show

# Optional: FTP server (if needed)
apk add vsftpd
service vsftpd start
```

## Step 2: Setup Alpine 2 (Source)

**Console into Alpine 2:**
```sh
# Install dependencies
apk update
apk add python3 py3-pip python3-dev gcc musl-dev libffi-dev openssl-dev

# Install Python packages
pip3 install --user paramiko pycryptodome pythonping

# Create PyTgen directory
mkdir -p ~/PyTgen-master
# Copy PyTgen files here (use GNS3 file transfer or manual copy)
```

## Step 3: Configure Target IP

**Edit the config file to match your setup:**
```sh
# Check Alpine 3's IP
ping alpine3_ip  # Replace with actual IP

# Update ALPINE2.py config with correct IP
vi ~/PyTgen-master/configs/ALPINE2.py
# Change: alpine3_ip = '192.168.1.3'  to your actual Alpine 3 IP
```

## Step 4: Run the Test

**Start PyTgen on Alpine 2:**
```sh
cd ~/PyTgen-master
python3 run.py

# Monitor logs
tail -f logs/ALPINE2.log
```

## Expected Results

**You should see:**
- ✅ Ping tests every 30 seconds to Alpine 3
- ✅ HTTP requests to Alpine 3:8000 every 2 minutes  
- ✅ Local file generation every 5 minutes
- ⚠️ SSH attempts (may fail if no credentials set)
- ⚠️ FTP attempts (may fail if no FTP server)

## Troubleshooting

**If ping fails:**
```sh
# Check connectivity manually
ping alpine3_ip
traceroute alpine3_ip
```

**If HTTP fails:**
```sh
# Verify HTTP server on Alpine 3
curl http://alpine3_ip:8000
```

**If SSH fails:**
```sh
# Test SSH manually
ssh root@alpine3_ip
# Default Alpine password might be empty or 'alpine'
```
