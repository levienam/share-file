#!/usr/bin/env bash


IP=$(hostname -I | awk '{print $1}')


if [ ! -d "venv_transfert" ]; then
    python3 -m venv venv_transfert
fi


source venv_transfert/bin/activate


pip install --upgrade pip
pip install flask qrcode pillow


python3 transfert.py "$IP"

