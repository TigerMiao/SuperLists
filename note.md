# 一、搭建开发环境
先创建项目目录superlist。

## 1. 编写功能测试
编写第一个功能测试，验证开发环境是否已经搭建完成，创建文件 functional_test.py:

functional_test.py

    from selenium import webdriver

    browser = webdriver.Firefox()
    browser.get('http://localhost:8000')

    assert 'Django' in browser.title

这段代码的作用为：

* 启动一个 Selenium webdriver，打开一个真正的 Firefox 浏览器窗口；
* 在这个浏览器中打开期望的网页；
* 检查（测试断言）这个网页的标题中是否包含单词“Django”。

运行该功能测试：

    python function_tests.py

现在一般会得到一个失败的测试。这意味着，我们目前的开发环境还没有配置完成。

## 2. 创建虚拟环境
如果virtualenv还没有安装，可以先执行以下命令安装：

    pip3 install --user virtualenv

然后，进入项目目录后执行以下命令创建虚拟环境：

    python3 -m venv myvenv

接着执行下面的目录激活虚拟环境：

    source myvenv/bin/activate

如果要停止虚拟环境，可执行下面的命令：

    deactivate

## 3. 安装Django并创建项目
创建并激活虚拟环境后，就可以安装Django了：

    pip install Django

查看 Django 版本：

    python -m django --version

然后创建名为superlist的项目：

    django-admin.py startproject superlists .

## 4. 安装 Selenium
Selenium 是浏览器自动化工具，我们要用它来驱动功能测试。

    pip install --upgrade selenium

## 5. 运行功能测试
首先，运行开发服务器：

    python manage.py runserver

再次运行测试：

    python functional_tests.py

如果开发环境配置成功，测试就会运行通过。

## 6. 创建Git版本库
在项目目录中执行以下命令：

    git init

编辑.gitignore文件，如下：

    *.pyc
    __pycache__
    myvenv
    db.sqlite3
    .DS_Store
    .vscode

然后把代码递交到git仓库：

    git status
    git add --all .
    git commit -m "Initial commit."

## 7. 推送代码到GitHub上
在GitHub.com网站创建一个新的仓库，命名为"SuperLists"。保持"initialise with a README“复选框未选中状态，.gitignore选项为无，让License设置为无。

拷贝仓库克隆URL，然后我们需要把电脑上的Git仓库和GitHub上的关联起来。

    $ git remote add origin https://github.com/TigerMiao/SuperLists.git
    $ git push -u origin master

**注意**： 如果在GitHub创建仓库时选中了生成README文件，需要先执行下面的命令：

    git pull --rebase origin master

执行这个命令后会先将GitHub上的仓库先同步到本地，然后才能将本地仓库上传到GitHub。

# 二、使用 unittest 模块扩展功能测试
第一个功能测试只是检查 Django “可用了”，下面才是真正开始检查在真实的网站页面中的内容。

## 1. 使用功能测试驱动开发一个最简可用的应用
打开 functional_tests.py，编写一个类似下面的用户故事（user story)：

functional_test.py

    from selenium import webdriver

    browser = webdriver.Firefox()

    # 伊迪丝听说有一个很酷的在线待办事项应用 # 她去看了这个应用的首页 browser.get('http://localhost:8000')
    # 她注意到网页的标题和头部都包含“To-Do”这个词 
    assert 'To-Do' in browser.title

    # 应用邀请她输入一个待办事项

    # 她在一个文本框中输入了“Buy peacock feathers(”购买孔雀羽毛)
    # 伊迪丝的爱好是使用假蝇做饵钓鱼 
    
    # 她按回车键后，页面更新了
    # 待办事项表格中显示了“1: Buy peacock feathers”
    
    # 页面中又显示了一个文本框，可以输入其他的待办事项
    # 她输入了“Use peacock feathers to make a fly(”使用孔雀羽毛做假蝇) 
    # 伊迪丝做事很有条理

    # 页面再次更新，她的清单中显示了这两个待办事项 
    
    # 伊迪丝想知道这个网站是否会记住她的清单

    # 她看到网站为她生成了一个唯一的URL 
    # 而且页面中有一些文字解说这个功能

    # 她访问那个URL，发现她的待办事项列表还在 
    
    # 她很满意，去睡觉了

    browser.quit()

# 2. Python标准库中的 unittest 模块
标准库中的 unittest 模块提供了测试的解决方法，在 functional_tests.py 中写入如下代码：

functional_test.py

    from selenium import webdriver
    import unittest

    class NewVisitorTest(unittest.TestCase): #➊ 
    
        def setUp(self): #➋
            self.browser = webdriver.Firefox()

        def tearDown(self): #➌ 
            self.browser.quit()

        def test_can_start_a_list_and_retrieve_it_later(self): #➍ 
            # 伊迪丝听说有一个很酷的在线待办事项应用
            # 她去看了这个应用的首页 
            self.browser.get('http://localhost:8000')

            # 她注意到网页的标题和头部都包含“To-Do”这个词 
            self.assertIn('To-Do', self.browser.title) #➎ 
            self.fail('Finish the test!') #➏

            # 应用邀请她输入一个待办事项 
            [......其余的注释和之前一样]

    if __name__ == '__main__': #➐ 
        unittest.main(warnings='ignore') #➑

➊ 测试类继承自 unittest.TestCase。

➋ ➌ setUp 和 tearDown 是特殊的方法，分别在各个测试方法之前和之后运行。

➍ 测试的主要代码写在名为 test_can_start_a_list_and_retrieve_it_later 的方法中。 名字以 test_ 开头的方法都是测试方法，由测试运行程序运行。

