import socket
import threading
import ipaddress
import time
import queue
from typing import List


class NetworkScanner:
    """Multi-threaded network port scanner with graceful shutdown"""

    def __init__(
        self,
        target: str,
        ports: str = "1-1000",
        max_threads: int = 50,
        timeout: float = 1.0,
    ):
        self.target = target
        self.ports_to_scan = self._parse_ports(ports)
        self.max_threads = max_threads
        self.timeout = timeout
        self.open_ports = []
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.scanned_ports = 0
        self.total_ports = 0

    def _parse_ports(self, port_spec: str) -> List[int]:
        """Parse port specification string"""
        ports = []
        for part in port_spec.split(","):
            if "-" in part:
                start, end = part.split("-")
                ports.extend(range(int(start), int(end) + 1))
            else:
                ports.append(int(part))
        return sorted(set(ports))

    def _get_hosts(self) -> List[str]:
        """Get list of hosts to scan"""
        try:
            network = ipaddress.ip_network(self.target, strict=False)
            return [str(ip) for ip in network.hosts()]
        except ValueError:
            return [self.target]

    def _scan_worker(self, port_queue: queue.Queue, host: str):
        """Worker thread to scan ports from a queue"""
        while not self.stop_event.is_set():
            try:
                port = port_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(self.timeout)
                    if sock.connect_ex((host, port)) == 0:
                        with self.lock:
                            self.open_ports.append(port)
                            print(f"Port {port}: OPEN")
            except socket.gaierror:
                with self.lock:
                    print(f"Hostname could not be resolved for port {port}")
            except socket.error as e:
                with self.lock:
                    print(f"Couldn't connect to port {port}: {e}")
            finally:
                with self.lock:
                    self.scanned_ports += 1
                port_queue.task_done()

    def _progress_reporter(self):
        """Reports the scanning progress"""
        while not self.stop_event.is_set() and self.scanned_ports < self.total_ports:
            time.sleep(2)
            with self.lock:
                progress = (self.scanned_ports / self.total_ports) * 100
                print(
                    f"Progress: {self.scanned_ports}/{self.total_ports} ports scanned ({progress:.2f}%)"
                )

    def scan(self):
        """Perform the network scan"""
        hosts = self._get_hosts()
        self.total_ports = len(hosts) * len(self.ports_to_scan)

        print(f"Starting scan on {len(hosts)} host(s) for {len(self.ports_to_scan)} ports each.")
        print(f"Total ports to scan: {self.total_ports}")
        print(f"Using {self.max_threads} threads. Timeout: {self.timeout}s.")
        print("-" * 50)
        start_time = time.time()

        try:
            for host in hosts:
                print(f"\nScanning host: {host}")
                self.open_ports = []
                self.scanned_ports = 0
                
                port_queue = queue.Queue()
                for port in self.ports_to_scan:
                    port_queue.put(port)

                threads = []
                for _ in range(self.max_threads):
                    thread = threading.Thread(
                        target=self._scan_worker, args=(port_queue, host)
                    )
                    thread.daemon = True
                    thread.start()
                    threads.append(thread)
                
                progress_thread = threading.Thread(target=self._progress_reporter)
                progress_thread.daemon = True
                progress_thread.start()

                port_queue.join()
                self.stop_event.set() 
                
                for thread in threads:
                    thread.join()
                
                progress_thread.join()
                self.stop_event.clear()

                print(f"\nHost {host} scan summary:")
                if self.open_ports:
                    print(f"  Open ports: {sorted(self.open_ports)}")
                else:
                    print("  No open ports found.")

        except KeyboardInterrupt:
            print("\n[!] Scan interrupted by user. Shutting down gracefully...")
            self.stop_event.set()

        end_time = time.time()
        print("\n" + "=" * 50)
        print("SCAN COMPLETE")
        print(f"Total scan duration: {end_time - start_time:.2f} seconds")
        print("=" * 50)

