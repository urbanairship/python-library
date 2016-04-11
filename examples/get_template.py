from wallet import *

"""
    This file shows how to create a template object from an existing template
"""

w = Wallet(debug_on=True)

template = Template.get(w, 49336)

print '=== Template ==='
print template

print '=== Template Fields ==='
pretty_print(template.fields)
