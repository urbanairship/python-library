"""
    Smoke test of the API
"""

from wallet import *

import pytest
import requests
import math
import logging
import StringIO
import csv

logging.basicConfig(format='')


host = pytest.config.getvalue('host')
key = pytest.config.getvalue('api_key')

print 'Running tests against ' + host

w = Wallet(host, key, True)


if host == 'prod':
    S3_URL = 'https://s3.amazonaws.com/passtools_prod/1/images/'
elif host == 'stag':
    S3_URL = 'https://s3.amazonaws.com/passtools_staging/1/images/'
else:
    S3_URL = 'https://s3.amazonaws.com/passtools-localhost/1/images/'


class TestObjectAPI:
    """
        Tests the object create/update/get and delete API
    """

    @pytest.mark.parametrize("proj_type", [
        # ProjectType.OFFER,                                 # TODO put this back in when bug is fixed WAL-935
        ProjectType.LOYALTY,
        ProjectType.BOARDING_PASS,
        ProjectType.COUPON,
        ProjectType.EVENT_TICKET,
        ProjectType.GENERIC,
        ProjectType.GIFT_CARD,
        ProjectType.MEMBER_CARD
    ])
    def test_project_api(self, proj_type):
        p = Project('NAME', proj_type, 'DESCRIPTION')
        resp = w.create_project(p);
        assert p.description == 'DESCRIPTION'
        assert p.project_type == proj_type
        assert p.name == 'NAME'
        created = p.created_at

        p.description = 'NEW_DESCRIPTION'
        p.name = 'NEW_NAME'
        resp = w.update_project(p, p.id);

        assert p.description == 'NEW_DESCRIPTION'
        assert p.project_type == proj_type
        assert p.name == 'NEW_NAME'
        # assert p.created_at == created                     # TODO put this back in when bug is fixed WAL-936

        p2 = Project.get(w, p.id)

        # pretty_print(resp)

        assert p2.description == 'NEW_DESCRIPTION'
        assert p2.project_type == proj_type
        assert p2.name == 'NEW_NAME'
        # assert p2.created_at == p.created_at               # TODO put this back in when bug is fixed
        # assert p2.updated_at == p.updated_at               # TODO put this back in when bug is fixed
        # assert p2.created_at == created                    # TODO put this back in when bug is fixed

        w.delete_project(p.id)

        with pytest.raises(requests.exceptions.HTTPError):
            Project.get(w, p.id)

    def test_template_and_pass_api(self):
        p = Project('NAME', ProjectType.GIFT_CARD, 'DESCRIPTION')
        resp = w.create_project(p);

        t1 = Template(p.id, 'TEMPLATE', TemplateType.STORE_CARD, Vendor.APPLE, 'DESCRIPTION')
        set_template_values(t1)

        resp = w.create_template(t1, p.id);

        t2 = Template.get(w, t1.id)

        test_template_values(t2)

        assert t2.created_at is not None
        assert t2.updated_at is not None
        assert t2.expiry_duration is not None

        t1.add_field(TextField('FieldNameOne', 'Event', 'Rock Concert', AppleFieldLocation.PRIMARY))
        t1.update(w)
        t2 = Template.get(w, t1.id)

        assert (t2.get_field('FieldNameOne') is not None)
        t2.delete_field('FieldNameOne')
        t2.update(w)
        with pytest.raises(KeyError):
            t2.get_field('FieldNameOne')

        t2.add_field(TextField('KEY', 'LABL', 'VAL', AppleFieldLocation.BACK))
        t2.update(w)
        t3 = Template.get(w, t2.id)
        field = t3.get_field('KEY')
        assert field.value == 'VAL'
        assert field.location == AppleFieldLocation.BACK
        assert field.label == 'LABL'
        assert field.text_alignment == TextAlign.LEFT

        pazz = Pass(t1)
        pazz.create(w)

        pazz2 = Pass.get(w, pazz.id)

        pazz3 = Pass.get(w, pazz2.id)
        field = pazz3.get_field('KEY')
        assert field.value == 'VAL'
        assert field.location == AppleFieldLocation.BACK
        assert field.label == 'LABL'

        field.value = 'NEWVALUE'
        wait_for_ticket(w, pazz3.update(w), 0.3)
        pazz4 = Pass.get(w, pazz3.id)
        field = pazz4.get_field('KEY')
        assert field.value == 'NEWVALUE'
        assert field.location == AppleFieldLocation.BACK
        assert field.label == 'LABL'

        pazz.delete(w)

        w.delete_template(t1.id)

        with pytest.raises(requests.exceptions.HTTPError):
            Template.get(w, t1.id)

        w.delete_project(p.id)

    def test_beacons_api(self):
        p = Project('NAME', ProjectType.GIFT_CARD, 'DESCRIPTION')
        p.create(w)

        t = Template(p.id, 'TEMPLATE', TemplateType.STORE_CARD, Vendor.APPLE, 'DESCRIPTION')
        t.create(w)

        assert len(t.beacons) == 0

        lst = []
        lst.append(Beacon('55502220-A123-A88A-F321-555A444B333C', 'TEXT1', 1, 2))
        lst.append(Beacon('55502220-A123-A88A-F321-555A444B333D', 'TEXT2', 1, 2))
        lst.append(Beacon('55502220-A123-A88A-F321-555A444B333E', 'TEXT3', 1, 2))
        t.beacons = lst

        t.update(w)
        t2 = Template.get(w, t.id)

        assert len(t2.beacons) == 3

        # lst = t2.beacons
        # for beacon in lst:
        #    print beacon

        # TODO Add more tests when we can update beacons without NPE in back end WAL-932

        t.delete(w)
        p.delete(w)

    def test_locations_api(self):
        p = Project('NAME', ProjectType.GIFT_CARD, 'DESCRIPTION')
        p.create(w)

        # TODO: What to do with the STORE_CARD/GIFT_CARD issue
        t = Template(p.id, 'TEMPLATE', TemplateType.STORE_CARD, Vendor.APPLE, 'DESCRIPTION')
        t.create(w)

        assert len(t.locations) == 0

        # TODO: Why dont we support integer JSON input? WAL-940
        lst = []
        lst.append(Location(1.3, 22.3, 'TEXT1', 'STREET1', 'STREET2', 'CITY', 'REGION', 'REGION_CODE', 'COUNTRY'))
        lst.append(Location(1.3, 22.3, 'TEXT1', 'STREET1', 'STREET2', 'CITY', 'REGION', 'REGION_CODE', 'COUNTRY'))
        lst.append(Location(1.3, 22.3, 'TEXT1', 'STREET1', 'STREET2', 'CITY', 'REGION', 'REGION_CODE', 'COUNTRY'))

        resp = w.add_locations_template(lst, t.id)

        t2 = Template.get(w, t.id)
        # print t2

        assert len(t2.locations) == 3
        loc = t2.locations[0]
        # def __init__(self, longitude, latitude, text, street_address_1 = None, street_address_2 = None, city = None, region = None, region_code = None, country = None):

        # print loc

        assert math.fabs(loc.longitude - 1.3) < 0.1
        assert math.fabs(loc.latitude - 22.3) < 0.1
        assert loc.text == 'TEXT1'
        assert loc.street_address_1 == 'STREET1'
        assert loc.street_address_2 == 'STREET2'
        assert loc.city == 'CITY'
        assert loc.region == 'REGION'
        assert loc.region_code == 'REGION_CODE'
        assert loc.country == 'COUNTRY'

        w.delete_location_template(t.id, loc.id)

        t2 = Template.get(w, t.id)
        assert len(t2.locations) == 2
        w.delete_location_template(t.id, t2.locations[0].id)
        w.delete_location_template(t.id, t2.locations[1].id)
        t2 = Template.get(w, t.id)
        assert len(t2.locations) == 0

        t.delete(w)
        p.delete(w)

