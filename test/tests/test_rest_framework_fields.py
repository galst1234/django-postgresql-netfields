from __future__ import absolute_import, unicode_literals

from rest_framework import serializers

import unittest2 as unittest
from netfields import rest_framework as fields
from netfields.address_families import IPV4_FAMILY, IPV6_FAMILY


class FieldsTestCase(unittest.TestCase):
    def test_validation_inet_field(self):

        class TestSerializer(serializers.Serializer):
            ip = fields.InetAddressField()

        address = '10.0.0.'
        serializer = TestSerializer(data={'ip': address})
        with self.assertRaises(serializers.ValidationError) as e:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(e.exception.detail['ip'],
                         ["Invalid IP address."])

    def test_validation_inet_ipv4_field(self):

        class TestSerializer(serializers.Serializer):
            ip = fields.InetAddressField(address_family=IPV4_FAMILY)

        address = '6c5b:de87:7a15:5eba:67b5:69ae:f454:ce1'
        serializer = TestSerializer(data={'ip': address})
        with self.assertRaises(serializers.ValidationError) as e:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(e.exception.detail['ip'],
                         ["Invalid {} address.".format(IPV4_FAMILY)])

    def test_validation_inet_ipv6_field(self):

        class TestSerializer(serializers.Serializer):
            ip = fields.InetAddressField(address_family=IPV6_FAMILY)

        address = '1.2.3.4'
        serializer = TestSerializer(data={'ip': address})
        with self.assertRaises(serializers.ValidationError) as e:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(e.exception.detail['ip'],
                         ["Invalid {} address.".format(IPV6_FAMILY)])

    def test_validation_cidr_field(self):

        class TestSerializer(serializers.Serializer):
            cidr = fields.CidrAddressField()

        address = '10.0.0.'
        serializer = TestSerializer(data={'cidr': address})
        with self.assertRaises(serializers.ValidationError) as e:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(e.exception.detail['cidr'],
                         ["Invalid CIDR address."])

    def test_validation_cidr_ipv4_field(self):

        class TestSerializer(serializers.Serializer):
            cidr = fields.CidrAddressField(address_family=IPV4_FAMILY)

        address = '2001:db8::/32'
        serializer = TestSerializer(data={'cidr': address})
        with self.assertRaises(serializers.ValidationError) as e:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(e.exception.detail['cidr'],
                         ["Invalid {} CIDR address.".format(IPV4_FAMILY)])

    def test_validation_cidr_ipv6_field(self):

        class TestSerializer(serializers.Serializer):
            cidr = fields.CidrAddressField(address_family=IPV6_FAMILY)

        address = '10.0.0.0/24'
        serializer = TestSerializer(data={'cidr': address})
        with self.assertRaises(serializers.ValidationError) as e:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(e.exception.detail['cidr'],
                         ["Invalid {} CIDR address.".format(IPV6_FAMILY)])

    def test_network_validation_cidr_field(self):

        class TestSerializer(serializers.Serializer):
            cidr = fields.CidrAddressField()

        address = '10.0.0.1/24'
        serializer = TestSerializer(data={'cidr': address})
        with self.assertRaises(serializers.ValidationError) as e:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(e.exception.detail['cidr'],
                         ["Must be a network address."])

    def test_validation_mac_field(self):

        class TestSerializer(serializers.Serializer):
            mac = fields.MACAddressField()

        for invalid_address in ("de:", {"not": "a mac"}):
            with self.subTest(invalid_address=invalid_address):
                serializer = TestSerializer(data={'mac': invalid_address})
                with self.assertRaises(serializers.ValidationError) as e:
                    serializer.is_valid(raise_exception=True)
                self.assertEqual(e.exception.detail['mac'], ["Invalid MAC address."])

    def test_inet_validation_additional_validators(self):
        def validate(value):
            raise serializers.ValidationError('Invalid.')

        class TestSerializer(serializers.Serializer):
            ip = fields.InetAddressField(validators=[validate])

        address = '1.2.3.4/24'
        serializer = TestSerializer(data={'ip': address})
        with self.assertRaises(serializers.ValidationError) as e:
            serializer.is_valid(raise_exception=True)
        self.assertItemsEqual(e.exception.detail['ip'], ['Invalid.'])

    def test_cidr_validation_additional_validators(self):
        def validate(value):
            raise serializers.ValidationError('Invalid.')

        class TestSerializer(serializers.Serializer):
            ip = fields.CidrAddressField(validators=[validate])

        address = '1.2.3.0/24'
        serializer = TestSerializer(data={'ip': address})
        with self.assertRaises(serializers.ValidationError) as e:
            serializer.is_valid(raise_exception=True)
        self.assertItemsEqual(e.exception.detail['ip'], ['Invalid.'])

    def test_mac_validation_additional_validators(self):
        def validate(value):
            raise serializers.ValidationError('Invalid.')

        class TestSerializer(serializers.Serializer):
            ip = fields.MACAddressField(validators=[validate])

        address = '01:23:45:67:89:ab'
        serializer = TestSerializer(data={'ip': address})
        with self.assertRaises(serializers.ValidationError) as e:
            serializer.is_valid(raise_exception=True)
        self.assertItemsEqual(e.exception.detail['ip'], ['Invalid.'])
