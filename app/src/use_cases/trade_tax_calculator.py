def calculate_taxes(operations):
    taxes = []

    # Estoque atual de ações
    total_quantity = 0
    total_cost = 0.0

    # Prejuízo acumulado para dedução futura
    accumulated_loss = 0.0

    for op in operations:
        if op["operation"] == "buy":
            # 📘 Regra 1: Compras não geram imposto
            quantity = op["quantity"]
            unit_cost = op["unit-cost"]

            # Atualiza estoque e custo total
            total_quantity += quantity
            total_cost += quantity * unit_cost

            taxes.append({"tax": 0.0})

        elif op["operation"] == "sell":
            quantity = op["quantity"]
            unit_sell_price = op["unit-cost"]
            revenue = quantity * unit_sell_price

            # 📘 Regra 5: Calcula preço médio ponderado
            average_cost = total_cost / total_quantity if total_quantity > 0 else 0.0
            cost_basis = quantity * average_cost
            profit = revenue - cost_basis

            # Atualiza estoque e custo total após venda
            total_quantity -= quantity
            total_cost -= cost_basis

            # 📘 Regra 2: Isenção se receita da venda ≤ R$ 20.000
            if revenue <= 20000:
                taxes.append({"tax": 0.0})

                # 📘 Regra 4: Acumula prejuízo mesmo em vendas isentas
                if profit < 0:
                    accumulated_loss += abs(profit)
                continue

            # 📘 Regra 4: Deduz prejuízo acumulado do lucro
            net_profit = profit - accumulated_loss

            if net_profit <= 0:
                # Ainda há prejuízo a compensar
                accumulated_loss = abs(net_profit)
                taxes.append({"tax": 0.0})
            else:
                # 📘 Regra 3: Aplica imposto de 20% sobre lucro líquido
                tax = round(net_profit * 0.20, 2)
                accumulated_loss = 0.0
                taxes.append({"tax": tax})

    return taxes