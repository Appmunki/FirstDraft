if [ "$UID" -ne 0 ]
    then echo "Please run as root"
    exit
fi

rm -rf static/content/
mkdir static/content/

python2 reset-db.py
