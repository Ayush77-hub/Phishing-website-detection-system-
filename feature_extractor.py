import re

def extract_features(url):
    # 1. URL Length
    url_len = len(url)
    
    # 2. Number of Dots
    dot_count = url.count('.')
    
    # 3. Number of Digits
    digit_count = sum(c.isdigit() for c in url)
    
    # 4. Number of Hyphens
    hyphen_count = url.count('-')
    
    # 5. HTTPS Availability
    has_https = 1 if url.startswith('https') else 0
    
    # 6. IP Address Detection
    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    has_ip = 1 if re.search(ip_pattern, url) else 0
    
    # 7. @ Symbol Detection
    has_at = 1 if '@' in url else 0
    
    return [url_len, dot_count, digit_count, hyphen_count, has_https, has_ip, has_at]