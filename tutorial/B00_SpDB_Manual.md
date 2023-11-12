## SpDB Manual

### **概述**
**SpDB**是一个自主开发的Python库，用于处理EAST数据分析中涉及的多种科学数据格式。它以MAS IDS为标准规范的本体，引入数据集成的思想将以不同语义和格式存储的数据在统一的数据模型下进行检索、查询。

**SpDB**专门为集成建模分析系统FyTok的数据交互而设计，但是不一定与之绑定，独立于FyTok仍然可以使用。

**SpDB**可以为用户提供：
- 以IMAS IDS为标准的数据交互语义，将数据绑定到 IMAS DD，以便在 IMAS DD 名称空间下统一异构多源数据。但是不依赖于IMAS ，不需要安装IMAS 。
- 独立的python包，易安装、上手。可独立于ShenMa集群运行，安装在任何有python3.10+的环境下
- 囊括日常科研工作中常用数据格式的处理，且以插件形式管理，开发者用户易对其进行扩展
- 读取的数据在内存中以Python中数据格式进行交互，其数据的语义是严格遵守IMAS IDS的树状结构
- 写数据是灵活的。

### **SpDB的设计思想**
**SpDB**是一个数据集成工具。它基于标准的数据模型，为用户提供一种全局的中介模式，将来自不同、异构的数据源集成到一个全局的地址空间，通过唯一的URI实现对数据的统一访问，即是数据集成研究的范畴。它的实现，包含三层构架：面向用户的统一访问层及底层的映射层和转化层。


<img src="./figures/three-layer_spdb.png" width = "500" height = "400" alt="/three-layer" align=center />

### **SpDB的处理对象**

**SpDB**是一个通用的数据集成工具，意在将聚变研究中常用的数据格式都统一映射在标准的语义表述下，同时降低用户处理对不同格式的数据源的门槛。
**SpDB**可以处理常用的多种类型的科学数据格式，包括：
- Python原生的数据格式：字典、List。
    - 直接在内存中交互
- 半结构化数据结构，如：Namelist、JSON、XML、HDF5、netCDF等。
    - 按照半结构化数据的已有的树状路径查询
- 结构化数据结构，如：Gdskfile，、Inputfile等。
    - 数据量比较小，拿回来全部放在内存中，直接访问。
- 远程数据库系统，如EAST实验的MDSplus及CFETR设计的MDSplus数据库等。
    - 将原始的数据源映射在标准的树状结构的语义下。
    - 支持延迟执行
    - 支持不同类型数据的集成，统一的入口访问。
        - 静态装置描述数据
        - 动态实验测量数据

#### **SpDB已支持的数据格式及完成的映射**


<table>
    <tr>
        <td><b>数据格式</b></td>
        <td><b>插件名称</b> </td>
        <td><b>format标识</b></td>
        <td><b>映射和转化</b></td>
        <td><b>备注</b></td>
    </tr>
    <tr>
        <td rowspan="1">内存中数据</td>
        <td>无</td>
        <td>Dict，List</td>
        <td>无</td>
        <td>无</td>
    </tr>
    <tr>
        <td rowspan="3">非结构化数据</td>
        <td>plugin_gdskfile</td>
        <td>["gfile", "gdskfile"，“GDSKfile”]</td>
        <td>无界限</td>
        <td>数据直接读入内存</td>
    </tr>
    <tr>
        <td>plugin_namelist </td>
        <td>["namelist"] </td>
        <td>无界限</td>
        <td>数据直接读入内存</td>
    </tr>
    <tr>
        <td>......</td>
        <td>......</td>
        <td>......</td>
        <td>......</td>
    </tr>
    <tr>
        <td rowspan="5">半结构化数据</td>
        <td>plugin_netcdf</td>
        <td>["nc", "netcdf", "NetCDf"]</td>
        <td>分开</td>
        <td>延迟执行</td>
    </tr>
    <tr>
        <td>plugin_hdf5 </td>
        <td>["h5", "hdf5", "HDF5"]</td>
        <td>分开</td>
        <td>延迟执行</td>
    </tr>
    <tr>
        <td>plugin_json</td>
        <td> ["json", "JSON"]  </td>
        <td>分开</td>
        <td>延迟执行</td>
    </tr>
    <tr>
        <td>plugin_yaml </td>
        <td>["yaml", "YAML"]  </td>
        <td>分开</td>
        <td>延迟执行</td>
    </tr>
    <tr>
        <td>plugin_xml</td>
        <td> ["xml"] </td>
        <td>分开</td>
        <td>延迟执行</td>
    </tr>
    <tr>
        <td rowspan="2">远程数据库系统</td>
        <td>plugin_mdsplus</td>
        <td>["mdsplus", "mds", "mds+", "MDSplus"]</td>
        <td>分开</td>
        <td>wall,pf_active,tf,magnetics,eq</td>
    </tr>
    <tr>
        <td>......</td>
        <td>......</td>
        <td>......</td>
        <td>......</td>
    </tr>

