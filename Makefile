install:
	pip3 install -r requirements.txt

pm2:
	pm2 delete downtobox
	pm2 start ecosystem.config.js
	pm2 save