➎ 使用 self.assertIn 代替 assert 编写测试断言。unittest 提供了很多这种用于编写测 试断言的辅助函数，如 assertEqual、assertTrue 和 assertFalse 等。更多断言辅助函数参见 [unittest 的文档](http://docs.python.org/3/library/unittest.html)。

➏ 不管怎样，self.fail 都会失败，生成指定的错误消息。使用这个方法提醒测试结束了。

➐ 最后是 if __name__ == '__main__' 分句，Python 脚本使用这个语句检查自己是否在命令行中运行，而不是在其他脚本中导入。 我们调用 unittest.main() 启动 unittest 的测试运行程序，这个程序会在文件中自动查找测试类和方法，然后运行。

➑ warnings='ignore' 的作用是禁止抛出 ResourceWarning 异常。

运行该功能测试会产生一个预期失败。

# 3. 提交

    git status
    git diff
    git commit -a -m "使用注释编写规格的首个功能测试， 而且使用了 unittest。"

**TDD概念**:

* 用户故事（user story）

    从用户的角度描述应用应该如何运行。用来组织功能测试。

* 预期失败

    意料之中的失败。

# 三、使用单元测试测试简单的首页
## 1. 第一个Django应用，第一个单元测试
Django以“应用”的形式组织代码，一个项目可以放多个应用，而且可以使用其他人开发的第三方应用，也可以重用自己在其他项目中开发的应用。

为待办事项清单创建一个应用：

    python manage.py startapp lists

这个命令会在 SuperLists 文件夹中创建子文件夹lists，与 superslists 子文件夹相邻，并在 lists中创建一些文件，用来保存模型、视图以及测试：

## 2. 单元测试及其与功能测试的区别
从用户的角度描述应用应该如何运行。用来组织功能测试。

我们遵从 TDD 方法同时使用这两种类型测试应用。采用的工作流程大致如下：

(1) 先写功能测试，从用户的角度描述应用的新功能。

(2) 功能测试失败后，想办法编写代码让它通过(或者说至少让当前失败的测试通过)。此时，使用一个或多个单元测试定义希望代码实现的效果，保证为应用中的每一行代码
 (至少)编写一个单元测试。

(3) 单元测试失败后，编写最少量的应用代码，刚好让单元测试通过。有时，要在第 2 步和 第 3 步之间多次往复，直到我们觉得功能测试有一点进展为止。

(4) 然后，再次运行功能测试，看能否通过，或者有没有进展。这一步可能促使我们编写一 些新的单元测试和代码等。

由此可以看出，这整个过程中，功能测试站在高层驱动开发，而单元测试则从低层驱动我 们做些什么。

功能测试的作用是帮助你开发具有所需功能的应用，还能保证你不会无意中 破坏这些功能。单元测试的作用是帮助你编写简洁无错的代码。

## 3. Django中的单元测试
打开文件 lists/tests.py：

lists/tests.py

    from django.test import TestCase

    # Create your tests here.

Django 建议我们使用 TestCase 的一个特殊版本。这个版本由 Django 提供，是标准版 unittest.TestCase 的增强版，添加了一些 Django 专用的功能。

先编写一个会失败的冒烟测试：

lists/tests.py

    from django.test import TestCase

    class SmokeTest(TestCase):

        def test_bad_maths(self):
             self.assertEqual(1 + 1, 3)

运行单元测试：

    python manage.py test

然后提交代码：

    git status  # 会显示一个消息，说没跟踪lists/
    git add lists
    git diff --staged # 会显示将要提交的内容差异
    git commit -m"Add app for lists, with deliberately failing unit test"

## 4. Django中的MVC、URL和视图函数
总的来说，Django 遵守了经典的“模型 - 视图 - 控制器”(Model-View-Controller，MVC) 模式，但并没严格遵守。Django 确实有模型，但视图更像是控制器，模板其实才是视图。可以参考 Django [常见问题解答](https://docs.djangoproject.com/en/1.7/faq/general/)中的详细说明。

抛开这些，Django 和任何一种 Web 服务器一样，其主要任务是决定用户访问网站中的某 个 URL 时做些什么。Django 的工作流程有点儿类似下述过程:

(1) 针对某个 URL 的 HTTP 请求进入;

(2) Django 使用一些规则决定由哪个视图函数处理这个请求(这一步叫作解析 URL); 

(3) 选中的视图函数处理请求，然后返回 HTTP 响应。

因此要测试两件事情：

* 能否解析网站根路径(“/”)的 URL，将其对应到我们编写的某个视图函数上?
* 能否让视图函数返回一些 HTML，让功能测试通过?

先编写第一个单元测试。打开 lists/tests.py，把之前编写的冒烟测试改成如下代码:

lists/tests.py

    from django.urls import resolve 
    from django.test import TestCase
    from lists.views import home_page #➊

    class HomePageTest(TestCase):
    
        def test_root_url_resolves_to_home_page_view(self): 
            found = resolve('/') #➋ 
            self.assertEqual(found.func, home_page) #➌

这段代码的意思是：

➊ 这是接下来要定义的视图函数，其作用是返回所需的 HTML。从
import 语句可以看出，要把这个函数保存在文件 lists/views.py 中。

➋ ➌ resolve 是 Django 内部使用的函数，用于解析 URL，并将其映射到相应的视图函数
上。检查解析网站根路径“/”时，是否能找到名为 home_page 的函数。

运行测试会得到试图导入未定义函数的异常：

    $ python3 manage.py test
    ImportError: cannot import name 'home_page'

预料之中的异常也算是预期失败。

## 5. 编写应用代码
使用 TDD 时要耐着性子，步步为营。尤其是学习和起步阶段，一次只能修改(或添加)一行代码。每一次修改的代码要尽量少，让失败的测试通过即可。

在 lists/views.py 中写入下面的代码：

lists/views.py

    from django.shortcuts import render
    
    # 在这儿编写视图 
    home_page = None

再次运行测试：

    python manage.py test

测试失败。失败的原因是尝试解析“/”时，Django抛出了404错误，也即是说，Django无法找到“/”的URL映射。

## 6. urls.py
Django 在 urls.py 文件中定义如何把 URL 映射到视图函数上。修改 superlists/urls.py文件：

superlists/urls.py

    from django.contrib import admin
    from django.urls import path
    from lists import views

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', views.home_page, name='home')
    ]

然后再次运行测试:

    django.core.exceptions.ViewDoesNotExist: Could not import
    lists.views.home_page. View is not callable.

单元测试把地址“/”和文件 lists/views.py 中的 home_page = None 连接起来了，现在测试抱 怨 home_page 无法调用，即不是函数。修改文件 lists/views.py，把 home_page 从None变成真正的函数。

lists/views.py

    from django.shortcuts import render

    # 在这儿编写视图 
    def home_page():
        pass

再次运行测试，测试通过。

提交代码：

    git diff # 会显示urls.py、tests.py和views.py中的变动
    git commit -am"First unit test and url mapping, dummy view"

把 a 和 m 标志放在一起使用，意思是添加所有已跟踪文件中的改动，而且使用命令行中输入的提交消息。

## 7. 为视图编写单元测试
打开 lists/tests.py，添加一个新测试方法：

lists/tests.py

    from django.urls import resolve 
    from django.test import TestCase 
    from django.http import HttpRequest

    from lists.views import home_page 

    class HomePageTest(TestCase):

        def test_root_url_resolves_to_home_page_view(self): 
            found = resolve('/') 
            self.assertEqual(found.func, home_page)

        def test_home_page_returns_correct_html(self): 
            request = HttpRequest()
            response = home_page(request)
            html = response.content.decode('utf8') 
            self.assertTrue(html.startswith('<html>')) 
            self.assertIn('<title>To-Do lists</title>', html) 
            self.assertTrue(html.endswith('</html>'))


* 创建了一个 HttpRequest 对象，用户在浏览器中请求网页时，Django 看到的就是
HttpRequest 对象。

* 把这个 HttpRequest 对象传给 home_page 视图，得到响应。

* 接着，我们提取响应中的 .content。这些是原始字节，将被发送到用户浏览器的1和0。我们调用 .decode() 把它们转换成 HTML 字符串。

* 希望响应以 `<html>` 标签开头，并在结尾处关闭该标签。

* 希望响应中有一个 `<title>` 标签，其内容包含单词“To-Do”——因为在功能测试中
做了这项测试。

## “单元测试/编写代码”循环
(1) 在终端里运行单元测试，看它们是如何失败的;

(2) 在编辑器中改动最少量的代码，让当前失败的测试通过。 

然后不断重复。

想保证编写的代码无误，每次改动的幅度就要尽量小。这么做才能确保每一部分代码都有 对应的测试监护。乍看起来工作量很大，但熟练后速度还是很快的。

* 小幅代码改动:

lists/views.py

    def home_page(request):
        pass

* 运行测试:

    self.assertTrue(response.content.startswith(b'<html>'))
    AttributeError: 'NoneType' object has no attribute 'content'

* 编写代码:

lists/views.py

    from django.http import HttpResponse
    # 在这儿编写视图
    def home_page(request):
        return HttpResponse()

* 再运行测试:

    self.assertTrue(response.content.startswith(b'<html>'))
    AssertionError: False is not true

* 再编写代码:

lists/views.py

    def home_page(request):
        return HttpResponse('<html>')

* 运行测试:

    AssertionError: b'<title>To-Do lists</title>' not found in b'<html>'

* 编写代码:

lists/views.py

    def home_page(request):
        return HttpResponse('<html><title>To-Do lists</title>')

* 运行测试:

    self.assertTrue(response.content.endswith(b'</html>'))
    AssertionError: False is not true

* 最后一击:

    def home_page(request):
        return HttpResponse('<html><title>To-Do lists</title></html>')

* 运行测试：

    python manage.py test

测试通过。

运行功能测试：

    python3 functional_tests.py

测试通过。

提交代码：

    git diff # 会显示tests.py中的新测试方法，以及views.py中的视图
    git commit -am"Basic view now returns minimal HTML"

    git log --oneline

## 有用的命令和概念
* 启动 Django 的开发服务器 

    python manage.py runserver

* 运行功能测试

    python functional_tests.py

* 运行单元测试

    python manage.py test

* “单元测试 / 编写代码”循环

    (1) 在终端里运行单元测试;

    (2) 在编辑器中改动最少量的代码; 

    (3) 重复上两步。

# 四、编写这些测试有什么用
## 1. 使用 Selenium 测试用户交互
打开 functional_tests.py 文件，扩充其中的功能测试:

functional_tests.py

    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import time
    import unittest

    class NewVisitorTest(unittest.TestCase):

        def setUp(self):
            self.browser = webdriver.Firefox()
            self.browser.implicitly_wait(3)

        def tearDown(self):
            self.browser.quit()

        def test_can_start_a_list_and_retrieve_it_later(self): 
            # 伊迪丝听说有一个很酷的在线待办事项应用
            # 她去看了这个应用的首页 
            self.browser.get('http://localhost:8000')

            # 她注意到网页的标题和头部都包含“To-Do”这个词 
            self.assertIn('To-Do', self.browser.title)
            header_text = self.browser.find_element_by_tag_name('h1').text 
            self.assertIn('To-Do', header_text)

            # 应用邀请她输入一个待办事项
            inputbox = self.browser.find_element_by_id('id_new_item') 
            self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
            )

            # 她在一个文本框中输入了“Buy peacock feathers(”购买孔雀羽毛)
            # 伊迪丝的爱好是使用假蝇做鱼饵钓鱼 
            inputbox.send_keys('Buy peacock feathers')

            # 她按回车键后，页面更新了
            # 待办事项表格中显示了“1: Buy peacock feathers” 
            inputbox.send_keys(Keys.ENTER)
            time.sleep(1)

            table = self.browser.find_element_by_id('id_list_table')
            rows = table.find_elements_by_tag_name('tr')
            self.assertTrue(
                any(row.text == '1: Buy peacock feathers' for row in rows)
            )

            # 页面中又显示了一个文本框，可以输入其他的待办事项
            # 她输入了“Use peacock feathers to make a fly(”使用孔雀羽毛做假蝇)
            # 伊迪丝做事很有条理 
            self.fail('Finish the test!')

            # 页面再次更新，她的清单中显示了这两个待办事项 
            [...]

