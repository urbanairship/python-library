import urbanairship as ua
import segment

airship = ua.Airship("ISex_TTJRuarzs9-o_Gkhg", "cqEQS-QzSFW4TdssghiBLQ")
seg = segment.Segment(airship, 'test_segment1', {"display_name": "Test Segment, ignore"})
seg.set_criteria({"and":[{"tag": "news"}, {"not":{"tag":"sports"}}]})
seg.create()