class TestCSVAPI:

    def test_csv_api(self):
        p = Project('NAME', ProjectType.GIFT_CARD, 'DESCRIPTION')
        p.create(w)

        t = Template(p.id, 'TEMPLATE', TemplateType.STORE_CARD, Vendor.APPLE, 'DESCRIPTION')
        f1 = TextField('CSV CATS1', 'LABEL', '123', AppleFieldLocation.BACK, 1)
        f2 = TextField('CSV is it', 'LABEL', '123', AppleFieldLocation.BACK, 2)
        f3 = TextField('csv likes cats', 'LABEL', '123', AppleFieldLocation.BACK, 3)
        f4 = TextField('csv likes cats more', 'LABEL', '123', AppleFieldLocation.BACK, 4)
        f5 = TextField('CSV light my fire', 'LABEL', '123', AppleFieldLocation.BACK, 5)
        t.add_field(f1)
        t.add_field(f2)
        t.add_field(f3)
        t.add_field(f4)
        t.add_field(f5)
        print t
        t.create(w)
        #t2 = Template.get(w, t.id)

        # Copy of local file csv_smoke.csv
        url = 'https://urbanairship.box.com/shared/static/vu63duew3mccdf5coelkaotjbopb3p25.csv'

        # Test with updated mapping
        resp =w.create_csv_upload(url, t.id)
        upload_id = resp['uploadId']
        mapping = resp['csvHeaderToFieldMapping']
        mapping['CSV nice'] = 'CSV CATS1'
        mapping['CSV'] = 'csv likes cats more'
        w.update_csv_upload(resp, upload_id)
        self.verify_results(upload_id, 1)

        # Impossible is not a valid column
        resp = w.create_csv_upload(url, t.id)
        upload_id = resp['uploadId']
        mapping = resp['csvHeaderToFieldMapping']
        mapping['Impossible'] = 'CSV CATS1'
        with pytest.raises(requests.exceptions.HTTPError):
            w.update_csv_upload(resp, upload_id)

        # Crazy is not a valid field
        resp = w.create_csv_upload(url, t.id)
        upload_id = resp['uploadId']
        mapping = resp['csvHeaderToFieldMapping']
        mapping['CSV'] = 'Crazy'
        with pytest.raises(requests.exceptions.HTTPError):
            w.update_csv_upload(resp, upload_id)

        # Invalid URL
        with pytest.raises(requests.exceptions.HTTPError):
            w.create_csv_upload('bla', t.id)

        # Invalid id
        with pytest.raises(requests.exceptions.HTTPError):
            w.create_csv_upload(url, 133333337)

        # Simple test
        resp = w.create_csv_upload(url, t.id)
        upload_id = resp['uploadId']
        self.verify_results(upload_id, 2)

        t.delete(w)
        p.delete(w)

    def verify_results(self, uploadId, case):
        resp = w.process_csv_upload(uploadId)
        wait_for_ticket(w, resp['ticketId'])
        resp = w.get_csv_upload(uploadId)
        url = resp['url']
        output = requests.get(url, verify=False)

        f = StringIO.StringIO(output.content)
        reader = csv.reader(f, delimiter=',')
        r = 0
        for row in reader:
            if r > 0:
                pazz = Pass.get(w, row[5])
                #print pazz
                f1 = pazz.get_field('CSV CATS1')
                f2 = pazz.get_field('CSV is it')
                f3 = pazz.get_field('csv likes cats')
                f4 = pazz.get_field('csv likes cats more')
                f5 = pazz.get_field('CSV light my fire')
                if case is 1:
                    assert f1.value == 'P' + str(r) + 'C4'
                    assert f4.value == 'P' + str(r) + 'C1'
                else:
                    assert f1.value == 'P' + str(r) + 'C1'
                    assert f4.value == '123'

                assert f2.value == 'P' + str(r) + 'C2'
                assert f3.value == 'P' + str(r) + 'C3'
                assert f5.value == 'P' + str(r) + 'C5'

                pazz.delete(w)
            r += 1

