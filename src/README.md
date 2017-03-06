<h1>The Flask App</h1>

<h3>CONTENTS</h3>
<pre>
.
├── app.py
├── config.py
├── static
│   ├── images
│   ├── jquery.min.js
│   ├── normalize.css
│   ├── skeleton.css
│   └── style.css
└── templates
    ├── 404.html
    ├── facility_inventory.html
    ├── index.html
    ├── layout.html
    ├── login.html
    ├── logout.html
    ├── moving_inventory.html
    └── report_filter.html
</pre>

Key files and descriptions
<ul>
    <li><b>app.py</b> - This is a small Flask web app file. It maps what <i>would</i> be inside __init__.py, run.py, and entry.wsgi into one file</li>
    <li><b>config.py</b> - This module contains global variables for the Flask app instantiation</li>
    <li><b>static/</b> - Directory filled with style sheets, scripts, and images being used</li>
    <li><b>templates/</b> - Directory filled with Jinja outlined HTML files for rendering the web app</li>
</ul>
<br>

<h3>USAGE</h3>
From shell, within src/, run...
<pre>
$ python3 app.py
</pre>
and open
<pre>
localhost:8080
</pre>
in your local browser.

<br>

<a href="https://classes.cs.uoregon.edu//17W/cis322/assignments/"><h3>Assignment Information</h3></a>