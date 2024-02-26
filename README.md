# Odoo: OpenAcademy

En este repositorio, explicaremos cómo hacer uso de OpenAcademy en Odoo.

Open Academy es un módulo de Odoo que permite a las empresas crear cursos y sesiones de formación para sus empleados.

# Conexion a BD

En el siguiente fragmento de código se muestra la conexión a la base de datos de Odoo (haciendo referencia a nuestro Docker Compose).

```dockerfile
  #servicio gestor de base de datos
  mydb_dev:
    #imagen utilizada y su version
    image: postgres:15
    #mapeo de puertos para acceder a las bases de datos desde el IDE
    ports:
      - 5432:5432
    #variables de entorno de la imagen postgres 15
    environment:
      #nombre de la base de datos predeterminada
      - POSTGRES_DB=postgres
      #contraseña del administrador
      - POSTGRES_PASSWORD=castelao
      #usuario administrador
      - POSTGRES_USER=castelao
 
 ```

Empleando el usuario, contraseña y puerto correspondiente, se puede acceder a la base de datos de Odoo. (Sección Data Source - PostgreSQL)

![img2.png](media%2Fimg2.png)

## Instalación del Módulo

Para instalar este módulo, creamos inicialmente en nuestro proyecto una carpeta denominada 'extra-addons'.

Posteriormente, realizamos el uso de los siguientes comandos en la terminal:
+ **docker exec -u root -it sxe_odoo2-web_dev-1 /bin/bash** : para ingresar al contenedor de Odoo.
+ **cd /mnt/extra-addons** : para ingresar a la carpeta 'extra-addons'.
+ **odoo scaffold openacademy** : para crear la estructura de carpetas y archivos del módulo.
+ **chmod -R 777 openacademy** : para dar permisos a la carpeta del módulo.

Posteriormente, reiniciamos el contenedor para asegurarnos que los cambios se hayan aplicado correctamente.

![img.png](media%2Fimg.png)

# Configuración del Módulo y Creación de una Tabla

Una vez instalado el módulo, reiniciamos nuestro contenedor, e ingresamos a Odoo y nos dirigimos a la sección de 'Aplicaciones' y buscaremos 'OpenAcademy'.

> [!WARNING]
> Para poder visualizar el módulo, es necesario actualizar la lista de aplicaciones, y estar en modo desarrollador para acceder a toda su información.

![img3.png](media%2Fimg3.png)

En el apartado de 'Más información', nos encontraremos con lo siguiente:

![img4.png](media%2Fimg4.png)

Para modificar estos datos, nos dirigimos a la carpeta 'openacademy' y modificamos el archivo 'manifest.py'. Este archivo contiene toda la información del módulo.

```python
# -*- coding: utf-8 -*-
{
    'name': "openacademy",

    'summary': """
        Resumen corto""",

    'description': """
        Esta es otra descripcion
    """,

    'author': "Book And Code",
    'website': "https://www.bookandcoding.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '2.5',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/datos.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

```

En este archivo, podemos modificar el nombre, resumen, descripción, autor, sitio web, categoría, versión, dependencias, datos, y demostraciones del módulo.

---
Por otro lado, para crear una tabla, nos dirigimos a la carpeta 'models' y modificamos el archivo 'models.py'. En este archivo, se encuentra la estructura de la tabla (siendo renombrado, tabla_nombres).

```python
# -*- coding: utf-8 -*-

from odoo import fields, models

class TestModel(models.Model):
    _name = "test_model"
    _description = "Modelo de prueba"

    name = fields.Char(string="Nombre")
    description = fields.Text(string="Descripcion")

```

Una vez modificado el archivo, reiniciamos el contenedor y actualizamos nuestra base de datos. Nos encontraremos con nuestra tabla registrada en la sección "public -> tables". Denominada "test_model".

![img5.png](media%2Fimg5.png)

***NOTA: Crear la tabla no implica que pueda ser visualizada directamente en el OpenAcademy*** 