</table>


### **安装SpDB**
#### ShenMa集群上的**SpDB** 模块
目前，ShenMa集群内（service108）服务器上SpDB模块是可用的。你能运行下面命令，加载其环境：


```python
module load spdm/0.0.0-foss-2022b
```

另外，如果你想使用MDSplus 后端，需要load：


```python
module load MDSplus-Python/7.131.5-gfbf-2022b-Python-3.10.8
```

测试安装：


```python
python -c "import spdm; print(spdm.__version__)"
```

#### 个人Python环境本地安装
推荐使用anconda维护个人Python环境，Python版本3.10+。
SpDB的发行包已上传在pip 仓库中，运行pip install直接安装:


```python
pip install --upgrade pip
pip install spdm 
```

或者，也可以下载打包好的whl源码包安装：


```python
wget https://gitee.com/SimPla/SpDM/releases/tag/0.3.0-rc
pip install --upgrade pip
pip install spdm 
```

如果pip安装指定了安装目录，需先添加安装目录到PYTHONPATH中。否者在默认的~/.local/lib/下面：


```python
export PYTHONPATH=${INSTALLPATH}/site-packages:${PYTHONPATH}
```

测试你的安装：


```python
cd ~
python -c "import spdm; print(spdm.__version__)"
```

### **SpDB**用法
#### **SpDB** 访问Python中原生数据类型访问


```python
from spdm.data.Entry import open_entry
from spdm.utils.logger import logger
#缺少例子？？？？？

```

#### **SpDB** 处理Python中非结构化数据,如GDSKfile等


```python
from spdm.data.File import File
from spdm.utils.logger import logger
from pathlib import Path
current_path = "/scratch/jupytertest/workspace_fytok/fytok_tutorial/tutorial"
### For NameList File
DATA_INPUT = current_path+"/data/"
with File(DATA_INPUT+"/g070754.05000", mode="r", format="GEQdsk") as fid:
    doc = fid.read()
    eq_test = doc.dump()
```


```python
#### eq_test是Python中的字典，其key遵守IMAS IDS的组织结构
eq_test.keys()
```




    dict_keys(['wall', 'equilibrium'])




```python
#### 查看equilibrium中的数据
eq_test["equilibrium"].keys()
```




    dict_keys(['time', 'vacuum_toroidal_field', 'time_slice'])



#### **SpDB** 访问Python中半结构化数据,如NameList,netCDF,HDF5等


```python
### 初始化环境
from spdm.data.File import File
from spdm.utils.logger import logger
from pathlib import Path
current_path = "/scratch/jupytertest/workspace_fytok/fytok_tutorial/tutorial"
### For NameList File
DATA_INPUT = current_path+"/data/"
```

##### **NameList**文件


