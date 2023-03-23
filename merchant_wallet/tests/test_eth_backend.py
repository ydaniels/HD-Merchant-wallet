import unittest
import datetime
from merchant_wallet.backends.eth import (
    convert_from_wei,
    extract_latest_transaction,
    confirm_transaction_date_without_previous_hash,
    EthereumBackend,
    get_address_details,
    get_transaction_details,
)


class TestMerchantWallet(unittest.TestCase):
    def setUp(self):
        public_key = "xpub6CyKZud8ucCgWNSbU1RPQpwL5kEWFDjmr2x8zFtL5VA7kwLGz7HzkuDYxg5DYBtQysKwFxTFr91xAtYd8L81HewwfKqe2aFqjoftm35RZBm"
        self.backend = EthereumBackend(public_key)

    def test_wei_eth_convert(self):
        self.assertEqual(1, convert_from_wei(1000000000000000000))
        self.assertEqual(0.07877000, convert_from_wei(78770000000000000))
        self.assertEqual(0.09065697, convert_from_wei(90656970000000000))

    def test_extract_latest_transaction_by_received_date(self):
        selected_transaction = {
            "received": datetime.datetime.now() + datetime.timedelta(days=5)
        }
        other_date = datetime.datetime.now() + datetime.timedelta(days=2)
        other_date_one = datetime.datetime.now() - datetime.timedelta(days=4)
        other_date_two = datetime.datetime.now() - datetime.timedelta(days=7)
        transactions = [
            {"received": datetime.datetime.now()},
            selected_transaction,
            {"received": other_date_one},
            {"received": other_date_two},
            {"received": other_date},
        ]

        self.assertEqual(selected_transaction, extract_latest_transaction(transactions))

    def test_confirm_transaction_date_without_previous_hash(self):
        selected_transaction = {
            "received": datetime.datetime.utcnow() - datetime.timedelta(days=1)
        }
        transaction = confirm_transaction_date_without_previous_hash(
            selected_transaction, 25 * 60
        )
        self.assertEqual(selected_transaction, transaction)
        transaction = confirm_transaction_date_without_previous_hash(
            selected_transaction, 60
        )
        self.assertIsNone(transaction)

    def test_generate_new_address(self):
        self.assertEqual(
            self.backend.generate_new_address(0).lower(), "0xAd6f048e89cCac509111b60a529962560F64e55E".lower()
        )
        self.assertEqual(
            self.backend.generate_new_address(1).lower(), "0x4bC2EAaCb9d266658438d4E0554b5304Eecfd5c4".lower()
        )

    def test_can_get_adddres_details(self):
        address = "0xAd6f048e89cCac509111b60a529962560F64e55E".lower()
        data = get_address_details(address)
        # print(data)
        self.assertEqual(data["address"], address)

    def test_convert_from_fiat(self):
        result = self.backend.convert_from_fiat(0.01, "USD")
        self.assertEqual(type(result), float)

    def test_convert_to_fiat(self):
        result = self.backend.convert_to_fiat(1, "EUR")
        self.assertEqual(type(result), float)

    def test_get_transaction_details(self):
        hash_value = "0bbe3720f05b8f8b354ec86f7d3c4f6fe415e40adfe2b8434003da28f27c2f53"
        res = get_transaction_details(hash_value)
        self.assertEqual(res["hash"], hash_value)

    def test_confirm_address_payment(self):
        res, _ = self.backend.confirm_address_payment(
            "0xAd6f048e89cCac509111b60a529962560F64e55E".lower(), 0.01, confirmation_number=5000
        )
        self.assertEqual(res, self.backend.NO_HASH_ADDRESS_BALANCE)
        res, _ = self.backend.confirm_address_payment(
            "0xb4262e8560f874ddb0a508fb5c13b5cdb673acee",
            0.1,
            confirmation_number=3,
            accept_confirmed_bal_without_hash_mins=5256000,
        )
        self.assertEqual(res, self.backend.UNDERPAID_ADDRESS_BALANCE)
        res, _ = self.backend.confirm_address_payment(
            "0xb4262e8560f874ddb0a508fb5c13b5cdb673acee",
            0.00545412,
            confirmation_number=3,
            accept_confirmed_bal_without_hash_mins=5256000,
        )
        self.assertEqual(res, self.backend.CONFIRMED_ADDRESS_BALANCE)

    def test_confirm_address_payment_with_hash(self):

        res, _ = self.backend.confirm_address_payment(
            "0xb4262e8560f874ddb0a508fb5c13b5cdb673acee".lower(),
            0.00545412,
            tx_hash="0bbe3720f05b8f8b354ec86f7d3c4f6fe415e40adfe2b8434003da28f27c2f53",
            confirmation_number=500000,
        )
        self.assertEqual(res, self.backend.UNCONFIRMED_ADDRESS_BALANCE)
        res, _ = self.backend.confirm_address_payment(
            "0xb4262e8560f874ddb0a508fb5c13b5cdb673acee",
            0.1,
            tx_hash="0bbe3720f05b8f8b354ec86f7d3c4f6fe415e40adfe2b8434003da28f27c2f53",
            confirmation_number=50,
        )
        self.assertEqual(res, self.backend.UNDERPAID_ADDRESS_BALANCE)
        res, _ = self.backend.confirm_address_payment(
            "0xb4262e8560f874ddb0a508fb5c13b5cdb673acee",
            0.00545412,
            tx_hash="0bbe3720f05b8f8b354ec86f7d3c4f6fe415e40adfe2b8434003da28f27c2f53",
            confirmation_number=50,
        )
        self.assertEqual(res, self.backend.CONFIRMED_ADDRESS_BALANCE)