* 我们使用了 Selenium 提供的几个用来查找网页内容的方法:find_element_by_tag_name，find_element_by_id 和 find_elements_by_tag_name(注意有个 s，也就是说这个方法会返回 多个元素)。

* 还使用了 send_keys，这是 Selenium 在输入框中输入内容的方法。

* 还使用了 Keys 类，它的作用是发送回车键等特殊的按键，还有 Ctrl 等修改键。

* 当我们按回车键时，页面会刷新。time.sleep 是用来确保当我们验证页面时，浏览器已经加载完成。这被称作“explicit wait”。

**小心 Selenium 中 find_element_by... 和 find_elements_by... 这两类函 数的区别。前者返回一个元素，如果找不到就抛出异常;后者返回一个列 表，这个列表可能为空**

* any 函数是 Python 中的原生函数。any函数的参数是个生成器表达式（generator expression），类似于列表推导（list comprehension）。

运行功能测试：

    python3 functional_tests.py

测试报错在页面中找不到 `<h1>` 元素。

提交代码：

    git diff # 会显示对functional_tests.py的改动
    git commit -am "Functional test now checks we can input a to-do item"

## 2. 遵守“不测试常量”规则，使用模板解决这个问题
一般来说，单元测试的规则之一是“不测试常量”。以文本形式测试 HTML 很大程度上就是测试常量。

