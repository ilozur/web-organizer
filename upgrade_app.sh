cd /home/eva/eva
echo "Stop gunicorn server"
sudo /usr/sbin/service gunicorn_eva stop

echo "Get code"
git checkout master
git pull
git checkout production
git merge master

echo "Upgrade packages"
/home/eva/eva/venv.bin/pip install -r /home/eva/eva/requirements.txt

echo "Refresh db"
/home/eva/eva/venv/bin/python manage.py migrate

#echo "Some cheats with static files"
#rm -rf static_root
#/home/eva/eva/venv/bin/python manage.py collectstatic
#mv static_root static_tmp
#mkdir static_root
#mv static_tmp static_root
#mv static_root/static_tmp static_root/static

echo "make documentation"
rm -rf /home/eva/eva/docs
doxygen

echo "restart server"
sudo /usr/sbin/service gunicorn_eva start
sudo /usr/sbin/service nginx restart
