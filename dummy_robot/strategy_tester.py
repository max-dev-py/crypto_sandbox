import pandas as pd
import datetime


def analyze_robot_trading(df, Robot, amount=10000, buy_rate=0.95, profit_rate=1.05, save_rate=0, amount_rate=0.05):
    min_amount, max_amount = amount, amount
    min_total, max_total = amount, amount

    robot = Robot(amount=min_amount, buy_rate=buy_rate, profit_rate=profit_rate,
                  save_rate=save_rate, amount_rate=amount_rate)

    new_df = []
    for id, data in df.iterrows():
        if robot.apply(**data):
            # print(len(robot.deals), data.timestamp, data.close, robot.status)
            # print(robot.deals[-1], 'BUY' if robot.deals[-1].quantity > 0 else 'SELL')
            # print('___' * 20)
            if robot.amount < min_amount:
                min_amount = robot.amount
            if max_amount < robot.amount:
                max_amount = robot.amount
            if robot.get_total_assets() < min_total:
                min_total = robot.get_total_assets()
            if robot.get_total_assets() > max_total:
                max_total = robot.get_total_assets()
            new_df.append(
                {
                    'Date': data.timestamp,
                    'Price': float(data.close),
                    'Amount': robot.amount,
                    'Quantity': robot.get_quantity(),
                    'Value': robot.get_total_assets() - robot.amount,
                    'Total': robot.get_total_assets(),
                    'Check Price': robot.check_price,
                    'Deal quantity': robot.deals[-1].quantity,
                }
            )

    days = abs((robot.deals[-1].date - robot.deals[0].date).days) if robot.deals else 0
    investment = amount - min_amount
    profit = robot.get_total_assets() - amount
    margin = profit / amount
    modified_margin = profit / (investment if investment > 0 else 1)
    total_value = robot.get_total_assets()
    quantity = robot.get_quantity()
    result = {'amount': amount, 'investment': investment, 'profit': profit, 'total_value': total_value,
              'margin': margin,
              'yield': (margin / (days if days > 0 else 1)) * 365,
              'modified_margin': modified_margin,
              'modified_yield': modified_margin / (days if days > 0 else 1) * 365,
              'days': days, 'current_amount': robot.amount,
              'quantity': quantity, 'price': (total_value - robot.amount) / (quantity or 1), 'min_amount': min_amount,
              'max_amount': max_amount, 'min_total': min_total, 'max_total': max_total,
              'from': min([_.date for _ in robot.deals]) if robot.deals else datetime.date.today(),
              'to': max([_.date for _ in robot.deals]) if robot.deals else datetime.date.today() + datetime.timedelta(
                  days=1),
              'deals_count': len(robot.deals), 'df': pd.DataFrame(new_df)}

    return result