A continuación, ingresaremos valores a nuestra tabla, para ello hay que realizar una carpeta denominada "data", la cual contendrá un archivo XML con la siguiente estructura:

```xml
<odoo>
    <data>
        <record model="test_model" id="openacademy.nombres">
            <field name="name">Pepe</field> <!-- El nombre debe ser el mismo que la variable del modelo -->
            <field name="description">50</field> <!--El nombre debe ser el mismo que la variable del modelo-->
        </record>
    </data>
</odoo>
```

Una vez creado el archivo, lo añadimos al archivo 'manifest.py' en la sección de 'data'.

```python
    # always loaded
    'data': [
        ...
        'data/datos.xml',
        ...
    ]

```
Con estos cambios, al reiniciar el contenedor y actualizar la base de datos, podremos visualizar los valores ingresados en la tabla.

![img6.png](media%2Fimg6.png)

---
Para que nuestra tabla pueda ser visualizada desde el Odoo, debemos modificar el archivo 'views.xml' en la carpeta 'views'. Este archivo contiene la estructura de la vista de la tabla.

```xml
<odoo>
  <data>
    <!-- explicit list view definition -->
<!--
    <record model="ir.ui.view" id="openacademy.list">
      <field name="name">openacademy list</field>
      <field name="model">openacademy.openacademy</field>
      <field name="arch" type="xml">
        <tree>
          <field name="name"/>
          <field name="value"/>
          <field name="value2"/>
        </tree>
      </field>
    </record>
-->

    <!-- actions opening views on models -->

    <record model="ir.actions.act_window" id="openacademy.action_window">
      <field name="name">openacademy window</field>
      <field name="res_model">test_model</field>
      <field name="view_mode">tree,form</field>
    </record>


    <!-- server action to the one above -->
<!--
    <record model="ir.actions.server" id="openacademy.action_server">
      <field name="name">openacademy server</field>
      <field name="model_id" ref="model_openacademy_openacademy"/>
      <field name="state">code</field>
      <field name="code">
        action = {
          "type": "ir.actions.act_window",
          "view_mode": "tree,form",
          "res_model": model._name,
        }
      </field>
    </record>
-->

    <!-- Top menu item -->

    <menuitem name="openacademy" id="openacademy.menu_root"/>

    <!-- menu categories -->

    <menuitem name="Menu 1" id="openacademy.menu_1" parent="openacademy.menu_root"/>
    <menuitem name="Menu 2" id="openacademy.menu_2" parent="openacademy.menu_root"/>

    <!-- actions -->

    <menuitem name="List" id="openacademy.menu_1_list" parent="openacademy.menu_1"
              action="openacademy.action_window"/>
<!--
    <menuitem name="Server to list" id="openacademy" parent="openacademy.menu_2"
              action="openacademy.action_server"/>
-->
  </data>
</odoo>
```

Como se puede observar en el código, descomentamos la sección de 'actions opening views on models' y 'Top menu item'. En la sección de 'actions opening views on models', se define la vista de la tabla, y en la sección de 'Top menu item', se define el menú de la tabla.

Con respecto al "manifest.py", se debe descomentar el apartado de security, para que se pueda visualizar la tabla.

```python
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/datos.xml'
    ],
```
Para acceder a este archivo, nos ubicaremos en la carpeta 'security' y modificaremos el archivo 'ir.model.access.csv'. En este, modificaremos el nombre del modelo y el grupo al que pertenece.

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_openacademy_openacademy,openacademy.openacademy,model_test_model,base.group_user,1,1,1,1
```

Una vez realizados estos cambios, reiniciamos el contenedor y actualizamos la base de datos. Nos dirigimos a la sección de 'Aplicaciones' y buscamos 'OpenAcademy'. Nos encontraremos con la tabla creada.

![img7.png](media%2Fimg7.png)

![img8.png](media%2Fimg8.png)

---
## Espero esta información sea de ayuda para ustedes. ¡Hasta la próxima! :smile:








