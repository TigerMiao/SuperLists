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

然后创建名为superlist的项目：

    django-admin.py startproject superlists .

## 4. 安装 Selenium
Selenium 是浏览器自动化工具，我们要用它来驱动功能测试。

    pip install --update selenium

## 5. 运行功能测试
首先，运行开发服务器：

    python manage.py runserver

再次运行测试：

    python functional_tests.py

如果开发环境配置成功，测试就会运行通过。

## 6. 创建Git版本库
在项目目录中执行以下命令：

    git init

编辑.gitignoore文件，如下：

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

