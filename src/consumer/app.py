import pika, sys, os, time
from cpu_load_generator import load_all_cores

def main():

    credentials = pika.credentials.PlainCredentials("user", "password")

    connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq.rabbitmq.svc', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue',
                          durable=True)

    def callback(ch, method, properties, body):
        print(f' [x] Working for {body.decode()} seconds')
        load_all_cores(duration_s=int(body.decode()), target_load=0.1)
        time.sleep(int(body.decode()))
        print(' [x] Done')
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=5)
    channel.basic_consume(queue='task_queue',
                          on_message_callback=callback)

    channel.start_consuming()

main()

