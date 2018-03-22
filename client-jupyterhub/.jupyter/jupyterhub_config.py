import os

from jupyterhub.spawner import LocalProcessSpawner

class DefaultUserLocalProcessSpawner(LocalProcessSpawner):

    def user_env(self, env):
        env['USER'] = 'default'
        env['HOME'] = '/opt/app-root/data/%s' % self.user.name
        env['SHELL'] = '/bin/bash'
        return env
    
    def get_env(self):
        env = super().get_env()
        if self.user_options.get('env'):
            env.update(self.user_options['env'])
        env['LD_LIBRARY_PATH'] = os.environ['LD_LIBRARY_PATH']
        env['LD_PRELOAD'] = os.environ['LD_PRELOAD']
        env['NSS_WRAPPER_PASSWD'] = os.environ['NSS_WRAPPER_PASSWD']
        env['NSS_WRAPPER_GROUP'] = os.environ['NSS_WRAPPER_GROUP']
        return env

    def make_preexec_fn(self, name):
        def preexec():
            home = '/opt/app-root/data/%s' % name
            if not os.path.exists(home):
                os.mkdir(home)
            os.chdir(home)
        return preexec

config = '/opt/app-root/src/.jupyter/jupyter_notebook_config.py'

class NB2KGLocalProcessSpawner(DefaultUserLocalProcessSpawner):

    args = [ '--config=%s' % config ]

    def _options_form_default(self):
        return """
        <label for="gateway">Kernel Gateway</label>
        <input name="gateway" placeholder="http://nb2kg-kg:8080/"></input>
        <label for="token">Auth Token</label>
        <input name="token" placeholder="colonels"></input>
        """
    
    def options_from_form(self, formdata):
        options = {}
        options['gateway'] = formdata.get('gateway', [''])[0]
        if not options['gateway']:
            raise RuntimeError('Kernel Gateway option required.')
        options['token'] = formdata.get('token', [''])[0]
        if not options['token']:
            raise RuntimeError('Auth Token option required.')
        return options

    def get_env(self):
        env = super().get_env()
        options = self.user_options
        env['KG_URL'] = options['gateway']
        env['KG_AUTH_TOKEN'] = options['token']
        return env

c.JupyterHub.spawner_class = NB2KGLocalProcessSpawner
