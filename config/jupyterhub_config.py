import os

## set public interface
c.JupyterHub.ip = os.environ["JUPYTERHUB_IP"]
c.JupyterHub.port = int(os.environ["JUPYTERHUB_PORT"])
c.JupyterHub.hub_connect_ip = os.environ["JUPYTERHUB_IP"]

## jupyterhub auth settings
admin_users = os.environ['ADMIN_USERS']
print("Admin Users", admin_users)
admin_users_set = set(filter(len, map(str.strip, admin_users.split(','))))
print("Admin Users Set", admin_users_set)

# c.JupyterHub.authenticator_class = "oauthenticator.LocalGitHubOAuthenticator"
c.JupyterHub.authenticator_class = "nativeauthenticator.NativeAuthenticator"

c.LocalGitHubOAuthenticator.create_system_users = True
c.LocalGitHubOAuthenticator.allowed_users = admin_users_set
c.Authenticator.admin_users = admin_users_set
#c.JupyterHub.admin_access = True

## mount a data location to persist login and user data
data_dir = os.environ['JUPYTERHUB_DATA']
c.JupyterHub.cookie_secret_file = os.path.join(data_dir, 'jupyterhub_cookie_secret')

## remove proxy file as it gives error if it exists on container restart
#proxy_pid_file = "/var/run/jupyterhub-proxy.pid"
#if os.path.exists(proxy_pid_file):
#    print("Cleaning up proxy pid file")
#    os.remove(proxy_pid_file)
#c.ConfigurableHTTPProxy.pid_file = proxy_pid_file

from subprocess import check_call


def pre_spawn_hook(spawner):
    username = spawner.user.name
    try:
        check_call(['useradd', '-ms', '/bin/bash', username])
    except Exception as e:
        print(f'{e}')
c.Spawner.pre_spawn_hook = pre_spawn_hook
