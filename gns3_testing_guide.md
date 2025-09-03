# PyTgen GNS3 Testing Guide

## Topology Overview
Your GNS3 setup shows:
- Multiple Kali Linux VMs (perfect for PyTgen)
- Cisco routers and switches
- Cloud connections
- Multi-subnet architecture

## Deployment Strategy

### Phase 1: Single Node Testing
1. **Install on one Kali VM first**
   ```bash
   # Console into KaliLinux1-1
   sudo apt update && sudo apt install python3-pip
   pip3 install paramiko pycryptodome pythonping
   
   # Transfer PyTgen files
   # Use GNS3's drag-drop or shared folder
   ```

2. **Test basic connectivity**
   ```bash
   cd PyTgen-master
   python3 run.py  # Uses hostname-based config
   ```

### Phase 2: Multi-Node Coordination
Deploy PyTgen on multiple nodes for distributed testing:

**Node Roles:**
- **KaliLinux1-1**: Traffic Generator (ping, HTTP)  
- **KaliLinux1-2**: Server simulator (HTTP, FTP, SSH)
- **KaliLinux1-3**: Network monitor/analyzer
- **KaliLinux1-4**: Load generator

### Phase 3: Network Path Testing

**Test Different Paths:**
1. **Intra-subnet**: VM to VM same network
2. **Inter-subnet**: Cross router/switch boundaries  
3. **WAN simulation**: Through cloud connections
4. **Convergence testing**: Link failures and recovery

## Testing Scenarios

### Scenario 1: Basic Connectivity Matrix
```python
# Generate ping tests between all nodes
targets = ['10.0.1.10', '10.0.1.11', '10.0.1.12', '10.0.1.13']
for target in targets:
    ('ping_gen', [(0,0), (23,59), (1,0)], [target, 5])
```

### Scenario 2: Bandwidth Testing
```python
# Large file transfers between nodes
('ftp_gen', [(0,0), (23,59), (5,0)], 
    ['10.0.1.11', 'testuser', 'pass', 
     ['/tmp/large_file.dat'], ['/tmp/received.dat'], 3, False, 30])
```

### Scenario 3: Protocol Mix
```python
# Simulate realistic network traffic
jobs = [
    ('ping_gen', [(0,0), (23,59), (0,30)], ['gateway_ip', 3]),      # Heartbeat
    ('http_gen', [(0,0), (23,59), (2,0)], [['http://server_ip'], 5, 15]), # Web
    ('ssh_gen', [(0,0), (23,59), (10,0)], ['target_ip', 22, 'user', 'pass', 1, ['ls', 'ps aux'], 30]), # Management
    ('ftp_gen', [(0,0), (23,59), (30,0)], ['target_ip', 'user', 'pass', [], [], 2, False, 20]) # Bulk transfer
]
```

## Monitoring and Analysis

### Real-time Monitoring
```bash
# Monitor logs across all nodes
tail -f ~/PyTgen-master/logs/*.log

# Network utilization 
iftop -i eth0

# Connection tracking
ss -tuln | grep ESTAB
```

### Performance Metrics
- **Latency**: Ping response times
- **Throughput**: FTP transfer rates  
- **Concurrent connections**: HTTP session count
- **Error rates**: Failed connection attempts

## Advanced Testing

### Network Failure Simulation
1. **Link Down Testing**:
   - Disconnect interfaces in GNS3
   - Observe PyTgen failover behavior
   - Monitor convergence times

2. **Congestion Testing**:
   - Run multiple PyTgen instances
   - Saturate network links
   - Measure performance degradation

3. **Security Testing**:
   - SSH brute force simulation
   - HTTP flood testing
   - Protocol vulnerability tests

## Configuration Examples

### Router/Switch Testing
```python
# Test network infrastructure
('ssh_gen', [(0,0), (23,59), (15,0)], 
    ['router_mgmt_ip', 22, 'admin', 'cisco', 1, 
     ['show ip route', 'show interface brief', 'show version'], 60])
```

### Load Balancing Testing
```python
# Test multiple server targets
('http_gen', [(0,0), (23,59), (3,0)], 
    [['http://server1_ip', 'http://server2_ip', 'http://server3_ip'], 10, 5])
```

## Troubleshooting

### Common Issues:
1. **Permission denied**: Run with proper user privileges
2. **Network unreachable**: Check routing tables
3. **Connection timeout**: Verify firewall rules
4. **DNS resolution**: Use IP addresses initially

### Debug Commands:
```bash
# Network connectivity
ping -c 3 target_ip
traceroute target_ip
nmap -sn network/24

# PyTgen debugging
python3 run.py --debug
tail -f logs/$(hostname).log | grep ERROR
```
