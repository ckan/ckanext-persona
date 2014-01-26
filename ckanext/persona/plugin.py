'''A CKAN plugin that enables logging into CKAN using Mozilla Persona.

'''
import json
import uuid

import requests

# Unfortunately we need to import pylons directly here, because we need to
# put stuff into the Beaker session and CKAN's plugins toolkit doesn't let
# us do that yet.
import pylons

import pylons.config as config

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as helpers


class PersonaVerificationError(Exception):
    '''The exception class that is raised if trying to verify a Persona
    assertion fails.

    '''
    pass


class PersonaPlugin(plugins.SingletonPlugin):
    '''A CKAN plugin that enables logging into CKAN using Mozilla Persona.

    '''
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IAuthenticator)

    def update_config(self, config):
        '''Update CKAN's config with settings needed by this plugin.

        '''
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')
        toolkit.add_resource('fanstatic', 'persona')

    def login(self):
        '''Handle an attempt to login using Persona.

        '''
        # Get the params that were posted to /user/login.
        params = toolkit.request.params

        if 'assertion' in params:
            # We've found an assetion from Persona, try to verify it.
            try:
                email = verify_login(params['assertion'])
            except PersonaVerificationError, e:
                toolkit.abort(500)

            user = get_user(email)
            if not user:
                # A user with this email address doesn't yet exist in CKAN,
                # so create one.
                user = toolkit.get_action('user_create')(
                    context={'ignore_auth': True},
                    data_dict={'email': email,
                               'name': generate_user_name(email),
                               'password': generate_password()})

            # Store the name of the verified logged-in user in the Beaker
            # sesssion store.
            pylons.session['ckanext-persona-user'] = user['name']
            pylons.session['ckanext-persona-email'] = email
            pylons.session.save()

    def identify(self):
        '''Identify which user (if any) is logged-in via Persona.

        If a logged-in user is found, set toolkit.c.user to be their user name.

        '''
        # Try to get the item that login() placed in the session.
        user = pylons.session.get('ckanext-persona-user')
        if user:
            # We've found a logged-in user. Set c.user to let CKAN know.
            toolkit.c.user = user

    def _delete_session_items(self):
        import pylons
        if 'ckanext-persona-user' in pylons.session:
            del pylons.session['ckanext-persona-user']
        if 'ckanext-persona-email' in pylons.session:
            del pylons.session['ckanext-persona-email']
        pylons.session.save()

    def logout(self):
        '''Handle a logout.'''

        # Delete the session item, so that identify() will no longer find it.
        self._delete_session_items()

    def abort(self, status_code, detail, headers, comment):
        '''Handle an abort.'''

        # Delete the session item, so that identify() will no longer find it.
        self._delete_session_items()


def get_user(email):
    '''Return the CKAN user with the given email address.

    :rtype: A CKAN user dict

    '''
    # We do this by accessing the CKAN model directly, because there isn't a
    # way to search for users by email address using the API yet.
    import ckan.model
    users = ckan.model.User.by_email(email)

    assert len(users) in (0, 1), ("The Persona plugin doesn't know what to do "
                                  "when CKAN has more than one user with the "
                                  "same email address.")

    if users:

        # But we need to actually return a user dict, so we need to convert it
        # here.
        user = users[0]
        user_dict = toolkit.get_action('user_show')(data_dict={'id': user.id})
        return user_dict

    else:
        return None


def generate_user_name(email):
    '''Generate a random user name for the given email address.

    '''
    # FIXME: Generate a better user name, based on the email, but still making
    # sure it's unique.
    return str(uuid.uuid4())


def generate_password():
    '''Generate a random password.

    '''
    # FIXME: Replace this with a better way of generating passwords, or enable
    # users without passwords in CKAN.
    return str(uuid.uuid4())


def verify_login(assertion):
    '''Verify the given login assertion with Persona's Verification Service.

    :returns: the email address of the successfully verified user
    :rtype: string

    :raises: :py:class:`PersonaVerificationError`: if the verification fails

    '''
    # This requires ckan.site_url to be set in the CKAN config file.
    data = {'assertion': assertion, 'audience': config.get('ckan.site_url')}
    response = requests.post('https://verifier.login.persona.org/verify',
                             data=data, verify=True)

    if response.ok:
        verification_data = json.loads(response.content)
        if verification_data['status'] == 'okay':
            email = verification_data['email']
            return email
        else:
            raise PersonaVerificationError(verification_data)
    else:
        raise PersonaVerificationError(response)
