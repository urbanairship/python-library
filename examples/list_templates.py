from wallet import *

"""
    This shows how to list templates for a user
"""

w = Wallet()
list = TemplateIterable(w)

for template in list:
    print 'Id=' + str(template.id) + ' Name=' + template.name
