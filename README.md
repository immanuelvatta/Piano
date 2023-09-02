# Score Viewer

Score Viewer is an online application skillfully built with a combination of Python, Flask, MySQL, HTML, CSS, JavaScript, and Bootstrap. It provides you with the capability to both upload and preview scores in the PDF format.

Furthermore, Score Viewer includes a convenient built-in search function that allows users to quickly find specific titles they are interested in.

What's more, Score Viewer offers an engaging interactive digital keyboard that users can play either by using their computer keyboard or by clicking on it. Users also have the option to choose from a variety of tones, all of which are customizable to suit their preferences. This functionality is achieved through the utilization of ToneJs.
## Authors

- [Immanuel Vattakunnel](https://www.github.com/immanuelvatta)


## Demo

![preview](/flask_app/static/img/Music_Score_Website.gif)
## Pipfile Packages

To run this project, you will need to add the following packages to your Pipfile 

`[packages]`
```
flask = "*"
pymysql = "*"
flask-bcrypt = "*"
pypdf2 = "*"
```

## Run Locally

Clone the project

```bash
  git clone https://github.com/immanuelvatta/Piano.git
```

Go to the project directory

```bash
  cd piano-main
```

Create a virtual enviornment 

```bash
  pipenv shell
```

Start the server

```bash
  py server.py
```

