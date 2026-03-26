import datetime
import re
import sys
from collections import Counter


def read_log():
    log_entries = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        fields = line.split("\t")
        if len(fields) < 14:
            continue
        ts = datetime.datetime.fromtimestamp(float(fields[0]))
        uid = fields[1]
        orig_h = fields[2]
        orig_p = int(fields[3])
        resp_h = fields[4]
        resp_p = int(fields[5])
        method = fields[7]
        host = fields[8]
        uri = fields[9]
        status_code = int(fields[12])
        log_entries.append(
            (ts, uid, orig_h, orig_p, resp_h, resp_p, method, host, uri, status_code)
        )
    return log_entries


def sort_log(log, index):
    if not 0 <= index < len(log[0]):
        raise IndexError(f"Invalid index: {index}")
    return sorted(log, key=lambda x: x[index])


def get_entries_by_code(log, code):
    if not isinstance(code, int):
        raise TypeError("Code must be an integer")
    if not (100 <= code < 600):
        raise ValueError("Invalid HTTP status code")
    return [entry for entry in log if entry[9] == code]


def is_valid_ip(addr):
    pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
    if not re.match(pattern, addr):
        return False
    parts = addr.split(".")
    return all(0 <= int(part) <= 255 for part in parts)


def get_entries_by_addr(log, addr):
    if is_valid_ip(addr):
        return [entry for entry in log if entry[2] == addr]
    else:
        return [entry for entry in log if entry[7] == addr]


def get_failed_reads(log, merge=False):
    errors_4xx = [entry for entry in log if 400 <= entry[9] < 500]
    errors_5xx = [entry for entry in log if 500 <= entry[9] < 600]
    if merge:
        return errors_4xx + errors_5xx
    return errors_4xx, errors_5xx


def get_entries_by_extension(log, ext):
    if not ext.startswith("."):
        ext = "." + ext
    return [entry for entry in log if entry[8].split("?")[0].endswith(ext)]


def get_top_ips(log, n=10):
    ips = [entry[2] for entry in log]
    counter = Counter(ips)
    return counter.most_common(n)


def get_unique_methods(log):
    methods = set(entry[6] for entry in log)
    return sorted(list(methods))


def get_entries_in_time_range(log, start, end):
    if not isinstance(start, datetime.datetime) or not isinstance(
        end, datetime.datetime
    ):
        raise TypeError("Start and end must be datetime objects")
    if start > end:
        raise ValueError("Start must be before end")
    return [entry for entry in log if start <= entry[0] < end]


def count_by_method(log):
    methods = [entry[6] for entry in log]
    return dict(Counter(methods))


def get_top_uris(log, n=10):
    uris = [entry[8] for entry in log]
    counter = Counter(uris)
    return counter.most_common(n)


def count_status_classes(log):
    result = {"2xx": 0, "3xx": 0, "4xx": 0, "5xx": 0}
    for entry in log:
        code = entry[9]
        if 200 <= code < 300:
            result["2xx"] += 1
        elif 300 <= code < 400:
            result["3xx"] += 1
        elif 400 <= code < 500:
            result["4xx"] += 1
        elif 500 <= code < 600:
            result["5xx"] += 1
    return result


def entry_to_dict(entry):
    return {
        "ts": entry[0],
        "uid": entry[1],
        "ip": entry[2],
        "port": entry[3],
        "resp_h": entry[4],
        "resp_p": entry[5],
        "method": entry[6],
        "host": entry[7],
        "uri": entry[8],
        "code": entry[9],
    }


def log_to_dict(log):
    result = {}
    for entry in log:
        uid = entry[1]
        entry_dict = entry_to_dict(entry)
        if uid not in result:
            result[uid] = []
        result[uid].append(entry_dict)
    return result


def print_dict_entry_dates(log_dict):
    for uid, entries in log_dict.items():
        ips = set(e["ip"] for e in entries)
        hosts = set(e["host"] for e in entries)
        count = len(entries)
        timestamps = [e["ts"] for e in entries]
        first_ts = min(timestamps)
        last_ts = max(timestamps)
        methods = [e["method"] for e in entries]
        method_counts = Counter(methods)
        total = len(methods)
        method_percentages = {m: (c / total * 100) for m, c in method_counts.items()}
        codes_2xx = sum(1 for e in entries if 200 <= e["code"] < 300)
        ratio_2xx = (codes_2xx / total * 100) if total > 0 else 0
        print(f"UID: {uid}")
        print(f"  IPs: {', '.join(ips)}")
        print(f"  Hosts: {', '.join(hosts)}")
        print(f"  Requests: {count}")
        print(f"  First: {first_ts}, Last: {last_ts}")
        print(f"  Methods: {method_percentages}")
        print(f"  2xx ratio: {ratio_2xx:.2f}%")


def get_most_active_session(log_dict):
    max_count = 0
    max_uid = None
    for uid, entries in log_dict.items():
        if len(entries) > max_count:
            max_count = len(entries)
            max_uid = uid
    return max_uid, max_count


def get_session_paths(log):
    result = {}
    for entry in log:
        uid = entry[1]
        uri = entry[8]
        if uid not in result:
            result[uid] = []
        result[uid].append(uri)
    return result


def detect_sus(log, threshold):
    ip_counts = Counter(entry[2] for entry in log)
    sus_ips = []
    for ip, count in ip_counts.items():
        if count >= threshold:
            sus_ips.append((ip, count))
    return sorted(sus_ips, key=lambda x: x[1], reverse=True)


def get_extension_stats(log):
    extensions = []
    for entry in log:
        uri = entry[8].split("?")[0]
        if "." in uri:
            ext = uri.rsplit(".", 1)[1]
            extensions.append(ext)
        else:
            extensions.append("")
    return dict(Counter(extensions))


def analyze_log(log):
    top_ips = get_top_ips(log, 5)
    top_uris = get_top_uris(log, 5)
    method_dist = count_by_method(log)
    status_classes = count_status_classes(log)
    errors_4xx = sum(1 for entry in log if 400 <= entry[9] < 500)
    errors_5xx = sum(1 for entry in log if 500 <= entry[9] < 600)
    total = len(log)
    unique_ips = len(set(entry[2] for entry in log))
    unique_uris = len(set(entry[8] for entry in log))
    unique_methods = len(set(entry[6] for entry in log))
    return {
        "top_ips": top_ips,
        "top_uris": top_uris,
        "method_distribution": method_dist,
        "status_classes": status_classes,
        "4xx_errors": errors_4xx,
        "5xx_errors": errors_5xx,
        "total_requests": total,
        "unique_ips": unique_ips,
        "unique_uris": unique_uris,
        "unique_methods": unique_methods,
    }


if __name__ == "__main__":
    log = read_log()
    print(len(log))
