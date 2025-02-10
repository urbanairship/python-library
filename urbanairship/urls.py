from typing import Optional


class Urls:
    def __init__(
        self,
        location: Optional[str] = None,
        base_url: Optional[str] = None,
        oauth_base: bool = False,
    ) -> None:
        if base_url:
            self.base_url = base_url
        elif not location or location.lower() == "us":
            if oauth_base:
                self.base_url = "https://api.asnapius.com/api/"
            else:
                self.base_url = "https://go.urbanairship.com/api/"
        elif location.lower() == "eu":
            if oauth_base:
                self.base_url = "https://api.asnapieu.com/api/"
            else:
                self.base_url = "https://go.airship.eu/api/"

        self.channel_url = self.base_url + "channels/"
        self.open_channel_url = self.channel_url + "open/"
        self.device_token_url = self.base_url + "device_tokens/"
        self.apid_url = self.base_url + "apids/"
        self.push_url = self.base_url + "push/"
        self.validate_url = self.push_url + "validate/"
        self.schedules_url = self.base_url + "schedules/"
        self.tags_url = self.base_url + "tags/"
        self.segments_url = self.base_url + "segments/"
        self.reports_url = self.base_url + "reports/"
        self.lists_url = self.base_url + "lists/"
        self.attributes_url = self.channel_url + "attributes/"
        self.attributes_list_url = self.base_url + "attribute-lists/"
        self.message_center_delete_url = self.base_url + "user/messages/"
        self.subscription_lists_url = self.channel_url + "subscription_lists/"
        self.templates_url = self.base_url + "templates/"
        self.schedule_template_url = self.templates_url + "schedules/"
        self.pipelines_url = self.base_url + "pipelines/"
        self.named_user_url = self.base_url + "named_users/"
        self.named_user_tag_url = self.named_user_url + "tags/"
        self.named_user_disassociate_url = self.named_user_url + "disassociate/"
        self.named_user_associate_url = self.named_user_url + "associate/"
        self.named_user_uninstall_url = self.named_user_url + "uninstall/"
        self.sms_url = self.channel_url + "sms/"
        self.sms_opt_out_url = self.sms_url + "opt-out/"
        self.sms_uninstall_url = self.sms_url + "uninstall/"
        self.sms_custom_response_url = self.base_url + "sms/custom-response/"
        self.email_url = self.channel_url + "email/"
        self.email_tags_url = self.email_url + "tags/"
        self.email_uninstall_url = self.email_url + "uninstall/"
        self.create_and_send_url = self.base_url + "create-and-send/"
        self.schedule_create_and_send_url = self.schedules_url + "create-and-send/"
        self.experiments_url = self.base_url + "experiments/"
        self.experiments_schedule_url = self.experiments_url + "scheduled/"
        self.experiments_validate = self.experiments_url + "validate/"
        self.attachment_url = self.base_url + "attachments/"
        self.custom_events_url = self.base_url + "custom-events/"
        self.tag_lists_url = self.base_url + "tag-lists/"

    def get(self, endpoint: str) -> str:
        url: str = getattr(self, endpoint)

        if not url:
            raise AttributeError("No url for endpoint %s" % endpoint)

        return url
