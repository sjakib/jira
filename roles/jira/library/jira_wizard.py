#!/usr/bin/python
import urllib
import urllib2
from HTMLParser import HTMLParser


##
## Module Ansible JIRA setup du wizard
##

# class gestion de la connexion
class Connexion():
    cookies = None
    def get(self, url):
        request = urllib2.Request(url='%s' % url)
        if (self.cookies != None) :
            request.add_header('Cookie', self.cookies)

        response = urllib2.urlopen(request)
        self.cookies = response.info()['Set-Cookie']
        self.url = response.geturl();
        body = response.read()
        response.close()

        print(body)

        parser = FormParser()
        return parser.getForm(body)

    def post(self, url, action, data):
        target = '%s%s%s' % (url, "/secure/" , action)
        request = urllib2.Request(target, data)
        request.add_header('Cookie', self.cookies)

        response = urllib2.urlopen(request)
        self.cookies = response.info()['Set-Cookie']
        body = response.read()

        print(body)

        response.close()

        parser = FormParser()
        return parser.getForm(body)
# end Connexion

class Form:
    action = None
    input = {}
# end Form

# recuperation du formulaire
class FormParser(HTMLParser):
    form = Form()

    def handle_starttag(self, tag, attrs):
        if (tag == 'form'):
            for attr, value in attrs:
                if (attr == 'action'):
                    self.form.action = value
                    break
        elif (tag == 'input'):
            input_name = None
            input_value = 'true'
            for attr, value in attrs:
                if (attr == 'name'):
                    input_name = value
                elif (attr == 'value'):
                    input_value = value
            if (input_name != None):
                self.form.input.update({input_name : input_value})

    def getForm(self, html):
        self.feed(html)
        return self.form
# end FormParser

def setup_properties(data):
    cnx = Connexion();

    # run
    url = "%s" % data['baseUrl']
    form = cnx.get(url)

    # SetupApplicationProperties.jspa
    form_properties = {
        'title': '%s' % data['title'],
        'mode': 'private',
        'baseUrl': '%s' % data['baseUrl'],
        'nextStep': 'true',
        'atl_token': '%s' % form.input['atl_token'],
    }
    form = cnx.post(form.action, form_properties)

    # secure/SetupLicense.jspa
    form_license = {
        'setupLicenseKey': '%s' % data['license'],
        'atl_token': '%s' % form.input['atl_token'],
    }

    form = cnx.post(form.action, form_license)

    # SetupAdminAccount.jspa
    form_admin = {
        'fullname': '%s' % data['admin']['fullname'],
        'email': '%s' % data['admin']['email'],
        'username': '%s' % data['admin']['username'],
        'password': '%s' % data['admin']['password'],
        'confirm': '%s' % data['admin']['password'],
        'atl_token': '%s' % form.input['atl_token'],
    }

    form = cnx.post(form.action, form_admin)

def main():
    data = {
        'title' : 'TAAS IDO',
        'baseUrl' : 'http://s00vl9978105:8080',
        'license' : 'AAABdg0ODAoPeNp9UUtvgkAQvvMrSHppDxBB4yshKYU10ihaoNpDL1scdRtkyexi678vr6ZaH8fZne85d0tYqT7fq+ZAbQ2GbXNodlUnjFSzZfSUDQKkW55lgPqExZAKICsmGU8t4kckmAdeSBQ/330AztavAlBYmqE4PJU0lj7dgZXwhOt8D/i42VGW6DHfKZ8MqX6GmucYb6kAl0qwSnnNMLR2S2mEo0MGFaMzm05J4Hj25PeLfGcMD0c4s8Q1Lsi0kL1oIwQsHjzXehotl9p4/jLWZu5boC3a5qj2mCFf5bHUy0ETfC2/KIJekLI9WBJzqNeuV3OhwEs5CouphJSm8ZUsN9yc9djoFLkmnhsSX5sYrV6n0+/2lWKyTl9uEIeSogS01jQRoMxwQ1MmaJUwsu1QcRCq6f+9klp/Udgpd82TEqDIiRky0fTngoiRZRXrsxfYatjIq/f1eR7ehyrZ0ySvtGq/1w5wqdpj8WPcH2c9/wDiSQl4MCwCFBRe7FdyJrZPdAVE5GZXzfJ1lbjQAhRbJBAWTHRjvj97EljJOw5QPClC+A==X02ia',
        'admin' :  {
            'fullname' : 'ADMIN JIRA',
            'email' : 'jira-ido@bnp.com',
            'username' : 'jira',
            'password' : 'Password'
        }
    }
    setup_properties(data);

main()