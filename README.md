# Pixelbox: PyLE Driver & PyDE Pyper

PyLE - Python Light Environment
PyDE - Python Development Environment

PyLE Driver is a light framework that consumes JSON as a markup language. The markup is a GUI development tool allowing
developers to create robust user interfaces. The PyLE framework is conducive to creating manageable graphic interfaces
that implement the Model-View-Presenter (MVP) paradigm.

The PyLE framework relies on several conventions. The first is how a project is organized:

<p align="center">
  <img src="https://github.com/badkraft/razorware.pixelbox/blob/master/repo_images/conv_proj_org.png"
       alt="PyLE project organization by convention"
       title="Convention 1: Project Organization"/>
</p>

1. `models` - this is where plain old class objects (POCOs) or data-transfer objects (DTOs) are kept.
2. `presenters` - where the behavioral binders are placed.
3. `views` - .json markup files placed here

This *convention* is not a requirement but makes organization much easier to maintain and standardizes how the framework
will find all the parts necessary to properly render data and bind commands to menus, etc.
