ckanext-persona
===============

A CKAN extension that lets users login to a site using
[Mozilla Persona](http://www.mozilla.org/en-US/persona/). Users can login
using just their existing email address, without having to create a new user
name and password for CKAN.

Traditional username and password login and registration are still enabled when this
plugin is active, the user is given the choice of Persona or traditional login.

Here's [short video of logging in to CKAN with Persona](https://vimeo.com/85054941).

This is an early, proof-of-concept implementation. It hasn't had much testing
or polishing and isn't suitable for production yet. It has been developed against
CKAN 2.3 alpha.

There's one big problem with this implementation - Persona uses email addresses
to uniquely identify users, but in CKAN two users can have the same email
address. If that happens, ckanext-persona will crash. It needs to be fixed to
present the user with a list of the accounts that have her email address, and
ask her which one she wants to login to (since we've verified via Persona that
the user owns this email address, we assume that she owns any CKAN accounts that
have this email address, so we'll let her login to any of them without providing
the account password).

The second major limitation is that the plugin currently requires JavaScript.
I think it should be possible to implement JavaScript-less Persona logins though.

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

In no particular order:

- Handle multiple users with the same email address in CKAN:
  show all the accounts to the user, and ask her which one she wants
  to login to
- Generate better unique user names based on emails
  (e.g. first half of email, with a random number appended if necessary)
- Give the user a chance to change the generated email address before their account is created
- Implement logging-in via Persona without JavaScript
- Add an API function to CKAN for searching for users by email, so this plugin
  doesn't need to access CKAN's model directly to do it
- Tweak the templates in CKAN that this plugin overrides,
  we need a couple of new template blocks on the login and register pages in CKAN so that his plugin
  doesn't need to duplicate template code from core
- Verify SSL certificates (or is `requests` already doing this?)
- Implement [CSRF protection](https://developer.mozilla.org/en-US/Persona/Security_Considerations)
- Tests, Mozilla [recommend Selenium for this](https://developer.mozilla.org/en-US/Persona/The_implementor_s_guide/Testing?redirectlocale=en-US&redirectslug=Persona%2FThe_implementor_s_guide%2FTesting)
- Better error handling when verification fails
- Allow passwordless accounts in CKAN
- Allow users to have multiple email addresses in CKAN, and verify those addresses using Persona:    
  <https://developer.mozilla.org/en-US/Persona/The_implementor_s_guide/Adding_extra_email_addresses_with_Persona>
