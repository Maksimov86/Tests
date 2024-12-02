import argparse
from confluent_kafka import Producer, Consumer, KafkaError


def produce_message(kafka_server, topic, message):
    producer = Producer({'bootstrap.servers': kafka_server})
    producer.produce(topic, message)
    producer.flush()
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
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break
            print(f"Received message: {msg.value().decode('utf-8')}")
    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        consumer.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka Producer and Consumer")
    subparsers = parser.add_subparsers(dest="command")

    # Producer command
    produce_parser = subparsers.add_parser('produce')
    produce_parser.add_argument('--message', required=True, help='Message to send')
    produce_parser.add_argument('--topic', required=True, help='Kafka topic')
    produce_parser.add_argument('--kafka', required=True, help='Kafka server address')

    # Consumer command
    consume_parser = subparsers.add_parser('consume')
    consume_parser.add_argument('--topic', required=True, help='Kafka topic')
    consume_parser.add_argument('--kafka', required=True, help='Kafka server address')

    args = parser.parse_args()

    if args.command == 'produce':
        produce_message(args.kafka, args.topic, args.message)
    elif args.command == 'consume':
        consume_messages(args.kafka, args.topic)
    else:
        parser.print_help()
