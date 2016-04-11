from wallet import *

"""
    This example creates an apple pass from scratch then deletes after itself
"""

w = Wallet(debug_on=False)

project = Project('Apple Test Project', ProjectType.EVENT_TICKET, 'Description')
resp = project.create(w)

template = Template(project.id,'My Event Ticket',TemplateType.EVENT_TICKET, Vendor.APPLE, 'Once upon a template....')
template.set_background_color(100, 25, 32)
template.set_label_color(5, 64, 180)
template.strip_image = 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png'

# create and add some fields
template.add_field(TextField('FieldNameOne', 'Event', 'Rock Concert', AppleFieldLocation.PRIMARY))
template.add_field(NumberField('Info', 'Number', 555, AppleFieldLocation.BACK))

q = template.get_field('Info')
print 'Value=' + str(q.value)
print 'Number Style=' + q.number_style

resp = template.create(w)
pazz = Pass(template)
pazz.set_public_url_type_single()
resp = pazz.create(w)

# Check some of the return values
print 'Url=' + pazz.url
print 'Status=' + pazz.status
print 'Serial=' + pazz.serial_number
print 'Remove the delete calls for these to work!'
print 'Download URL=' + pazz.public_url
print 'Pass Image=' + pazz.pass_image

pazz.delete(w)
template.delete(w)
project.delete(w)
