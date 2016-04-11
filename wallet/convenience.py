from .wallet import *
import time

logger = logging.getLogger('urbanairship')

###########################################################

class TicketStatus:
    """
        Enum for the ticket status
    """
    QUEUED = 'QUEUED'  # The ticket is queued
    COMPLETED = 'COMPLETED'  # The ticket is done
    PREQUED = 'PREQUED'  # The ticket is not yet queued
    ABORTED = 'ABORTED'  # The ticket was cancelled
    FAILED = 'FAILED'  # Ticket operation failed
    ABANDONED = 'ABANDONED'  # Ticket was abandoned


###########################################################
#                CONVENIENCE FUNCTIONS                    #
###########################################################

def create_uploadable_template_from_downloaded_template(downloaded_template):
    """
        Munges the JSON of a downloaded template to match the expected uploaded template
        :param downloaded_template:
        :return: a JSON dict
    """

    if 'templateHeader' in downloaded_template and 'fieldsModel' in downloaded_template:
        locations = {}
        if 'userlocations' in downloaded_template:
            locations = downloaded_template['userlocations']

        copy = dict(downloaded_template['templateHeader'].items() + downloaded_template['fieldsModel'].items())

        copy['locations'] = locations

        # Copy headers section into output dictionary for Apple Wallet templates
        if downloaded_template.get('headers'):
            copy['headers'] = downloaded_template.get('headers')

        # Change the numberstyle to match upload format
        if copy.get('fields'):
            for fieldName in copy['fields']:
                oldValue = copy['fields'][fieldName].get('numberStyle')
                if oldValue:
                    copy['fields'][fieldName]['numberStyle'] = oldValue.replace('PKNumberStyle', 'numberStyle')
        else:
            if copy.get('imageModulesData'):
                if copy['imageModulesData'].get('imageModulesData'):
                    copy['imageModulesData'] = copy['imageModulesData']['imageModulesData']

        # Copy Android Pay specific keys into output dictionary
        if downloaded_template.get('titleModule'):
            copy['titleModule'] = downloaded_template.get('titleModule')

        if downloaded_template.get('imageModulesData'):
            copy['imageModulesData'] = downloaded_template.get('imageModulesData')

        return copy

    return downloaded_template


###########################################################

def wait_for_ticket(wallet_object, ticket_id, poll_delay=1.0, number_retries=3):
    """
         Waits for a ticket queued in wallet to complete
         This function polls the back end at increasingly longer intervals
         until the ticket status changes to COMPLETED
         If the back end fails to respond 3 times it will exit
        :param ticket_id: The id of the ticket to wait for
    """
    status = TicketStatus.PREQUED
    failures = 0;
    while status != TicketStatus.COMPLETED:
        try:
            time.sleep(poll_delay)
            response = wallet_object.get_ticket_status(ticket_id)
            status = response['Status']
            if status == TicketStatus.ABANDONED or status == TicketStatus.ABORTED or status == TicketStatus.FAILED:
                logger.error('Ticket failed with status=' + status)
                return status

            poll_delay *= 1.4
            max_poll_delay = 60 * 60  # Cap it at an hour
            if poll_delay > max_poll_delay:
                poll_delay = max_poll_delay
        except requests.exceptions.HTTPError:
            failures += 1
            if failures >= number_retries:
                raise requests.exceptions.HTTPError('Connection to server failed after retries')

        logger.info('Waiting for ticket... Status=' + status + ' polling with delay ~' + str(int(poll_delay)) + 's')

    logger.info('Ticket done status=' + status)
    return status
