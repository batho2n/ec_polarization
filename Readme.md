## Program guid


1. Requiremets
	* Python3.x
	* virtualenv
	* pip3

2. Install
- Git clone
```sh
$ git clone https://github.com/batho2n/ec_polarization.git
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
* Default image canvas max size is 800 x 800
```sh
(venv) $ python ec_polarization.py
```
* If you want to change image canvas max size, enter size as input argument
	* Ex) Max size 1024 x 1024
```sh
(venv) $ python ec_polarization.py 1024
```

4. Caution.
* You must deactivate virtualenv when you finish program.
```sh
(venv) $ deactivate
$
```
