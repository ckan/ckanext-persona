ckanext-persona
===============

A CKAN extension that lets users login to a site using
[Mozilla Persona](http://www.mozilla.org/en-US/persona/). Users can login
using just their existing email address, without having to create a new user
name and password for CKAN.

This is an early, proof-of-concept implementation. It hasn't had much testing
or polishing and isn't suitable for production.

There's one big problem with this implementation - Persona uses email addresses
to uniquely identify users, but in CKAN two users can have the same email
address. If that happens, ckanext-persona will crash.

To install, activate your CKAN virtualenv and then do:

    git clone 'https://github.com/seanh/ckanext-persona.git'
    cd ckanext-persona
    python setup.py develop

Then add 'persona' to the ckan.plugins line in your CKAN config file, e.g:

    ckan.plugins = resource_proxy stats datastore persona

Finally, restart CKAN.


TODO
---

- [ ] Follow the Persona UI guidelines
- [ ] Verify SSL certificates
- [ ] Implement CSRF protection
- [ ] Tests
- [ ] Better error handling when verification fails
- [ ] Generate better unique user names based on emails
- [ ] Better random password generator or enable users without passwords in
      CKAN
- [ ] API function for searching for users by email
- [ ] Handle multiple users with the same email address in CKAN ... but how?
