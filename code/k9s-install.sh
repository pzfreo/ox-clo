mkdir k9s
cd k9s
wget https://github.com/derailed/k9s/releases/download/v0.24.14/k9s_Linux_x86_64.tar.gz
tar xvfz k9s_Linux_x86_64.tar.gz
sudo mv k9s /usr/local/bin
rm LICENSE README.md k9s_Linux_x86_64.tar.gz
cd ..
rmdir k9s
k9s version