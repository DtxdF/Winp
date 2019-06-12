# Winp
> Un script en python para la interacción remota de varias terminales o basicamente un script para la creación de una botnet.
## Requerimientos (**Principal**)
* python 2.7
## Requerimientos (**Python**)
* PySocks
* pycrypto
* rsa
* win-inet-pton - (**Si PySocks genera un error**)
* readline, gnureadline - (**Linux**)
* pyreadline - (**Windows**)
## Requerimientos (**Opcional**)
* Tor o un proxy
## Instalación
```
Windows:

pip install win-inet-pton
pip install pyreadline
PyCrypto en windows se tiene que instalar "manualmente". Puedes descargarlo desde http://www.voidspace.org.uk/python/modules.shtml#pycrypto

Linux:

pip install readline
o
pip install gnureadline
pip install pycrypto

Los dos:

pip install PySocks
pip install rsa
pip install terminaltables

git clone https://github.com/DtxdF/Winp
cd Winp
python gen.py
Winp> help
...
Winp>
```

> **NOTA:** *Solo esta probado en Windows y Linux, por lo tanto solo se indicaran las caracteristicas/requerimientos para estos*. (**Windows 7**, **Kali linux**)
