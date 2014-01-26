ckanext-persona
===============

A CKAN extension that lets users login to a site using
[Mozilla Persona](http://www.mozilla.org/en-US/persona/). Users can login
using just their existing email address, without having to create a new user
name and password for CKAN.

Here's [short video of logging in to CKAN with Persona](https://vimeo.com/85054941).

This is an early, proof-of-concept implementation. It hasn't had much testing
or polishing and isn't suitable for production.

There's one big problem with this implementation - Persona uses email addresses
to uniquely identify users, but in CKAN two users can have the same email
address. If that happens, ckanext-persona will crash. This needs to be fixed
in CKAN - user email addresses should be unique, and they should be verified.

To install, activate your CKAN virtualenv and then do:

    git clone 'https://github.com/seanh/ckanext-persona.git'
    cd ckanext-persona
    python setup.py develop

Then add 'persona' to the ckan.plugins line in your CKAN config file, for example:

    ckan.plugins = resource_proxy stats datastore persona
    
Also make sure you have `ckan.site_url` set correctly in your config file, for example:

    ckan.site_url = http://scotdata.ckan.net

Finally, restart your web server.


TODO
---

- Generate better unique user names based on emails
  (e.g. first half of email, with a random number appended if necessary)
- Tests
- Verify SSL certificates (or is `requests` already doing this?)
- Implement CSRF protection
- Better error handling when verification fails
- Better random password generator
- Add an API function to CKAN for searching for users by email, so this plugin
  doesn't need to access CKAN's model directly to do it
- Handle multiple users with the same email address in CKAN
