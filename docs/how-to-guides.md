The main problem this project is designed to solve is the collection and updating of metadata about Web Content.

Let's say you have a list of URLs whose basic metadata and propagation online you want to track. You've stored those URLs in a CSV file with the column `target_url`.

|target_url|
|---|
|https://github.com/medialab/minet|
|https://zenodo.org/records/7974793|
|https://archive.fosdem.org/2020/schedule/event/open_research_web_mining/|


## How to use from the command line

Download the code from this GitHub repository and place
the `calculator/` folder in the same directory as your
Python script:

    your_project/
    │
    ├── calculator/
    │   ├── __init__.py
    │   └── calculations.py
    │
    └── your_script.py

Inside of `your_script.py` you can now import the
`add()` function from the `calculator.calculations`
module:

    # your_script.py
    from calculator.calculations import add

After you've imported the function, you can use it
to add any two numbers that you need to add:

    # your_script.py
    from calculator.calculations import add

    print(add(20, 22))  # OUTPUT: 42.0

You're now able to add any two numbers, and you'll
always get a `float` as a result.

Example from [https://realpython.com/python-project-documentation-with-mkdocs/](https://realpython.com/python-project-documentation-with-mkdocs/)
