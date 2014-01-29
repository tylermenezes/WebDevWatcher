import os;
import subprocess;

vcs_root = '/Users/tylermenezes/Github'
apache_root = '/tmp/apache'
root_domain = 'example.org'

orgs = [ name for name in os.listdir(vcs_root) if os.path.isdir(os.path.join(vcs_root, name)) and not name[0] == '.' ]
apache_refresh_required = False
for org in orgs:
    org_dir = os.path.join(vcs_root, org)
    projects =  [ name for name
                    in os.listdir(org_dir)
                        if os.path.isdir(os.path.join(org_dir, name)) and not name[0] == '.'
                ]

    for project in projects:
        site_name = '.'.join((project.lower(), org.lower(), root_domain.lower()))
        site_config_file= os.path.join(apache_root, 'sites-available', '.'.join((site_name, 'conf')))
        site_config_link= os.path.join(apache_root, 'sites-enabled', '.'.join((site_name, 'conf')))

        if not os.path.exists(site_config_file):
            webroot = os.path.join(vcs_root, org_dir, project)

            apache_config = '''
                <VirtualHost *>
                    DocumentRoot "{0}"
                    ServerName {1}
                    ServerAlias *.{1}
                    <Directory "{0}">
                        allow from all
                        Options +Indexes
                        AllowOverride All
                        Require all granted
                    </Directory>
                </VirtualHost>
            '''

            with open(site_config_file, 'w') as config:
                config.write(apache_config.format(webroot, site_name))

            os.symlink(site_config_file, site_config_link)
            apache_refresh_required = True

if apache_refresh_required:
    subprocess.call(['service', 'apache2', 'restart'])