class TestListAPI:
    def test_project_list_api(self):
        name = generate_unique_random_string()
        p1 = Project(name + '1', ProjectType.GIFT_CARD, 'DESCRIPTION')
        w.create_project(p1);
        p2 = Project(name + '2', ProjectType.GIFT_CARD, 'DESCRIPTION')
        w.create_project(p2);
        p3 = Project(name + '3', ProjectType.GIFT_CARD, 'DESCRIPTION')
        w.create_project(p3);
        lst = ProjectIterable(w)

        count = 0
        for project in lst:
            if project.name.startswith(name):
                count += 1

        assert count == 3
        w.delete_project(p1.id)
        w.delete_project(p2.id)
        w.delete_project(p3.id)

    def test_template_list_api(self):
        name = generate_unique_random_string()
        p = Project('PARENT_PROJECT', ProjectType.GIFT_CARD, 'DESCRIPTION')
        w.create_project(p)
        t1 = Template(p.id, name + '1', TemplateType.STORE_CARD, Vendor.APPLE, 'DESCRIPTION')
        w.create_template(t1, p.id);
        t2 = Template(p.id, name + '2', TemplateType.STORE_CARD, Vendor.APPLE, 'DESCRIPTION')
        w.create_template(t2, p.id);
        t3 = Template(p.id, name + '3', TemplateType.STORE_CARD, Vendor.APPLE, 'DESCRIPTION')
        w.create_template(t3, p.id);

        lst = TemplateIterable(w)

        count = 0
        for template in lst:
            if template.name.startswith(name):
                count += 1

        assert count == 3
        w.delete_template(t1.id)
        w.delete_template(t2.id)
        w.delete_template(t3.id)
        w.delete_project(p.id)

    def test_pass_list_api(self):

        p = Project('PARENT_PROJECT', ProjectType.GIFT_CARD, 'DESCRIPTION')
        w.create_project(p)
        t = Template(p.id, 'PARENT_TEMPLATE', TemplateType.STORE_CARD, Vendor.APPLE, 'DESCRIPTION')
        f = TextField('FieldNameOne', 'Event', 'Rock Concert', AppleFieldLocation.PRIMARY)
        n = NumberField('Info', 'Number', 555, AppleFieldLocation.BACK)
        t.add_field(f)
        t.add_field(n)
        w.create_template(t, p.id);

        p1 = Pass(t.id, TemplateType.LOYALTY, Vendor.APPLE)
        w.create_pass(p1, t.id)
        p2 = Pass(t.id, TemplateType.LOYALTY, Vendor.APPLE)
        w.create_pass(p2, t.id)
        p3 = Pass(t.id, TemplateType.LOYALTY, Vendor.APPLE)
        w.create_pass(p3, t.id)

        lst = PassIterable(w, t.id)

        count = 0
        for pazz in lst:
            count += 1

        w.delete_pass(p1.id)
        w.delete_pass(p2.id)
        w.delete_pass(p3.id)
        w.delete_template(t.id)
        w.delete_project(p.id)


