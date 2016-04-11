from wallet import *

"""
    This shows how to list projects for a user
    and deletes all projects with a specific name
"""

w = Wallet()
list = ProjectIterable(w)

name_to_delete = 'HL API Test Project CHANGE THIS WITH CARE OK :)'

for project in list:
    print 'Id=' + str(project.id) + ' Name=' + project.name
    if project.name == name_to_delete :
        w.delete_project( project.id )
        print 'Project Deleted'
