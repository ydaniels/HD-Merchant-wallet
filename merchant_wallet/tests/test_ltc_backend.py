import unittest
import datetime
from merchant_wallet.backends.btc import (
    convert_from_satoshi,
    extract_latest_transaction,
    confirm_transaction_date_without_previous_hash,
    BitcoinBackend,
    get_address_details,
    get_transaction_details,
)



class TestGenericMerchantWallet(unittest.TestCase):
    def setUp(self):
        public_key = "zpub6ngHGoj9bYhcpcNisKTkhTKXw2ezUrTSSwxwQRSnqfVSzoS2B4SUzSSxBzhNodjwjGKNHgmiuU8AUXMjFQ1HgEFjVAJs8e7Qab2UkqcNrTo"
        self.backend = BitcoinBackend(public_key, "LTC")

    def test_satoshi_btc_convert(self):
        self.assertEqual(1, convert_from_satoshi(100000000))
        self.assertEqual(0.07877000, convert_from_satoshi(7877000))
        self.assertEqual(0.09065697, convert_from_satoshi(9065697))

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
            self.backend.generate_new_address(0, address_type='p2pkh'), "LKFs5jYUjFbALJJEESVbj4bYvJq41JdXcm"
        )
        self.assertEqual(
            self.backend.generate_new_address(1, address_type='p2pkh'), "LLRRrSkvYMEZxGk9qW9KFJpNzemHJkx8Uf"
        )

    def test_can_get_adddres_details(self):
        address = "ltc1qzqe3cegsrqzpc3emt04zcszd4gnga4l4rv6uhy"

        data = get_address_details(address, coin_symbol=self.backend.crypto_currency)

        self.assertEqual(data["address"], address)

    def test_convert_from_fiat(self):
        result = self.backend.convert_from_fiat(1, "USD")
        self.assertEqual(type(result), float)

    def test_convert_to_fiat(self):
        result = self.backend.convert_to_fiat(1, "USD")
        self.assertEqual(type(result), float)

    def test_get_transaction_details(self):
        hash_value = "beff54dbf22ca7af33aabd2d13a66f32c952b3e3db5b09ee78f32ff98f28623d"
        res = get_transaction_details(hash_value, self.backend.crypto_currency)
        print(res)
        self.assertEqual(res["hash"], hash_value)

    def test_confirm_address_payment(self):
        res, _ = self.backend.confirm_address_payment(
            "M9zVjzUgrDrEfAEtSSUPCqVe7uXCPKMspo", 0.01, confirmation_number=5000
        )
        self.assertEqual(res, self.backend.NO_HASH_ADDRESS_BALANCE)
        res, _ = self.backend.confirm_address_payment(
            "ltc1q2rrxp7fs87ttmh8g7cunjh6e56qkwr3k2eshqc",
            5.3,
            confirmation_number=18,
            accept_confirmed_bal_without_hash_mins=5256000,
        )
        self.assertEqual(res, self.backend.UNDERPAID_ADDRESS_BALANCE)
        res, _ = self.backend.confirm_address_payment(
            "ltc1q2rrxp7fs87ttmh8g7cunjh6e56qkwr3k2eshqc",
            5.1,
            confirmation_number=12,
            accept_confirmed_bal_without_hash_mins=5256000,
        )
        self.assertEqual(res, self.backend.CONFIRMED_ADDRESS_BALANCE)

    def test_confirm_address_payment_with_hash(self):

        res, _ = self.backend.confirm_address_payment(
            "ltc1q2rrxp7fs87ttmh8g7cunjh6e56qkwr3k2eshqc",
            0.00176959,
            tx_hash="c3705925f6c66acf08b55e064bb51893b7f8c07394c571baac5f8a47932fb301",
            confirmation_number=500000,
        )
        self.assertEqual(res, self.backend.UNCONFIRMED_ADDRESS_BALANCE)
        res, _ = self.backend.confirm_address_payment(
            "ltc1q2rrxp7fs87ttmh8g7cunjh6e56qkwr3k2eshqc",
            6.01176959,
            tx_hash="c3705925f6c66acf08b55e064bb51893b7f8c07394c571baac5f8a47932fb301",
            confirmation_number=2,
        )
        self.assertEqual(res, self.backend.UNDERPAID_ADDRESS_BALANCE)
        res, _ = self.backend.confirm_address_payment(
            "ltc1q2rrxp7fs87ttmh8g7cunjh6e56qkwr3k2eshqc",
            5.1,
            tx_hash="c3705925f6c66acf08b55e064bb51893b7f8c07394c571baac5f8a47932fb301",
            confirmation_number=5,
        )
        self.assertEqual(res, self.backend.CONFIRMED_ADDRESS_BALANCE)
