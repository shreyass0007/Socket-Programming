#!/usr/bin/env python3
import socket
import ipaddress

def resolve_hostname(host: str):
    # Collect IPv4/IPv6 addresses for the hostname
    addrs = set()
    try:
        results = socket.getaddrinfo(host, None, family=socket.AF_UNSPEC, type=socket.SOCK_STREAM)
        for family, socktype, proto, canonname, sockaddr in results:
            ip = sockaddr[0]
            addrs.add(ip)
        cname = socket.getfqdn(host)
        return cname, sorted(addrs)
    except socket.gaierror as e:
        raise RuntimeError(f"Could not resolve host name: {host}") from e

def reverse_lookup(ip: str):
    try:
        name, aliases, addrs = socket.gethostbyaddr(ip)
        # gethostbyaddr may return multiple addresses; deduplicate
        return name, sorted(set(addrs))
    except (socket.herror, socket.gaierror):
        # No PTR record or not resolvable
        return ip, [ip]

def main():
    print("1. Enter Host Name")
    print("2. Enter IP address")
    choice = input("Choice = ").strip()

    if choice == "1":
        host = input("\nEnter host name: ").strip()
        if not host:
            print("Host name cannot be empty")
            return
        try:
            name, ips = resolve_hostname(host)
            # Mimic Java-style fields
            primary_ip = ips[0] if ips else "N/A"
            print(f"IP address: {primary_ip}")
            print(f"Host name: {name}")
            print(f"Host and IP: {name} / {primary_ip}")
            if len(ips) > 1:
                print("All IPs:")
                for ip in ips:
                    print(f"  - {ip}")
        except RuntimeError as e:
            print(str(e))

    elif choice == "2":
        ip = input("\nEnter IP address: ").strip()
        try:
            # Validate IP literal (supports IPv4/IPv6)
            ipaddress.ip_address(ip)
        except ValueError:
            print("Invalid IP address format")
            return

        name, addrs = reverse_lookup(ip)
        # Mimic Java-style fields
        print(f"Host name: {name}")
        print(f"IP address: {ip}")
        print(f"Host and IP: {name} / {ip}")
        if len(addrs) > 1:
            print("All PTR IPs seen:")
            for a in addrs:
                print(f"  - {a}")
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
