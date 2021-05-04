import unittest
import json

from onestop.KafkaPublisher import KafkaPublisher
from unittest.mock import ANY, patch, MagicMock
from confluent_kafka.schema_registry import SchemaRegistryClient

class KafkaPublisherTest(unittest.TestCase):
    kp = None
    conf_w_security = None
    conf_wo_security = None

    @classmethod
    def setUp(cls):
        print("Set it up!")
        cls.conf_w_security = {
            "metadata_type" : "GRANULE",
            "brokers" : "onestop-dev-cp-kafka:9092",
            "schema_registry" : "http://onestop-dev-cp-schema-registry:8081",
            "security" : {
                "enabled" : True,
                "caLoc" : "/etc/pki/tls/cert.pem",
                "keyLoc" : "/etc/pki/tls/private/kafka-user.key",
                "certLoc" : "/etc/pki/tls/certs/kafka-user.crt"
            },
            "collection_topic_publish" : "psi-collection-input-unknown",
            "granule_topic_publish" : "psi-granule-input-unknown",
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
        publisher = KafkaPublisher(**self.conf_w_security)

        self.assertEqual(publisher.metadata_type, self.conf_w_security['metadata_type'])
        self.assertEqual(publisher.brokers, self.conf_w_security['brokers'])
        self.assertEqual(publisher.schema_registry, self.conf_w_security['schema_registry'])
        self.assertEqual(publisher.security_enabled, self.conf_w_security['security']['enabled'])
        self.assertEqual(publisher.collection_topic, self.conf_w_security['collection_topic_publish'])
        self.assertEqual(publisher.granule_topic, self.conf_w_security['granule_topic_publish'])

    def test_init_security_enabled(self):
        publisher = KafkaPublisher(**self.conf_w_security)

        self.assertEqual(publisher.security_caLoc, self.conf_w_security['security']['caLoc'])
        self.assertEqual(publisher.security_keyLoc, self.conf_w_security['security']['keyLoc'])
        self.assertEqual(publisher.security_certLoc, self.conf_w_security['security']['certLoc'])

    def test_init_security_disabled(self):
        publisher = KafkaPublisher(**self.conf_wo_security)

        self.assertRaises(AttributeError, getattr, publisher, "security_caLoc")
        self.assertRaises(AttributeError, getattr, publisher, "security_keyLoc")
        self.assertRaises(AttributeError, getattr, publisher, "security_certLoc")

    def test_init_metadata_type_valid(self):
        publisher = KafkaPublisher(**self.conf_w_security)

        self.assertEqual(publisher.metadata_type, self.conf_w_security['metadata_type'])

    def test_init_metadata_type_invalid(self):
        wrong_metadata_type_config = dict(self.conf_w_security)
        wrong_metadata_type_config['metadata_type'] = "invalid_type"

        self.assertRaises(ValueError, KafkaPublisher, **wrong_metadata_type_config)

    def test_init_extra_params(self):
        conf = dict(self.conf_wo_security)
        conf['junk_key'] = 'junk_value'
        KafkaPublisher(**conf)

    @patch.object(SchemaRegistryClient, '__init__', autospec=True)
    def test_register_client_w_security(self, mock_client):
        exp_security_conf = {
            'url':self.conf_w_security['schema_registry'],
            'ssl.ca.location': self.conf_w_security['security']['caLoc'],
            'ssl.key.location': self.conf_w_security['security']['keyLoc'],
            'ssl.certificate.location': self.conf_w_security['security']['certLoc']
        }
        mock_client.return_value = None

        publisher = KafkaPublisher(**self.conf_w_security)
        publisher.register_client()

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

        publisher = KafkaPublisher(**self.conf_wo_security)
        publisher.register_client()
        try:
            mock_client.assert_called_with(ANY, exp_security_conf)
        except:
            return
        raise AssertionError('Expected register_client() to not have been called with security arguments.')

    @patch('onestop.KafkaPublisher.AvroSerializer')
    @patch('onestop.KafkaPublisher.SerializingProducer')
    def test_create_producer_calls_AvroSerializer(self, mock_serializing_publisher, mock_avro_serializer):
        conf_w_security_collection = dict(self.conf_w_security)
        conf_w_security_collection['metadata_type'] = "COLLECTION"

        publisher = KafkaPublisher(**conf_w_security_collection)
        reg_client = publisher.register_client()
        reg_client.get_latest_version = MagicMock()
        publisher.create_producer(reg_client)

        # Verify AvroSerializer called with expected registry client
        mock_avro_serializer.assert_called_with(ANY, reg_client)

    @patch('onestop.KafkaPublisher.AvroSerializer')
    @patch('onestop.KafkaPublisher.SerializingProducer')
    def test_create_producer_collection_w_security(self, mock_serializing_producer, mock_avro_serializer):
        conf_w_security_collection = dict(self.conf_w_security)
        topic = conf_w_security_collection['collection_topic_publish']
        conf_w_security_collection['metadata_type'] = 'COLLECTION'

        publisher = KafkaPublisher(**conf_w_security_collection)
        reg_client = MagicMock()
        prod = publisher.create_producer(reg_client)

        # Verify metadata type was taken into consideration for getting topic information
        reg_client.get_latest_version.assert_called_with(topic + '-value')

        # Verify security passed into SerializingProducer
        mock_serializing_producer.assert_called_with(
            {
                'bootstrap.servers': conf_w_security_collection['brokers'],
                'security.protocol': 'SSL',
                'ssl.ca.location': conf_w_security_collection['security']['caLoc'],
                'ssl.key.location': conf_w_security_collection['security']['keyLoc'],
                'ssl.certificate.location': conf_w_security_collection['security']['certLoc'],
                'value.serializer': ANY,
            })

        self.assertIsNotNone(prod)

    @patch('onestop.KafkaPublisher.AvroSerializer')
    @patch('onestop.KafkaPublisher.SerializingProducer')
    def test_create_producer_collection_wo_security(self, mock_serializing_producer, mock_avro_serializer):
        conf_wo_security_collection = dict(self.conf_wo_security)
        topic = conf_wo_security_collection['collection_topic_publish']
        conf_wo_security_collection['metadata_type'] = 'COLLECTION'

        publisher = KafkaPublisher(**conf_wo_security_collection)
        reg_client = MagicMock()
        prod = publisher.create_producer(reg_client)

        # Verify metadata type was taken into consideration for getting topic information
        reg_client.get_latest_version.assert_called_with(topic + '-value')

        # Verify no security passed into SerializingProducer
        mock_serializing_producer.assert_called_with(
            {
                'bootstrap.servers': conf_wo_security_collection['brokers'],
                'value.serializer': ANY,
            })

        self.assertIsNotNone(prod)

    @patch('onestop.KafkaPublisher.AvroSerializer')
    @patch('onestop.KafkaPublisher.SerializingProducer')
    def test_create_producer_granule_w_security(self, mock_serializing_producer, mock_avro_serializer):
        conf_w_security_granule = dict(self.conf_w_security)
        topic = conf_w_security_granule['granule_topic_publish']
        conf_w_security_granule['metadata_type'] = 'GRANULE'

        publisher = KafkaPublisher(**conf_w_security_granule)
        reg_client = MagicMock()
        prod = publisher.create_producer(reg_client)

        # Verify metadata type was taken into consideration for getting topic information
        reg_client.get_latest_version.assert_called_with(topic + '-value')

        # Verify security passed into SerializingProducer
        mock_serializing_producer.assert_called_with(
            {
                'bootstrap.servers': conf_w_security_granule['brokers'],
                'security.protocol': 'SSL',
                'ssl.ca.location': conf_w_security_granule['security']['caLoc'],
                'ssl.key.location': conf_w_security_granule['security']['keyLoc'],
                'ssl.certificate.location': conf_w_security_granule['security']['certLoc'],
                'value.serializer': ANY,
            })

        self.assertIsNotNone(prod)

    @patch('onestop.KafkaPublisher.AvroSerializer')
    @patch('onestop.KafkaPublisher.SerializingProducer')
    def test_create_producer_granule_wo_security(self, mock_serializing_producer, mock_avro_serializer):
        conf_wo_security_granule = dict(self.conf_wo_security)
        exp_topic = conf_wo_security_granule['granule_topic_publish']
        conf_wo_security_granule['metadata_type'] = 'GRANULE'

        publisher = KafkaPublisher(**conf_wo_security_granule)
        reg_client = MagicMock()
        prod = publisher.create_producer(reg_client)

        # Verify metadata type was taken into consideration for getting topic information
        reg_client.get_latest_version.assert_called_with(exp_topic + '-value')

        # Verify no security passed into SerializingProducer called with expected configuration
        mock_serializing_producer.assert_called_with(
            {
                'bootstrap.servers': conf_wo_security_granule['brokers'],
                'value.serializer': ANY,
            })

        self.assertIsNotNone(prod)

    def test_connect(self):
        mock_client = MagicMock()

        publisher = KafkaPublisher(**self.conf_w_security)
        publisher.register_client = MagicMock(return_value=mock_client)
        publisher.create_producer = MagicMock(return_value=MagicMock(mock_client))
        publisher.connect()

        publisher.register_client.assert_called_once()
        publisher.create_producer.assert_called_with(mock_client)

    def test_get_collection_key_from_uuid(self):
        expKey = '12345678-1234-5678-1234-567812345678'
        for uuid in [
            '{12345678-1234-5678-1234-567812345678}',
            '12345678123456781234567812345678',
            'urn:uuid:12345678-1234-5678-1234-567812345678',
            b'\x12\x34\x56\x78'*4,
#            b'\x78\x56\x34\x12\x34\x12\x78\x56' + b'\x12\x34\x56\x78\x12\x34\x56\x78',
#            {0x12345678, 0x1234, 0x5678, 0x12, 0x34, 0x567812345678},
#            0x12345678123456781234567812345678,
        ]:
            with self.subTest(uuid=uuid):
                print ("Testing uuid "+str(uuid))
                key = KafkaPublisher.get_collection_key_from_uuid(uuid)
                print("Acquired uuid="+str(key))
                self.assertEqual(key, expKey)

    @patch('onestop.KafkaPublisher.SerializingProducer')
    def test_publish_collection(self, mock_collection_producer):
        uuid = '{12345678-1234-5678-1234-567812345678}'
        content_dict = {
            'title': 'this is a test',
            'location': 'somewhere in space'
        }
        method = 'PUT'
        publisher = KafkaPublisher(**self.conf_w_security)
        publisher.register_client = MagicMock(return_value=MagicMock())
        mock_collection_producer.produce = MagicMock()
        mock_collection_producer.poll.side_effect = [1]

        publisher.publish_collection(mock_collection_producer, uuid, content_dict, method)

        # Verify kafka produce called once
        mock_collection_producer.produce.assert_called_with(
            topic=self.conf_w_security['collection_topic_publish'],
            value={
                'type': 'collection',
                'content': json.dumps(content_dict),
                'contentType': 'application/json',
                'method': method,
                'source': 'unknown',
            },
            key=publisher.get_collection_key_from_uuid(uuid),
            on_delivery=publisher.delivery_report
        )

        # Verify kafka produce poll called once
        mock_collection_producer.poll.assert_called_once()


    @patch('onestop.KafkaPublisher.SerializingProducer')
    def test_publish_granule(self, mock_collection_producer):
        uuid = '{12345678-1234-5678-1234-567812345678}'
        content_dict = {
            'title': 'this is a test',
            'location': 'somewhere in space',
            'relationships': [{"type": "COLLECTION",
                               "id": '{12345678-1234-5678-1234-567812345678}'}],
            'errors': [],
            'analysis': 'No analysis',
            'fileLocations': 'archived',
            'fileInformation': 'no information',
            'discovery': 'AWS'
        }
        publisher = KafkaPublisher(**self.conf_w_security)
        publisher.register_client = MagicMock(return_value=MagicMock())
        mock_collection_producer.produce = MagicMock()
        mock_collection_producer.poll.side_effect = [1]

        publisher.publish_granule(mock_collection_producer, uuid, content_dict)

        # Verify kafka produce called once
        mock_collection_producer.produce.assert_called_with(
            topic=self.conf_w_security['granule_topic_publish'],
            value={
                'type': 'granule',
                'content': json.dumps(content_dict),
                #'contentType': 'application/json',
                'method': 'PUT',
                'source': 'unknown',
                'operation': None,
                'relationships': content_dict['relationships'],
                'errors': content_dict['errors'],
                'analysis': content_dict['analysis'],
                'fileLocations': {'fileLocation': content_dict['fileLocations']},
                'fileInformation': content_dict['fileInformation'],
                'discovery': content_dict['discovery']
            },
            key=publisher.get_collection_key_from_uuid(uuid),
            on_delivery=publisher.delivery_report
        )

        # Verify kafka produce poll called once
        mock_collection_producer.poll.assert_called_once()

if __name__ == '__main__':
    unittest.main()