import csv
import os
import socket


# Function to ping an IP address
def ping_ip(ip):
    try:
        response = os.system(f"ping -c 1 {ip}")
        return response == 0
    except Exception as e:
        print(f"Error pinging {ip}: {e}")
        return False


# Function to perform reverse DNS lookup on an IP address
def reverse_dns_lookup(ip):
    try:
        fqdn, _, _ = socket.gethostbyaddr(ip)
        return fqdn
    except socket.herror:
        return None


# Function to process CSV and check IP and DNS resolution
def process_csv(file_path):
    results = []

    # Open the CSV file
    with open(file_path, mode='r') as csv_file:
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
                'FQDN from NSLookup': fqdn_from_nslookup,
                'DNS Matches': dns_matches
            })

    # Print the results
    print_results(results)


# Function to print results
def print_results(results):
    print(f"{'IP':<15} {'FQDN from CSV':<30} {'Pingable':<10} {'FQDN from NSLookup':<30} {'DNS Matches':<12}")
    print("-" * 110)

    for result in results:
        # Use 'N/A' if FQDN from NSLookup is None
        fqdn_nslookup = result['FQDN from NSLookup'] if result['FQDN from NSLookup'] else 'Not Found'
        print(
            f"{result['IP']:<15} {result['FQDN from CSV']:<30} {str(result['Pingable']):<10} {fqdn_nslookup:<30} {str(result['DNS Matches']):<12}")


# Main function
if __name__ == '__main__':
    file_path = 'input.csv'  # Replace with your CSV file path
    process_csv(file_path)
