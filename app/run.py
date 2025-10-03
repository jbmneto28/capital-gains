import json
import sys

from src.use_cases.trade_tax_calculator import calculate_taxes

if __name__ == '__main__':
    for line in sys.stdin:
        line = line.strip()
        if not line:
            break
        operations = json.loads(line)
        taxes = calculate_taxes(operations)
        print(json.dumps(taxes))
