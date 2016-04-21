# Estofadora Manager

> Manage bills, income, expenses and clients.


This project was made for my grandfather's business (who does not have so much contact with tech), who is an upholsterer. 
So I tried to keep as simple as possible.

Feel free to contribute and if you have any quention, open an issue and we'll talk about it.

> As the product was made for an brazilian, the whole system is in portuguese (but the code is in english).

## Python version

* Python 3.5

## Installation

* Install pip -> https://pip.pypa.io/en/latest/installing.html
* Install virtualenv -> https://virtualenv.pypa.io/en/latest/installation.html
* Create a folder with virtualenv:
```sh
$ virtualenv folder
```
* Activate the virtual enviroment:
```sh
$ cd folder
$ source bin/activate
```
* Clone this repository for the folder.

* Install the dependencies: 
```sh
pip install -r requirements.txt
```

## Usage example

* Create and configure the database:
```sh
$ python manage.py makemigrations
$ python manage.py migrate
```

* Create an admin user:
```sh
$ python manage.py createsuperuser
```

* Runs the server:
```sh
$ python manage.py runserver
```

* Access the site: `http://127.0.0.1:8000/`
* Access the admin page: `http://127.0.0.1:8000/login`

## Development setup

The project is covered by unit tests, you can run them by doing:

```sh
$ python manage.py test
```

## ScreenShots

#### Dashboard Page
![Dashboard page](screenshots/home.jpg "Dashboard page")

#### Clients Page
![Clients page](screenshots/clients.jpg "Clients page")

#### Items Page
![Items page](screenshots/items.jpg "Items page")

#### Images from an item

You can add some photos of the item to show how it was before and after the work, for example.
If the image was marked (the checkbox), it will appear on the portfolio page on the website, automatically.

![Item images](screenshots/item-images.jpg "Item images")

#### Financial reports: daily, monthly and annually
![Reports](screenshots/charts.jpg "Reports")

## Meta

Fellipe Pinheiro – [@pinheirofellipe](https://twitter.com/pinheirofellipe) – pinheiro.llip[at]gmail[dot]com

Distributed under the MIT license. See [``LICENSE``](https://opensource.org/licenses/MIT) for more information.

[https://github.com/delete/estofadora](https://github.com/delete/estofadora)
