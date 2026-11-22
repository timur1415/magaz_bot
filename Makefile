runserver:
	uvicorn main:app --reload

tunnel:
	ssh -p 2222 -R app:80:localhost:8000 timur@tun.romanenko-dev.ru