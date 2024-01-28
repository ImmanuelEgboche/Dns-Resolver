# DNS Resolver with Python

This Python script serves as a basic DNS resolver, allowing you to query DNS servers and resolve hostnames to IP addresses. The script uses the UDP protocol to send DNS queries and parse the responses.

## Prerequisites

Make sure you have Python installed on your system. The script should work with Python 3.

## How to Run

1. Clone the repository to your local machine:

   ```bash
   git clone <repository-url>
   
2. Navigate to the directory containing the script:

    ```
    cd dns-resolver-python
    ```
3. Run the script 
    ```
    python dns.py
    ```



## Usage

The script is set up to query the root DNS server (IP address: 198.41.0.4) for a specified domain. You can modify the `resolve_with_root_name_server` function in the script to query other DNS servers or change the target domain.

## How It Works


[ Your Computer ]        [ Google's DNS Server ]
           |                         |
      Create Socket                   |
           |                         |
      Send Message ------------------>|
           |                         |
      Receive Response <--------------|
           |                         |
   Check ID in Response               |
           |                         |



The script follows these steps:

1. Sends a DNS query to the specified DNS server for the given domain.
2. Parses the DNS response, extracting information from the header, question section, answer section, and additional section.
3. Decodes the domain names and prints details such as the resolved IP address or authoritative name servers.
4. Handles different DNS record types, including A records (IPv4 addresses) and NS records (authoritative name servers).

## Example

Running the script with the default settings queries the root DNS server for the domain "dns.google.com" and prints the resolved IP address.

## Possible Use Cases

This script can be used for educational purposes to understand the DNS resolution process. It provides a simple implementation that can be extended for more complex scenarios, such as building a custom DNS resolver or exploring DNS security issues.
