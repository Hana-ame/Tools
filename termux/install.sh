#!/data/data/com.termux/files/usr/bin/sh

# Stop on any error
set -e

# please download .env first
# 0. Load .env file
DOTENV_FILE="$HOME/.env"

if [ -f "$DOTENV_FILE" ]; then
    echo "Loading variables from $DOTENV_FILE..."
    # This reads the .env file, ignores comments, and exports the variables
    export $(grep -v '^#' "$DOTENV_FILE" | xargs)
else
    echo "Error: .env file not found at $DOTENV_FILE"
    echo "Please create a .env file with CF_TUNNEL_TOKEN and other required vars."
    exit 1
fi

# Check if essential variable exists
if [ -z "$CF_TUNNEL_TOKEN" ]; then
    echo "Error: CF_TUNNEL_TOKEN is not defined in .env"
    exit 1
fi

# 1. Update and install required packages
export DEBIAN_FRONTEND=noninteractive
pkg update -y && pkg upgrade -y
pkg install termux-services openssh python3 curl cloudflared git -y
# ok it is possible
source $PREFIX/etc/profile.d/start-services.sh
pip install dotenv requests
git clone https://github.com/Hana-ame/Tools.git -b script script

# add ssh key to
cat ~/script/authorized_keys >> .ssh/authorized_keys

# 2. Setup DDNS Python Script
mkdir -p $HOME
curl -L "https://proxy.moonchan.xyz/Hana-ame/cloudflare-ddns-python/refs/heads/master/cf_ddns.py?proxy_host=raw.githubusercontent.com" -o $HOME/ddns_cf.py

# 3. Setup DDNS Service
mkdir -p $PREFIX/var/service/ddns_cf
cat <<EOF > $PREFIX/var/service/ddns_cf/run
#!/data/data/com.termux/files/usr/bin/sh
termux-wake-lock
# The loop ensures it runs forever
while true; do
    python $HOME/ddns_cf.py
    sleep 300
done
EOF
chmod +x $PREFIX/var/service/ddns_cf/run

# 4. Setup Cloudflared Service
mkdir -p $PREFIX/var/service/cloudflared
cat <<EOF > $PREFIX/var/service/cloudflared/run
#!/data/data/com.termux/files/usr/bin/sh
termux-wake-lock
# We hard-code the token from the .env here during install
exec cloudflared tunnel run --token ${CF_TUNNEL_TOKEN} 2>&1
EOF
chmod +x $PREFIX/var/service/cloudflared/run

# 5. Setup Termux:Boot (The Reboot Trigger)
mkdir -p ~/.termux/boot
cat <<EOF > ~/.termux/boot/start-services
#!/data/data/com.termux/files/usr/bin/sh
termux-wake-lock
# This sources the environment so termux-services can start
. $PREFIX/etc/profile.d/start-services.sh
EOF
chmod +x ~/.termux/boot/start-services

# 6. Enable Services

# 1. Force start the service daemon
# termux-services
# sleep 2

sv-enable ddns_cf
sv-enable cloudflared

# 1. Ensure openssh is installed
# pkg install openssh -y

# 2. Create the service directory
mkdir -p $PREFIX/var/service/sshd

# 3. Create the 'run' file
# The -D flag is CRITICAL: it tells sshd to stay in the foreground 
# so the service manager can monitor and restart it.    
cat <<EOF > $PREFIX/var/service/sshd/run
#!/data/data/com.termux/files/usr/bin/sh
termux-wake-lock
exec sshd -D
EOF

# 4. Make it executable
chmod +x $PREFIX/var/service/sshd/run

# 5. Enable the service
sv-enable sshd

echo "SSH service is now managed and will restart automatically."

echo "-------------------------------------------------------"
echo "Setup complete successfully!"
echo "Services 'ddns_cf' and 'cloudflared' are running."
echo "Note: Ensure Termux:Boot app is installed and opened once."
echo "-------------------------------------------------------"