class TestWalletObjects:
    """
        Tests the individual objects constructors getters and setters
    """

    def test_beacon_object(self):
        b = Beacon('UUID', 'TEXT', 'MAJOR', 'MINOR')
        assert b.uuid is 'UUID'
        assert b.text is 'TEXT'
        assert b.major is 'MAJOR'
        assert b.minor is 'MINOR'
        b.uuid = 'NEW_UUID'
        b.text = 'NEW_TEXT'
        b.major = 'NEW_MAJOR'
        b.minor = 'NEW_MINOR'
        assert b.uuid is 'NEW_UUID'
        assert b.text is 'NEW_TEXT'
        assert b.major is 'NEW_MAJOR'
        assert b.minor is 'NEW_MINOR'

    def test_location_object(self):
        l = Location(1, 2, 'TEXT1', 'STREET1', 'STREET2', 'CITY', 'REGION', 'REGION_CODE', 'COUNTRY')
        assert l.longitude == 1
        assert l.latitude == 2
        assert l.text == 'TEXT1'
        assert l.street_address_1 == 'STREET1'
        assert l.street_address_2 == 'STREET2'
        assert l.city == 'CITY'
        assert l.region == 'REGION'
        assert l.region_code == 'REGION_CODE'
        assert l.country == 'COUNTRY'
        l.longitude = 3
        l.latitude = 4
        l.street_address_1 = 'NEW_STREET1'
        l.street_address_2 = 'NEW_STREET2'
        l.city = 'NEW_CITY'
        l.region = 'NEW_REGION'
        l.region_code = 'NEW_REGION_CODE'
        l.country = 'NEW_COUNTRY'
        assert l.longitude == 3
        assert l.latitude == 4
        assert l.street_address_1 == 'NEW_STREET1'
        assert l.street_address_2 == 'NEW_STREET2'
        assert l.city == 'NEW_CITY'
        assert l.region == 'NEW_REGION'
        assert l.region_code == 'NEW_REGION_CODE'
        assert l.country == 'NEW_COUNTRY'

    def test_project_object(self):
        p = Project('NAME', 'TYPE', 'DESCRIPTION')
        assert p.name == 'NAME'
        assert p.project_type == 'TYPE'
        assert p.description == 'DESCRIPTION'
        assert p.created_at is None
        assert p.updated_at is None
        assert p.id is None
        p.name = 'NEW_NAME'
        p.project_type = 'NEW_TYPE'
        p.description = 'NEW_DESCRIPTION'
        assert p.name == 'NEW_NAME'
        assert p.project_type == 'NEW_TYPE'
        assert p.description == 'NEW_DESCRIPTION'

    def test_field_object(self):
        def confirm_values(f):
            assert f.name == 'NAME'
            assert f.label == 'LABEL'
            assert f.value == 'VALUE'
            assert f.location == AppleFieldLocation.AUXILIARY
            assert f.order == 2
            assert f.change_message is None
            f.name = 'NEW_NAME'
            f.label = 'NEW_LABEL'
            f.value = 'NEW_VALUE'
            f.location = AppleFieldLocation.BACK
            f.order = 3
            assert f.name == 'NEW_NAME'
            assert f.label == 'NEW_LABEL'
            assert f.value == 'NEW_VALUE'
            assert f.location == AppleFieldLocation.BACK
            assert f.order == 3

        f = TextField('NAME', 'LABEL', 'VALUE', AppleFieldLocation.AUXILIARY, 2, TextAlign.LEFT)
        confirm_values(f)
        assert f.text_alignment == TextAlign.LEFT
        assert f.format_type == FormatType.STRING

        f = NumberField('NAME', 'LABEL', 'VALUE', AppleFieldLocation.AUXILIARY, 2, NumberStyle.PERCENT)
        confirm_values(f)
        assert f.number_style == NumberStyle.PERCENT
        assert f.format_type == FormatType.NUMBER

        f = CurrencyField('NAME', 'LABEL', 'VALUE', AppleFieldLocation.AUXILIARY, 2, "USD")
        confirm_values(f)
        assert f.currency_code is "USD"
        assert f.format_type == FormatType.CURRENCY

        f = DateField('NAME', 'LABEL', 'VALUE', AppleFieldLocation.AUXILIARY, 2)
        confirm_values(f)
        assert f.format_type == FormatType.DATE

        f = URLField('NAME', 'LABEL', 'VALUE', AppleFieldLocation.AUXILIARY, 2)
        confirm_values(f)
        assert f.format_type == FormatType.URL

    def test_template_pass_object(self):
        t = Template(1337, 'NAME', TemplateType.BOARDING_PASS, Vendor.APPLE, 'DESCRIPTION')
        set_template_values(t)
        test_template_values(t)
        p = Pass(1337, TemplateType.BOARDING_PASS, Vendor.APPLE)
        assert p.created_at is None
        assert p.updated_at is None
        assert p.expiration_date is None
        assert p.status is None
        assert p.serial_number is None


