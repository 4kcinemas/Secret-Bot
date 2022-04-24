if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/rahulrahamanx/Netflix-AutoFilterBot-.git /Netflix-AutoFilterBot
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /Netflix-AutoFilterBot
fi
cd /Netflix-AutoFilterBot
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
