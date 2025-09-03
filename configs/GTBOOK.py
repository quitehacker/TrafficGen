'''
Local testing configuration for PyTgen
Safe configuration that targets localhost for testing
'''

import logging

class Conf:
    # Maximum number of worker threads
    maxthreads = 20
    
    # Set logging level
    loglevel = logging.INFO
    
    # SSH/Shell commands for local testing
    ssh_commands = ['dir', 'echo hello', 'python --version', 'whoami', 'hostname']
    
    # Local HTTP targets (start with: python -m http.server 8000)
    http_local = ['http://localhost:8000', 'http://127.0.0.1:8000']
    
    # Files for FTP testing (will need local FTP server)
    ftp_put = ['C:/Windows/System32/drivers/etc/hosts']  # Small test file
    ftp_get = ['test.txt']  # File to download
    
    # Files for SFTP testing
    sftp_put = [('C:/Windows/System32/drivers/etc/hosts', '/tmp/hosts')]
    sftp_get = [('/etc/passwd', 'C:/temp/passwd')]
    
    # Job definitions for comprehensive testing
    jobdef = [
        # Ping tests - every 45 seconds
        ('ping_gen', [(0, 0), (23, 59), (0, 45)], ['127.0.0.1', 4]),
        ('ping_gen', [(0, 0), (23, 59), (1, 0)], ['8.8.8.8', 2]),  # Google DNS
        
        # HTTP requests - every 3 minutes
        ('http_gen', [(0, 0), (23, 59), (3, 0)], [http_local, 3, 10]),
        ('http_gen', [(0, 0), (23, 59), (5, 0)], [['https://httpbin.org/get'], 1, 15]),
        
        # SMTP test (will fail gracefully if no server)
        ('smtp_gen', [(0, 0), (23, 59), (10, 0)], ['localhost', 'test@localhost', 'password', 'pytgen@localhost', 'test@localhost']),
        
        # FTP test (will fail gracefully if no server)
        ('ftp_gen', [(0, 0), (23, 59), (15, 0)], ['localhost', 'anonymous', 'test@localhost', [], [], 1, False, 5]),
        
        # File copying operations - every 5 minutes
        ('copy_gen', [(0, 0), (23, 59), (5, 0)], [None, 'C:/temp/pytgen_test.txt', 10]),  # Generate 10KB file
        
        # SSH test (will fail gracefully if no SSH server)
        ('ssh_gen', [(0, 0), (23, 59), (20, 0)], ['localhost', 22, 'testuser', 'password', 2, ssh_commands, 30]),
        
        # SFTP test (will fail gracefully if no SSH server)  
        ('sftp_gen', [(0, 0), (23, 59), (25, 0)], ['localhost', 22, 'testuser', 'password', [], [], 2, 30]),
        
        # Reboot test - COMMENTED OUT for safety
        # ('reboot_gen', [(23, 55), (23, 59), (24, 0)], []),
    ]
