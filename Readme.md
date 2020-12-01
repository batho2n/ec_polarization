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

* To calculate Polarity Index and Rayleigh 
a) Copy csv files to data path
```sh
(venv) $ ls data
artery-1.csv avm.csv      test.csv
```

b) Generate file.scp file
```sh
(venv) $ ls data/* > file.scp
(venv) $ cat file.scp
data/artery-1.csv
data/avm.csv
data/test.csv
```

c) Run calc_index file
```sh
(venv) $ python calc_index.py file.scp
FILE: data/artery-1.csv, Data #: 869
PI:  0.779301315611742
RAY: 6.30732516017992e-230

FILE: data/avm.csv, Data #: 1355
PI:  0.11524434119894715
RAY: 1.5289418766307256e-08

FILE: data/test.csv, Data #: 4
PI:  0.596197015652498
RAY: 0.25634877337973183
```

4. Caution.
* You must deactivate virtualenv when you finish program.
```sh
(venv) $ deactivate
$
```
