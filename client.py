import pika
import uuid


class Order:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        equeue = self.channel.queue_declare(queue='', exclusive=True)
        self.qname = equeue.method.queue
        self.channel.basic_consume(queue=self.qname, on_message_callback=self.on_res, auto_ack=True)

    def on_res(self, ch, method, properties, body):
        if self.correlation_id == properties.correlation_id:
            self.confirm = body.decode()

    def register_order(self, order_no):
        self.correlation_id = str(uuid.uuid4)
        self.confirm = None
        self.channel.basic_publish(exchange='', routing_key='regis_ord', body=order_no,
                                   properties=pika.BasicProperties(reply_to=self.qname,
                                                                   correlation_id=self.correlation_id))
        while (self.confirm == None):
            self.connection.process_data_events()
        return self.confirm


milad_order = Order()
result = milad_order.register_order("regux-5567")
print(result)
