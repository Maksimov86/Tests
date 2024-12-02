import argparse
from confluent_kafka import Producer, Consumer, KafkaError


def produce_message(kafka_server, topic, message):
    producer = Producer({'bootstrap.servers': kafka_server})
    producer.produce(topic, message)
    producer.flush()  # Ждёт завершения отправки всех сообщений
    print(f"Produced message to topic {topic}: {message}")


def consume_messages(kafka_server, topic):
    consumer = Consumer({
        'bootstrap.servers': kafka_server,
        'group.id': 'python-consumer',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    print(f"Subscribed to topic {topic}. Waiting for messages...")
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg and not msg.error():
                print(f"Received message: {msg.value().decode('utf-8')}")
            elif msg and msg.error().code() != KafkaError._PARTITION_EOF:
                print(msg.error())
                break
    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        consumer.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka Producer and Consumer")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for cmd, args in {
        "produce": [("--message", True, "Message to send"), ("--topic", True, "Kafka topic"), ("--kafka", True, "Kafka server address")],
        "consume": [("--topic", True, "Kafka topic"), ("--kafka", True, "Kafka server address")],
    }.items():
        sp = subparsers.add_parser(cmd)
        for arg, req, desc in args:
            sp.add_argument(arg, required=req, help=desc)

    args = parser.parse_args()
    func = {"produce": produce_message, "consume": consume_messages}.get(args.command)
    func(args.kafka, args.topic, getattr(args, "message", None))
