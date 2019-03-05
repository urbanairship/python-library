import logging

from urbanairship import common

logger = logging.getLogger('urbanairship')

class CreateAndSend(object):
    """
    docstring plz
    """

    def __init__(self, airship, channels=[]):
        self._airship = airship
        self.channels = channels
        self.notification = None
        self.campaigns = None

    @property
    def device_types(self):
        return self._device_types

    @device_types.setter
    def device_types(self, value):
        accepted_device_types = ('sms', 'email', 'open::')

        if len(value) != 1:
            raise ValueError('only a single device_type may be used.')
        
        if value[:6] not in accepted_device_types:
            raise ValueError(
                'device_types must be one of' % str(accepted_device_types)
                )
        
        self._device_types = value

    @property
    def audience(self):
        if 'email' in self.device_types:
            return self._email_audience()
        elif 'sms' in self.device_types:
            return self._sms_audience()
        else:
            return self._open_channel_audience()

    @property
    def payload(self):
        data = {
            'audience': self.audience,
            'notification': self.notification,
            'device_types': self.device_types
        }
        if self.campaigns is not None:
            data['campaigns'] = self.campaigns
        return data

    def _email_audience(self):
        return None

    def _sms_audience(self):
        addresses = []
        
        for sms in self.channels:
            if sms.__name__.__class__ != 'Sms':
                raise TypeError(
                    'Can only use Sms objects when device_types is sms'
                    )
            
            addresses.append(sms.create_and_send_audience)
        
        audience = {'create_and_send': addresses}

        return audience

    def _open_channel_audience(self):
        return None

    def send(self):
        pass