############################## CONVENIENCE ##############################

@pytest.fixture(scope="module")
def set_template_values(obj):
    obj.add_barcode('Aztec', '123', 'BARCODE_LABEL', 'iso-8859-1', 'BARCODE_ALT_TEXT')
    obj.background_image = S3_URL + 'default-pass-logo.png'
    obj.strip_image = S3_URL + 'default-pass-logo.png'
    obj.footer_image = S3_URL + 'default-pass-logo.png'
    obj.icon_image = S3_URL + 'default-pass-icon.png'
    obj.thumbnail_image = S3_URL + 'default-pass-icon.png'
    obj.label_color = 'rgb(123,33,33)'
    obj.background_color = 'rgb(33,22,11)'
    obj.value_color = 'rgb(33,22,111)'
    f1 = URLField('NAME1', 'LABEL', 'VALUE', AppleFieldLocation.BACK, 2)
    f2 = CurrencyField('NAME2', 'LABEL', '123', AppleFieldLocation.AUXILIARY, 2, "USD")
    obj.add_field(f2)
    obj.add_field(f1)


@pytest.fixture(scope="module")
def test_template_values(obj):
    assert obj.background_image == S3_URL + 'default-pass-logo.png'
    assert obj.strip_image == S3_URL + 'default-pass-logo.png'
    assert obj.footer_image == S3_URL + 'default-pass-logo.png'
    assert obj.icon_image == S3_URL + 'default-pass-icon.png'
    assert obj.thumbnail_image == S3_URL + 'default-pass-icon.png'
    assert obj.label_color == 'rgb(123,33,33)'
    assert obj.background_color == 'rgb(33,22,11)'
    assert obj.value_color == 'rgb(33,22,111)'
    assert obj.barcode_alt_text == 'BARCODE_ALT_TEXT'
    assert obj.barcode_value == '123'
    assert obj.barcode_type == 'Aztec'
    assert obj.barcode_label == 'BARCODE_LABEL'
    assert obj.barcode_encoding == 'iso-8859-1'
    f1 = URLField('NAME1', 'LABEL', 'VALUE', AppleFieldLocation.BACK, 2)
    f2 = CurrencyField('NAME2', 'LABEL', '123', AppleFieldLocation.AUXILIARY, 2, "USD")
    g1 = obj.get_field('NAME1')
    g2 = obj.get_field('NAME2')
    assert g1.name == f1.name
    assert g1.format_type == FormatType.URL
    assert g2.name == f2.name
    assert g2.format_type == FormatType.CURRENCY
