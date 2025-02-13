import pandas as pd
from dummy_robot.cinco import CincoRobot


def test(df, amount=10000, buy_rate=0.95, profit_rate=1.05, save_rate=0, amount_rate=0.05):
    print(df)
    min_amount, max_amount = amount, amount
    min_total, max_total = amount, amount

    robot = CincoRobot(amount=min_amount, buy_rate=buy_rate, profit_rate=profit_rate,
                       save_rate=save_rate, amount_rate=amount_rate)

    new_df = []
    for id, data in df.iterrows():
        if robot.apply(**data):
            print(len(robot.deals), data.timestamp, data.close, robot.status)
            print(robot.deals[-1], 'BUY' if robot.deals[-1].quantity > 0 else 'SELL')
            print('___' * 20)
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
                    'Date': data.timestamp.date(),
                    'Price': float(data.close),
                    'Amount': robot.amount,
                    'Quantity': robot.get_quantity(),
                    'Value': robot.get_total_assets() - robot.amount,
                    'Total': robot.get_total_assets(),
                    'Check Price': robot.check_price,
                    'Deal quantity': robot.deals[-1].quantity,
                }
            )

    days = abs((robot.deals[-1].date - robot.deals[0].date).days)
    investment = amount - min_amount
    profit = robot.get_total_assets() - amount
    margin = profit / amount
    modified_margin = profit / investment
    total_value = robot.get_total_assets()
    quantity = robot.get_quantity()
    result = {
        'amount': amount,
        'investment': investment,
        'profit': profit,
        'total_value': total_value,
        'margin': margin,
        'yield': (margin / days) * 365,
        'modified_margin': modified_margin,
        'modified_yield': modified_margin / days * 365,
        'days': days,
        'current_amount': robot.amount,
        'quantity': quantity,
        'price': (total_value - robot.amount) / (quantity or 1),
        'min_amount': min_amount, 'max_amount': max_amount,
        'min_total': min_total, 'max_total': max_total,
        'from': min([_.date for _ in robot.deals]),
        'to': max([_.date for _ in robot.deals]),
        'deals_count': len(robot.deals),
    }

    result['df'] = pd.DataFrame(new_df)

    return result


df = pd.read_pickle('prices.pickle')
norm_result = test(df, buy_rate=0.93, profit_rate=1.05, save_rate=0.005)
reversed_result = test(df.sort_index(ascending=False), buy_rate=0.93, profit_rate=1.05, save_rate=0.005)
# reversed_result = norm_result

print(
    f'''
        Amount: {norm_result['amount']:.2f} Investment: {norm_result['investment']:.2f}   |     Amount: {reversed_result['amount']:.2f} Investment: {reversed_result['investment']:.2f}
        Profit: {norm_result['profit']:.2f}                        |     Profit: {reversed_result['profit']:.2f}
        Total values: {norm_result['total_value']:.2f}                 |     Total values: {reversed_result['total_value']:.2f}
        Margin: {norm_result['margin']:.2%}                         |     Margin: {reversed_result['margin']:.2%}
        Yield: {norm_result['yield']:.2%} for {norm_result['days']} days              |     Yield: {reversed_result['yield']:.2%} for {reversed_result['days']} days
        Modified Margin: {norm_result['modified_margin']:.2%}                |     Modified Margin: {reversed_result['modified_margin']:.2%}
        Modified Yield: {norm_result['modified_yield']:.2%} for {norm_result['days']} days    |     Modified Yield: {reversed_result['modified_yield']:.2%} for {norm_result['days']} days
        Current Amount: {norm_result['current_amount']:.2f}                     |     Current Amount: {reversed_result['current_amount']:.2f}
        Quantity: {norm_result['quantity']} price {norm_result['price']:.2f} |     Quantity: {reversed_result['quantity']:.2f} price {reversed_result['price']:.2f}
        Min amount: {norm_result['min_amount']:.2f} Max amount: {norm_result['max_amount']:.2f}     |     Min amount: {reversed_result['min_amount']:.2f} Max amount: {reversed_result['max_amount']:.2f}
        Min total: {norm_result['min_total']:.2f} Max total: {norm_result['max_total']:.2f}       |     Min total: {reversed_result['min_total']:.2f} Max total: {reversed_result['max_total']:.2f}
        Deals: {norm_result['deals_count']}                                    |     Deals: {reversed_result['deals_count']}
        From: {norm_result['from']} to: {norm_result['to']}      |     From: {reversed_result['from']} to: {reversed_result['to']} 
    '''
)

