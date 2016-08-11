import logging
import json

from wallet import common


logger = logging.getLogger('urbanairship')


def get_pass(wallet, pass_id=None, external_id=None):
    """Retrieve a pass.

    Args:
        wallet (obj): A wallet client object.
        pass_id (str): The pass ID of the pass you wish to retrieve.
        pass_external_id (str): The external ID of the pass you wish to
        retrieve.

    Returns:
        A pass object.

    Example:
        >>> my_pass = Pass.get_pass(pass_external_id=12345)
        <id:67890745, templateId:51010>
    """
    if not (pass_id or external_id) or (pass_id and external_id):
        raise ValueError('Please specify only one of pass_id or external_id.')

    response = wallet.request(
        method='GET',
        body=None,
        url=Pass.build_url(
            common.PASS_BASE_URL,
            main_id=pass_id,
            pass_external_id=external_id
        ),
        version=1.2
    )
    payload = response.json()
    return Pass.from_data(payload)


def delete_pass(wallet, pass_id=None, external_id=None):
    """Delete a pass.

    Arguments:
        wallet (obj): A UA Wallet object.
        pass_id (str or int): The ID of the pass you wish to delete.
        external_id (str or int): The external ID of the pass you wish
            to delete.

    Returns:
        A response object.

    Raises:
        ValueError: If neither, or both, of pass_id and external_id
            are specified.

    Example:
        >>> delete_pass(ua_wallet, pass_id='123456')
        <Response [200]>
    """
    if not (pass_id or external_id) or (pass_id and external_id):
        raise ValueError('Please specify only one of pass_id or external_id.')

    response = wallet.request(
        method='DELETE',
        body=None,
        url=Pass.build_url(
            common.PASS_BASE_URL,
            main_id=pass_id,
            pass_external_id=external_id
        ),
        version=1.2
    )
    logger.info('Successful pass deletion: {}'.format(
        pass_id if pass_id else external_id
    ))
    return response


def add_pass_locations(wallet, locations, pass_id=None, external_id=None):
    """Add locations to a pass.

    Arguments:
        wallet (Wallet object): A wallet client object.
        locations (list): A list of dictionaries representing location
            objects.
        pass_id (str): The ID of the pass you wish to add
            locations to.
        external_id (str): The external ID of the pass you wish to add
            locations to.

    Returns:
        A response object.

    Raises:
        ValueError: If neither, or both of, pass_id and external_id
            are specified.

    Example:
        >>> add_locations(location1, location2, pass_id=12345)
        <Response [200]>
    """
    if not (pass_id or external_id) or (pass_id and external_id):
        raise ValueError('Please specify only one of pass_id or external_id.')

    response = wallet.request(
        method='POST',
        body=json.dumps({"locations": locations}),
        url=Pass.build_url(
            common.PASS_ADD_LOCATION_URL,
            main_id=pass_id,
            pass_external_id=external_id
        ),
        content_type='application/json',
        version=1.2
    )
    logger.info('Successfully added {} locations to pass {}.'.format(
        len(locations),
        pass_id if pass_id else external_id
    ))
    return response


def delete_pass_location(wallet, location_id, pass_id=None, external_id=None):
    """Delete a location from a pass.

    Arguments:
        wallet (Wallet object): A wallet client object.
        location_id (str or int): The ID of the location you wish to delete.
        pass_id (str or itn): The ID of the pass you wish to delete
            locations from.
        external_id (str or int): The external ID of the pass you wish
            to delete locations from.

    Returns:
        A response object.
    Raises:
        ValueError: If both or neither of pass_id and external_id are
            specified.

    Example:
        >>> delete_location(ua_wallet, 12345, pass_id=44444)
    """
    if not (pass_id or external_id) or (pass_id and external_id):
        raise ValueError('Please specify only one of pass_id or external_id.')

    response = wallet.request(
        method='DELETE',
        body=None,
        url=Pass.build_url(
            common.PASS_DELETE_LOCATION_URL,
            main_id=pass_id,
            pass_external_id=external_id,
            location_id=location_id
        ),
        version=1.2
    )
    logger.info('Successfully deleted location {} from pass {}.'.format(
        location_id,
        pass_id if pass_id else external_id
    ))
    return response


class Pass(object):

    @classmethod
    def from_data(cls, data):
        return data

    @staticmethod
    def build_url(
        base_url,
        main_id=None,
        template_external_id=None,
        pass_external_id=None,
        location_id=None
    ):
        if base_url == common.PASS_ADD_LOCATION_URL:
            if main_id:
                return base_url.format(main_id)
            else:
                return base_url.format('id/' + str(pass_external_id))
        elif base_url == common.PASS_DELETE_LOCATION_URL:
            if main_id:
                return base_url.format(main_id, location_id)
            else:
                return base_url.format(
                    'id/' + str(pass_external_id), location_id
                )
        else:
            if main_id and not (template_external_id or pass_external_id):
                return base_url.format(main_id)
            elif template_external_id and not (main_id or pass_external_id):
                return base_url.format('id/' + str(external_id))
            elif pass_external_id and main_id and not template_external_id:
                return base_url.format(
                    str(main_id) + '/id/' + str(pass_external_id)
                )
            elif template_external_id and pass_external_id and not main_id:
                return base_url.format(
                    'id/' + str(template_external_id) + '/id/' + str(pass_external_id)
                )
            else:
                return base_url.format('')
