if docker ps | grep -q FCFB-Porygon-Bot; then
    echo STOPPING PORYGON BOT..
    docker stop FCFB-Porygon-Bot
    echo PORYGON BOT STOPPED!
    echo
    echo REMOVING OLD PORYGON BOT...
    docker remove FCFB-Porygon-Bot
    echo REMOVED OLD PORYGON BOT!
    echo
else
    echo PORYGON BOT NOT RUNNING!
    echo
fi
echo BUILDING NEW PORYGON BOT...
docker build -t "fcfb-porygon-bot:porygon_bot.Dockerfile" . -f porygon_bot.Dockerfile
echo NEW PORYGON BOT BUILT!
echo
echo STARTING NEW PORYGON BOT...
docker run -d --restart=always --name FCFB-Porygon-Bot -v /home/apkick/fcfb_scorebugs/:/project/../fcfb/graphics/scorebugs -v /home/apkick/fcfb_win_probability/:/project/../fcfb/graphics/win_probability fcfb-porygon-bot:porygon_bot.Dockerfile
echo NEW PORYGON BOT STARTED!
echo DONE!

docker system prune -a --force