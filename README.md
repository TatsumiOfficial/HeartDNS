# HeartDNS

HeartDNS is a DNS service that provides an API for searching domain information.

## API Usage

### URL Endpoint
http://heartdns.com/API/index.php
### Method

The method used is `POST`.

### Parameter

To access the HeartDNS API, you need to provide two parameters:

- `ip_address` (required): the IP address to search for information
- `apikey` (required): the API key to access the HeartDNS service

Example parameter usage:
ip_address=192.168.1.1&apikey=1234567890

### Response

The result of the HeartDNS API call will be returned in JSON format with a structure like this:

```json
{
    "error": 0,
    "domain": [
        ["example.com"]
    ]
}

Explanation:

error: error code of the API call. If it has a value of 0, it means no error occurred.
domain: a list of domains associated with the searched IP address. This list is a multidimensional array, where each element of the second array contains the domain name associated with that IP address. The example above shows that there is only one domain associated with the IP address 192.168.1.1, which is example.com.
