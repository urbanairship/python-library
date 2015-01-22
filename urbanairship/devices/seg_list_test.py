# coding: utf-8
import urbanairship as ua
import segment

airship = ua.Airship("ISex_TTJRuarzs9-o_Gkhg", "cqEQS-QzSFW4TdssghiBLQ")
slist = segment.SegmentList(airship)
slist.listSegments()
