'''
GNS3 Network Testing Configuration for PyTgen
Multi-node network traffic generation and testing
'''

import logging

class Conf:
    # Increased threads for network testing
    maxthreads = 30
    
    # Set logging level
    loglevel = logging.INFO
    
    # Network topology IPs (adjust based on your GNS3 setup)
    target_networks = {
        'local_subnet': ['10.0.0.1', '10.0.0.2', '10.0.0.3'],
        'remote_subnet': ['192.168.1.1', '192.168.1.10', '192.168.1.20'],
        'wan_targets': ['8.8.8.8', '1.1.1.1'],
        'internal_servers': ['172.16.1.10', '172.16.1.20']
    }
    
    # SSH commands for network testing
    ssh_commands = [
        'ip route show',
        'ping -c 3 8.8.8.8',
        'netstat -tuln',
        'ss -tuln', 
        'ifconfig',
        'arp -a',
        'nslookup google.com'
    ]
    
    # HTTP targets for web traffic simulation
    http_targets = [
        'http://10.0.0.1:8000',
        'http://192.168.1.10:80', 
        'https://www.google.com',
        'https://httpbin.org/get'
    ]

    # Jobs for comprehensive network testing
    jobs = [
        # === CONNECTIVITY TESTING ===
        # Local subnet ping tests
        ('ping_gen', [(0, 0), (23, 59), (0, 30)], ['10.0.0.1', 5]),
        ('ping_gen', [(0, 0), (23, 59), (0, 45)], ['10.0.0.2', 3]),
        
        # Cross-subnet connectivity  
        ('ping_gen', [(0, 0), (23, 59), (1, 0)], ['192.168.1.1', 4]),
        ('ping_gen', [(0, 0), (23, 59), (1, 30)], ['192.168.1.10', 3]),
        
        # Internet connectivity
        ('ping_gen', [(0, 0), (23, 59), (2, 0)], ['8.8.8.8', 2]),
        ('ping_gen', [(0, 0), (23, 59), (2, 30)], ['1.1.1.1', 2]),
        
        # === WEB TRAFFIC SIMULATION ===
        # Internal web services
        ('http_gen', [(0, 0), (23, 59), (3, 0)], [['http://10.0.0.1:8000'], 2, 10]),
        ('http_gen', [(0, 0), (23, 59), (4, 0)], [['http://192.168.1.10:80'], 1, 15]),
        
        # External web traffic
        ('http_gen', [(0, 0), (23, 59), (5, 0)], [['https://www.google.com'], 1, 20]),
        ('http_gen', [(0, 0), (23, 59), (6, 0)], [['https://httpbin.org/get'], 1, 25]),
        
        # === FILE TRANSFER TESTING ===
        # FTP traffic simulation
        ('ftp_gen', [(0, 0), (23, 59), (10, 0)], ['10.0.0.1', 'testuser', 'password', [], [], 2, False, 10]),
        ('ftp_gen', [(0, 0), (23, 59), (15, 0)], ['192.168.1.10', 'anonymous', 'test@domain.com', [], [], 1, False, 15]),
        
        # === SSH/REMOTE TESTING ===
        # SSH to network devices
        ('ssh_gen', [(0, 0), (23, 59), (20, 0)], ['10.0.0.1', 22, 'admin', 'password', 1, ssh_commands, 30]),
        ('ssh_gen', [(0, 0), (23, 59), (25, 0)], ['192.168.1.1', 22, 'root', 'toor', 1, ssh_commands, 45]),
        
        # SFTP file transfers
        ('sftp_gen', [(0, 0), (23, 59), (30, 0)], ['10.0.0.1', 22, 'testuser', 'password', ['/tmp/test1.txt'], ['/tmp/received1.txt'], 1, 30]),
        
        # === EMAIL TRAFFIC ===
        # SMTP testing (if mail server available)
        ('smtp_gen', [(0, 0), (23, 59), (35, 0)], ['192.168.1.10', 'user@domain.com', 'password', 'pytgen@test.com', 'admin@domain.com']),
        
        # === LOCAL FILE OPERATIONS ===
        # Generate test files for transfers
        ('copy_gen', [(0, 0), (23, 59), (8, 0)], [None, '/tmp/pytgen_net_test.dat', 50]),
    ]
