def calculate_taxes(operations):
    taxes = []
    total_quantity = 0
    total_cost = 0.0
    accumulated_loss = 0.0

    for op in operations:
        if op["operation"] == "buy":
            quantity = op["quantity"]
            unit_cost = op["unit-cost"]
            total_quantity += quantity
            total_cost += quantity * unit_cost
            taxes.append({"tax": 0.0})

        elif op["operation"] == "sell":
            quantity = op["quantity"]
            unit_sell_price = op["unit-cost"]
            revenue = quantity * unit_sell_price

            # Evita divisão por zero
            if total_quantity == 0:
                average_cost = 0.0
            else:
                average_cost = total_cost / total_quantity

            cost_basis = quantity * average_cost
            profit = revenue - cost_basis

            # Atualiza estoque
            total_quantity -= quantity
            total_cost -= cost_basis

            # Isenção se receita da venda for até 20 mil
            if revenue <= 20000:
                taxes.append({"tax": 0.0})
                if profit < 0:
                    accumulated_loss += abs(profit)
                continue

            # Deduz prejuízo acumulado
            net_profit = profit - accumulated_loss
            if net_profit <= 0:
                accumulated_loss = abs(net_profit)
                taxes.append({"tax": 0.0})
            else:
                tax = round(net_profit * 0.20, 2)
                accumulated_loss = 0.0
                taxes.append({"tax": tax})

    return taxes