markup = {
    "Main:Frame": [
        {
            "namespace": "PyLE_Driver_Testing.test_app.views.main",
            "master": "Tk",
            "import": ["tkinter"],
            "title": "Test App"
        },
        {
            "Grid": [
                "<!-- Ignored Control -->",
                {},
                "Label",
                {
                    "master": "Main.master",
                    "text": "First",
                    "grid": {
                        "row": 0,
                        "col": 0,
                        "align": "left"
                    }
                },
                "Entry",
                {
                    "master": "Main.master",
                    "grid": {
                        "row": 0,
                        "col": 1
                    }
                },
                "Label",
                {
                    "master": "main.master",
                    "text": "Second",
                    "grid": {
                        "row": 1,
                        "col": 0,
                        "align": "left"
                    }
                },
                "Entry",
                {
                    "master": "Main.master",
                    "grid": {
                        "row": 1,
                        "col": 1
                    }
                }
            ]
        }
    ]
}