单元测试要测试的其实是逻辑、流程控制和配置。编写断言检测 HTML 字符串中是否有指定的字符序列，不是单元测试应该做的。

而且，在 Python 代码中插入原始字符串真的不是处理 HTML 的正确方式。我们有更好的方法，那就是使用模板。

### 使用模板重构
先把 HTML 字符串提取出来写入单独的文件。新建用于保存模板的文件夹 lists/templates/lists，然后新建文件 lists/templates/home.html，再把 HTML 写入这个文件。

lists/templates/lists/home.html

    <html>
        <title>To-Do lists</title>
    </html>

接下来修改视图函数:

lists/views.py

    from django.shortcuts import render
        def home_page(request):
            return render(request, 'lists/home.html')


现在不自己构建 HttpResponse 对象了，转而使用 Django 中的 render 函数。这个函数的第一个参数是请求对象，第二个参数是渲染的模板名。

运行测试，测试失败，测试无法找到模板。原因是还没有正式在 Django 中注册 lists 应用。打开 settings.py，找到变量 INSTALLED_APPS，把 lists 加进去:

superlists/settings.py

    # Application definition
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'lists',
    )

再次运行测试，还是无法通过。原因是转用模板后在响应的末尾引入了一个额外的空行(\n)。按下面的方式修改可以让测试通过:

lists/tests.py

    self.assertTrue(html.strip().endswith('</html>'))

再次运行测试，测试通过。

### Django测试客户端
现在可以修改测试，不再测试 常量，检查是否渲染了正确的模板。

一种方法是在测试中手动渲染模板，然后和视图返回内容进行比较。Django中有个函数叫 render_to_string 可以提供帮助：

lists/tests.py

    from django.template.loader import render_to_string 
    [...]

    def test_home_page_returns_correct_html(self): 
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8') 
        expected_html = render_to_string('lists/home.html') 
        self.assertEqual(html, expected_html)

第二种方法，Django提供了一个测试客户端，其中有用于测试模板的工具。

lists/tests.py

    def test_home_page_returns_correct_html(self): 
        response = self.client.get('/')

        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))

        self.assertTemplateUsed(response, 'lists/home.html')
    
* 不是手动创建 HttpResponse 对象，而是直接调用视图函数。我们调用的是 self.client.get，然后把要测试的 URL 传递给它。

* 我们现在把旧的测试留在那里，只是为了确保一切都是按照我们的想法进行。

* .assertTemplateUsed 是 Django TestCase 类给我们提供的测试方法。它让我们检查使用什么模板来渲染响应，它只对测试客户端检索的响应起作用。

运行测试，测试通过。

现在可以把旧的断言删掉了。我们也可以删掉旧的 test_root_url_resolves_to_home_page_view 测试，因为 Django 测试客户端已经隐含的对它进行了测试。

