```
python -m PyInstaller -w -F <filename>.py
```

> -w: it prevents the command window from opening when running the executable

> -F: it includes all the dependencies into the exuctable instead of creating a separate file

> -i: give a custom icon to you file. you need to include the path of the icon in inverted comma in .ico format

```
pyinstaller -w -F -i "path/icon.ico" filename.py
```

The resultant .exe file will be in the **dist folder** that will be created.

![9a5aef357ca3abff14e77f1b56ac9bc6.png](file:///C:/Users/Abhay/.config/joplin-desktop/resources/6a78dd493503424fb66536cdfce9afa2.png)

We need the pyinstaller module first

```
pip install pyinstaller
```

The pyinstaller converts the given python file into an executable along with all its dependencies.

Go to the path of the file and

```
pyinstaller filename.py
```

However, using this default option creates a lot of folders and other files along with our executable. Also, when we run the file it opens the command window in the background. To avoid this we use a few flags.

to convert png to ico we can use [convertico.com](http://convertico.com "http://convertico.com")

![fc76065b0c6b04093fa785eeeb19717e.png](file:///C:/Users/Abhay/.config/joplin-desktop/resources/2237dcacdb234cbe93edb85ae7275e3e.png)