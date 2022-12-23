# Download chrome browser for linux env
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb

# Download chromedriver for linux env
wget https://chromedriver.storage.googleapis.com/108.0.5359.71/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver
mv -f chromedriver /usr/local/bin/chromedriver

# Error while loading shared libraries
apt search libnss3
sudo apt install -y libnss3


# wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