lists/tests.py

    def test_home_page_returns_correct_html(self): 
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

提交代码：

    git status # 会看到tests.py，views.py，settings.py，以及新建的templates文件夹 git add . # 还会添加尚未跟踪的templates文件夹
    git diff --staged # 审查我们想提交的内容
    git commit -m"Refactor home page view to use a template"

## 3. 修改首页
修改模板让功能测试通过：

lists/templates/lists/home.html

    <html>
        <head>
            <title>To-Do lists</title>
        </head>

        <body>
            <h1>Your To-Do list</h1>
            <input id="id_new_item" placeholder="Enter a to-do item" />
            <table id="id_list_table">
            </table>
        </body>
    </html>

提交代码：

    git diff
    git commit -am"Front page HTML now generated from a template"

# 五、保存用户输入
## 1. 编写表单，发送POST请求
若想让浏览器发送 POST 请求，要给 <input> 元素指定 name= 属性，然后把它放在 <form> 标签中，并为 <form> 标签指定 method="POST" 属性，这样浏览器才能向服务器发送 POST 请求。调整一下 lists/templates/lists/home.html 中的模板:

lists/templates/lists/home.html

    <h1>Your To-Do list</h1> 
    <form method="POST">
        <input name="item_text" id="id_new_item" placeholder="Enter a to-do item" /> 
    </form>
    <table id="id_list_table">

现在运行功能测试，会看到一个晦涩难懂、预料之外的错误.

如果功能测试出乎意料地失败了，可以做下面几件事，找出问题所在:
* 添加 print 语句，输出页面中当前显示的文本是什么; 
* 改进错误消息，显示当前状态的更多信息;
* 亲自手动访问网站;
* 在测试执行过程中使用 time.sleep 暂停。

在错误发生位置的前面加上 time.sleep:

functional_tests.py

    # 按回车键后，页面更新了
    # 待办事项表格中显示了"1: Buy peacock feathers" inputbox.send_keys(Keys.ENTER)
    import time
    time.sleep(10)
    table = self.browser.find_element_by_id('id_list_table')

再次运行功能测试，显示有 CSRF（跨站请求伪造）错误。Django 针对 CSRF 的保护措施是在生成的每个表单中放置一个自动生成的令牌，通过这个令牌判断 POST 请求是否来自同一个网站。

使用“模板标签” (template tag)添加 CSRF 令牌。模板标签的句法是花括号和百分号形式，即 {% ... %}。

lists/templates/lists/home.html

    <form method="POST">
        <input name="item_text" id="id_new_item" placeholder="Enter a to-do item" />
        {% csrf_token %}
    </form>

渲染模板时，Django 会把这个模板标签替换成一个 <input type="hidden"> 元素，其值是
CSRF 令牌。现在运行功能测试，会看到一个预期失败:

    AssertionError: False is not true : New to-do item did not appear in table

可以看到，提交表单后新添加的 待办事项不见了，页面刷新后又显示了一个空表单。这是因为还没连接服务器让它处理 POST 请求，所以服务器忽略请求，直接显示常规首页。

其实，现在可以缩短 time.sleep 的时间了:

functional_tests.py

    # 待办事项表格中显示了“1: Buy peacock feathers”
    inputbox.send_keys(Keys.ENTER)

    import time
    time.sleep(1)

    table = self.browser.find_element_by_id('id_list_table')

## 2. 在服务器中处理POST请求
还没为表单指定 action= 属性，因此提交表单后默认返回之前渲染的页面，即“/”，这个
页面由视图函数 home_page 处理。

打开文件 lists/tests.py，在 HomePageTest 类中添加一个新方法：

lists/tests.py

    def test_uses_home_template(self):
        response = self.client.get('/') 
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())

要实现 POST，我们调用了 self.client.post，并且传递了一个 data 参数，该参数包含了我们想发送的表单数据。然后再检查 POST 请求渲染得到的 HTML 中是否有指定的文本。运行测试后，会看到预期的失败:

    python3 manage.py test
    [...]
    AssertionError: 'A new list item' not found in '<html> [...]

为了让测试通过，可以添加一个 if 语句，为 POST 请求提供一个不同的代码执行路径。

    from django.http import HttpResponse 
    from django.shortcuts import render

    def home_page(request):
        if request.method == 'POST':
            return HttpResponse(request.POST['item_text']) 
        return render(request, 'lists/home.html')

## 3. 把 Python 变量传入模板中渲染
把 Python 变量传入模板使用的符号是 {{ ... }}：

    <body>
        <h1>Your To-Do list</h1> 
        <form method="POST">
            <input name="item_text" id="id_new_item" placeholder="Enter a to-do item" />
            {% csrf_token %}
        </form>

        <table id="id_list_table">
            <tr><td>{{ new_item_text }}</td></tr>
        </table> 
    </body>

调整单元测试，以便检查我们是否还在使用模板：

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode()) 
        self.assertTemplateUsed(response, 'lists/home.html')

运行测试会产生预期的失败：

    AssertionError: No templates used to render the response

然后重写视图函数，把 POST 请求中的参数传入模板。render 函数使用一个字典把它作为第三个参数，将模板变量名映射到它们的值。

lists/views.py

    def home_page(request):
        return render(request, 'home.html', {
            'new_item_text': request.POST['item_text'],
        })

然后再运行单元测试：

    ERROR: test_home_page_returns_correct_html (lists.tests.HomePageTest)
    [...]
        'new_item_text': request.POST['item_text'],
    KeyError: 'item_text'

