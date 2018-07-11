#!venv/bin/python3
# -*- encoding: utf-8 -*-
"""
Autor: alexfrancow
"""

from app import app

if __name__ == "__main__":
	app.run(debug=True, host="10.0.0.1", port="80")

