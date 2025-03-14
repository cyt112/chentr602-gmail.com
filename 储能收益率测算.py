import math


def calculate_bch_profitability():
    print("工商业储能收益率测算程序")

    # 用户输入部分
    try:
        total_capacity = float(input("\n1. 储能系统容量 (kWh): "))
        high_price = float(input("\n2. 最高电价 (元/kWh): "))
        low_price = float(input("\n3. 最低电价 (元/kWh): "))
        discharge_times = int(input("\n4. 每日充放电次数："))
        discharge_days = int(input("\n5. 每年工作日数："))
        operation_cost = float(input("\n6. 运营成本（元/年）："))
        initial_investment = float(input("\n7. 初始投资（元）："))
        investment_period = int(input("\n8. 投资期限（年）："))
    except ValueError:
        print("请检查输入是否为数字")
        return

    # 参数合法性检查
    if total_capacity <= 0 or discharge_times <= 0 or discharge_days <= 0 or investment_period <= 0:
        print("某些参数不能为非正数，请重新检查输入。")
        return

    # 如果充放电次数大于2次，则逐次输入每次循环的高低电价
    if discharge_times > 1:
        prices = []
        for i in range(discharge_times):
            print(f"\n请输入第{i + 1}次循环的高电价 (元/kWh): ")
            high_price_single = float(input())
            print(f"请输入第{i + 1}次循环的低电价 (元/kWh): ")
            low_price_single = float(input())
            prices.append((high_price_single, low_price_single))
    else:
        prices = [(high_price, low_price)]

    # 计算每日收益
    daily_profits = []
    for high_p, low_p in prices:
        daily_profit = (high_p - low_p) * total_capacity
        daily_profits.append(daily_profit)

    total_daily_profit = sum(daily_profits) * discharge_times
    total_annual_profit = total_daily_profit * discharge_days

    annual_operation_cost = operation_cost
    annual_depreciation = initial_investment / investment_period
    total_annual_expenses = annual_operation_cost + annual_depreciation
    net_annual_cash_flow = (total_annual_profit - total_annual_expenses)

    # 构建现金流量序列
    cash_flows = [-initial_investment]
    for _ in range(investment_period):
        cash_flows.append(net_annual_cash_flow)

    # 计算净现值（NPV）
    discount_rate = 0.08
    npv = sum(c / (1 + discount_rate) ** i for i, c in enumerate(cash_flows))

    # 计算内部收益率（IRR），防止除以零的情况
    def calculate_irr(cash_flows):
        n = len(cash_flows)
        if n == 0:
            return 0.0
        low = -1.0
        high = 2.0
        for _ in range(100):
            mid = (low + high) / 2
            if mid <= -1.0:
                break
            try:
                pv = sum(cash_flows[i] / (1 + mid) ** i for i in range(n))
            except ZeroDivisionError:
                # 避免除法错误，退出循环
                break
            if pv > 0:
                low = mid
            else:
                high = mid
            if abs(pv) < 1e-6:
                break
        return round(low * 100, 2)

    # 计算IRR，允许负数结果
    irr = calculate_irr(cash_flows)

    # 输出结果
    print("\n计算结果：")
    print(f"储能系统总容量: {int(total_capacity)} kWh")
    print(f"每日充放电次数: {discharge_times} 次")
    for i, (high_p, low_p) in enumerate(prices):
        print(f"第{i + 1}次循环单次收益: {(high_p - low_p) * total_capacity:.2f} 元")
    print(f"每日总收益：{total_daily_profit:.2f} 元")

    print("\n项目成本部分:")
    print(f"运营成本年均值: {annual_operation_cost:.2f} 元")
    print(f"初始投资折旧：{annual_depreciation:.2f} 元")
    print(f"总年支出：{total_annual_expenses:.2f} 元")

    print("\n项目财务指标：")
    print(f"净现值（NPV）：{npv:.2f} 元")
    print(f"内部收益率（IRR）：{irr}%")  # 保持两位小数

    if npv > 0 and irr >= 0:
        print("项目具有较高的盈利能力。")
    elif npv < 0 or (irr < 0):
        print("项目可能亏损，建议重新评估参数和数据输入是否正确。")
    else:
        print("项目盈亏平衡点附近，需进一步分析。")

    print("\n程序完毕，输出已完成。")


calculate_bch_profitability()
