This tuto was based on https://github.com/jfmatth/openshift-django17, Thanks jfmatth

# Django-OpenShift-1.8

###How to use this repository
- Create an account at https://www.openshift.com
- Install the RHC client tools if you have not already done so.
```
sudo gem install rhc
rhc setup
```
- Create a Python 3.3 application
```
rhc app create django python-3.3
```
- Add the database cartridge (choose one)
```
rhc add-cartridge postgresql-9.2 --app django

OR

rhc add-cartridge mysql-5.5 --app django 
```
- Add this upstream repo
```
cd django
git remote add upstream -m master https://github.com/Gpzim98/Django-OpenShift-1.8.git
git pull -s recursive -X theirs upstream master
```
- set the WSGI application to django's built in WSGI application (stored in the wsgi folder).
```
rhc env set OPENSHIFT_PYTHON_WSGI_APPLICATION=wsgi/wsgi.py --app django
```
- Push the repo upstream
```
git push
```
- SSH into the application to create a django superuser.
```
python app-root/repo/manage.py createsuperuser
```
- Now use your browser to connect to the Admin site.


If your deploy can't install django, you will may log in your app by ssh and make:
'''
pip install django
'''
For log in your app, access your account on OpenShift, select your app and find the url of ssh for your app.

More details on my blog:
blog.gregorypacheco.com.br    
