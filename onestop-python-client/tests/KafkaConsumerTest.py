import unittest

from unittest.mock import ANY, patch, MagicMock, call
from onestop.KafkaConsumer import KafkaConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient

class KafkaConsumerTest(unittest.TestCase):
    kp = None
    conf_w_security = None
    conf_wo_security = None

    @classmethod
    def setUp(cls):
        print("Set it up!")
        cls.conf_w_security = {
            "metadata_type" : "GRANULE",
            "brokers" : "onestop-dev-cp-kafka:9092",
            "group_id" : "sme-test",
            "auto_offset_reset" : "earliest",
            "schema_registry" : "http://onestop-dev-cp-schema-registry:8081",
            "security" : {
                "enabled" : True,
                "caLoc" : "/etc/pki/tls/cert.pem",
                "keyLoc" : "/etc/pki/tls/private/kafka-user.key",
                "certLoc" : "/etc/pki/tls/certs/kafka-user.crt"
            },
            "collection_topic_consume" : "psi-collection-input-unknown",
            "granule_topic_consume" : "psi-granule-input-unknown",
            "log_level" : "DEBUG"
        }
        cls.conf_wo_security = dict(cls.conf_w_security)
        # Remove security credential section.
        cls.conf_wo_security['security'] = {
            "enabled":False
        }

    @classmethod
    def tearDown(self):
        print("Tear it down!")

    def test_init_happy_nonconditional_params(self):
        consumer = KafkaConsumer(**self.conf_w_security)

        self.assertEqual(consumer.metadata_type, self.conf_w_security['metadata_type'])
        self.assertEqual(consumer.brokers, self.conf_w_security['brokers'])
        self.assertEqual(consumer.group_id, self.conf_w_security['group_id'])
        self.assertEqual(consumer.auto_offset_reset, self.conf_w_security['auto_offset_reset'])
        self.assertEqual(consumer.schema_registry, self.conf_w_security['schema_registry'])
        self.assertEqual(consumer.security_enabled, self.conf_w_security['security']['enabled'])
        self.assertEqual(consumer.collection_topic, self.conf_w_security['collection_topic_consume'])
        self.assertEqual(consumer.granule_topic, self.conf_w_security['granule_topic_consume'])

    def test_init_security_enabled(self):
        consumer = KafkaConsumer(**self.conf_w_security)

        self.assertEqual(consumer.security_caLoc, self.conf_w_security['security']['caLoc'])
        self.assertEqual(consumer.security_keyLoc, self.conf_w_security['security']['keyLoc'])
        self.assertEqual(consumer.security_certLoc, self.conf_w_security['security']['certLoc'])

    def test_init_security_disabled(self):
        consumer = KafkaConsumer(**self.conf_wo_security)

        self.assertRaises(AttributeError, getattr, consumer, "security_caLoc")
        self.assertRaises(AttributeError, getattr, consumer, "security_keyLoc")
        self.assertRaises(AttributeError, getattr, consumer, "security_certLoc")

    def test_init_metadata_type_valid(self):
        consumer = KafkaConsumer(**self.conf_w_security)

        self.assertEqual(consumer.metadata_type, self.conf_w_security['metadata_type'])

    def test_init_metadata_type_invalid(self):
        wrong_metadata_type_config = dict(self.conf_w_security)
        wrong_metadata_type_config['metadata_type'] = "invalid_type"

        self.assertRaises(ValueError, KafkaConsumer, **wrong_metadata_type_config)

    def test_init_extra_params(self):
        conf = dict(self.conf_wo_security)
        conf['junk_key'] = 'junk_value'
        KafkaConsumer(**conf)

    @patch.object(SchemaRegistryClient, '__init__', autospec=True)
    def test_register_client_w_security(self, mock_client):
        exp_security_conf = {
            'url':self.conf_w_security['schema_registry'],
            'ssl.ca.location': self.conf_w_security['security']['caLoc'],
            'ssl.key.location': self.conf_w_security['security']['keyLoc'],
            'ssl.certificate.location': self.conf_w_security['security']['certLoc']
        }
        mock_client.return_value = None

        consumer = KafkaConsumer(**self.conf_w_security)
        consumer.register_client()

        mock_client.assert_called()
        mock_client.assert_called_with(ANY, exp_security_conf)

    @patch.object(SchemaRegistryClient, '__init__', autospec=True)
    def test_register_client_wo_security(self, mock_client):
        exp_security_conf = {
            'url':self.conf_w_security['schema_registry'],
            'ssl.ca.location': self.conf_w_security['security']['caLoc'],
            'ssl.key.location': self.conf_w_security['security']['keyLoc'],
            'ssl.certificate.location': self.conf_w_security['security']['certLoc']
        }
        mock_client.return_value = None

        consumer = KafkaConsumer(**self.conf_wo_security)
        consumer.register_client()
        try:
            mock_client.assert_called_with(ANY, exp_security_conf)
        except:
            return
        raise AssertionError('Expected register_client() to not have been called with security arguments.')

    @patch('onestop.KafkaConsumer.AvroDeserializer')
    @patch('onestop.KafkaConsumer.DeserializingConsumer')
    def test_create_consumer_calls_AvroDeserializer(self, mock_deserializing_consumer, mock_avro_deserializer):
        conf_w_security_collection = dict(self.conf_w_security)
        conf_w_security_collection['metadata_type'] = "COLLECTION"

        consumer = KafkaConsumer(**conf_w_security_collection)
        reg_client = consumer.register_client()
        reg_client.get_latest_version = MagicMock()
        deser_consumer = consumer.create_consumer(reg_client)

        # Verify AvroDeserializer called with expected registry client
        mock_avro_deserializer.assert_called_with(ANY, reg_client)

        self.assertIsNotNone(deser_consumer)

    @patch('onestop.KafkaConsumer.AvroDeserializer')
    @patch('onestop.KafkaConsumer.DeserializingConsumer')
    def test_create_consumer_collection_w_security(self, mock_deserializing_consumer, mock_avro_deserializer):
        conf_w_security_collection = dict(self.conf_w_security)
        topic = conf_w_security_collection['collection_topic_consume']
        conf_w_security_collection['metadata_type'] = 'COLLECTION'

        consumer = KafkaConsumer(**conf_w_security_collection)
        reg_client = MagicMock()
        deser_consumer = consumer.create_consumer(reg_client)

        # Verify metadata type was taken into consideration for getting topic information
        reg_client.get_latest_version.assert_called_with(topic + '-value')

        # Verify security passed into DeserializingConsumer
        mock_deserializing_consumer.assert_called_with(
            {
                'bootstrap.servers': conf_w_security_collection['brokers'],
                'security.protocol': 'SSL',
                'ssl.ca.location': conf_w_security_collection['security']['caLoc'],
                'ssl.key.location': conf_w_security_collection['security']['keyLoc'],
                'ssl.certificate.location': conf_w_security_collection['security']['certLoc'],
                'key.deserializer': ANY,
                'value.deserializer': ANY,
                'group.id': conf_w_security_collection['group_id'],
                'auto.offset.reset': conf_w_security_collection['auto_offset_reset']
            })
        mock_deserializing_consumer.return_value.subscribe.assert_called_with([topic])

        self.assertIsNotNone(deser_consumer)

    @patch('onestop.KafkaConsumer.AvroDeserializer')
    @patch('onestop.KafkaConsumer.DeserializingConsumer')
    def test_create_consumer_collection_wo_security(self, mock_deserializing_consumer, mock_avro_deserializer):
        conf_wo_security_collection = dict(self.conf_wo_security)
        topic = conf_wo_security_collection['collection_topic_consume']
        conf_wo_security_collection['metadata_type'] = 'COLLECTION'

        consumer = KafkaConsumer(**conf_wo_security_collection)
        reg_client = MagicMock()
        deser_consumer = consumer.create_consumer(reg_client)

        # Verify metadata type was taken into consideration for getting topic information
        reg_client.get_latest_version.assert_called_with(topic + '-value')

        # Verify no security passed into DeserializingConsumer
        mock_deserializing_consumer.assert_called_with(
            {
                'bootstrap.servers': conf_wo_security_collection['brokers'],
                'key.deserializer': ANY,
                'value.deserializer': ANY,
                'group.id': conf_wo_security_collection['group_id'],
                'auto.offset.reset': conf_wo_security_collection['auto_offset_reset']
            })
        mock_deserializing_consumer.return_value.subscribe.assert_called_with([topic])

        self.assertIsNotNone(deser_consumer)

    @patch('onestop.KafkaConsumer.AvroDeserializer')
    @patch('onestop.KafkaConsumer.DeserializingConsumer')
    def test_create_consumer_granule_w_security(self, mock_deserializing_consumer, mock_avro_deserializer):
        conf_w_security_granule = dict(self.conf_w_security)
        topic = conf_w_security_granule['granule_topic_consume']
        conf_w_security_granule['metadata_type'] = 'GRANULE'

        consumer = KafkaConsumer(**conf_w_security_granule)
        reg_client = MagicMock()
        deser_consumer = consumer.create_consumer(reg_client)

        # Verify metadata type was taken into consideration for getting topic information
        reg_client.get_latest_version.assert_called_with(topic + '-value')

        # Verify security passed into DeserializingConsumer
        mock_deserializing_consumer.assert_called_with(
            {
                'bootstrap.servers': conf_w_security_granule['brokers'],
                'security.protocol': 'SSL',
                'ssl.ca.location': conf_w_security_granule['security']['caLoc'],
                'ssl.key.location': conf_w_security_granule['security']['keyLoc'],
                'ssl.certificate.location': conf_w_security_granule['security']['certLoc'],
                'key.deserializer': ANY,
                'value.deserializer': ANY,
                'group.id': conf_w_security_granule['group_id'],
                'auto.offset.reset': conf_w_security_granule['auto_offset_reset']
            })
        mock_deserializing_consumer.return_value.subscribe.assert_called_with([topic])

        self.assertIsNotNone(deser_consumer)

    @patch('onestop.KafkaConsumer.AvroDeserializer')
    @patch('onestop.KafkaConsumer.DeserializingConsumer')
    def test_create_consumer_granule_wo_security(self, mock_deserializing_consumer, mock_avro_deserializer):
        conf_wo_security_granule = dict(self.conf_wo_security)
        exp_topic = conf_wo_security_granule['granule_topic_consume']
        conf_wo_security_granule['metadata_type'] = 'GRANULE'

        consumer = KafkaConsumer(**conf_wo_security_granule)
        reg_client = MagicMock()
        deser_consumer = consumer.create_consumer(reg_client)

        # Verify metadata type was taken into consideration for getting topic information
        reg_client.get_latest_version.assert_called_with(exp_topic + '-value')

        # Verify no security passed into DeserializingConsumer called with expected configuration
        mock_deserializing_consumer.assert_called_with(
            {
                'bootstrap.servers': conf_wo_security_granule['brokers'],
                'key.deserializer': ANY,
                'value.deserializer': ANY,
                'group.id': conf_wo_security_granule['group_id'],
                'auto.offset.reset': conf_wo_security_granule['auto_offset_reset']
            })
        mock_deserializing_consumer.return_value.subscribe.assert_called_with([exp_topic])

        self.assertIsNotNone(deser_consumer)

    def test_connect(self):
        mock_client = MagicMock()

        consumer = KafkaConsumer(**self.conf_w_security)
        consumer.register_client = MagicMock(return_value=mock_client)
        consumer.create_consumer = MagicMock(return_value=MagicMock(mock_client))
        consumer.connect()

        consumer.register_client.assert_called_once()
        consumer.create_consumer.assert_called_with(mock_client)

    @patch('confluent_kafka.cimpl.Message')
    @patch('onestop.KafkaConsumer.DeserializingConsumer')
    def test_consume(self, mock_metadata_consumer, mock_message):
        mock_message_key = 'key1'
        mock_message_value = 'value1'
        consumer = KafkaConsumer(**self.conf_w_security)
        consumer.register_client = MagicMock(return_value=MagicMock())
        mock_message.key.return_value = mock_message_key
        mock_message.value.return_value = mock_message_value
        mock_metadata_consumer.poll.side_effect = [None, mock_message, Exception]
        mock_handler = MagicMock()

        # Would have liked not having the try/catch but it wasn't ignoring the exception. Just need to not fail due to end of loop.
        try:
            self.assertRaises(Exception, consumer.consume(mock_metadata_consumer, mock_handler))
        except Exception as e:
            print("Ignoring exception: {}".format(e))

        # Verify kafka consumer poll called expected number of times
        self.assertEqual(mock_metadata_consumer.poll.call_count, 3)
        mock_metadata_consumer.poll.assert_has_calls([call(10), call(10), call(10)])

        # Verify callback function was called once with expected message attributes
        mock_handler.assert_called_once()
        mock_handler.assert_called_with(mock_message_key, mock_message_value)

if __name__ == '__main__':
    unittest.main()