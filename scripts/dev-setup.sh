if [-e "./.venv"]; then
    echo ".venv exists"
else
    python3 -m venv .venv

fi

source .venv/bin/activate
python3 -m pip install -r requirements.txt

