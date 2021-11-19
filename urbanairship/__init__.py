"""Python package for using the Urban Airship API"""
import logging

from .automation import Automation, Pipeline
from .common import AirshipFailure, Unauthorized
from .core import Airship
from .devices import (APIDList, Attribute, AttributeResponse, ChannelInfo,
                      ChannelList, ChannelTags, ChannelUninstall, DeviceInfo,
                      DeviceTokenList, Email, EmailAttachment, EmailTags,
                      LocationFinder, ModifyAttributes, NamedUser,
                      NamedUserList, NamedUserTags, OpenChannel,
                      OpenChannelTags, Segment, SegmentList, Sms, StaticList,
                      StaticLists)
from .experiments import ABTest, Experiment, Variant
from .push import (CreateAndSendPush, Push, ScheduledList, ScheduledPush,
                   Template, TemplateList, TemplatePush, absolute_date,
                   actions, alias, all_, amazon, amazon_channel, and_, android,
                   android_channel, apid, best_time, campaigns, channel,
                   date_attribute, device_token, device_types, email, in_app,
                   interactive, ios, ios_channel, local_scheduled_time,
                   location, merge_data, message, named_user, not_,
                   notification, number_attribute, open_channel, open_platform,
                   options, or_, public_notification, recent_date,
                   scheduled_time, segment, sms, sms_id, sms_sender, style,
                   tag, tag_group, text_attribute, wearable, web, wns,
                   wns_payload)
from .reports import (AppOpensList, CustomEventsList, DevicesReport,
                      ExperimentReport, IndividualResponseStats, OptInList,
                      OptOutList, PushList, ResponseList, ResponseReportList,
                      TimeInAppList, WebResponseReport)

__all__ = [
    Airship,
    AirshipFailure,
    Unauthorized,
    all_,
    Push,
    ScheduledPush,
    TemplatePush,
    ios_channel,
    android_channel,
    amazon_channel,
    channel,
    open_channel,
    device_token,
    apid,
    wns,
    tag,
    tag_group,
    alias,
    segment,
    sms_id,
    sms_sender,
    and_,
    or_,
    not_,
    location,
    recent_date,
    absolute_date,
    notification,
    ios,
    android,
    amazon,
    web,
    wns_payload,
    open_platform,
    message,
    in_app,
    options,
    campaigns,
    actions,
    interactive,
    device_types,
    scheduled_time,
    local_scheduled_time,
    sms,
    email,
    wearable,
    public_notification,
    style,
    best_time,
    named_user,
    merge_data,
    ChannelList,
    ChannelInfo,
    OpenChannel,
    Sms,
    DeviceTokenList,
    APIDList,
    DeviceInfo,
    Segment,
    SegmentList,
    ChannelUninstall,
    NamedUser,
    NamedUserList,
    NamedUserTags,
    IndividualResponseStats,
    ResponseList,
    DevicesReport,
    OptInList,
    OptOutList,
    PushList,
    ResponseReportList,
    AppOpensList,
    TimeInAppList,
    CustomEventsList,
    StaticList,
    StaticLists,
    LocationFinder,
    Template,
    TemplateList,
    ScheduledList,
    Automation,
    Pipeline,
    Email,
    EmailTags,
    EmailAttachment,
    CreateAndSendPush,
    date_attribute,
    text_attribute,
    number_attribute,
    ChannelTags,
    OpenChannelTags,
    Attribute,
    AttributeResponse,
    ModifyAttributes,
    WebResponseReport,
    ExperimentReport,
]


logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(logging.WARNING)
