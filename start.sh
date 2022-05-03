if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/4kcinemas/SeSecret-Bot.git /Secret-Bot
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /Secret-Bot
fi
cd /Secret-Bot
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
