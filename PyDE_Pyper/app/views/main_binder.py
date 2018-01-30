markup = {
    "Main:Frame": [
        {
            "namespace": "app.views.main",
            "master": "Tk",
            "import": ["tkinter"],
            "title": "PyDE Pyper",
            "l:presenters": "mod-app.presenters"
        },
        {
            "resources": {
                "context": "presenters:main.Main"
            }
        },
        {
            "Menu": [
                "File", [
                    "Item1", {"command": ""},
                    "Item2", {"command": ""},
                    "|", {},
                    "Exit", {"parameter": "{view master}", "command": "{binding quit}"}
                ],
                "Edit", [
                    "Item1", {"command": ""},
                    "Item2", {"command": ""},
                    "|", {},
                    "Item3", {"command": ""}
                ]
            ]
        },
        {
            "Grid": [
                "PanedWindow", {
                    "width": 550,
                    "height": 300,
                    "background": "#1E1E29",
                    "borderstyle": "ridge",
                    "bd": 3,
                    "grid": {
                        "row": 0,
                        "col": 0,
                        "align": "right top bottom"
                    },
                    "content": [
                        "Label", {
                            "text": "Hello"
                        },
                        "Label", {
                            "text": "World"
                        }
                    ]
                },
                "PanedWindow", {
                    "width": 550,
                    "height": 300,
                    "background": "#1E1E29",
                    "borderstyle": "ridge",
                    "bd": 3,
                    "orient": "vertical",
                    "grid": {
                        "row": 0,
                        "col": 1,
                        "align": "right top bottom"
                    },
                    "content": [
                        "Frame", {
                            "height": 150,
                            "background": "#1E1E29",
                            "borderstyle": "solid",
                            "bd": 3,
                            "content": [
                                "Label", {
                                    "text": "That said ...",
                                    "bg": "#1E1E29",
                                    "fg": "#CFCFFF",
                                    "grid": {
                                        "row": 0
                                    }
                                }
                            ]
                        },
                        "Label", {
                            "text": "Good bye, World!"
                        }
                    ]
                }
            ]
        }
    ]
}
