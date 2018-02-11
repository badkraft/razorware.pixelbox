# Pixelbox: PyLE Driver & PyDE Pyper

Pixelbox is a pythonic microframework for creating lightweight desktop GUIs.

This microframework introduces the following:

* **PyLE Driver** is a light framework that consumes JSON as a markup language. The markup is a GUI development tool allowing developers to create robust user interfaces. The PyLE (Python Light Environment) framework is conducive to creating manageable graphic interfaces that implement the Model-View-Presenter (MVP) paradigm.
* **PyDE Pyper** is a ____ that _____ ... Python Development Environment.

## Conventions
The PyLE framework relies on several conventions. The first is how a project is organized:
<p align="center">
  <img src="https://github.com/badkraft/razorware.pixelbox/blob/master/repo_images/conv_proj_org.png"
       alt="PyLE project organization by convention"
       title="Convention 1: Project Organization"/>
</p>

1. `models` - this is where plain old class objects (POCOs) or data-transfer objects (DTOs) are kept.<br><br>

2. `presenters` - where the behavioral binders are placed.<br> 
    ![PyLE presenter content naming by convention][conv_1b]  

3. `views` - .json markup files placed here.<br>
    ![PyLE view content naming by convention][conv_1c]

    NOTE: *Conventions* are not always a requirement but makes organization much easier to maintain and standardizes how items are found. That said, documentation will assume this convention.<br><br>

4. `application.json` - the application markup; provides information to the framework about the application.
    ```json
    {
      "application": "PydePyper",
      "imports": [
        "tkinter@tk"
      ],
      "f:root": "cls-tk.Tk",
      "startup": "app.views.main"
    }
    ```
    There is a lot going on in this example. JSON is, as its primary    strength, a standardized data structure. The PyLE framework takes advantage of the standardized structure and its *native* characterization as a Python dictionary. Within the data structure, we essentially write a specialized coding scheme that the framework interprets. The details will be covered further in documentation.<br><br>
  
    However, concerning convention, the `startup` key is what is important.  Here we tell the framework the path to the initial view to be rendered.  See the naming convention in the `views` module above. Both items are  named `main` with only the extension being the difference. Likewise,  the presenter (and presumably, a model if applicable) has the same name.<br><br>
  
    Naming conventions are required although the organization of the    project is not. Again, this convention is assumed throughout the documentation.<br><br>

5. `bootstrap.py` - this is the how the framework (PyLE Driver) knows *where to start*.
    ```python
    import importlib
    
    from PyLE_Driver import TargetInfo
    from PyLE_Driver.bootstrap import Bootstrap
    
    
    _mod_info = TargetInfo(importlib.import_module('PyDE_Pyper'),
                           'application.json')
    
    
    class Application(Bootstrap):
    
      def __init__(self):
        Bootstrap.__init__(self, _mod_info)
    
    
    app = Application()
    app.mainloop()
    ```
    
    NOTE: Regarding `import PyLE_Driver` and packages, different platforms require the package be found in a path or loaded from the `sys.path.insert(...)` command.  For example, since Windows and Linux have different ways to handle finding the package, we will standardize this as best as we can.

**Please consider contributing by submitting Pull Requests.**

## Views
The 2 files for the view — `main.json` and `main.py` — are necessary because one is the descriptive language that provides layout information for the rendering engine (initially interpreted by PyLE) as well as data and command bindings via the associated presenter...

```json
{
  "header": {
    "class": "main.Main",
    "import": [],
    "title": "PyDE Pyper"
  },
  "content": {
    "Grid": [
      [
        "<!-- Ignored Control -->",
        {}
      ],
      [
        "Label",
        {
          "text": "Hello, World!",
          "width": 75,
          "grid": {
            "row": 0,
            "col": 0,
            "align": "left"
          }
        }
      ]
    ]
  }
}
```

...and the other is a stub for the view code itself:

```python
from PyLE_Driver.framework import View


class Main(View):
  def __init__(self, ext, cnf=None):
    View.__init__(self, master=ext['root'](), cnf=cnf)
```

This particular example renders the following:
<p align="center">
  <img src="https://github.com/badkraft/razorware.pixelbox/blob/master/repo_images/sample_hello_world.png"
       alt="Sample 'Hello, World!'"
       title="Hello, World!"/>
</p>


[conv_1b]: https://github.com/badkraft/razorware.pixelbox/blob/master/repo_images/content_presenters.png "Convention 1b: Presenter Naming Convention"
[conv_1c]: https://github.com/badkraft/razorware.pixelbox/blob/master/repo_images/content_views.png "Convention 1c: View Naming Convention"