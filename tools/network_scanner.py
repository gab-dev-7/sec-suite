import socket
import threading
import ipaddress
import time
from typing import List, Tuple


class NetworkScanner:
    """Multi-threaded network port scanner"""

    def __init__(
        self,
        target: str,
        ports: str = "1-1000",
        max_threads: int = 50,
        timeout: float = 1.0,
    ):
        self.target = target
        self.ports = self._parse_ports(ports)
        self.max_threads = max_threads
        self.timeout = timeout
        self.open_ports = []
        self.lock = threading.Lock()
        self.scanned = 0
        self.total_ports = len(self.ports)

    def _parse_ports(self, port_spec: str) -> List[int]:
        """Parse port specification string"""
        ports = []

        for part in port_spec.split(","):
            if "-" in part:
                start, end = part.split("-")
                ports.extend(range(int(start), int(end) + 1))
            else:
                ports.append(int(part))

        return sorted(set(ports))  # Remove duplicates

    def _scan_port(self, target: str, port: int):
        """Scan a single port"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((target, port))

                with self.lock:
                    self.scanned += 1
                    if result == 0:
                        self.open_ports.append(port)
                        print(f"Port {port}: OPEN")

                    if self.scanned % 100 == 0:
                        progress = (self.scanned / self.total_ports) * 100
                        print(
                            f"Progress: {progress:.1f}% ({self.scanned}/{self.total_ports})"
                        )

        except Exception as e:
            with self.lock:
                self.scanned += 1

    def _get_hosts(self) -> List[str]:
        """Get list of hosts to scan"""
        try:
            network = ipaddress.ip_network(self.target, strict=False)
            return [str(ip) for ip in network.hosts()]
        except:
            # Single host
            return [self.target]

    def scan(self):
        """Perform the network scan"""
        hosts = self._get_hosts()

        print(f"Starting scan of {len(hosts)} host(s)")
        print(f"Scanning {self.total_ports} ports per host")
        print(f"Using {self.max_threads} threads")
        print("-" * 50)

        start_time = time.time()

        for host in hosts:
            print(f"\nScanning host: {host}")
            self._scan_host(host)

        end_time = time.time()

        print("\n" + "=" * 50)
        print("SCAN RESULTS")
        print("=" * 50)
        print(f"Open ports: {sorted(self.open_ports)}")
        print(f"Scan duration: {end_time - start_time:.2f} seconds")

    def _scan_host(self, host: str):
        """Scan all ports for a single host"""
        threads = []
        port_index = 0

        # Resolve hostname to IP
        try:
            ip = socket.gethostbyname(host)
            print(f"Resolved {host} to {ip}")
        except socket.gaierror:
            print(f"Could not resolve {host}")
            return

        # Create and start threads
        while port_index < len(self.ports):
            # Wait if too many active threads
            if threading.active_count() - 1 >= self.max_threads:
                time.sleep(0.1)
                continue

            port = self.ports[port_index]
            thread = threading.Thread(target=self._scan_port, args=(ip, port))
            thread.daemon = True
            thread.start()
            threads.append(thread)
            port_index += 1

        # Wait for all threads to complete
        for thread in threads:
            thread.join()
