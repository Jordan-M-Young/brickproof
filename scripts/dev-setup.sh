if [-e "./git_folder.json"]; then
    python3 -m venv .venv
else
    echo ".venv exists"
fi

source .venv/bin/activate
python3 -m pip install -r requirements.txt

