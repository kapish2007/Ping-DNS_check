import csv
import os
import socket
from ipaddress import ip_network

# Function to ping an IP address
def ping_ip(ip):
    try:
        # Check if the input is a subnet
        if '/' in ip:
            network = ip_network(ip, strict=False)
            ping_results = {}
            for host_ip in network.hosts():
                response = os.system(f"ping -c 1 {host_ip}")
                ping_results[str(host_ip)] = (response == 0)
            return ping_results  # Dictionary of IP: ping status
        else:
            # Single IP address
            response = os.system(f"ping -c 1 {ip}")
            return {ip: response == 0}
    except Exception as e:
        print(f"Error pinging {ip}: {e}")
        return {ip: False}

# Function to perform reverse DNS lookup on an IP address
def reverse_dns_lookup(ip):
    try:
        fqdn, _, _ = socket.gethostbyaddr(ip)
        return fqdn
    except socket.herror:
        return None

# Function to process CSV and check IP and DNS resolution
def process_csv(input_file, output_file):
    results = []
    
    # Open the input CSV file
    with open(input_file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            ip = row['IP']
            fqdn_from_csv = row['FQDN']
            
            # Ping the IP
            is_pingable = ping_ip(ip)
            
            # Perform reverse DNS lookup
            fqdn_from_nslookup = reverse_dns_lookup(ip)
            
            # Cross-reference reverse DNS lookup result with FQDN from CSV
            dns_matches = fqdn_from_nslookup == fqdn_from_csv if fqdn_from_nslookup else False
            
            # Save the result
            results.append({
                'IP': ip,
                'FQDN from CSV': fqdn_from_csv,
                'Pingable': is_pingable,
                'FQDN from NSLookup': fqdn_from_nslookup if fqdn_from_nslookup else 'Not Found',
                'DNS Matches': dns_matches
            })
    
    # Write the results to an output CSV
    write_to_csv(output_file, results)

# Function to write the results to a CSV file
def write_to_csv(output_file, results):
    fieldnames = ['IP', 'FQDN from CSV', 'Pingable', 'FQDN from NSLookup', 'DNS Matches']
    
    with open(output_file, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        for result in results:
            writer.writerow(result)

# Main function
if __name__ == '__main__':
    input_file = 'input.csv'   # Replace with your input CSV file path
    output_file = 'output.csv' # Specify the output CSV file path
    process_csv(input_file, output_file)
    print(f"Results written to {output_file}")
