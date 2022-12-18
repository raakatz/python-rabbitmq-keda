import pika
import random

task_length = [1, 2, 3, 4, 5]

credentials = pika.credentials.PlainCredentials("user", "password")

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))

channel = connection.channel()

channel.queue_declare(queue='task_queue',
                      durable=True)

for i in range(50):
    message = random.choice(task_length)
    channel.basic_publish(exchange='',
                          routing_key='task_queue',
                          body=str(message),
                          properties=pika.BasicProperties(
                              delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

connection.close()
