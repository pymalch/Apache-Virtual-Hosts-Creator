#!/usr/bin/env python
import os

# Clear the console.
os.system("clear")

def msg(stat):
    print '\033[1;42m'+'\033[1;37m'+stat+'\033[1;m'+'\033[1;m'

def newline():
	print ""

def getUser():
	if os.environ.has_key('SUDO_USER'):
		  return os.environ['SUDO_USER']
	else:
		  return os.environ['USER']

def new_hosts(domain,public_dir,www,user):
	msg(" What would be the public directory name? \n - Press enter to keep default name (\""+public_dir+"\") ")
	public_dir_temp = raw_input()

	# Chceck and set name of the public directory.
	if public_dir_temp !="":
	    public_dir = public_dir_temp

	newline()

	msg(" Creating the Directory Structure ")
	os.system("sudo mkdir -p "+www+domain+"/"+public_dir)

	newline()

	msg(" Granting Proper Permissions ")
	msg("sudo chown -R "+user+" "+www+domain)
	os.system("sudo chown -R "+user+" "+www+domain)

	newline()

	msg(" Making Sure Read Access is Permitted ")
	os.system("sudo chmod -R 755 "+www)

	newline()

	msg(" Adding A Demo Page ")
	file_object = open(www+domain+"/"+public_dir+"/index.html", "w")
	file_object.write("<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Virtual Hosts Created Successfully!</title><style>html{background-color: #508bc9;color: #fff;font-family: sans-serif, arial;}.container{width: 80%;margin: auto auto;}.inl{text-align: center;}.inl img{border-radius: 10px;}a{color: #f2d8ab;}</style></head><body><div class='container'><h1>Virtual Hosts Created Successfully!</h1><p><b>Apache Virtual Hosts Generator</b> has successfully created a virtual host in your server.<br>We can code it better! Join at <a href='https://github.com/rakibtg/Apache-Virtual-Hosts-Creator' target='_blank'>GitHub</a><br>Created by <a href='https://www.twitter.com/rakibtg' target='_blank'>Hasan</a></p><div class='divider'><div class='inl'><h1>Let's celebrate!</h1><img src='http://i.imgur.com/vCbBhwy.gif' alt='Scene from Spider Man Movie (C) Spider Man Movie ..'></div></div></div></body></html>")
	file_object.close()

	newline()

	msg(" Creating Virtual Host File ")
	host_file = open("/tmp/"+domain+".conf", "w")
	host_file.write("<VirtualHost *:80>\nServerAdmin localserver@localhost\nServerName "+domain+" \nServerAlias www."+domain+"\nDocumentRoot "+www+domain+"/"+public_dir+"\n<Directory "+www+domain+"/"+public_dir+">\nDirectoryIndex index.php\nOptions Indexes FollowSymLinks\nAllowOverride All\nRequire all granted\n</Directory>\nErrorLog ${APACHE_LOG_DIR}/error.log\nCustomLog ${APACHE_LOG_DIR}/access.log combined\n</VirtualHost>")
	host_file.close()
	os.system("sudo mv \"/tmp/"+domain+".conf\" \"/etc/apache2/sites-available/\"")

	newline()

	msg(" Activating New Virtual Host ")
	os.system("sudo a2dissite 000-default.conf")
	os.system("sudo a2ensite "+domain+".conf")

	newline()

	msg(" Restarting Apache ")
	os.system("sudo service apache2 restart")
	os.system("service apache2 reload")

	newline()

	msg(" Setting Up Local Host File ")

	os.system("sudo sed -i -e '1i127.0.1.1   "+domain+"\' \"/etc/hosts\"")


	print "\nSuccess! Please visit http://"+domain+"/ from any web browser\n\n"

host_flag = 0
user = getUser()

#config
www="/home/%s/www/" % user
public_dir = "public_html"

newline()

print "\n Welcome to Apache Virtual Hosts Creator\n - This script will setup a Apache Virtual Hosts for you\n - All you have to do, answer few questions\n - Make sure you have Apache configured\n"

newline()

domain=""
while domain=="":
	msg(" What would be the domain name? (you must set a name!) ")
	domain = raw_input()

msg("What would be the path of www root apache? \n - Press enter to keep default path (\""+www +"\")")
www_temp=raw_input()

if www_temp!="":
	www=www_temp


if os.path.exists(www+domain):
	msg(" IMPORTANT: It seems that you have already configured a virtual hosts with the same domain name \n If you continue then all your data of http://"+domain+"/ will be overwritten and can not be undo \n Continue? (yes/no) ")
	flag = raw_input()
	host_flag = 1

	if (flag == "no" or flag == ""):
		newline()
		msg(" New Virtual Hosts was not created due to conflict \n Please choose a different name and try again. ")
		newline()
	if flag == "yes":
		newline()
		msg(" Existing host will be overwritten ... ")
		new_hosts(domain,public_dir,www,user)
else:
	new_hosts(domain,public_dir,www,user)
