cd ~;

( cat ~/nohup.out | grep coo | grep -v 127.0.0.1 ; printf '\n\n\n' ; cat ~/nohup.out | grep bid=23 | grep -v 127.0.0.1 ; printf '\n\n\n' ; cat ~/nohup.out | grep bid=101 | grep -v 127.0.0.1 ; printf '\n\n\n'; cat ~/nohup.out | grep 99999 ) | py ~/upload.py --gzip;

py ~/upload.py ~/twitter/nohup.out --gzip;

reboot;