看到的是意料之外的失败。

这次失败的修正方法如下:

lists/views.py

    def home_page(request):
        return render(request, 'home.html', {
            'new_item_text': request.POST.get('item_text', ''),
        })

这个单元测试现在应该可以通过了。

错误消息没太大帮助。使用另一种功能测试的调试技术:改进错误消息。

functional_tests.py

    self.assertTrue(
        any(row.text == '1: Buy peacock feathers' for row in rows),
        f"New to-do item did not appear in table. Contents were:\n{table.text}"
    )

你只需要在字符串前加上f，就可以使用大括号语法插入局部变量。

改进后，测试给出了更有用的错误消息:

    AssertionError: False is not true : New to-do item did not appear in table.
    Contents were:
    Buy peacock feathers

修改功能测试：

functional_tests.py

    self.assertIn('1: Buy peacock feathers', [row.text for row in rows])

修改模板文件：

lists/templates/lists/home.html

    <tr><td>1: {{ new_item_text }}</td></tr>

现在扩充功能测试，检查表格中添加的第二个待办事项：

functional_tests.py

    # 页面中还有一个文本框，可以输入其他的待办事项
    # 她输入了“Use peacock feathers to make a fly(”使用孔雀羽毛做假蝇) # 伊迪丝做事很有条理
    inputbox = self.browser.find_element_by_id('id_new_item') 
    inputbox.send_keys('Use peacock feathers to make a fly') 
    inputbox.send_keys(Keys.ENTER)

    # 页面再次更新，清单中显示了这两个待办事项
    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    self.assertIn('1: Buy peacock feathers', [row.text for row in rows]) 
    self.assertIn(
        '2: Use peacock feathers to make a fly',
        [row.text for row in rows]
    )

    # 伊迪丝想知道这个网站是否会记住她的清单 
    # 她看到网站为她生成了一个唯一的URL
    # 页面中有一些文字解说这个功能 
    self.fail('Finish the test!')

    # 她访问那个URL，发现待办事项清单还在