```python
###以GENRAY的输入文件genray.dat为例，它是一个NameList格式的文件。
with File(f"{DATA_INPUT}/genray.dat", format= "namelist" ,mode="r") as oid:
### 仅仅建立链接，而没有拿回数据
    output_entry = oid.read()
### 拿回所有数据
    output_data = oid.read().dump()
###获取namelist中的关键字key
logger.info(output_data.keys())
### 通过child获取某个子节点的值，而不需要把整个树读回来
logger.info(output_entry.child("main_lobes").__value__)
```

    [0;34m2023-11-11 14:04:56,391 [    spdm]     INFO: dict_keys(['main_lobes', 'genr', 'tokamak', 'wave', 'scatnper', 'dispers', 'numercl', 'output', 'plasma', 'species', 'varden', 'denprof', 'tpopprof', 'vflprof', 'zprof', 'tprof', 'grill', 'rz_launch_grill_tab', 'eccone', 'dentab', 'dentab_nonuniform_line', 'temtab', 'temtab_nonuniform_line', 'tpoptab', 'tpoptab_nonuniform_line', 'vflowtab', 'vflowtab_nonuniform_line', 'zeftab', 'zeftab_nonuniform_line', 'read_diskf', 'emission', 'ox', 'adj_nml', 'edge_prof_nml', 'lsc_approach_nml', 'edctsctab', 'jpartsctab'])[0m
    [0;34m2023-11-11 14:04:56,393 [    spdm]     INFO: OrderedDict([('total_grills', 5),
                 ('main_grills', 4),
                 ('bt_direction', 1),
                 ('power_fraction_factor', 0.8248)])[0m



```python
#### NotImplementedError: TODO: NAMELISTFile.write
# with File(f"{DATA_INPUT}/test-eq.h5", mode="w", format="namelist") as oid:
#     oid.write(eq_test)
```

##### **netCDF**文件


```python
### 以GENRAY的剖面输入文件genray_profs_in.nc为例，它是一个netCDF格式的文件。
with File(f"{DATA_INPUT}/genray_profs_in.nc", format= "NetCDf" ,mode="r") as oid:
### 仅仅建立链接，而没有拿回数据
    output_entry = oid.read()
### 拿回所有数据
    output_data = oid.read().dump()
###获取namelist中的关键字key
logger.info(output_data.keys())
logger.info(output_data["dmass"].data)
### 通过child获取某个子节点的值，而不需要把整个树读回来
# logger.info(output_entry.child("dmass").__value__)
```

    [0;34m2023-11-11 14:30:54,238 [    spdm]     INFO: dict_keys(['charge', 'dmass', 'en', 'eqdsk_name', 'nj', 'nspecgr', 'r', 'temp', 'zeff', 'title'])[0m
    [0;34m2023-11-11 14:30:54,239 [    spdm]     INFO: [1.00000000e+00 1.83619995e+03 3.67239990e+03 2.20343994e+04][0m



```python
#### 写.nc文件
with File(f"{DATA_INPUT}/test-eq.nc", mode="w", format="netcdf") as oid:
    oid.write(eq_test)
with File(f"{DATA_INPUT}/test-eq.nc", format= "NetCDf" ,mode="r") as oid: 
    test_data = oid.read().dump()
    logger.info(test_data.keys())
    logger.info(test_data["wall"])
```

    [0;34m2023-11-11 14:50:11,262 [    spdm]     INFO: dict_keys(['wall', 'equilibrium'])[0m
    [0;34m2023-11-11 14:50:11,263 [    spdm]     INFO: {'description_2d': {'0': {'limiter': {'unit': {'0': {'outline': {'r': array([1.35838, 1.35838, 1.35838, 1.36314, 1.4371 , 1.43721, 1.44164,
           1.4297 , 1.39169, 1.39151, 1.37929, 1.399  , 1.43623, 1.45919,
           1.47791, 1.54494, 1.61204, 1.63506, 1.66054, 1.66519, 1.6955 ,
           1.70668, 1.71388, 1.714  , 1.73649, 1.76324, 1.80199, 1.80237,
           1.93972, 1.97063, 2.07495, 2.1771 , 2.27925, 2.35   , 2.35   ,
           2.35   , 2.27925, 2.1771 , 2.07495, 1.9728 , 1.97063, 1.92059,
           1.87055, 1.82051, 1.79281, 1.76511, 1.75421, 1.67782, 1.60143,
           1.48426, 1.36709, 1.33132, 1.37874, 1.42615, 1.40528, 1.3844 ,
           1.36353, 1.35838, 1.35838, 1.35838, 1.35838]),
                                                                     'z': array([ 0.      ,  0.227   ,  0.454   ,  0.455735,  0.798332,  0.798821,
            0.838195,  0.908908,  1.01426 ,  1.01473 ,  1.04859 ,  1.03946 ,
            1.0256  ,  1.02095 ,  1.02514 ,  1.05454 ,  1.08394 ,  1.09586 ,
            1.114   ,  1.11765 ,  1.14183 ,  1.16211 ,  1.13093 ,  1.13044 ,
            1.033   ,  0.969832,  0.92567 ,  0.925347,  0.809223,  0.783389,
            0.68838 ,  0.58904 ,  0.4897  ,  0.49    ,  0.      , -0.49    ,
           -0.4897  , -0.58904 , -0.68838 , -0.78772 , -0.783389, -0.832375,
           -0.881361, -0.930347, -1.05034 , -1.17034 , -1.13917 , -1.03465 ,
           -0.930138, -0.95338 , -0.976622, -1.01072 , -0.879327, -0.747939,
           -0.65062 , -0.5533  , -0.455981, -0.454   , -0.227   ,  0.      ,
            0.      ])}}}}}}}[0m


##### **HDF5**文件


```python
### 以testall.h5，它是一个HDF5格式的文件。
with File(f"{DATA_INPUT}/testall.h5", format= "HDF5" ,mode="r") as oid:
### 仅仅建立链接，而没有拿回数据
    output_entry = oid.read()
### 拿回所有数据
    output_data = oid.read().dump()
###获取namelist中的关键字key
logger.info(output_data.keys())
logger.info(output_data["coherent_wave"]["global_quantities"])

### 通过child获取某个子节点的值，而不需要把整个树读回来
# logger.info(output_entry.child("coherent_wave.current_tor").__value__)
```

    [0;34m2023-11-11 14:36:42,362 [    spdm]     INFO: dict_keys(['coherent_wave'])[0m
    [0;34m2023-11-11 14:36:42,363 [    spdm]     INFO: {'current_tor': 461821.31203568814,
     'frequency': 4600000000.0,
     'power': 19375694355948.902}[0m



```python
#### 写.nc文件
with File(f"{DATA_INPUT}/test-eq.hdf5", mode="w", format="HDF5") as oid:
    oid.write(eq_test)
with File(f"{DATA_INPUT}/test-eq.hdf5", format= "HDF5" ,mode="r") as oid: 
    test_data = oid.read().dump()
    logger.info(test_data.keys())
    logger.info(test_data["wall"])
```

    [0;34m2023-11-11 14:52:25,458 [    spdm]     INFO: dict_keys(['equilibrium', 'wall'])[0m
    [0;34m2023-11-11 14:52:25,459 [    spdm]     INFO: {'description_2d': [{'limiter': {'unit': [{'outline': {'r': array([1.35838, 1.35838, 1.35838, 1.36314, 1.4371 , 1.43721, 1.44164,
           1.4297 , 1.39169, 1.39151, 1.37929, 1.399  , 1.43623, 1.45919,
           1.47791, 1.54494, 1.61204, 1.63506, 1.66054, 1.66519, 1.6955 ,
           1.70668, 1.71388, 1.714  , 1.73649, 1.76324, 1.80199, 1.80237,
           1.93972, 1.97063, 2.07495, 2.1771 , 2.27925, 2.35   , 2.35   ,
           2.35   , 2.27925, 2.1771 , 2.07495, 1.9728 , 1.97063, 1.92059,
           1.87055, 1.82051, 1.79281, 1.76511, 1.75421, 1.67782, 1.60143,
           1.48426, 1.36709, 1.33132, 1.37874, 1.42615, 1.40528, 1.3844 ,
           1.36353, 1.35838, 1.35838, 1.35838, 1.35838]),
                                                           'z': array([ 0.      ,  0.227   ,  0.454   ,  0.455735,  0.798332,  0.798821,
            0.838195,  0.908908,  1.01426 ,  1.01473 ,  1.04859 ,  1.03946 ,
            1.0256  ,  1.02095 ,  1.02514 ,  1.05454 ,  1.08394 ,  1.09586 ,
            1.114   ,  1.11765 ,  1.14183 ,  1.16211 ,  1.13093 ,  1.13044 ,
            1.033   ,  0.969832,  0.92567 ,  0.925347,  0.809223,  0.783389,
            0.68838 ,  0.58904 ,  0.4897  ,  0.49    ,  0.      , -0.49    ,
           -0.4897  , -0.58904 , -0.68838 , -0.78772 , -0.783389, -0.832375,
           -0.881361, -0.930347, -1.05034 , -1.17034 , -1.13917 , -1.03465 ,
           -0.930138, -0.95338 , -0.976622, -1.01072 , -0.879327, -0.747939,
           -0.65062 , -0.5533  , -0.455981, -0.454   , -0.227   ,  0.      ,
            0.      ])}}]}}]}[0m


注：（1）其他的半结构化数据,YAML,JSON等，访问形式类似。

#### **SpDB**处理远程MDSplus数据库系统

在**SpDB**中，使用open_entry()建立统一的访问入口,支持远程MDSplus Server数据库的访问，及本地MDSplus的数据库中数据的访问。支持两个有用的功能：

（1）**不同数据源的自动集成**

SpDB中提供**open_entry**建立访问链接，**wall，pf，tf，magnetics**等被映射的数据均可以通过该链接入口访问。数据源来自于静态的XML文件，动态的MDS数据库中的不同tree：east,pcs_east,efit_east等

SpDB中数据的访问方式是按照IDS的树状结构逐层访问。

（2）**“懒惰加载”数据**

SpDB支持”懒惰加载“数据，因为，SpDB后台已经自动集成了不同数据源的数据，对应于不同的IDS条目中。所请求的条目或者某个条目中可能存储了大量的数据，如果请求的时候便立即从底层访问层后端读取所有数据，可能需要很长时间才能完成。通常情况下，用户可能只需要个别的数据子集，”懒惰加载”使得用户仅仅建立链接，只有在需要的时候才真正获取数据，这样会利于加速。

- **.child()**操作可以将链接指针移动到下一个树节点，建立新的链接，而不会获取数据
- **.get()**操作则直接将获得全部数据。

#### 加载基本环境


```python
### import基本环境
from spdm.data.Entry import open_entry
from spdm.utils.logger import logger
import fytok
import MDSplus
import os

### 指定mappingfile的路径
os.environ["SP_DATA_MAPPING_PATH"] = "${workdir}/fytok_data/mapping"
```

#### 访问远程EAST MDSplus数据库


```python
### 访问远程EAST MDS数据库中70754炮的数据，
shot_num = 70754
time_slice = 10
entry = open_entry("east+mdsplus://202.127.204.12?enable=efit_east&shot={shot_num}")
```

#### 访问远程本地MDSplus数据库


```python
# ### 访问本地MDSplus路径中中的70754炮的数据
shot_num = 70754
time_slice = 10
DATA_PATH = "/scratch/jupytertest/workspace_fytok/fytok_data"
entry = open_entry(f"east+mdsplus://{DATA_PATH}/mdsplus/~t/?shot=70745")
```

##### .child()支持“懒惰执行”


```python
### .child操作会将链接进一步指向wall
wall = entry.child("wall")
### 打印wall的类型，仍然是个entry
type(wall)
```




    spdm.data.Entry.EntryProxy




```python
### 继续移动链接到wall中的下一个子节点中,outline仍然是个entry
outline = entry.child("wall.description_2d[0].limiter.unit[0].outline")
### 获取outline的数据
print(outline.__value__)
```

    {'r': array([2.277, 2.273, 2.267, 1.94 , 1.94 , 1.802, 1.773, 1.751, 1.736,
           1.714, 1.707, 1.696, 1.665, 1.656, 1.635, 1.612, 1.478, 1.459,
           1.44 , 1.436, 1.399, 1.379, 1.392, 1.43 , 1.439, 1.442, 1.437,
           1.363, 1.361, 1.361, 1.361, 1.363, 1.421, 1.423, 1.422, 1.418,
           1.331, 1.367, 1.564, 1.597, 1.598, 1.624, 1.754, 1.765, 1.814,
           1.824, 1.825, 1.841, 1.971, 1.971, 2.267, 2.273, 2.277, 2.277,
           2.306, 2.328, 2.343, 2.35 , 2.35 , 2.35 , 2.343, 2.328, 2.306,
           2.277]), 'z': array([ 0.485,  0.485,  0.493,  0.809,  0.809,  0.926,  0.956,  0.993,
            1.033,  1.131,  1.162,  1.142,  1.117,  1.111,  1.096,  1.084,
            1.025,  1.021,  1.024,  1.026,  1.039,  1.049,  1.014,  0.909,
            0.873,  0.835,  0.799,  0.456,  0.454,  0.   , -0.454, -0.456,
           -0.725, -0.748, -0.749, -0.77 , -1.011, -0.977, -0.938, -0.941,
           -0.941, -0.961, -1.139, -1.17 , -0.959, -0.934, -0.932, -0.91 ,
           -0.783, -0.783, -0.493, -0.485, -0.485, -0.309, -0.244, -0.176,
           -0.106, -0.036,  0.   ,  0.036,  0.106,  0.176,  0.244,  0.309])}


##### .get()直接获取数据


```python
###.get()操作直接获取数据，以dict字典的形式返回
entry.get("wall")
```




    {'ids_properties': {'comment': {},
      'provider': 'Guo, Yong',
      'creation_date': '2020-10-12',
      'homogeneous_time': 2},
     'description_2d': {'type': {'name': 'equilibrium', 'index': 1},
      'limiter': {'type': {'name': 'limiter', 'index': 0},
       'unit': {'name': 'limiter',
        'closed': 1,
        'outline': {'r': array([2.277, 2.273, 2.267, 1.94 , 1.94 , 1.802, 1.773, 1.751, 1.736,
                1.714, 1.707, 1.696, 1.665, 1.656, 1.635, 1.612, 1.478, 1.459,
                1.44 , 1.436, 1.399, 1.379, 1.392, 1.43 , 1.439, 1.442, 1.437,
                1.363, 1.361, 1.361, 1.361, 1.363, 1.421, 1.423, 1.422, 1.418,
                1.331, 1.367, 1.564, 1.597, 1.598, 1.624, 1.754, 1.765, 1.814,
                1.824, 1.825, 1.841, 1.971, 1.971, 2.267, 2.273, 2.277, 2.277,
                2.306, 2.328, 2.343, 2.35 , 2.35 , 2.35 , 2.343, 2.328, 2.306,
                2.277]),
         'z': array([ 0.485,  0.485,  0.493,  0.809,  0.809,  0.926,  0.956,  0.993,
                 1.033,  1.131,  1.162,  1.142,  1.117,  1.111,  1.096,  1.084,
                 1.025,  1.021,  1.024,  1.026,  1.039,  1.049,  1.014,  0.909,
                 0.873,  0.835,  0.799,  0.456,  0.454,  0.   , -0.454, -0.456,
                -0.725, -0.748, -0.749, -0.77 , -1.011, -0.977, -0.938, -0.941,
                -0.941, -0.961, -1.139, -1.17 , -0.959, -0.934, -0.932, -0.91 ,
                -0.783, -0.783, -0.493, -0.485, -0.485, -0.309, -0.244, -0.176,
                -0.106, -0.036,  0.   ,  0.036,  0.106,  0.176,  0.244,  0.309])},
        '@id': '0'}},
      'vessel': {'unit': {'name': 'EAST',
        'identifier': 'EAST',
        'annular': {'outline_inner': {'closed': 1,
          'r': array([2.7286, 2.7069, 2.664 , 2.6007, 2.5178, 2.417 , 2.2997, 2.1681,
                 2.0244, 1.8708, 1.709 , 1.5435, 1.3902, 1.2814, 1.2402, 1.237 ,
                 1.237 , 1.237 , 1.237 , 1.237 , 1.237 , 1.237 , 1.237 , 1.237 ,
                 1.237 , 1.2402, 1.2814, 1.3902, 1.5435, 1.709 , 1.8708, 2.0244,
                 2.1681, 2.2997, 2.417 , 2.5178, 2.6007, 2.664 , 2.7069, 2.7286]),
          'z': array([ 0.083289,  0.24846 ,  0.40942 ,  0.56347 ,  0.708   ,  0.84058 ,
                  0.95892 ,  1.061   ,  1.1452  ,  1.2095  ,  1.2454  ,  1.2439  ,
                  1.1907  ,  1.075   ,  0.91857 ,  0.75173 ,  0.58468 ,  0.41763 ,
                  0.25058 ,  0.083526, -0.083526, -0.25058 , -0.41763 , -0.58468 ,
                 -0.75173 , -0.91857 , -1.075   , -1.1907  , -1.2439  , -1.2454  ,
                 -1.2095  , -1.1452  , -1.061   , -0.95892 , -0.84058 , -0.708   ,
                 -0.56347 , -0.40942 , -0.24846 , -0.083289])},
         'outline_outer': {'closed': 1,
          'r': array([2.844 , 2.8204, 2.7737, 2.7046, 2.6143, 2.5045, 2.3771, 2.2343,
                 2.0786, 1.9127, 1.7389, 1.5637, 1.3995, 1.2722, 1.2108, 1.199 ,
                 1.199 , 1.199 , 1.199 , 1.199 , 1.199 , 1.199 , 1.199 , 1.199 ,
                 1.199 , 1.2108, 1.2722, 1.3995, 1.5637, 1.7389, 1.9127, 2.0786,
                 2.2343, 2.3771, 2.5045, 2.6143, 2.7046, 2.7737, 2.8204, 2.844 ]),
          'z': array([ 0.089216,  0.26608 ,  0.43828 ,  0.6028  ,  0.75671 ,  0.89735 ,
                  1.0223  ,  1.1292  ,  1.2164  ,  1.282   ,  1.3197  ,  1.3165  ,
                  1.2605  ,  1.1444  ,  0.98288 ,  0.80532 ,  0.62636 ,  0.4474  ,
                  0.26844 ,  0.08948 , -0.08948 , -0.26844 , -0.4474  , -0.62636 ,
                 -0.80532 , -0.98288 , -1.1444  , -1.2605  , -1.3165  , -1.3197  ,
                 -1.282   , -1.2164  , -1.1292  , -1.0223  , -0.89735 , -0.75671 ,
                 -0.6028  , -0.43828 , -0.26608 , -0.089216])}},
        '@id': '0'}},
      '@id': '0'}}



##### SpDB中数据以字典形式在内存中直接交互


```python
### 打印IDS magnetics中的关键keys
shot_num = 70754
time_slice = 10
DATA_PATH = "/scratch/jupytertest/workspace_fytok/fytok_data"
entry = open_entry(f"east+mdsplus://{DATA_PATH}/mdsplus/~t/?shot=70745")
entry.get("magnetics]").keys()

```




    dict_keys(['ids_properties', 'b_field_pol_probe', 'flux_loop', 'ip'])



##### SpDB中list的访问


```python
### 例如，b_field_pol_probe探针有多个，以list形式存在
type(entry.get("magnetics")["b_field_pol_probe"])

```




    list




```python

### 每个探针下面是一个字典结构，获得其keys
entry.get("magnetics.b_field_pol_probe[0]").keys()

```




    dict_keys(['name', 'identifier', 'position', 'toroidal_angle', 'field', '@id'])




```python

entry.child("magnetics.b_field_pol_probe[0].position").__value__
```




    [{'r': 1.2905, 'z': 0.0, '@id': '*'}]



##### SpDB中数据按照树状结构层层访问


```python
### SpDB中数据按照层层路径进行访问:wall.description_2d[0].limiter.unit.outlin
### 获取outline的数据：
entry.get("wall.description_2d[0].limiter.unit.outline")
```




    {'r': array([2.277, 2.273, 2.267, 1.94 , 1.94 , 1.802, 1.773, 1.751, 1.736,
            1.714, 1.707, 1.696, 1.665, 1.656, 1.635, 1.612, 1.478, 1.459,
            1.44 , 1.436, 1.399, 1.379, 1.392, 1.43 , 1.439, 1.442, 1.437,
            1.363, 1.361, 1.361, 1.361, 1.363, 1.421, 1.423, 1.422, 1.418,
            1.331, 1.367, 1.564, 1.597, 1.598, 1.624, 1.754, 1.765, 1.814,
            1.824, 1.825, 1.841, 1.971, 1.971, 2.267, 2.273, 2.277, 2.277,
            2.306, 2.328, 2.343, 2.35 , 2.35 , 2.35 , 2.343, 2.328, 2.306,
            2.277]),
     'z': array([ 0.485,  0.485,  0.493,  0.809,  0.809,  0.926,  0.956,  0.993,
             1.033,  1.131,  1.162,  1.142,  1.117,  1.111,  1.096,  1.084,
             1.025,  1.021,  1.024,  1.026,  1.039,  1.049,  1.014,  0.909,
             0.873,  0.835,  0.799,  0.456,  0.454,  0.   , -0.454, -0.456,
            -0.725, -0.748, -0.749, -0.77 , -1.011, -0.977, -0.938, -0.941,
            -0.941, -0.961, -1.139, -1.17 , -0.959, -0.934, -0.932, -0.91 ,
            -0.783, -0.783, -0.493, -0.485, -0.485, -0.309, -0.244, -0.176,
            -0.106, -0.036,  0.   ,  0.036,  0.106,  0.176,  0.244,  0.309])}



#####  写GDSDKfile文件（待确认）


```python
# shot_num = 70754

# time_slice = 10

# OUTPUT_PATH ="/scratch/jupytertest/workspace_fytok/output"
# entry = open_entry(f"east+mdsplus://202.127.204.12?enable=efit_east&shot={shot_num}")

# data = {
#     "wall": entry.child(f"wall"),
#     "equilibrium": {"time_slice": [entry.child(f"equilibrium/time_slice/{time_slice}")]}
# }

# with File(f"{OUTPUT_PATH}/g{shot_num}.gfile", mode="w", format="geqdsk") as fid:
#     fid.write(data, description="equilibrium")
```
