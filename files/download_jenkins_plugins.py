#!/bin/python3
import urllib.request, zipfile, re

force_newest = True
optional = True
update_url="https://updates.jenkins.io"
plugins = []

def parsePlugin(plugin):
    plugin_name=None
    plugin_version=None
    if plugin.count(':') == 1 or plugin.count(';') == 1:
        if plugin.count(';') == 1:
            if optional:
                plugin_name = plugin.strip().split(';')[0].split(':')[0]
                plugin_version = plugin.strip().split(';')[0].split(':')[1]
            else:
                return 0
        else:
            plugin_name = plugin.strip().split(':')[0]
            plugin_version = plugin.strip().split(':')[1]

        if force_newest:
            plugin_version = 'latest'
            
        for i in plugins:
            if i['name'] == plugin_name:
                if i["version"] == plugin_version or i['version'] == 'latest':
                    return 0
                else:
                    #Not implemented check version
                    i['version'] = 'latest'
                    i['status'] = 'New'
                    return 0

    elif plugin.count(':') == 0:
        plugin_name = plugin
        plugin_version = 'latest'
    else:
        print('ERROR:Invalid syntax \'%s\' to much \':\' occurences' % plugin.strip())
        return 0
    plugins.append({"name" : plugin_name, "version" : plugin_version, "status" : "New"})

for plugin in open('plugins.list'):
    parsePlugin(plugin.strip())

for plugin in plugins:
    if plugin['status'] == 'New':
        if plugin["version"] == 'latest':
            print('%s/latest/%s.hpi' % (update_url, plugin["name"]))
            urllib.request.urlretrieve('%s/latest/%s.hpi' % (update_url, plugin["name"]), 'plugins/%s.hpi' % plugin["name"])
        else:
            print('%s/download/plugins/%s/%s/%s.hpi' % (update_url, plugin["name"], plugin["version"], plugin["name"]))
            urllib.request.urlretrieve('%s/download/plugins/%s/%s/%s.hpi' % (update_url, plugin["name"], plugin["version"], plugin["name"]), 'plugins/%s.hpi' % plugin["name"])
        plugin['status'] = 'Downloaded'
        data = zipfile.ZipFile('plugins/%s.hpi' % plugin["name"], 'r').open('META-INF/MANIFEST.MF').read()
        dependences = re.findall(b"(Plugin-Dependencies: )(.*?)(\r\n[A-Z])", data, re.DOTALL)

        if len(dependences) == 1:
            for x in str(dependences[0][1].decode('UTF-8')).replace('\r\n ','').split(','):
                parsePlugin(x)