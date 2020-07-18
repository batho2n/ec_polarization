## Program guid


1. Requiremets
* Python3.x
* virtualenv
* pip3

2. Install
- Git clone
```sh
$ git clone
$ cd ec_polarization
```
- Create virtual environment
```sh
$ make
test -d venv || virtualenv -p python3 venv
...
...

$ ls venv
bin        lib        pyvenv.cfg

```
- Activate Virtual environment
```sh
$ source venv/bin/activate
(venv) $
```

3. Run program
```sh
(venv) $ python ec_polarization.py
```

4. Caution.
* You must deactivate virtualenv when you finish program.
```sh
(venv) $ deactivate
$
```
