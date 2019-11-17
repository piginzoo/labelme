# https://stackoverflow.com/questions/16344756/auto-reloading-python-flask-app-upon-code-changes
# 这样运行，可以自动reload web pages
echo "启动调试模式：此模式下页面自动reload..."
FLASK_APP=web/server.py FLASK_DEBUG=1 python -m flask run