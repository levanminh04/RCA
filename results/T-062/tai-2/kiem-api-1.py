events=api('GET','/api/v1/events')
print(json.dumps({'eventList':events}))
event=api('GET','/api/v1/events/1c936e96-a861-419b-a42e-17775bd642a7')
orders=api('GET','/api/v1/orders','BUYER')
print(json.dumps({'orders':orders}))
if isinstance(orders,dict):
    entries=orders.get('content',orders.get('items',orders.get('orders',[])))
else:
    entries=orders
for order in entries[:3]:
    oid=order['orderId']
    api('GET',f'/api/v1/orders/{oid}','BUYER')
    api('GET',f'/api/v1/orders/{oid}/payment','BUYER')
    api('GET',f'/api/v1/orders/{oid}/tickets','BUYER')
api('GET','/api/v1/payments/vnpay/ipn')
api('GET','/api/v1/payments/vnpay/return')
print(json.dumps({'requests':evidence}))
