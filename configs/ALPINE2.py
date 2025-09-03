'''
Two-host testing configuration: Alpine 2 → Alpine 3
Simple connectivity and traffic generation testing
'''

import logging

class Conf:
    # Lightweight configuration for Alpine
    maxthreads = 10
    
    # Set logging level
    loglevel = logging.INFO
    
    # Alpine 3 target (adjust IP based on your GNS3 setup)
    # Common GNS3 Alpine IPs: 192.168.1.x or 10.0.0.x
    alpine3_ip = '192.168.3.14'  # Change this to Alpine 3's actual IP
    
    # Test scenarios from Alpine 2 to Alpine 3
    jobs = [
        # === BASIC CONNECTIVITY ===
        # Ping test every 30 seconds
        ('ping_gen', [(0, 0), (23, 59), (0, 30)], [alpine3_ip, 4]),
        
        # === HTTP TESTING ===
        # Test HTTP service on Alpine 3 (if available)
        ('http_gen', [(0, 0), (23, 59), (2, 0)], [[f'http://{alpine3_ip}:8000'], 2, 10]),
        
        # === FILE OPERATIONS ===
        # Generate test files locally
        ('copy_gen', [(0, 0), (23, 59), (5, 0)], [None, '/tmp/alpine2_test.dat', 20]),
        
        # === SSH TESTING ===
        # SSH to Alpine 3 (common Alpine credentials)
        ('ssh_gen', [(0, 0), (23, 59), (10, 0)], [alpine3_ip, 22, 'root', 'alpine', 1, 
            ['hostname', 'ip addr show', 'ps aux', 'df -h', 'free -m'], 30]),
        
        # === FTP TESTING ===
        # FTP to Alpine 3 (if FTP server running)
        ('ftp_gen', [(0, 0), (23, 59), (15, 0)], [alpine3_ip, 'anonymous', 'test@alpine.com', 
            [], [], 1, False, 20]),
    ]