这个功能测试会返回一个错误:

    AssertionError: '1: Buy peacock feathers' not found in ['1: Use peacock
    feathers to make a fly']

## 4. 重构
提交目前已编写的代码：

    git diff # 会看到functional_tests.py，home.html，tests.py和views.py中的变动
    git commit -a

在功能测试中定义辅助方法：

functional_tests.py

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        [...]
        # 她按回车键后，页面更新了
        # 待办事项表格中显示了“1: Buy peacock feathers” 
        inputbox.send_keys(Keys.ENTER) 
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 她输入了“Use peacock feathers to make a fly(”使用孔雀羽毛做假蝇) 
        # 伊迪丝做事很有条理
        inputbox = self.browser.find_element_by_id('id_new_item') 
        inputbox.send_keys('Use peacock feathers to make a fly') 
        inputbox.send_keys(Keys.ENTER)

        # 页面再次更新，她的清单中显示了这两个待办事项 
        self.check_for_row_in_list_table('1: Buy peacock feathers') 
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # 伊迪丝想知道这个网站是否会记住她的清单 
        [...]

再次运行功能测试，看重构前后的表现是否一致:

    AssertionError: '1: Buy peacock feathers' not found in ['1: Use peacock
    feathers to make a fly']

提交这次针对功能测试的重构:

    git diff # 查看functional_tests.py中的改动
    git commit -a

## 5. Django ORM
“对象关系映射器”(Object-Relational Mapper，ORM)是一个数据抽象层，描述存储在数据库中的表、行和列。处理数据库时，可以使用熟悉的面向对象方式，写出更好的代码。 在 ORM 的概念中，类对应数据库中的表，属性对应列，类的单个实例表示数据库中的一行数据。

在 lists/tests.py 文件中新建一个测试类：

lists/tests.py

    from lists.models import Item
    [...]

    class ItemModelTest(TestCase):

        def test_saving_and_retrieving_items(self):
            first_item = Item()
            first_item.text = 'The first (ever) list item'
            first_item.save()

            second_item = Item()
            second_item.text = 'Item the second'
            second_item.save()

            saved_items = Item.objects.all()
            self.assertEqual(saved_items.count(), 2)

            first_saved_item = saved_items[0]
            second_saved_item = saved_items[1]
            self.assertEqual(first_saved_item.text, 'The first (ever) list item')
            self.assertEqual(second_saved_item.text, 'Item the second')

在数据库中创建新记录的过程很简单:先创建一个对象，再为一些属 性赋值，然后调用 .save() 函数。Django 提供了一个查询数据库的 API，即类属性 .objects。 再使用可能是最简单的查询方法 .all()，取回这个表中的全部记录。得到的结果是一个类 似列表的对象，叫 QuerySet。从这个对象中可以提取出单个对象，然后还可以再调用其他函 数，例如 .count()。接着，检查存储在数据库中的对象，看保存的信息是否正确。

运行单元测试:

    ImportError: cannot import name 'Item'

下面在 lists/models.py 中写入一些代码:

lists/models.py

    from django.db import models

    class Item(models.Model):
        pass

### 5.1 第一个数据库迁移
在 Django 中，ORM 的任务是模型化数据库。创建数据库其实是由另一个系统负责的，叫 作“迁移”(migration)。迁移的任务是，根据你对 models.py 文件的改动情况，添加或删 除表和列。

使用 makemigrations 命令创建迁移:

    python manage.py makemigrations

运行单元测试：

    python manage.py test lists
    [...]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
    AttributeError: 'Item' object has no attribute 'text'

测试说明 Item 缺少 .text 属性。

继承 models.Model 的类映射到数据库中的一个表。默认情况下，这种类会得到一个自动生 成的 id 属性，作为表的主键，但是其他列都要自行定义。定义文本字段的方法如下:

lists/models.py

    class Item(models.Model):
        text = models.TextField()

Django 提供了很多其他字段类型，例如 IntegerField、CharField、DateField 等。使用 TextField 而不用 CharField，是因为后者需要限制长度，但是就目前而言，这个字段的长 度是随意的。

在数据库中添加了一个新字段，就要再创建一个迁移。

    python manage.py makemigrations

这个命令不允许添加没有默认值的列。选择第二个选项，然后在 models.py 中设定一个默 认值。

lists/models.py

    class Item(models.Model):
        text = models.TextField(default=")

现在可以顺利创建迁移了:

    python manage.py makemigrations

测试也能通过了:

    python manage.py test lists

提交代码：

    git status # 看到tests.py和models.py，以及两个没跟踪的迁移文件 
    git diff # 审查tests.py和models.py中的改动
    git add lists
    git commit -m"Model for list Items and associated migration"

## 6. 把 POST 请求中的数据存入数据库
接下来，要修改针对首页中 POST 请求的测试。希望视图把新添加的待办事项存入数据
库，而不是直接传给响应。

lists/tests.py

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1) #➊
        new_item = Item.objects.first() #➋
        self.assertEqual(new_item.text, 'A new list item') #➌

        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')

➊ 检查是否把一个新 Item 对象存入数据库。objects.count() 是 objects.all().count()
的简写形式。

➋ objects.first() 等价于 objects.all()[0]。 

➌ 检查待办事项的文本是否正确。

运行测试，会看到一个预期 失败:
    
    self.assertEqual(Item.objects.count(), 1)
    AssertionError: 0 != 1

修改一下视图：

lists/views.py

    from django.shortcuts import render 
    from lists.models import Item

    def home_page(request): 
        item = Item()
        item.text = request.POST.get('item_text', '')
        item.save()

        return render(request, 'home.html', {
            'new_item_text': request.POST.get('item_text', ''),
        })

测试通过。现在可以做些重构:

lists/views.py

    return render(request, 'home.html', {
        'new_item_text': item.text
    })

定义一个新测试方法：

lists/tests.py

    class HomePageTest(TestCase): 
        [...]

        def test_only_saves_items_when_necessary(self): 
            self.client.get('/') 
            self.assertEqual(Item.objects.count(), 0)

这个测试得到的是 1 != 0 失败。下面来修正这个问题。

lists/views.py

    def home_page(request):
        if request.method == 'POST':
            new_item_text = request.POST['item_text']
            Item.objects.create(text=new_item_text) 
        else:
            new_item_text = ''

        return render(request, 'home.html', { 
            'new_item_text': new_item_text,
        })

* 使用一个名为 new_item_text 的变量，其值是 POST 请求中的数据，或者是空字
符串。

* .objects.create 是创建新 Item 对象的简化方式，无需再调用 .save() 方法。

## 7. 处理完 POST 请求后重定向
处理完 POST 请求后一定要重定向(https://en.wikipedia.org/ wiki/Post/Redirect/Get)，那么接下来就实现这个功能吧。再次修改针对保存 POST 请求数 据的单元测试，不让它渲染包含待办事项的响应，而是重定向到首页：

lists/tests.py

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

不需要再拿响应中的 .content 属性值和渲染模板得到的结果比较，因此把相应的断言删掉 了。现在，响应是 HTTP 重定向，状态码是 302，让浏览器指向一个新地址。

修改之后运行测试，得到的结果是 200 != 302 错误。

lists/views.py

    from django.shortcuts import redirect, render 
    from lists.models import Item

    def home_page(request):
        if request.method == 'POST':
            Item.objects.create(text=request.POST['item_text']) 
            return redirect('/')

        return render(request, 'home.html')

现在，测试可以通过了。


### 更好的单元测试实践方法:一个测试只测试一件事
现在视图函数处理完 POST 请求后会重定向，这是习惯做法。

良好的单元测试实践方法要求，一个测试只能测试一件 事。因为这样便于查找问题。如果一个测试中有多个断言，一旦前面的断言导致测试失 败，就无法得知后面的断言情况如何。

lists/tests.py

    def test_can_save_a_POST_request(self):
        self.client.post('/', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': 'A new list item'}) 
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(response['location'], '/')

## 8. 在模板中渲染待办事项
编写一个新单元测试，检查模板是否也能显示 多个待办事项：

lists/tests.py

    class HomePageTest(TestCase): 
        [...]
        def test_displays_all_list_items(self): 
            Item.objects.create(text='itemey 1') 
            Item.objects.create(text='itemey 2')

            response = self.client.get('/')

            self.assertIn('itemey 1', response.content.decode())
            self.assertIn('itemey 2', response.content.decode())

这个测试和预期一样会失败:

    AssertionError: 'itemey 1' not found in '<html>\n  <head>\n [...]

Django的模板句法中有一个用于遍历列表的标签，即{% for .. in .. %}。可以按照下面 的方式使用这个标签:

lists/templates/lists/home.html

    <table id="id_list_table">
        {% for item in items %}
            <tr><td>1: {{ item.text }}</td></tr>
        {% endfor %}
    </table>

只修改模板还不能让测试通过，还要在首页的视图中把待办事项传入模板:

lists/views.py

    def home_page(request):
        if request.method == 'POST':
            Item.objects.create(text=request.POST['item_text']) 
            return redirect('/')

        items = Item.objects.all()
        return render(request, 'lists/home.html', {'items': items})

    这样单元测试就能通过了。

    运行功能测试，测试失败：

        python3 functional_tests.py
        [...]
        AssertionError: 'To-Do' not found in 'OperationalError at /'

## 9. 使用迁移创建生产数据库
功能测试失败的原因是没有正确设置数据库。为什么在单元测试中一切都运行良好呢？这是因为 Django 为单元测试创建了专用的测试数据库——这是 Django 中 TestCase 所做的神奇事情之一。

我们已经在 models.py 文件和后来创建的迁移文件中告诉 Django 创建数据库所需的一切信 息，为了创建真正的数据库，要使用 Django 中另一个强大的 manage.py 命令——migrate：

    python3 manage.py migrate

使用 Django 模板标签 forloop.counter 让清单显示正确的序号：

lists/templates/lists/home.html

    {% for item in items %}
        <tr><td>{{ forloop.counter }}: {{ item.text }}</td></tr>
    {% endfor %}

提交代码：

    git status
    git diff
    git commit -am "Redirect after POST, and show all items in template"

# 六、改进功能测试
## 1 确保功能测试之间相互隔离
运行单元测试时，Django 的测试运行程序会自动创建一个全新的测试数据库(和应用真正 使用的数据库不同)，运行每个测试之前都会清空数据库，等所有测试都运行完之后，再 删除这个数据库。但是功能测试目前使用的是应用真正使用的数据库 db.sqlite3。

从 1.4 版开始，Django 提供的一个新类，LiveServerTestCase，它可以代我们完成这 一任务。这个类会自动创建一个测试数据库(跟单元测试一样)，并启动一个开发服务器，让功能测试在其中运行。

LiveServerTestCase 必须使用 manage.py，由 Django 的测试运行程序运行。从 Django 1.6开始，测试运行程序查找所有名字以 test 开头的文件。为了保持文件结构清晰，要新建一 个文件夹保存功能测试，让它看起来就像一个应用。Django 对这个文件夹的要求只有一 个——必须是有效的 Python 模块，即文件夹中要有一个 `__init__.py` 文件。

    mkdir functional_tests
    touch functional_tests/__init__.py

然后要移动功能测试，把独立的 functional_tests.py 文件移到 functional_tests 应用中，并 把它重命名为 tests.py。使用 git mv 命令完成这个操作，让 Git 知道文件移动了:

    git mv functional_tests.py functional_tests/tests.py
    git status # 显示文件重命名为functional_tests/tests.py，而且新增了__init__.py

现在，运行功能测试不执行 python3 functional_tests.py 命令，而是使用 python3 manage.py test functional_tests 命令。

接下来编辑 functional_tests/tests.py，修改 NewVisitorTest 类，让它使用 LiveServerTestCase：

functional_tests/tests.py

    from django.test import LiveServerTestCase
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    
    class NewVisitorTest(LiveServerTestCase):

        def setUp(self):
            [...]

访问网站时，不用硬编码的本地地址(localhost:8000)，可以使用 LiveServerTestCase 提供的 live_server_url 属性:

functional_tests/tests.py

    def test_can_start_a_list_and_retrieve_it_later(self): 
        # 伊迪丝听说有一个很酷的在线待办事项应用
        # 她去看了这个应用的首页 
        self.browser.get(self.live_server_url)

还可以删除文件末尾的 `if __name__ == '__main__'` 代码块，因为之后都使用 Django 的测 试运行程序运行功能测试。

现在能使用 Django 的测试运行程序运行功能测试了，指明只运行 functional_tests 应用 中的测试：

    python manage.py test functional_tests

提交代码：

    git status # 重命名并修改了functional_tests.py，新增了__init__.py
    git add functional_tests
    git diff --staged -M
    git commit # 提交消息举例:"make functional_tests an app, use LiveServerTestCase"

git diff 命令中的 -M 标志很有用，意思是“检测移动”，所以 git 会注意到 functional_tests. py 和 functional_tests/tests.py 是同一个文件，显示更合理的差异。

## 2. 隐式和显式等待
修改功能测试，把函数 check_for_row_in_list_table 改名为 wait_for_row_in_list_table，然后增加 polling/retry 逻辑：

functional_tests/tests.py

    from selenium.common.exceptions import WebDriverException 
    
    MAX_WAIT = 10
    [...]
    
    def wait_for_row_in_list_table(self, row_text): 
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table') 
                rows = table.find_elements_by_tag_name('tr') 
                self.assertIn(row_text, [row.text for row in rows]) 
                return
            except (AssertionError, WebDriverException) as e: 
                if time.time() - start_time > MAX_WAIT:
                    raise e 
                time.sleep(0.5)

然后，就可以修改方法调用，并删除 time.sleeps 方法：

functional_tests/tests.py

    [...]
    # When she hits enter, the page updates, and now the page lists 
    # "1: Buy peacock feathers" as an item in a to-do list table inputbox.send_keys(Keys.ENTER) 
    self.wait_for_row_in_list_table('1: Buy peacock feathers')

    # There is still a text box inviting her to add another item. She 
    # enters "Use peacock feathers to make a fly" (Edith is very
    # methodical)
    inputbox = self.browser.find_element_by_id('id_new_item') inputbox.send_keys('Use peacock feathers to make a fly') inputbox.send_keys(Keys.ENTER)

    # The page updates again, and now shows both items on her list
    self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
    self.wait_for_row_in_list_table('1: Buy peacock feathers')
    [...]


