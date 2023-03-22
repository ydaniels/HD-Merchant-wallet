from decimal import Decimal
import simplejson as json
import requests

class RatesNotAvailableError(Exception):
    """
    Custome Exception when https://theforexapi.com is Down and not available for currency rates
    """
    pass


class DecimalFloatMismatchError(Exception):
    """
    A float has been supplied when force_decimal was set to True
    """
    pass

class BitPayConverter(object):
    
    def _get_rate(self, base_currency, currency):
        url = f"https://bitpay.com/rates/{base_currency.upper()}"
        headers = {'Content-Type': 'application/json', 'X-Accept-Version': '2.0.0'}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json().get('data', {})
            data_rate = { data[i]['code'].lower(): data[i]['rate'] for i in range(0, len(data)) }
            price = data_rate.get(currency.lower(), None)
            return price
        raise RatesNotAvailableError("BitCoin Rates not available")
    
    def convert_to_btc(self, amount, currency):
        """
        Convert X amount to Bit Coins
        """
        if isinstance(amount, Decimal):
            use_decimal = True
        else:
            use_decimal = False

        price = self._get_rate('BTC', currency)
        if price:
            if use_decimal:
                price = Decimal(price)
            try:
                converted_btc = amount/price
                return converted_btc
            except TypeError:
                raise DecimalFloatMismatchError("convert_to_btc requires amount parameter is of type Decimal when force_decimal=True")
        raise RatesNotAvailableError("BitCoin Rates not available")

    def convert_btc_to_cur(self, coins, currency):
        """
        Convert X bit coins to valid currency amount
        """
        if isinstance(coins, Decimal):
            use_decimal = True
        else:
            use_decimal = False

        price = self._get_rate('BTC', currency)
        if price:
            if use_decimal:
                price = Decimal(price)
            try:
                converted_amount = coins * price
                return converted_amount
            except TypeError:
                raise DecimalFloatMismatchError("convert_btc_to_cur requires coins parameter is of type Decimal when force_decimal=True")
        raise RatesNotAvailableError("BitCoin Rates Source Not Ready For Given date")
