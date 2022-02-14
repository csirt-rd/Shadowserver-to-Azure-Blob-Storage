<p align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img width="946" alt="Ciberseguridad" src="https://user-images.githubusercontent.com/46871300/125079966-38ef8380-e092-11eb-9b5e-8bd0314d9274.PNG">
  </a>
 
   <h3 align="center">Transfiere reportes de ShadowServer hacia Azure Blob Storage</h3>

  <p>
  Script para transferir reportes del ShadowServer REST API hacia Azure Blob Storage, en formato CSV.
  </p>
</p>

---

## TLP: WHITE

#### Requerimientos:

* [Python3.8+](https://www.python.org/downloads/)

#### Como ejecutar:

Ejecute:

```
python3 -m venv env
```

En Windows, corra:

```
env\Scripts\activate.bat
```

En Unix o MacOS, corra:

```
source env/bin/activate
```

Luego ejecute:

```
pip install -r requirements.txt
```

Finalmente:

```
python3 app.py
```

#### Configuración:

```python
AZURE_ACC_KEY = ...        #Cambiar a la llave de cuenta correspondiente.
AZURE_ACC_NAME = ...       #Cambiar al nombre de cuenta correspondiente.
container_name = ...       #Cambiar al nombre de blob container correspondiente.
AUTH_DETAILS = {
    'user': "",     #Cambiar como sea conveniente.
    'password': "", #Cambiar como sea conveniente.
    'login':'Login'
}
```

#### Referencias:

https://docs.microsoft.com/en-us/python/api/overview/azure/storage-blob-readme?view=azure-python
