import sys
import re
import os
import django
from django.conf import settings
from django.template import engines

PLUGIN_BASE_DIR = "pipeline_plugins/components/collections/sites"
JS_BASE_DIR = "pipeline_plugins/components/static/components/atoms"
TEST_FILE_BASE_DIR = "pipeline_plugins/tests/components/collections/sites"
DOCS_BASE_DIR = "pipeline_plugins/components/collections/sites"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [''],
    }
]

settings.configure(TEMPLATES=TEMPLATES)
django.setup()
django_engine = engines['django']


def create_plugin(v3_group_code, v3_plugin_code, v3_version, v3_plugin_env):
    # init文件模板
    with open("scripts/create_plugin_data/init.txt", "r", encoding="UTF-8") as f:
        init_content = f.read()
    # 插件后端文件模板
    with open("scripts/create_plugin_data/plugin_py.txt", "r", encoding="UTF-8") as f:
        plugin_content = f.read()
    # 插件前端文件模板
    with open("scripts/create_plugin_data/static_file.txt", "r", encoding="UTF-8") as f:
        static_content = f.read()
    # 插件单元测试文件模板
    with open("scripts/create_plugin_data/test_file.txt", "r", encoding="UTF-8") as f:
        test_content = f.read()
    # 说明文档文件模板
    with open("scripts/create_plugin_data/docs_file.txt", "r", encoding="UTF-8") as f:
        docs_content = f.read()

    # 判断输入是否合法
    if v3_plugin_env not in ["open", "ieod"]:
        print("The plugin version env{} is wrong. Please input again ".format(v3_plugin_env))
        sys.exit(0)
    if not re.match(r"v[0-9][.][0-9]", v3_version).group():
        print("The plugin version{} format is wrong. Please input again ".format(v3_plugin_env))
        sys.exit(0)

    # 创建group文件夹
    group_dir = "{base_file}/{plugin_env}/{group_code}".format(base_file=PLUGIN_BASE_DIR,
                                                               plugin_env=v3_plugin_env,
                                                               group_code=v3_group_code)
    if not os.path.exists(group_dir):
        os.makedirs(group_dir)
        with open("{group_dir}/__init__.py".format(group_dir=group_dir), "a", encoding="utf-8") as f:
            f.write(init_content)

    # 创建插件后端代码
    plugin_dir = "{group_dir}/{plugin_code}".format(group_dir=group_dir, plugin_code=v3_plugin_code)
    plugin_file = "{plugin_dir}/{version}.py".format(plugin_dir=plugin_dir, version=v3_version.replace(".", "_"))
    # 前端代码位置
    if v3_plugin_env == "open":
        js_dir = "{v3_group_code}/{v3_plugin_code}".format(v3_group_code=v3_group_code, v3_plugin_code=v3_plugin_code)
    else:
        js_dir = "sites/ieod/{v3_group_code}/{v3_plugin_code}".format(v3_group_code=v3_group_code,
                                                                      v3_plugin_code=v3_plugin_code)
    plugin_template_dir = {
        "v3_class_name": "".join([word.capitalize() for word in v3_plugin_code.split("_")]),
        "v3_plugin_code": "{v3_group_code}_{v3_plugin_code}".format(v3_group_code=v3_group_code,
                                                                    v3_plugin_code=v3_plugin_code),
        "version": v3_version,
        "static_file_path": js_dir
    }
    if not os.path.exists(plugin_dir):
        os.makedirs(plugin_dir)
        with open("{plugin_dir}/__init__.py".format(plugin_dir=plugin_dir), "a", encoding="utf-8") as f:
            f.write(init_content)
        with open(plugin_file, "a", encoding="utf-8") as f:
            template = django_engine.from_string(plugin_content)
            f.write(template.render(plugin_template_dir))
    else:
        if os.path.isfile(plugin_file):
            print("{}  is exist！".format(plugin_file))
            sys.exit(0)
        with open(plugin_file, "a", encoding="utf-8") as f:
            template = django_engine.from_string(plugin_content)
            f.write(template.render(plugin_template_dir))

    # 创建前端代码文件
    if v3_plugin_env == "open":
        static_group_dir = "{base_file}/{group_code}".format(base_file=JS_BASE_DIR, group_code=v3_group_code)
    else:
        static_group_dir = "{base_file}/sites/ieod/{group_code}".format(base_file=JS_BASE_DIR,
                                                                        group_code=v3_group_code)
    if not os.path.exists(static_group_dir):
        os.makedirs(static_group_dir)

    static_dir = "{static_group_dir}/{v3_plugin_code}".format(static_group_dir=static_group_dir,
                                                              v3_plugin_code=v3_plugin_code)
    static_file = "{static_dir}/{version}.js".format(static_dir=static_dir, version=v3_version.replace(".", "_"))
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
        template = django_engine.from_string(static_content)
        with open(static_file, "a", encoding="utf-8") as f:
            f.write(template.render({"v3_plugin_code": "{v3_group_code}_{v3_plugin_code}".
                                    format(v3_group_code=v3_group_code, v3_plugin_code=v3_plugin_code)}))
    else:
        if os.path.isfile(static_file):
            print("{}  is exist！".format(static_file))
            sys.exit(0)
        template = django_engine.from_string(static_content)
        with open(static_file, "a", encoding="utf-8") as f:
            f.write(template.render({"v3_plugin_code": "{v3_group_code}_{v3_plugin_code}".
                                    format(v3_group_code=v3_group_code, v3_plugin_code=v3_plugin_code)}))

    # 创建单元测试文件
    test_group_dir = "{test_file_base_dir}/{plugin_env}/{group_code}_test".format(test_file_base_dir=TEST_FILE_BASE_DIR,
                                                                                  group_code=v3_group_code,
                                                                                  plugin_env=v3_plugin_env)
    if not os.path.exists(test_group_dir):
        os.makedirs(test_group_dir)
        with open("{group_dir}/__init__.py".format(group_dir=test_group_dir), "a", encoding="utf-8") as f:
            f.write(init_content)

    test_group_file = "{test_group_dir}/{v3_plugin_code}.py".format(test_group_dir=test_group_dir,
                                                                    v3_plugin_code="test_{}".format(v3_plugin_code))
    test_file_dir = {
        "v3_plugin_path": plugin_file[:-3].replace('/', '.'),
        "component": "".join([word.capitalize() for word in v3_plugin_code.split("_")])
    }

    if os.path.isfile(test_group_file):
        print("{}  is exist！".format(test_group_file))
        sys.exit(0)
    template = django_engine.from_string(test_content)
    with open(test_group_file, "a", encoding="utf-8") as f:
        f.write(template.render(test_file_dir))

    # 创建说明文档文件
    docs_group_dir = "{base_file}/{v3_plugin_env}/docs/{group_code}".format(base_file=DOCS_BASE_DIR,
                                                                            v3_plugin_env=v3_plugin_env,
                                                                            group_code=v3_group_code)
    if not os.path.exists(static_group_dir):
        os.makedirs(static_group_dir)

    docs_dir = "{docs_group_dir}/{v3_plugin_code}".format(docs_group_dir=docs_group_dir,
                                                          v3_plugin_code=v3_plugin_code)
    docs_file = "{docs_dir}/{version}.md".format(docs_dir=docs_dir, version=v3_version.replace(".", "_"))
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
        template = django_engine.from_string(docs_content)
        with open(docs_file, "a", encoding="utf-8") as f:
            f.write(template.render({"group_code": v3_group_code, "plugin_code": v3_plugin_code}))
    else:
        if os.path.isfile(docs_file):
            print("{}  is exist！".format(docs_file))
            sys.exit(0)
        template = django_engine.from_string(docs_content)
        with open(docs_file, "a", encoding="utf-8") as f:
            f.write(template.render({"group_code": v3_group_code, "plugin_code": v3_plugin_code}))


if __name__ == "__main__":
    """
    python -m scripts.create_new_plugin group_code plugin_code version plugin_env
    eg. python -m scripts.create_new_plugin cc create_set v1.0 open
    """

    group_code = sys.argv[1]
    plugin_code = sys.argv[2]
    version = sys.argv[3]
    plugin_env = sys.argv[4]

    create_plugin(group_code, plugin_code, version, plugin_env)
