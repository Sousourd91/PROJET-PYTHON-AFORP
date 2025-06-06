import re
from collections import Counter

lignes = open("auth.log").readlines()
ips = [re.search(r"\d+\.\d+\.\d+\.\d+", l).group() for l in lignes if "Failed password" in l]
for ip, count in Counter(ips).most_common(5):
    print(ip, ":", count)