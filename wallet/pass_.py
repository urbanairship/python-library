import logging

from wallet import common

logger = logging.getLogger('urbanairship')


class Pass(object):

    @classmethod
    def get_pass(cls, wallet, pass_id=None, pass_external_id=None):
        """Retrieve a pass.

        Args:
            wallet (obj): A wallet client object.
            pass_id (str): The pass ID of the pass you wish to retrieve.
            pass_external_id (str): The external ID of the pass you wish to
            retrieve.

        Returns:
            An ApplePass or GooglePass object.

        Example:
            >>> my_pass = Pass.get_pass(pass_external_id=12345)
            <id:67890745, templateId:51010>
        """

        response = wallet.request(
            method='GET',
            body=None,
            url=Pass._build_url(pass_id, pass_external_id),
            version=1.2
        )
        payload = response.json()
        return payload

    @staticmethod
    def _build_url(pass_id=None, pass_external_id=None):
        if pass_id:
            return common.PASS_URL.format(pass_id)
        elif pass_external_id:
            return common.PASS_EXTERNAL_URL.format(pass_external_id)
        else:
            return common.PASS_URL  # will be used for listing passes
