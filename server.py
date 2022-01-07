import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='regis_ord')

def on_res(ch, method, properties, body):
    body = body.decode()
    print(f'Checking {body}')
    time.sleep(2)
    res = body + " accepted."
    ch.basic_publish(exchange='', routing_key=properties.reply_to, body=res,
                     properties=pika.BasicProperties(correlation_id=properties.correlation_id))


channel.basic_consume(queue='regis_ord', on_message_callback=on_res, auto_ack=True)
print("Waiting for response ...")
channel.start_consuming()
