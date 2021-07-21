Run test on local
```
pip install -r app/requirements.txt
python -m unittest
```


Build
> docker build -t berejant/camera-watchdog:v0.1 .

Run
> docker run  --name camera-watchdog -p 8000:8000 --rm --env-file=.env -v storage:/app/storage -v models:/app/nomeroff-net/NomeroffNet/Base/mcm/models  -it berejant/camera-watchdog:v0.1

Bash
> docker exec -it camera-watchdog /bin/bash 

Push to hub
> docker push berejant/camera-watchdog:v0.1
